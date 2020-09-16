from client import Register

DOMAIN = '@redes2020.xyz'


if __name__ == '__main__':
    username = 'alvin_yakitori'
    password = 'pas123'

    active = True

    while active:
        opcion = input('Ingrese una opcion')

        if opcion == '1': #Registrar un usuario
            register = Register(username+DOMAIN, password)
            if register.connect():
                print("Llego al if")
                register.process(block=True)
                print("Registro realizado")
            else:
                print("No ha sido posible conectarse")
        elif opcion == '2': #Iniciar sesión
            active = False
        else:
            print('Ha ingresado una opcion que no es valida, intente de nuevo')