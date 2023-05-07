import sys
import EFIFunct
import EFIRecibo
from PySide6.QtCore import QSize, QFile, Qt
from PySide6.QtGui import QIcon, QPixmap, QFont, QImage
from PySide6.QtWidgets import (QAbstractButton, QApplication, QButtonGroup,
                               QComboBox, QDialog, QDialogButtonBox,
                               QFormLayout, QGridLayout, QGroupBox,
                               QHBoxLayout, QLabel, QLineEdit, QMenu, QMenuBar,
                               QPushButton, QSpinBox, QRadioButton, QTextEdit, 
                               QVBoxLayout, QFrame, QGraphicsScene, QGraphicsView,
                               QCheckBox)

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# VENTANA DE MENÚ
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class MainMenu(QDialog):
    def __init__(self):
        super().__init__()

        self.colorgris = "#ff3d00"
        self.colornaranja = "#C1B9B6"

        self.setStyleSheet(f'''
        background-color: {self.colorgris};
        ''')


        self.secolstyle = f'''
                background-color: {self.colornaranja};
                color: {self.colorgris};
                font: 15pt;
                border: 5px double;
                border-color: black;
                padding: 18px 0px;
                '''

        self.buttonstyle = f'''
        background-color: {self.colornaranja};
        color: black;
        font: 10pt;
        padding: 5px 50px;
        '''

        # Los botones al fondo de si/no

        self._botones = QGroupBox()
        self.botonlayout = QHBoxLayout()
        # font = QFont("Comic Sans MS")
        font = QFont("Segoe Print")

        self.botonOK = QPushButton("¡Seguir!", self)
        self.botonOK.clicked.connect(self.continuar)
        self.botonOK.setFont(font)
        self.botonOK.setStyleSheet(self.buttonstyle)
        
        self.botonNO = QPushButton("Salir...", self)
        self.botonNO.clicked.connect(self.close)
        self.botonNO.setFont(font)
        self.botonNO.setStyleSheet(self.buttonstyle)

        self.botonlayout.addWidget(self.botonOK)
        self.botonlayout.addWidget(self.botonNO)

        self.botonOK.setEnabled(False)

        self.create_title_box()
        self.create_horizontal_group_box()
        self.create_second_row()
        self.create_second_column()


        self._botones.setLayout(self.botonlayout)
        # Oganización principal
        self.main_layout = QGridLayout()
        # Título pyburger (row 1, col 1, rowspan 1, colspan 2)
        self.main_layout.addWidget(self._title_box, 1, 1, 1, 2)
        # Añadiendo caja principal a la izquierda (row 2, col 1, rowspan 2, colspan 1)
        self.main_layout.addWidget(self._horizontal_group_box, 2, 1, 2, 1)
        # Segunda columna (row 2, col 2, rowspan 3)
        self.main_layout.addWidget(self._second_column, 2, 2, 3, Qt.AlignLeft)
        # Fila custom (row 4, col 1)
        self.main_layout.addWidget(self._second_row, 4, 1)
        # Botones si/no (row 5, col 2)
        self.main_layout.addWidget(self._botones, 5, 2)
        self.setLayout(self.main_layout)

        self.setFixedSize(790, 825)
        self.setWindowIcon(QIcon("./icons/zzzlogo.png"))
        self.setWindowTitle("PyBurger")

    # caja con el logo        
    def create_title_box(self):
        self._title_box = QGroupBox()
        self._title_box.setStyleSheet('''
                background-color: white;
                border: 5px double;
                border-color: black;
                ''')
        layout = QGridLayout()
        label = QLabel()

        pixmap = QPixmap("./icons/zzzsuperlogo.png")
        pixmap.scaled(QSize(100,100))

        label.setPixmap(pixmap)
        label.setStyleSheet('''
        border: none;
        ''')
        layout.addWidget(label, 1, 1, Qt.AlignHCenter)
        self._title_box.setLayout(layout)



    # Columna principal con imágenes y botones

    def create_horizontal_group_box(self):
        self._horizontal_group_box = QGroupBox("Elija su hamburguesa...")
        # font = QFont("Comic Sans MS")
        font = QFont("Segoe Print")
        self._horizontal_group_box.setFont(font)
        self._horizontal_group_box.setStyleSheet(self.secolstyle)

        # determinando núm de botones y columnas
        num_buttons = len(EFIFunct.hamburguesas)
        if num_buttons <= 4:
            num_grid_cols = 2
        elif num_buttons >= 5:
            num_grid_cols = 3

        layout = QGridLayout()
        for i in range(num_buttons):
            buttonbg = EFIFunct.hamburguesas[i]["icon"] # retira la URL del ícono a una variable desde archivo json
            button = QPushButton(f"{i}") # pone un int de texto: esto permitirá guardar qué opción seleccionó el usuario
            button.setFixedSize(QSize(200, 150)) # define tamaño
            button.clicked.connect(self.enableContinue) # enable botón de seguir 
            button.clicked.connect(self.writeSomething) # escribe desc ingredientes y precio

            button.setStyleSheet(f"""
            border-image: url({buttonbg}) 0 0 0 0 stretch stretch;
            """)

            col = i % num_grid_cols
            row = i / num_grid_cols
            layout.addWidget(button, row, col, Qt.AlignHCenter)

        self._horizontal_group_box.setLayout(layout)

    # Columna a la derecha con texto + groupbox

    def create_second_column(self):
        self._second_column = QGroupBox("¿Qué hay adentro?")
        # font = QFont("Comic Sans MS")
        font = QFont("Segoe Print")
        self._second_column.setFont(font)
        self._second_column.setStyleSheet(self.secolstyle)
        layout = QGridLayout()
        self.create_burgerdesc_box()
        self._second_column.setLayout(layout)

    # fila con boton custom

    def create_second_row(self):
        self._second_row = QGroupBox()
        layout = QHBoxLayout()

        self._second_row.setStyleSheet(f'''
        background-color: {self.colorgris};
        border-radius: 30px;
        border: 5px dashed;
        border-color: {self.colornaranja};
        ''')
        mysterybutton = QPushButton("custom")
        mysterybutton.clicked.connect(self.writeSomething)
        mysterybutton.clicked.connect(self.enableContinue)
        mysterybutton.setFixedSize(QSize(300, 200))

        layout.addWidget(mysterybutton)
        mysterybutton.setStyleSheet(f"""
            color: transparent;
            font: 1pt;
            border-image: url(./icons/zcustom) 0 0 0 0 stretch stretch;
            """)
        self._second_row.setLayout(layout)


    # Caja con descripción, se actualiza por clic
    def create_burgerdesc_box(self, var="Hacé clic en una foto."):

        layout = QGridLayout()
        self.description = QTextEdit(var)
        self.preciaje = QTextEdit() # son 2 cajas para tener desc ing y precios con contenidos diferentes
        self.preciaje.setReadOnly(True)
        self.description.setReadOnly(True) # evitar que sea editable
        self.description.setFrameStyle(QFrame.NoFrame) # quitar borde
        self.description.setFixedSize(300, 200)

        self.description.setStyleSheet(f'''
        background-color: {self.colornaranja};
        color: {self.colorgris};
        font-weight:700;
        border: none;
        border-bottom: 1px dotted;
        border-color: black;
        padding: 8px 0px;
        ''')
        self.preciaje.setStyleSheet(f'''
        background-color: {self.colornaranja};
        color: {self.colorgris};
        font-weight:700;
        border: none;
        padding: 8px 0px;
        ''')
        layout.addWidget(self.description, 1, 1, 1, 1)
        layout.addWidget(self.preciaje, 2, 1, 1, 1)

        self._second_column.setLayout(layout)

    def enableContinue(self):
        self.botonOK.setEnabled(True)

    def writeSomething(self):
        self.name = self.sender().text() # texto del botón (0, 1, 2, 3... X, y custom)
 
        if self.name != "custom":
            h = int(self.name)

            precioburger = EFIFunct.hamburguesas[h]['precio'] # recupera el precio

            todos = EFIFunct.GetIngredientes(EFIFunct.hamburguesas[h]) # recupera lista de ingredientes
            self.ingredientes = ""
            ingredientesFinal = ""
            for x in range(len(todos)-2): # los últimos dos ítems de la lista son la descripción y el nombre de la foto: acá queremos solo ingredientes
                pstr = todos[x].upper() # uppercase es la única manera que se vea plano, con otros se quitan/no hay mayúsculas que deberían haber
                self.ingredientes += f"{pstr}\n"
            ingredientesFinal = self.ingredientes + f"\nPRECIO: ${precioburger}"
            self.preciaje.setText(ingredientesFinal) # devuelve el texto a la caja de preciaje

            desc = EFIFunct.hamburguesas[h]['desc']
            nombreburger = EFIFunct.hamburguesas[h]['nombre']
            nombreburger = nombreburger.title()
            self.description.setText(f"{nombreburger}: {desc}") # retira descripción y nombre y construye el texto de la caja de descripción

            m = EFIFunct.hamburguesas[h]['medallones de carne']
            self.ingredientes = str(m) + "\n" + self.ingredientes
            self.ingredientes = str(precioburger) + "\n" + self.ingredientes
            self.ingredientes = self.ingredientes.split("\n")
            self.ingredientes = self.ingredientes[:-2]
            self.ingredientes.append(nombreburger.upper())

        else: # si es custom, pone una desc por defecto
            self.description.setText("¡Lo que vos quieras! Elegí los ingredientes que te parezcan, con los medallones que te parezcan.")
            self.preciaje.setText("") # y borra el texto en la caja de preciaje

    def continuar(self): # guarda la elección del cliente y determina si debe continuar al recibo
        if self.name != "custom":
            global cont
            global customerChoice
            customerChoice = self.ingredientes
            print(customerChoice)
            cont = 2
        else:
            cont = 1
        self.close()

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# VENTANA CUSTOM
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class Custom(QDialog):
    def __init__(self):
        super().__init__()
        self.custom_menu_layout = QGridLayout()

        self.botonesbottom = QGroupBox()
        self.bottomlayout = QHBoxLayout()

        self.botonOK = QPushButton("¡Seguir!", self)
        self.botonOK.clicked.connect(self.saveChoices)
        self.botonOK.clicked.connect(self.close)
        
        self.botonRE = QPushButton("Reset", self)
        self.botonRE.clicked.connect(self.close)


        self.botonNO = QPushButton("Salir...", self)
        self.botonNO.clicked.connect(self.skip)

        self.bottomlayout.addWidget(self.botonOK)
        self.bottomlayout.addWidget(self.botonRE)
        self.bottomlayout.addWidget(self.botonNO)

        self.botonOK.setEnabled(False)
        self.botonRE.setEnabled(False)

        self.botonesbottom.setLayout(self.bottomlayout)
        
        self.create_griditem()
        self.custom_menu_layout.addWidget(self._griditem, 1, 1)
        self.custom_menu_layout.addWidget(self.botonesbottom, 6, 1)

        self.medallones = ""

        self.setLayout(self.custom_menu_layout)

    def create_griditem(self):
        self._griditem = QGroupBox()

        layout = QGridLayout()
                
        bblayout = QGridLayout()
        bbgroup = QButtonGroup(self)
        for x in range(3):
            burgerlayout = QGridLayout()
            
            bbgroup.setExclusive(True)

            botonburger = QRadioButton(f"{x+1}", self)
            botonburger.toggled.connect(self.toggle)
            botonburger.toggled.connect(self.enable)

            bbgroup.addButton(botonburger)
            bblayout.addWidget(botonburger, 2, x, Qt.AlignCenter)

            bblabel = QLabel()
            bblabel.setStyleSheet(f"""
                border-image: url(./ingredientes/{x+1}.png) 0 0 0 0 stretch stretch;
                """)
            bblabel.setFixedSize(100, 100)

            bblayout.addWidget(bblabel, 1, x)
            bblayout.addLayout(burgerlayout, 1, x)

        inglayout = QGridLayout()
        for x in range(len(ing)):
            row = x % 5
            if x < 5:
                col = 1
            else:
                col = 4
            self.buttongroup = QButtonGroup(self)

            self.buttonlayout = QGridLayout()

            botoname = ing[x]
            botoname = botoname.upper()

            self.botonADD = QPushButton(f"{botoname}", self)
            self.botonADD.setCheckable(True)
            self.botonADD.toggled.connect(self.toggle)

            self.buttongroup.addButton(self.botonADD)

            self.buttonlayout.addWidget(self.botonADD, row, col)

            label = QLabel()
            label.setStyleSheet(f"""
                border-image: url(./ingredientes/{ing[x]}.png) 0 0 0 0 stretch stretch;
                """)
            label.setFixedSize(67, 70)

            layout.addWidget(label, row, col)
            layout.addLayout(self.buttonlayout, row, col+1)

        inglayout.addLayout(bblayout, 1, 1)
        inglayout.addLayout(layout, 2, 1)
        self._griditem.setLayout(inglayout)

    def enable(self):
        self.botonOK.setEnabled(True)
        self.botonRE.setEnabled(True)

    def skip(self):
        self.close()
        global cont
        cont = 0

    def toggle(self):
        self.sender().setStyleSheet('''
        QPushButton{
            background-color: lightgreen;
        }
        ''')

        collector = self.sender().text()
        cond = collector.isdigit()
        global customerChoice
        if (cond == True) and (collector not in self.medallones):
            self.medallones = collector
        elif c not in customerChoice:
            customerChoice.append(self.sender().text())
    
    def saveChoices(self):
        global precio
        global customerChoice

        precio = (len(customerChoice) * 100) + (int(self.medallones) * 250)
        customerChoice.insert(0, self.medallones)
        customerChoice.insert(0, str(precio))
        customerChoice.append("HAMBURGUESA PERSONALIZADA")
        print(customerChoice)
        global cont
        cont = 2

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# MAIN
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# Vars globales

customerChoice = []
precio = 0
cont = 0
iva = 1.21
valorXing = 120
ing = list(EFIFunct.hamburguesas[0].keys())
ing = ing[2:-3]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # SET CONT A 0 Y DESCOMENTAR ESTO 
    mm = MainMenu()
    mm.exec()
    continueVar = True
    while continueVar == True:
        match cont:
            case 1:
                c = Custom()
                c.exec()
            case 2:
                r = EFIRecibo.Recibito(customerChoice, iva, valorXing)
                r.exec()
                continueVar = False
            case _:
                continueVar = False

    sys.exit()