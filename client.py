from sleekxmpp import ClientXMPP
from sleekxmpp.xmlstream.stanzabase import ET, ElementBase
from sleekxmpp.plugins.xep_0096 import stanza, File
from sleekxmpp.exceptions import IqError, IqTimeout
import logging
import threading
from prettytable import PrettyTable

class Register(ClientXMPP):

    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("register", self.registerAccount)

        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0004') # Data forms
        self.register_plugin('xep_0077') # In-band Registration
        self.register_plugin('xep_0045') # Mulit-User Chat (MUC)
        self.register_plugin('xep_0096') # File transfer

    def start(self, event):
        self.send_presence()
        self.get_roster()
        self.disconnect()

    def registerAccount(self, iq):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password

        try:
            print('Ha entrado al try')
            resp.send(now=True)
            print("Account created for %s!" % self.boundjid)
            log = logging.getLogger("my-logger")
            log.info("Account created for %s!" % self.boundjid)
        except IqError as e:
            print("Could not register account: %s" % e.iq['error']['text'])
            log.error("Could not register account: %s" % e.iq['error']['text'])
            self.disconnect()
        except IqTimeout:
            print("No response from server.")
            log.error("No response from server.")
            self.disconnect()

class Client(ClientXMPP):
    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)
        self.auto_authorize = True
        self.auto_subscribe = True
        self.add_event_handler("session_start", self.start)
        self.add_event_handler('message', self.message)
        self.add_event_handler('presence_subscribe',self.new_user_suscribed)

        self.received = set()
        self.presences_received = threading.Event()


        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0004') # Data forms
        self.register_plugin('xep_0066') # Out-of-band Data
        self.register_plugin('xep_0077') # In-band Registration
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0045') # Multi-User Chat (MUC)
        self.register_plugin('xep_0096') # File transfer

        self.nick = ""

    def start(self, event):
        try:
            log = logging.getLogger("my-logger")
            self.send_presence()
            print(self.get_roster())
        except IqError as e:
            print("Could not login: %s" % e.iq['error']['text'])
            log.error("Could not login: %s" % e.iq['error']['text'])
            self.disconnect()
        except IqTimeout:
            print("No response from server.")
            log.error("No response from server.")
            self.disconnect()

    def logout(self):
        print("Desconectado")
        self.disconnect(wait=True)

    def new_user_suscribed(self,presence):
        print("Pero esto si llega")
        print(presence['from']+' se ha suscrito a ti ')

    def message(self,msg):
        if str(msg['type']) == 'chat':
        # print("Type: "+msg['type'])
            print("\nDe",msg['from'])
            print(msg['body'])
        elif str(msg['type']) == 'groupchat':
            print("Entro mensaje grupal")
            print('\n  (%(from)s): %(body)s' %(msg))
    
    def messageRoom(self,room,msg):
        try:
            self.send_message(mto=room+'@conference.redes2020.xyz',mbody=msg, mtype='groupchat')
            print("Mensaje enviado a: "+room)
        except IqError:
            print("No response from server.")

    def joinRoom(self, room, nick):
        status = "Hello :D"
        print("Te vas a unir al room ")
        self.plugin['xep_0045'].joinMUC(room+'@conference.redes2020.xyz', nick, pstatus=status, pfrom=self.boundjid.full, wait=True)
        self.nick = nick

    def createRoom(self, room, nick):
        status = "Hello :D"
        print("Te vas a unir al room ")
        self.plugin['xep_0045'].joinMUC(room+'@conference.redes2020.xyz', nick, pstatus=status, pfrom=self.boundjid.full, wait=True)
        self.nick = nick
        self.plugin['xep_0045'].setAffiliation(room+'@conference.redes2020.xyz', self.boundjid.full, affiliation='owner')
        self.plugin['xep_0045'].configureRoom(room+'@conference.redes2020.xyz',ifrom=self.boundjid.full)

    def changeStatus(self, show, status):
        show_text = ""
        if(show == 1):
            show_text = "chat"
        elif(show == 2):
            show_text = "away"
        elif(show == 3):
            show_text = "xa"
        elif(show == 4):
            show_text = "dnd"

        self.send_presence(pshow=show_text, pstatus=status)

    def saveUser(self,jid):
        self.send_presence_subscription(pto=jid)

    def sendMessage(self,jid,message):
        try:
            self.send_message(mto=jid+'@redes2020.xyz',mbody=message, mfrom=self.boundjid.user, mtype='chat')
            print("Mensaje enviado a: "+jid)
        except IqError:
            print("No response from server.")
        

    def unregister(self):
        iq = self.make_iq_set(ito='redes2020.xyz', ifrom=self.boundjid.user)
        item = ET.fromstring("<query xmlns='jabber:iq:register'> \
                                        <remove/> \
                                    </query>")
        iq.append(item)
        res = iq.send()
        if res['type'] == 'result':
            print("Cuenta eliminada")

    def getUser(self, username):
        print("========= Contacto a buscar ============")
        print('Esperando...\n')
        proof = False
        self.presences_received.wait(1)
        groups = self.client_roster.groups()
        t2 = PrettyTable(['Username','Subscription','Status'])
        for group in groups:
            for jid in groups[group]:
                temp = []
                sub = self.client_roster[jid]['subscription']           
                temp.append(jid)
                temp.append(sub)

                connections = self.client_roster.presence(jid)
                for res, pres in connections.items():
                    show = 'available'
                    if pres['show']:
                        show = pres['show']
                    temp.append(show)
                if len(temp) == 2:
                    temp.append('unavailable')
                if str(jid) == username+"@redes2020.xyz":
                    proof = True
                    t2.add_row(temp)
        if proof:
            print(t2)
        else:
            print("No se encontro al usuario")



    def getUsers(self):
        iq = self.Iq()
        iq['type'] = 'set'
        iq['id'] = 'search_result'
        iq['to'] = 'search.redes2020.xyz'

        item = ET.fromstring("<query xmlns='jabber:iq:search'> \
                                <x xmlns='jabber:x:data' type='submit'> \
                                    <field type='hidden' var='FORM_TYPE'> \
                                        <value>jabber:iq:search</value> \
                                    </field> \
                                    <field var='Username'> \
                                        <value>1</value> \
                                    </field> \
                                    <field var='search'> \
                                        <value>*</value> \
                                    </field> \
                                </x> \
                              </query>")
        iq.append(item)
        res = iq.send()
        # print(res)
        data = []
        temp = []
        cont = 0
        for i in res.findall('.//{jabber:x:data}value'):
            cont += 1
            txt = ''
            if i.text == None:
                txt = '--'
            else:
                txt = i.text

            temp.append(txt)
            if cont == 4:
                cont = 0
                data.append(temp)
                temp = []

        t = PrettyTable(['Email', 'JID', 'Username', 'Name'])
        for i in data:
            t.add_row(i)
        print(t)

        print("========= Lista de Contactos ============")
        print('Esperando...\n')
        self.presences_received.wait(1)
        groups = self.client_roster.groups()
        t2 = PrettyTable(['Username','Subscription','Status'])
        for group in groups:
            for jid in groups[group]:
                temp = []
                sub = self.client_roster[jid]['subscription']           
                temp.append(jid)
                temp.append(sub)

                connections = self.client_roster.presence(jid)
                for res, pres in connections.items():
                    show = 'available'
                    if pres['show']:
                        show = pres['show']
                    temp.append(show)
                if len(temp) == 2:
                    temp.append('unavailable')
                if str(jid) != str(self.boundjid.bare):
                    t2.add_row(temp)
        print(t2)
            

def wait_for_presences(self, pres):
        """
        Track how many roster entries have received presence updates.
        """
        self.received.add(pres['from'].bare)
        if len(self.received) >= len(self.client_roster.keys()):
            self.presences_received.set()
        else:
            self.presences_received.clear()