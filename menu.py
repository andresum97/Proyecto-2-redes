from client import Register,Client

DOMAIN = '@redes2020.xyz'


if __name__ == '__main__':
    username = 'alvin_yakitori'
    password = 'pas123'

    active = True
    login_flag = False

    menu_logout = """============ MENU ============== \n
    1. Registrar un usuario\n
    2. Login\n
    10. Salir
    """

    menu_login = """============ MENU ============== \n
    1. Registrar un usuario\n
    2. Logout\n
    3. Eliminar cuenta del servidor \n
    4. Mostrar todos los usuarios \n
    5. Agregar un usuario a los contactos \n
    6. Mostrar detalles de un usuario \n
    7. Enviar mensaje a usuario \n
    8. Participar en conversasiones grupales \n
    9. Definir mensaje de presencia \n
    10. Salir\n
    """

    while active:
        if login_flag:
            print(menu_login)
        else:
            print(menu_logout)
        opcion = input('Ingrese una opcion')

        if opcion == '1': #Registrar un usuario
            username = input('Ingrese nombre usuario: ')
            password = input('Ingrese contraseña: ')
            register = Register(username+DOMAIN, password)
            if register.connect():
                print("Llego al if")
                register.process(block=True)
            else:
                print("No ha sido posible conectarse")

        elif opcion == '2' and login_flag == False: #Iniciar sesión
            username = input('Ingrese nombre usuario: ')
            password = input('Ingrese contraseña: ')
            cliente = Client(username+DOMAIN, password)
            if cliente.connect():
                cliente.process()
                print("Conectado")
                login_flag = True
            else:
                print("No fue posible conectarse")

        elif opcion == '2' and login_flag == True: #Logout
            if cliente.connect():
                cliente.logout()
                login_flag = False
            else:
                print("No fue posible desconectarse")

        elif opcion == '3' and login_flag == True: #Eliminar cuenta
            cliente.unregister()
            login_flag = False
        
        elif opcion == '5' and login_flag == True: #Agregar usuarios
            user = input("Ingrese el usuario que desea agregar: ")
            cliente.saveUser(user+DOMAIN)

        elif opcion == '7' and login_flag == True: #Enviar mensaje
            jid = input("Usuario a enviar el mensaje: ")
            message = input("Mensaje a enviar")
            cliente.sendMessage(jid,message)

        elif opcion == '9' and login_flag == True: #Cambiar estado
            print("""
            ========== Opciones de status ==========
            1. chat - Estas disponible para conversar \n
            2. away - No estas disponible para IM por periodo corto de tiempo \n
            3. xa - No estas disponible para un periodo largo de tiempo \n
            4. dnd - Estas ocupado y no quieres interrupcciones \n
            """)
            state = True
            show = 0
            while state:
                try:
                    show = int(input("Ingrese una opcion de status: "))
                    if(show>=1 and show<=4):
                        state = False
                except:
                    print("Debe ingresar un valor numerico")
            status = input("Ingrese mensaje para el status")
            cliente.changeStatus(show,status)


        elif opcion == '10': #Salir
            active = False

        else:
            print('Ha ingresado una opcion que no es valida, intente de nuevo')