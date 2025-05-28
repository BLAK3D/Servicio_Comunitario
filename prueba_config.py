from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFrame, QPushButton, QMessageBox, QLineEdit, QSpinBox, QComboBox, QDateEdit
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIntValidator
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
        
        self.guardar.clicked.connect(self.guardar_info)
        
    #def cargar_info(self):
        
        
    #def eliminar_info(self):

        
    def guardar_info(self):
        nombre = self.nombre.text()
        apellido = self.apellido.text()
        altura = self.altura.text()
        peso = self.peso.text()
        fecha_nacimiento = self.fecha_nacimiento.text()
        
        if nombre == "" or apellido == "" or altura == "" or peso == "" or fecha_nacimiento == "":
            QMessageBox.critical(self, "Datos Faltantes", "Al parecer hay campos en blanco, por favor rellenalos", QMessageBox.Ok)
        else:
            sql.execute("INSERT INTO participantes (nombre, apellido, id_nacionalidad, peso, altura, fecha_nacimiento) VALUES (?, ?, 1, ?, ?, ?)",  (nombre, apellido, peso, altura, fecha_nacimiento))
            conexion.commit()
            print("Filas afectadas:", sql.rowcount)
        
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
        
        