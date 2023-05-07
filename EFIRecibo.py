import sys
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QLineEdit, QTextEdit, QFrame)
from PySide6.QtCore import Qt

class Recibito(QDialog):
    def __init__(self, ingredientes, iva, valorXing):
        super().__init__()
        self.setWindowTitle("Recibo")
        self.setFixedSize(300, 460)

        self.frame1 = QFrame(self)
        self.frame1.setGeometry(5, 0, 290, 100)
        self.frame1.setStyleSheet('''
        margin: -1px;
        ''')

        self.frame2 = QFrame(self)
        self.frame2.setGeometry(5, 90, 290, 350)
        self.frame2.setStyleSheet('''
        margin: -1px;
        ''')


        self.GridPrincipal = QGridLayout()
        self.GridSecundario = QGridLayout()

        ingredientes[-1] = ingredientes[-1].upper()
        datos = f'{ingredientes[-1]}\n'
        for ingrediente in (ingredientes[2:-1]):
            match ingredientes[-1]:
                case 'HAMBURGUESA PERSONALIZADA':
                    datos += f'{ingrediente} \t  +${valorXing} \n'
                case _:
                    datos += ingrediente + "\n"

        medallones = (f'MEDALLON/ES DE CARNE: {ingredientes[1]} \t  +${int(ingredientes[1])*250} \n')
        datos += medallones + "\n"

        precio = int(ingredientes[0])

        datosfinales = (f'SUBTOTAL: \t  ${precio}')
        datosfinales += "\n"
        datosfinales += f'RECARGO IVA:  {iva}'
        total = (f'\nTOTAL: \t  ${precio*iva}')
        datosfinales += total + "\n"

        MostrarDatosGridSecundario = QTextEdit()
        MostrarDatosGridSecundario.setReadOnly(True)

        MostrarDatosGridPrincipal = QTextEdit()
        MostrarDatosGridPrincipal.setReadOnly(True)

        MostrarDatosGridFinal = QTextEdit()
        MostrarDatosGridFinal.setReadOnly(True)
        MostrarDatosGridFinal.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        gridstyle = '''
        border: 2px dotted;
        border-color: black;
        padding: 1px;
        '''

        MostrarDatosGridPrincipal.setStyleSheet(gridstyle)
        MostrarDatosGridSecundario.setStyleSheet(gridstyle)
        MostrarDatosGridFinal.setStyleSheet(gridstyle)


        fecha =  datetime.now().date()
        datosRecibo = (f'''PyBurger S.A.\t\tFECHA:{fecha}\nCUIT:    3042069123 ''')

        MostrarDatosGridPrincipal.setText(datosRecibo)
        self.GridPrincipal.addWidget(MostrarDatosGridPrincipal)
        self.frame1.setLayout(self.GridPrincipal)

        MostrarDatosGridSecundario.setText(datos)
        MostrarDatosGridFinal.setText(datosfinales)
        MostrarDatosGridFinal.setMaximumHeight(70)
        self.GridSecundario.addWidget(MostrarDatosGridSecundario)
        self.GridSecundario.addWidget(MostrarDatosGridFinal)
        self.frame2.setLayout(self.GridSecundario)





if __name__ == '__main__':
    lista = ['650','2','pepinillo', 'tomate', 'cebolla', 'ketchu', 'mayonesa','pepinillo', 'tomate', 'cebolla', 'ketchu', 'mayonesa', 'HAMBURGUESA PERSONALIZADA']
    iva = 1.21
    valor = 120
    
    pantalla_recibo = QApplication(sys.argv)
    window = Recibito(lista, iva, valor)
    window.show()
    pantalla_recibo.exec()
    sys.exit()
