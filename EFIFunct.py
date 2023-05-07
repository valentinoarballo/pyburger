from json import loads,dumps
import json
from dataclasses import dataclass
import os




# Abriendo DB
f = open('burgers.json', encoding="utf-8")
fa = f.read()
hamburguesas = loads(fa)

def Menu():
    print ("-- menu de hamburguesas --\n")

    c = 1
    print (f"{c} - hamburguesa personalizada")
    for hamburguesa in hamburguesas:
        c += 1
        print(f'{c} - hamburguesa {hamburguesa["nombre"]}')
    OpSalir = c+1
    print(f'{OpSalir} - salir')
    return OpSalir
    
def EleccionMenu():
    val = True
    while val == True:
        OpSalir = Menu() 

        opcionMenu = int(input("inserta un numero valor >> "))
        print ("")
        input(f"Has pulsado la opcion {opcionMenu}...\npulsa cualquier tecla para continuar")

        if opcionMenu == 1:
            pedido = PedidoPersonalizado()
        elif opcionMenu == OpSalir:
            os.system ("cls")
            break
        else:
            pedido = GetIngredientes(hamburguesas[opcionMenu-2])
        Recibo(pedido)
        val = False       

def GetIngredientes(hamburguesa):
    pedido=[]
    for ingrediente,buliano in hamburguesa.items():
        if buliano == True and (ingrediente != "medallones de carne" and ingrediente !="precio"):
            pedido.append(ingrediente)
        else:
            pass
    if hamburguesa["medallones de carne"] == 1:
        pedido.append("un medallon de carne")
    else:
        pedido.append(f'{hamburguesa["medallones de carne"]} medallones de carne') 
    pedido.append(hamburguesa["nombre"])
    pedido.append(hamburguesa["precio"])
    return pedido

def Recibo(pedido):
    os.system ("cls")
    print(f"su pedido de hamburguesa {pedido[-2]}:")
    for x in range((len(pedido)-2)):
        
        print(pedido[x])   
    print(f'costo -------------- ${pedido[-1]}')
    input('\n                    enter para finalizar >>')
    os.system ("cls")

def PedidoPersonalizado(): 
    ingredientes = []
    for ingrediente,valor in hamburguesas[0].items():
        if ingrediente != "medallones de carne" and (valor == True or valor == False):
            ingredientes.append(ingrediente)
        else:
            pass

    pedidopers = []
    precio = 650
    pedidopers.append("pan")

    print("\n")
    print ("1 - medallon de carne")
    print ("2 - doble medallon de carne")
    print ("3 - triple medallon de carne")
    medallones = int(input("inserta un numero valor >> "))
    match medallones:
        case 1:
            pedidopers.append("medallon de carne")
        case 2:
            pedidopers.append("doble medallon de carne")
            precio += 250
        case 3:
            pedidopers.append("triple medallon de carne")
            precio += 500

    for ingrediente in ingredientes:
        print("")
        print (f"1 - agregar {ingrediente}")
        print (f"2 - no incluir {ingrediente}")
        opcion = int(input("inserta un numero valor >> "))
        
        match opcion:
            case 1:
                pedidopers.append(ingrediente)
                precio += 100
            case 2:
                pass

    pedidopers.append("personalizada")    
    pedidopers.append(precio)
    return pedidopers

f.close()



def admin():
    def crear_hamburguesa():
        filename = 'burgers.json'
        NuevaHamburguesa = {}
        with open(filename, "r", encoding='utf-8') as file:
            hamburguesas = json.load(file)  
        nombre = input('nombre de la hamburguesa >> ')
        medallones = int(input('cantidad de medallones >> '))

        NuevaHamburguesa["nombre"]=nombre
        NuevaHamburguesa["medallones de carne"]=medallones
        for ingrediente,valor in hamburguesas[0].items():
            if ingrediente != "medallones de carne" and (valor == True or valor == False):
                print(f'la nueva hamburguesa "{nombre}" va a tener {ingrediente}?')
                var = int(input(f'1 - si\n2 - no\n >>'))
                
                match var:
                    case 1:
                        NuevaHamburguesa[f"{ingrediente}"]=True
                    case 2:
                        NuevaHamburguesa[f"{ingrediente}"]=False

        precio = int(input('precio de la hamburguesa >> '))
        icon = input('ubicacion del archivo imagen de la hamburguesa >> ')
        NuevaHamburguesa["precio"]=precio
        NuevaHamburguesa["icon"]=icon
        hamburguesas.append(NuevaHamburguesa)

        with open(filename, "w") as file:
            json.dump(hamburguesas, file)


    def eliminar_hamburguesa():
        filename = 'burgers.json'

        with open(filename, 'r', encoding='utf-8') as file:
            hamburguesas = json.load(file)



        print('que hamburguesa quiere eliminar del menu?')
        c = 0
        for hamburguesa in hamburguesas:
            c += 1
            print(f'{c} - hamburguesa {hamburguesa["nombre"]}')
        
        opcionMenu = int(input("inserta un numero valor >> "))
        confirmacion = input(f"\nHas pulsado la opcion {opcionMenu}...\nesta seguro que quiere borrar la hamburguesa {hamburguesas[opcionMenu-1]['nombre']} del menu? S/N\n   >>")
        match confirmacion:
            case "S":
                print(f'\nla hamburguesa {hamburguesas[opcionMenu-1]["nombre"]} se borro del menu.')
                for idx, obj in enumerate(hamburguesas):
                    if obj['nombre'] == hamburguesas[opcionMenu-1]["nombre"]:
                        hamburguesas.pop(idx)
                new_file = 'burgers.json'
                with open(new_file, 'w', encoding='utf-8') as file:
                    file.write(json.dumps(hamburguesas, indent=2))

            case _:
                print(f'\nhamburguesa {hamburguesas[opcionMenu-1]["nombre"]} no se borrara del menu.')
        continuar = input('\nprecionar enter para continuar >>')

    print('-- modo administrador --\n')
    print('1 - crear nueva hamburguesa')
    print('2 - borrar una hamburguesa del menu')
    print('3 - salir del modo administrador')
    opcion = int(input('   >> '))
    os.system ("cls")
    match opcion:
        case 1:
            crear_hamburguesa()
        case 2:
            eliminar_hamburguesa()
        case 3:
            pass
    
def MainMenu():
    user = 0
    while user != 3:
        print("1 - admin")
        print("2 - user")
        print("3 - salir")
        user = int(input("   >> "))
        os.system ("cls")
        match user:
            case 1:
                admin()
            case 2:
                EleccionMenu()

if __name__ == '__main__':
    MainMenu()