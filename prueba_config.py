from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFrame, QPushButton, QMessageBox, QLineEdit, QSpinBox, QComboBox, QDateEdit, QTableWidget, QTableWidgetItem, QFileDialog, QTabWidget
from PyQt5.QtCore import QTimer, Qt, QDate
from PyQt5.QtGui import QIntValidator
from datetime import datetime
import sys, shutil, os, sqlite3

class ConfigWindow(QMainWindow):
    def __init__(self):
        super(ConfigWindow,  self).__init__()
        loadUi("ConfigWindow.ui", self)
        self.nombre = self.findChild(QLineEdit, "nombre")
        self.apellido = self.findChild(QLineEdit, "apellido")
        self.edad = self.findChild(QLineEdit, "edad")
        self.id = self.findChild(QLineEdit, "id")
        self.buscador = self.findChild(QLineEdit, "buscador")
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
        self.tabWidget = self.findChild(QTabWidget, "tabWidget")
        self.estado = self.findChild(QLabel, "estado")
        
        self.guardar.clicked.connect(self.guardar_info)
        self.cargar_datos.clicked.connect(self.cargar_dato_ind)
        self.cargar_foto.clicked.connect(self.abrir_dialogo)
        self.eliminar.clicked.connect(self.eliminar_info)
        self.pais.currentTextChanged.connect(self.cargar_bandera)
        self.buscador.textEdited.connect(self.busqueda)
        self.fecha_nacimiento.dateChanged.connect(self.cambiar_edad)
       
        self.tabla_participantes.setColumnHidden(4, True)
        self.ruta_origen_imagen = ""
        
        self.cambiar_edad()
        sql.execute("SELECT pais FROM paises ORDER BY pais ASC")
        datos = sql.fetchall()
        
        for fila in datos:
            self.pais.addItem(fila[0])

        self.cargar_todos_los_datos()
    
    def abrir_dialogo(self):
        self.ruta_origen_imagen, _ = QFileDialog.getOpenFileName(self, "Seleccionar imagen", "", "Imágenes (*.png *.jpg *.bmp)")
        self.foto.setStyleSheet(f"QFrame {{ border-image: url({self.ruta_origen_imagen}) 0 0 0 0 stretch stretch; }}")

    def cargar_todos_los_datos(self):   
        
        # Obtener datos de la tabla
        sql.execute("SELECT nombre || ' ' || apellido, peso, altura, id, fecha_nacimiento FROM participantes")
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
                        edad = self.calcular_edad(registro[4])
                        self.tabla_participantes.setItem(fila, columna, QTableWidgetItem(str(edad)))
                        self.tabla_participantes.setItem(fila, columna + 1, QTableWidgetItem(str(valor)))

                    else:
                        self.tabla_participantes.setItem(fila, columna + 1, QTableWidgetItem(str(valor)))
                        
    def cargar_dato_ind(self):
        fila = self.tabla_participantes.currentRow()
        
        if fila >= 0:
            id = int(self.tabla_participantes.item(fila, 4).text())
            
            sql.execute(f"SELECT a.nombre, a.apellido, a.peso, a.altura, a.fecha_nacimiento, b.pais, a.ruta_imagen FROM participantes a INNER JOIN paises b ON a.id_nacionalidad = b.id WHERE a.id = {id}")
            datos = sql.fetchone()
            
            edad = self.calcular_edad(datos[4])
            
            self.nombre.setText(datos[0])
            self.apellido.setText(datos[1])
            self.peso.setValue(int(datos[2]))
            self.altura.setValue(int(datos[3]))
            self.edad.setText(str(edad))
            self.pais.setCurrentText(datos[5]) 
            self.id.setText(str(id))
            if datos[6]:
                self.foto.setStyleSheet(f"QFrame {{ border-image: url({datos[6]}) 0 0 0 0 stretch stretch; }}")
                self.ruta_modificar = datos[6]
                
            self.tabWidget.setCurrentIndex(0)
            self.buscador.setText("")
            self.cargar_todos_los_datos()
            self.estado.setText("Modificar") 
    
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

    def eliminar_info(self):
        id = self.id.text()
        if id == "":
            QMessageBox.critical(self, "Sin Datos Cargados", "No se ha cargado ningun dato que se pueda eliminar")
            return
        
        respuesta = QMessageBox.question(self, "Eliminar Registro", "¿Esta seguro de eliminar definitivamente este Registro", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if respuesta == QMessageBox.Yes:
            sql.execute(f"SELECT ruta_imagen FROM participantes WHERE id = {id}")
            rutas = sql.fetchone()
            ruta = rutas[0]
            
            if os.path.exists(ruta) and ruta != "":  # Verificar si el la imagen existe
                os.remove(ruta)
            
            sql.execute(f"DELETE FROM participantes WHERE id = {id}")
            conexion.commit()
            print("Filas afectadas:", sql.rowcount)
            
            self.nombre.setText("")
            self.apellido.setText("")
            self.id.setText("")
            self.fecha_nacimiento.setDate(QDate(2000, 1, 1))
            self.pais.setCurrentText("Alemania")
            self.peso.setValue(0)
            self.altura.setValue(0)
            self.foto.setStyleSheet("border: 3px solid black;")
            QMessageBox.information(self, "Datos Eliminados", "Registro Borrado exitosamente", QMessageBox.Ok)
            self.cargar_todos_los_datos()
            

         
    def guardar_info(self):
        nombre = self.nombre.text()
        apellido = self.apellido.text()
        altura = int(self.altura.text())
        peso = int(self.peso.text())
        pais = self.pais.currentText()
        fecha_nacimiento = self.fecha_nacimiento.text()
        id = self.id.text()
        
        if nombre == "" or apellido == "" or altura == 0 or peso == 0 or fecha_nacimiento == "":
            QMessageBox.critical(self, "Datos Faltantes", "Al parecer hay campos en blanco, por favor rellenalos", QMessageBox.Ok)
        else:
            if self.ruta_origen_imagen != "":
                ruta_destino = r"images\\participantes"
                os.makedirs(ruta_destino, exist_ok=True)
                nombre_base, extension = os.path.splitext(os.path.basename(self.ruta_origen_imagen))
                nuevo_nombre = f"ID-{id}{extension}"
                ruta_destino = os.path.join(ruta_destino, nuevo_nombre)
                shutil.copy(self.ruta_origen_imagen, ruta_destino)
                ruta_relativa = f"images/participantes/{nuevo_nombre}"
                
            
            sql.execute(f"SELECT id FROM paises WHERE pais LIKE '{pais}'")
            id_pais = sql.fetchone()
                
            if id == "" and self.estado.text() == "Registrar": # Crear Nuevo Registro
                
                if self.ruta_origen_imagen != "":
                    sql.execute("INSERT INTO participantes (nombre, apellido, id_nacionalidad, peso, altura, fecha_nacimiento, ruta_imagen) VALUES (?, ?, ?, ?, ?, ?, ?)", (nombre, apellido, id_pais[0], peso, altura, fecha_nacimiento, ruta_relativa))
                                
                else:
                    sql.execute("INSERT INTO participantes (nombre, apellido, id_nacionalidad, peso, altura, fecha_nacimiento) VALUES (?, ?, ?, ?, ?, ?)",  (nombre, apellido, id_pais[0], peso, altura, fecha_nacimiento))
            
                conexion.commit()
                print("Filas afectadas:", sql.rowcount)
                QMessageBox.information(self, "Datos Guardados", "Registro Creado exitosamente", QMessageBox.Ok)
                self.cargar_todos_los_datos()
                fila = self.tabla_participantes.rowCount() - 1
                self.id.setText(str(self.tabla_participantes.item(fila, 4).text()))
                
            elif id != "" and self.estado.text() == "Modificar": # Modificar Registro
                if self.ruta_origen_imagen != "":
                    sql.execute(f"UPDATE participantes SET nombre = ?, apellido = ?, peso = ?, altura = ?, fecha_nacimiento = ?, ruta_imagen = ?, id_nacionalidad = ? WHERE id = ?", (nombre, apellido, peso, altura, fecha_nacimiento, ruta_relativa, id_pais[0], id))
                                
                else:
                    sql.execute(f"UPDATE participantes SET nombre = ?, apellido = ?, peso = ?, altura = ?, fecha_nacimiento = ?, id_nacionalidad = ? WHERE id = ?", (nombre, apellido, peso, altura, fecha_nacimiento, id_pais[0], id))
                
                conexion.commit()
                print("Filas afectadas:", sql.rowcount)
                QMessageBox.information(self, "Datos Modificados", "Registro Modificado exitosamente", QMessageBox.Ok)
                self.cargar_todos_los_datos()
                
    def busqueda(self):
        texto = self.buscador.text()
         # Obtener datos de la tabla
        sql.execute(f"SELECT nombre || ' ' || apellido, peso, altura, id, fecha_nacimiento FROM participantes WHERE nombre || ' ' || apellido LIKE '%{texto}%'")
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
                        edad = self.calcular_edad(registro[4])
                        self.tabla_participantes.setItem(fila, columna, QTableWidgetItem(str(edad)))
                        self.tabla_participantes.setItem(fila, columna + 1, QTableWidgetItem(str(valor)))

                    else:
                        self.tabla_participantes.setItem(fila, columna + 1, QTableWidgetItem(str(valor)))
        
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

