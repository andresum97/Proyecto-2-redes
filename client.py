from sleekxmpp import ClientXMPP
from sleekxmpp.xmlstream.stanzabase import ET, ElementBase
from sleekxmpp.plugins.xep_0096 import stanza, File
from sleekxmpp.exceptions import IqError, IqTimeout
import logging

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
        print('Entro al register')
        ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler('message', self.message)

        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0004') # Data forms
        self.register_plugin('xep_0066') # Out-of-band Data
        self.register_plugin('xep_0077') # In-band Registration
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0045') # Multi-User Chat (MUC)
        self.register_plugin('xep_0096') # File transfer

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

    def message(self,msg):
        print("\n Tipo de mensaje",msg['type'])
        print("De",msg['from'])
        print(msg['body'])

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