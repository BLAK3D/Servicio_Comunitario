from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFrame, QPushButton, QMessageBox, QLineEdit, QSpinBox, QComboBox, QDateEdit, QTableWidget, QTableWidgetItem, QFileDialog
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIntValidator
from datetime import datetime
import sys
import sqlite3


class ConfigWindow(QMainWindow):
    def __init__(self):
        super(ConfigWindow,  self).__init__()
        loadUi("ConfigWindow.ui", self)
        self.nombre = self.findChild(QLineEdit, "nombre")
        self.apellido = self.findChild(QLineEdit, "apellido")
        self.edad = self.findChild(QLineEdit, "edad")
        self.peso = self.findChild(QSpinBox, "peso")
        self.altura = self.findChild(QSpinBox, "altura")
        self.pais = self.findChild(QComboBox, "pais")
        self.fecha_nacimiento = self.findChild(QDateEdit, "fecha_nacimiento")
        self.guardar = self.findChild(QPushButton, "guardar")
        self.eliminar = self.findChild(QPushButton, "eliminar")
        self.cargar_datos = self.findChild(QPushButton, "cargar_datos")
        self.cargar_foto = self.findChild(QPushButton, "cargar_foto")
        self.tabla_participantes = self.findChild(QTableWidget, "tabla_participantes")
        self.bandera = self.findChild(QFrame, "bandera")
        self.foto = self.findChild(QFrame, "foto")
        
        self.guardar.clicked.connect(self.guardar_info)
        self.cargar_datos.clicked.connect(self.cargar_dato_ind)
        self.cargar_foto.clicked.connect(self.abrir_dialogo)
        self.pais.currentTextChanged.connect(self.cargar_bandera)
        self.fecha_nacimiento.dateChanged.connect(self.cambiar_edad)
        
        
        self.cambiar_edad()
        sql.execute("SELECT pais FROM paises ORDER BY pais ASC")
        datos = sql.fetchall()
        
    
        for fila in datos:
            self.pais.addItem(fila[0])

        self.cargar_todos_los_datos()
    
    def abrir_dialogo(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Seleccionar imagen", "", "Imágenes (*.png *.jpg *.bmp)")
        if ruta:
            print(f"Ruta seleccionada: {ruta}")

        
    def cargar_todos_los_datos(self):   
        
        # Obtener datos de la tabla
        sql.execute("SELECT nombre || ' ' || apellido, peso, altura, fecha_nacimiento FROM participantes")
        datos = sql.fetchall()

        # Configurar el número de filas y columnas
        if datos:
            self.tabla_participantes.setRowCount(len(datos))
            self.tabla_participantes.setColumnCount(len(datos[0]))  # Basado en la primera fila

            # Insertar datos en la tabla
            for fila, registro in enumerate(datos):
                for columna, valor in enumerate(registro):
                    if columna == 0:
                        self.tabla_participantes.setItem(fila, columna, QTableWidgetItem(str(valor)))
                    elif columna == 1:
                        edad = self.calcular_edad(registro[3])
                        self.tabla_participantes.setItem(fila, columna, QTableWidgetItem(str(edad)))
                        self.tabla_participantes.setItem(fila, columna + 1, QTableWidgetItem(str(valor)))

                    else:
                        self.tabla_participantes.setItem(fila, columna + 1, QTableWidgetItem(str(valor)))
                        
    def cargar_dato_ind(self):
        fila = self.tabla_participantes.currentRow()
        
        if fila >= 0:
            nombre = self.tabla_participantes.item(fila, 0).text()
            
            sql.execute(f"SELECT a.nombre, a.apellido, a.peso, a.altura, a.fecha_nacimiento, b.pais FROM participantes a INNER JOIN paises b ON a.id_nacionalidad = b.id WHERE nombre || ' ' || apellido  LIKE '{nombre}'")
            datos = sql.fetchone()
            
            edad = self.calcular_edad(datos[4])
            
            self.nombre.setText(datos[0])
            self.apellido.setText(datos[1])
            self.peso.setValue(int(datos[2]))
            self.altura.setValue(int(datos[3]))
            self.edad.setText(str(edad))
            self.pais.setCurrentText(datos[5]) 
            #self.nombre.setText("")
            #self.nombre.setText("")
            
        else:
            print()
    
    def cambiar_edad(self):
        edad = self.calcular_edad(self.fecha_nacimiento.text())
        self.edad.setText(f"{edad}")
        
    def calcular_edad(self, fecha_nacimiento: str):
        # Convertir la fecha de nacimiento a objeto datetime
        nacimiento = datetime.strptime(fecha_nacimiento, "%d/%m/%Y")
    
        # Obtener la fecha actual
        hoy = datetime.today()

        # Calcular la edad
        edad = hoy.year - nacimiento.year

        # Ajustar si aún no ha pasado el cumpleaños en el año actual
        if (hoy.month, hoy.day) < (nacimiento.month, nacimiento.day):
            edad -= 1

        return edad

    
    def cargar_bandera(self):
        texto = self.pais.currentText()
        sql.execute("SELECT ruta_imagen FROM paises WHERE pais = ?", (texto,))
        ruta = sql.fetchone()
        
        if ruta:
            self.bandera.setStyleSheet(f"QFrame {{ border-image: url({ruta[0]}) 0 0 0 0 stretch stretch; }}")

    #def eliminar_info(self):
         
    def guardar_info(self):
        nombre = self.nombre.text()
        apellido = self.apellido.text()
        altura = int(self.altura.text())
        peso = int(self.peso.text())
        fecha_nacimiento = self.fecha_nacimiento.text()
        
        if nombre == "" or apellido == "" or altura == 0 or peso == 0 or fecha_nacimiento == "":
            QMessageBox.critical(self, "Datos Faltantes", "Al parecer hay campos en blanco, por favor rellenalos", QMessageBox.Ok)
        else:
            sql.execute("INSERT INTO participantes (nombre, apellido, id_nacionalidad, peso, altura, fecha_nacimiento) VALUES (?, ?, 1, ?, ?, ?)",  (nombre, apellido, peso, altura, fecha_nacimiento))
            conexion.commit()
            print("Filas afectadas:", sql.rowcount)
            QMessageBox.information(self, "Datos Guardados", "Datos guardados exitosamente", QMessageBox.Ok)
            self.cargar_todos_los_datos()
        
if __name__ ==  "__main__":
    try:
        conexion = sqlite3.connect("BD.db")
        sql = conexion.cursor()
        app = QApplication(sys.argv)
        WConfig = ConfigWindow()

        WConfig.show()
        
        sys.exit(app.exec_())
        
    except Exception as e:
        print(e)
        
        