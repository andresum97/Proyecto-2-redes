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
    7. Comunicacion 1 a 1 con usuario \n
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
            register = Register(username+DOMAIN, password)
            if register.connect():
                print("Llego al if")
                register.process(block=True)
                print("Registro realizado")
            else:
                print("No ha sido posible conectarse")

        elif opcion == '2' and login_flag == False: #Iniciar sesión
            cliente = Client(username+DOMAIN, password)
            if cliente.connect():
                cliente.process(block=False)
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

        elif opcion == '9': #Salir
            active = False

        else:
            print('Ha ingresado una opcion que no es valida, intente de nuevo')