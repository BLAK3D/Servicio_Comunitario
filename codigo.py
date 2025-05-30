from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFrame, QPushButton, QMessageBox, QLineEdit, QSpinBox, QComboBox, QDateEdit, QTableWidget, QTableWidgetItem, QFileDialog, QTabWidget
from PyQt5.QtCore import QTimer, Qt, QDate, QRegExp
from PyQt5.QtGui import QIntValidator, QPixmap, QRegExpValidator
from datetime import datetime
import sys, shutil, os, sqlite3, string, winsound, threading


class ViewerWindow(QMainWindow):
    
    def __init__(self):
        super(ViewerWindow,  self).__init__()
        loadUi("ViewerWindow.ui", self)
        self.WControl = None  # Referencia a la ventana de control (se asigna externamente)

        self.punto_azul = self.findChild(QLabel, "puntos_azul")
        self.punto_rojo = self.findChild(QLabel, "puntos_rojo1")
        self.contador = self.findChild(QLabel, "contador_1")
        self.contador2 = self.findChild(QLabel, "contador_2")
        self.medico_azul = self.findChild(QLabel, "medico_azul")
        self.medico_rojo = self.findChild(QLabel, "medico_rojo")
        self.bandera_azul = self.findChild(QLabel, "bandera_azul")
        self.bandera_rojo = self.findChild(QLabel, "bandera_rojo")
        self.foto_azul = self.findChild(QLabel, "foto_azul")
        self.foto_rojo = self.findChild(QLabel, "foto_rojo")
        self.nombre_azul = self.findChild(QLabel, "nombre_azul")
        self.nombre_rojo = self.findChild(QLabel, "nombre_rojo")
        self.blue_frame = self.findChild(QFrame, "frame_azul")
        self.yellow_blue_frame = self.findChild(QFrame, "tiempo_azul")
        self.yellow_red_frame = self.findChild(QFrame, "tiempo_rojo")
        self.foto_2 = self.findChild(QFrame, "foto_2")
        self.foto_1 = self.findChild(QFrame, "foto_1")
        self.info_rojo = self.findChild(QFrame, "info_rojo")
        self.info_azul = self.findChild(QFrame, "info_azul")
        self.amarilla_r1 = self.findChild(QFrame, "amarilla_r1")
        self.amarilla_r2 = self.findChild(QFrame, "amarilla_r2")
        self.amarilla_r3 = self.findChild(QFrame, "amarilla_r3")
        self.amarilla_a1 = self.findChild(QFrame, "amarilla_a1")
        self.amarilla_a2 = self.findChild(QFrame, "amarilla_a2")
        self.amarilla_a3 = self.findChild(QFrame, "amarilla_a3")
        self.tm1 = self.findChild(QPushButton, "tm1")
        self.tm2 = self.findChild(QPushButton, "tm2")
        
        self.tm1.hide()
        self.tm2.hide()
        self.medico_azul.hide()
        self.medico_rojo.hide()
        self.amarilla_a1.hide()
        self.amarilla_a2.hide()
        self.amarilla_a3.hide()
        self.amarilla_r1.hide()
        self.amarilla_r2.hide()
        self.amarilla_r3.hide()
        
        self.ajuste_tiempo(0)
        self.play_tiempo()
        
        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.cuadrar)
        self.timer2.start(1)
        
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowMinMaxButtonsHint) # Deshabilitar boton de cierre

    def ajuste_ventana(self):
        self.yellow_blue_frame.setGeometry(0, self.blue_frame.height() - 60, round(self.blue_frame.width() * 0.55), 116)
        self.yellow_red_frame.setGeometry(0, -60, round(self.blue_frame.width() * 0.55), 116)
        self.contador.setGeometry(self.yellow_blue_frame.width() - 265, 10, 250, 90)
        self.contador2.setGeometry(self.yellow_blue_frame.width() - 265, 10, 250, 90)
        self.punto_rojo.setGeometry(self.blue_frame.width() -320, round((self.blue_frame.height() - 240)/ 2), 300, 240)
        self.punto_azul.setGeometry(self.blue_frame.width() -320, round((self.blue_frame.height() - 240)/ 2), 300, 240)
        self.foto_1.setGeometry(30, round((self.blue_frame.height() -210)/2), 130, 150)
        self.foto_2.setGeometry(30, round(((self.blue_frame.height() -210)/2) +60), 130, 150)
        
        if self.blue_frame.width() > 1030:
            self.info_azul.setGeometry(170, round((self.blue_frame.height() -250)/2) , 540, 190)
            self.info_rojo.setGeometry(170, round((self.blue_frame.height() -250)/2) + 60 , 540, 190)
        else:
            self.info_azul.setGeometry(170, round((self.blue_frame.height() -250)/2), 410, 190)
            self.info_rojo.setGeometry(170, round((self.blue_frame.height() -250)/2) + 60 , 410, 190)
        
        self.tamano_letra(self.punto_azul, round(self.blue_frame.height() * 0.56))
        self.tamano_letra(self.punto_rojo, round(self.blue_frame.height() * 0.56))
        
    def resizeEvent(self, event):
        # Ajustar posición cuando la ventana cambia de tamaño 
        self.ajuste_ventana()
        super().resizeEvent(event)
       
    def cuadrar(self):
        self.ajuste_ventana()
        self.timer2.stop()
        
    def tamano_letra(self, label, tamaño: int):
        fuente_actual = label.font()  # Obtener la fuente actual
        fuente_actual.setPointSize(tamaño)  # Cambiar el tamaño en puntos
        label.setFont(fuente_actual)  # Aplicar de nuevo al label
        
    def actualizar_contador(self):
        if self.segundos >= 0:
            minutos = self.segundos // 60
            segundos = self.segundos % 60
            self.contador.setText(f"{minutos}:{segundos:02d}")
            self.contador2.setText(f"{minutos}:{segundos:02d}")
            self.segundos -= 1
        else:
            self.timer.stop() 
        
    def play_tiempo(self):
        if not self.timer.isActive():
            self.timer.start(1000)
            print("Temporizador iniciado")
    
    def pause_tiempo(self):
        if self.timer.isActive():
            self.timer.stop()
            print("Temporizador pausado")
            
    def ajuste_tiempo(self, seg: int):
        self.segundos = seg  # Tiempo inicial en segundos
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_contador)
   
class ControlWindow(QMainWindow):
    def __init__(self, WVierwer):
        super().__init__()
        loadUi("ControlWindow.ui", self)
        self.WVierwer = WVierwer
        self.WControl = None
        self.boton_control = self.findChild(QPushButton, "play_pause")
        self.editar = self.findChild(QPushButton, "editar")
        self.cancelar = self.findChild(QPushButton, "cancelar")
        self.subir_pts_azul = self.findChild(QPushButton, "subir_pts_azul")
        self.bajar_pts_azul = self.findChild(QPushButton, "bajar_pts_azul")
        self.subir_pts_rojo = self.findChild(QPushButton, "subir_pts_rojo")
        self.bajar_pts_rojo = self.findChild(QPushButton, "bajar_pts_rojo")
        self.un_pto = self.findChild(QPushButton, "un_pto")
        self.dos_pts = self.findChild(QPushButton, "dos_pts")
        self.cuatro_pts = self.findChild(QPushButton, "cuatro_pts")
        self.cerrar_dar_pts = self.findChild(QPushButton, "cerrar_dar_pts")
        self.amarilla_mas_azul = self.findChild(QPushButton, "amarilla_mas_azul")
        self.amarilla_menos_azul = self.findChild(QPushButton, "amarilla_menos_azul")
        self.amarilla_mas_rojo = self.findChild(QPushButton, "amarilla_mas_rojo")
        self.amarilla_menos_rojo = self.findChild(QPushButton, "amarilla_menos_rojo")
        self.tm_azul = self.findChild(QPushButton, "tm_azul")
        self.tm_rojo = self.findChild(QPushButton, "tm_rojo")
        self.reset_tm_azul = self.findChild(QPushButton, "reset_tm_azul")
        self.reset_tm_rojo = self.findChild(QPushButton, "reset_tm_rojo")
        self.config = self.findChild(QPushButton, "config")
        self.tiempo_seg = self.findChild(QLineEdit, "tiempo_seg")
        self.tiempo_min = self.findChild(QLineEdit, "tiempo_min")
        self.dar_pts = self.findChild(QFrame, "dar_pts")
        self.pausado = self.findChild(QLabel, "pausado")
        self.ctrl_pts_azul = self.findChild(QLabel, "ctrl_pts_azul")
        self.ctrl_pts_rojo = self.findChild(QLabel, "ctrl_pts_rojo")
        self.amarillas_azul = self.findChild(QLabel, "amarillas_azul")
        self.amarillas_rojo = self.findChild(QLabel, "amarillas_rojo")
        self.participante_azul = self.findChild(QLabel, "participante_azul")
        self.participante_rojo = self.findChild(QLabel, "participante_rojo")
        self.rojo_tm = self.findChild(QLabel, "rojo_tm")
        self.azul_tm = self.findChild(QLabel, "azul_tm")
        self.tiempo_min.setText("0")
        self.tiempo_seg.setText("00")
        self.cancelar.hide()
        self.dar_pts.hide()
        self.reset_tm_rojo.hide()
        self.reset_tm_azul.hide()
        
        self.config.clicked.connect(self.abrir_configuracion)
        self.boton_control.clicked.connect(self.cambiar_estado_timer)
        self.editar.clicked.connect(self.permitir_cambios)
        self.cancelar.clicked.connect(self.restaurar_tiempo)
        
        self.subir_pts_azul.clicked.connect(lambda: self.mostrar_dar_puntos("left", "azul", "+"))
        self.bajar_pts_azul.clicked.connect(lambda: self.mostrar_dar_puntos("left", "azul", "-"))
        self.subir_pts_rojo.clicked.connect(lambda: self.mostrar_dar_puntos("right", "rojo", "+"))
        self.bajar_pts_rojo.clicked.connect(lambda: self.mostrar_dar_puntos("right", "rojo", "-"))
        self.un_pto.clicked.connect(lambda: self.srPts(1)) # Sumar o Restar Pts
        self.dos_pts.clicked.connect(lambda: self.srPts(2)) # Sumar o Restar Pts
        self.cuatro_pts.clicked.connect(lambda: self.srPts(4)) # Sumar o Restar Pts
        self.cerrar_dar_pts.clicked.connect(self.mostrar_dar_puntos)
        
        self.amarilla_mas_azul.clicked.connect(lambda: self.srAmarillas("A", "+"))
        self.amarilla_menos_azul.clicked.connect(lambda: self.srAmarillas("A", "-"))
        self.amarilla_mas_rojo.clicked.connect(lambda: self.srAmarillas("R", "+"))
        self.amarilla_menos_rojo.clicked.connect(lambda: self.srAmarillas("R", "-"))
        
        self.tm_azul.clicked.connect(lambda: self.tiempo_medico("A"))
        self.tm_rojo.clicked.connect(lambda: self.tiempo_medico("R"))
        self.reset_tm_azul.clicked.connect(lambda: self.reset_tm("A"))
        self.reset_tm_rojo.clicked.connect(lambda: self.reset_tm("R"))

        validador_seg = QIntValidator(0, 59)
        self.tiempo_seg.setValidator(validador_seg)
        self.tiempo_seg.setMaxLength(2)
        self.tiempo_seg.textChanged.connect(self.validar_seg)
        
        validador_min = QIntValidator(0, 9)
        self.tiempo_min.setValidator(validador_min)
        self.tiempo_min.setMaxLength(1)
        self.tiempo_min.textChanged.connect(self.capturar_cambio_tiempo)
        
        self.timer_principal = QTimer()
        self.timer_principal.timeout.connect(self.actualizar_contador_control)
        
        self.timer_azul = QTimer()
        self.timer_azul.timeout.connect(lambda: self.contador_medico("A"))
        self.timer_rojo = QTimer()
        self.timer_rojo.timeout.connect(lambda: self.contador_medico("R"))
        
    def closeEvent(self, event):
        confirm = QMessageBox.question(
            self,
            "Confirmar cierre",
            "¿Estás seguro que deseas cerrar la ventana? (Se cerrara todas las ventanas del sistema)",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.WVierwer.close()  # Cierra la ventana de espectador
            event.accept()
        else:
            event.ignore()
    
    def mostrar_dar_puntos(self, lugar = "", color= "", SR=""): # SR = Sumar o Restar
        
        if lugar == "left":
            self.dar_pts.setGeometry(25, 250, 55, 180)
        elif lugar == "right":
            self.dar_pts.setGeometry(580, 250, 55, 180)
            
        if SR == "+":
            self.dar_pts.setStyleSheet(" QFrame { border: 3px solid black; border-radius: 8px; background-color: rgb(0, 0, 0); } QPushButton { color: rgb(0, 255, 255); border: 2px solid rgb(0, 255, 255); }")
        elif SR == "-":
            self.dar_pts.setStyleSheet("QFrame { border: 3px solid black; border-radius: 8px; background-color: rgb(0, 0, 0); } QPushButton { color: rgb(255, 0, 0); border: 2px solid rgb(255, 0, 0); }")
            
        if color != "" and SR != "":
            self.srPtsColor = color
            self.srPtsSR = SR
            self.dar_pts.show()
        else:
            self.dar_pts.hide()
 
    def reset_tm (self, color):

        color1 = "Azul" if color == "A" else "Rojo"
            
        confirm = QMessageBox.question(
            self,
            "Confirmar Restablecer Tiempo Medico",
            f"¿Esta seguro de Restablecer el Tiempo Medico del Participante {color1}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if color == "A" and confirm == QMessageBox.Yes:
            self.azul_tm.setText("2:00")
            self.WVierwer.medico_azul.hide()
            self.WVierwer.tm1.hide()
            self.reset_tm_azul.hide()
            
        elif color == "R" and confirm == QMessageBox.Yes:
            self.rojo_tm.setText("2:00")
            self.WVierwer.medico_rojo.hide()
            self.WVierwer.tm2.hide()
            self.reset_tm_rojo.hide()
        
    def tiempo_medico(self, color = ""):
        tmp = self.azul_tm.text().split(":")
        min = int(tmp[0])
        seg = int(tmp[1])
        self.seg_azul = seg + (min * 60)
            
        tmp = self.rojo_tm.text().split(":")
        min = int(tmp[0])
        seg = int(tmp[1])
        self.seg_rojo = seg + (min * 60)
            
        if color == "A":
            if not self.timer_azul.isActive():
                self.WVierwer.medico_azul.show()
                self.WVierwer.tm1.show()
                self.reset_tm_azul.hide()
                self.azul_tm.setStyleSheet("color: red;")
                self.timer_azul.start(1000)
                self.timer_principal.stop()
                self.WVierwer.timer.stop()
                self.pausado.setText("Pausado")
            else:
                self.azul_tm.setStyleSheet("")
                self.reset_tm_azul.show()
                self.timer_azul.stop()
                if not self.timer_rojo.isActive():
                    self.timer_principal.start(1000)
                    self.WVierwer.timer.start(1000)
                    self.pausado.setText("")
        else:
            if not self.timer_rojo.isActive():
                self.WVierwer.medico_rojo.show()
                self.WVierwer.tm2.show()
                self.reset_tm_rojo.hide()
                self.rojo_tm.setStyleSheet("color: red;")
                self.timer_rojo.start(1000)
                self.timer_principal.stop()
                self.WVierwer.timer.stop()
                self.pausado.setText("Pausado")
            else:
                self.rojo_tm.setStyleSheet("")
                self.reset_tm_rojo.show()
                self.timer_rojo.stop()
                if not self.timer_azul.isActive():
                    self.timer_principal.start(1000)
                    self.WVierwer.timer.start(1000)
                    self.pausado.setText("")

    def contador_medico(self, color):
        if self.seg_azul > 0 and color == "A":
            minutos = self.seg_azul // 60
            segundos = self.seg_azul % 60
            self.azul_tm.setText(f"{minutos}:{segundos:02d}")
            self.WVierwer.medico_azul.setText(f"{minutos}:{segundos:02d}")
            self.seg_azul -= 1
            
        elif self.seg_azul == 0 and color == "A":
            self.reset_tm_azul.show()
            self.timer_azul.stop()
            
        elif self.seg_rojo > 0 and color == "R":
            min2 = self.seg_rojo // 60
            seg2 = self.seg_rojo % 60
            self.rojo_tm.setText(f"{min2}:{seg2:02d}")
            self.WVierwer.medico_rojo.setText(f"{min2}:{seg2:02d}")
            self.seg_rojo -= 1
            
        elif self.seg_rojo == 0 and color == "R":
            self.reset_tm_rojo.show()
            self.timer_rojo.stop()
        
    def srAmarillas(self, color = "", sr = ""):
        aa = int(self.amarillas_azul.text()) #aa = Amarillas Azul
        ar = int(self.amarillas_rojo.text()) #ar = Amarillas Rojo
        
        if color == "A" and sr == "+" and aa < 3:
            aa += 1
            self.amarillas_azul.setText(f"{aa}")
            
            if aa == 1:
                self.WVierwer.amarilla_a1.show()
            elif aa == 2:
                self.WVierwer.amarilla_a2.show()
            else:
                self.WVierwer.amarilla_a3.show()
            
        elif color == "A" and sr == "-" and aa > 0:
            aa -= 1
            self.amarillas_azul.setText(f"{aa}")
            
            if aa == 0:
                self.WVierwer.amarilla_a1.hide()
            elif aa == 1:
                self.WVierwer.amarilla_a2.hide()
            else:
                self.WVierwer.amarilla_a3.hide()

        elif color == "R" and sr == "+" and ar < 3:
            ar += 1
            self.amarillas_rojo.setText(f"{ar}")
            
            if ar == 1:
                self.WVierwer.amarilla_r1.show()
            elif ar == 2:
                self.WVierwer.amarilla_r2.show()
            else:
                self.WVierwer.amarilla_r3.show()
                
        elif color == "R" and sr == "-" and ar > 0:
            ar -= 1
            self.amarillas_rojo.setText(f"{ar}")
            
            if ar == 0:
                self.WVierwer.amarilla_r1.hide()
            elif ar == 1:
                self.WVierwer.amarilla_r2.hide()
            else:
                self.WVierwer.amarilla_r3.hide()
    
    def srPts(self, nro: int):
        if self.srPtsColor == "azul" and self.srPtsSR == "+":
            self.ctrl_pts_azul.setText(str(int(self.ctrl_pts_azul.text()) + nro))
            self.WVierwer.punto_azul.setText(str(self.ctrl_pts_azul.text()))
            
        elif self.srPtsColor == "azul" and self.srPtsSR == "-":
            if int(self.ctrl_pts_azul.text()) - nro < 0:
                self.ctrl_pts_azul.setText("0")
            else:
                self.ctrl_pts_azul.setText(str(int(self.ctrl_pts_azul.text()) - nro))
            self.WVierwer.punto_azul.setText(str(self.ctrl_pts_azul.text()))
                
        elif self.srPtsColor == "rojo" and self.srPtsSR == "+":
            self.ctrl_pts_rojo.setText(str(int(self.ctrl_pts_rojo.text()) + nro))
            self.WVierwer.punto_rojo.setText(str(self.ctrl_pts_rojo.text()))
            
        elif self.srPtsColor == "rojo" and self.srPtsSR == "-":
            if int(self.ctrl_pts_rojo.text()) - nro < 0:
                self.ctrl_pts_rojo.setText("0")
            else:
                self.ctrl_pts_rojo.setText(str(int(self.ctrl_pts_rojo.text()) - nro))
            self.WVierwer.punto_rojo.setText(str(self.ctrl_pts_rojo.text()))
                
        self.dar_pts.hide()
                
    def validar_seg(self, texto):
        self.tiempo_seg.textChanged.disconnect()
        try:
            if texto:
                valor = int(texto)
                if valor > 59:
                    self.tiempo_seg.setText("59")
                elif valor < 0:
                    self.tiempo_seg.setText("00")
        except ValueError:
            self.tiempo_seg.setText("00")
        finally:
            self.tiempo_seg.textChanged.connect(self.validar_seg)
        self.capturar_cambio_tiempo()
    
    def capturar_cambio_tiempo(self):
        if not self.timer_principal.isActive():
            try:
                tm = int(self.tiempo_seg.text()) 
            except:
                tm = 0
            
            try:
                ts = int(self.tiempo_min.text()) * 60
            except:
                ts = 0
            
            seg = tm + ts
            if self.WVierwer.segundos + 1 != seg:
                self.cancelar.show()
                        
    def cambiar_estado_timer(self):
        if (self.participante_azul.text() == "Participante Azul" or self.participante_rojo.text() ==  "Participante Rojo") and self.timer_principal.isActive() == False:
            resp = QMessageBox.warning(self, "Sin Datos Cargados", "Hay datos de algun participante que no se han cargado, desea iniciar el tiempo de todas maneras?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if resp == QMessageBox.No:
                return
        
        if not self.WVierwer.timer.isActive(): # Cuando esta pausado (darle Play)
            try:
                tm = int(self.tiempo_seg.text()) 
            except:
                tm = 0
            
            try:
                ts = int(self.tiempo_min.text()) * 60
            except:
                ts = 0
            
            self.seg = tm + ts
            
            self.tiempo_min.setFocusPolicy(Qt.NoFocus)
            self.tiempo_seg.setFocusPolicy(Qt.NoFocus)
            self.tiempo_min.setReadOnly(True)
            self.tiempo_seg.setReadOnly(True)
            self.editar.hide()
            self.cancelar.hide()
            self.pausado.hide()
            
            self.WVierwer.ajuste_tiempo(self.seg)
            self.WVierwer.play_tiempo()
            self.timer_principal.start(1000)
            
        else: # Cuando esta activo (darle pause)
            self.editar.show()
            self.pausado.show()
            
            self.WVierwer.pause_tiempo()
            self.timer_principal.stop()
            
    def permitir_cambios(self):
        self.tiempo_min.setFocusPolicy(Qt.ClickFocus)
        self.tiempo_seg.setFocusPolicy(Qt.ClickFocus)
        self.tiempo_min.setReadOnly(False)
        self.tiempo_seg.setReadOnly(False)
        self.tiempo_seg.setFocus()
    
    def restaurar_tiempo(self):
        seg = self.WVierwer.segundos + 1
        if seg >= 0 :
            minutos = seg // 60
            segundos = seg % 60
        self.tiempo_min.setText(f"{minutos}")
        if segundos < 10:
            self.tiempo_seg.setText(f"0{segundos}")
        else:
            self.tiempo_seg.setText(f"{segundos}")
        self.cancelar.hide()
            
    def actualizar_contador_control(self):
        if self.seg > 0:
            minutos = self.seg // 60
            segundos = self.seg % 60
            self.tiempo_min.setText(f"{minutos}")
            if segundos < 10:
                self.tiempo_seg.setText(f"0{segundos}")
            else:
                self.tiempo_seg.setText(f"{segundos}")
            self.seg -= 1
        else:
            self.timer_principal.stop() 
            self.editar.show()   
            self.pausado.show()
            self.tiempo_seg.setText("00")
            threading.Thread(target=lambda: winsound.Beep(350, 1000)).start()
   
    def abrir_configuracion(self):
        if not self.timer_principal.isActive():
            WConfig.show()
        else:
            QMessageBox.critical(self, "Encuentro Acivo", "No se pueden realizar configuraciones mientras el encuentra esta activo. Finaliza el encuentro para hacer configuraciones")
        
class ConfigWindow(QMainWindow):
    def __init__(self, WViewer, WControl) :
        super(ConfigWindow,  self).__init__()
        loadUi("ConfigWindow.ui", self)
        self.WViewer = WViewer
        self.WControl = WControl
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
        self.asignar_rojo = self.findChild(QPushButton, "asignar_rojo")
        self.asignar_azul = self.findChild(QPushButton, "asignar_azul")
        self.vaciar_campos = self.findChild(QPushButton, "vaciar_campos")
        self.tabla_participantes = self.findChild(QTableWidget, "tabla_participantes")
        self.bandera = self.findChild(QFrame, "bandera")
        self.foto = self.findChild(QFrame, "foto")
        self.tabWidget = self.findChild(QTabWidget, "tabWidget")
        self.estado = self.findChild(QLabel, "estado")
        
        self.idRojoAsignado = ""
        self.idAzulAsignado = ""
        
        self.guardar.clicked.connect(self.guardar_info)
        self.cargar_datos.clicked.connect(self.cargar_dato_ind)
        self.cargar_foto.clicked.connect(self.abrir_dialogo)
        self.eliminar.clicked.connect(self.eliminar_info)
        self.vaciar_campos.clicked.connect(self.vaciarCampos)
        self.asignar_azul.clicked.connect(lambda: self.asignar_participante("A"))
        self.asignar_rojo.clicked.connect(lambda: self.asignar_participante("R"))
        self.pais.currentTextChanged.connect(self.cargar_bandera)
        self.buscador.textEdited.connect(self.busqueda)
        self.fecha_nacimiento.dateChanged.connect(self.cambiar_edad)
       
        solo_letras = QRegExp("[A-Za-zÁÉÍÓÚáéíóúÑñ ]+")
        self.buscador.setValidator(QRegExpValidator(solo_letras, self.buscador))
        self.nombre.setValidator(QRegExpValidator(solo_letras, self.nombre))
        self.apellido.setValidator(QRegExpValidator(solo_letras, self.apellido))

       
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
        else:
            self.tabla_participantes.setRowCount(0)
                        
    def cargar_dato_ind(self):
        fila = self.tabla_participantes.currentRow()
        
        if fila >= 0:
            id = int(self.tabla_participantes.item(fila, 4).text())
            
            sql.execute(f"SELECT a.nombre, a.apellido, a.peso, a.altura, a.fecha_nacimiento, b.pais, a.ruta_imagen FROM participantes a INNER JOIN paises b ON a.id_nacionalidad = b.id WHERE a.id = ?", (id,))
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
    
    def vaciarCampos(self):
        self.nombre.setText("")
        self.apellido.setText("")
        self.id.setText("")
        self.fecha_nacimiento.setDate(QDate(2000, 1, 1))
        self.pais.setCurrentText("Alemania")
        self.peso.setValue(0)
        self.altura.setValue(0)
        self.foto.setStyleSheet("border: 3px solid black;")
        self.estado.setText("Registrar")
    
    def eliminar_info(self):
        id = self.id.text()
        if id == "":
            QMessageBox.critical(self, "Sin Datos Cargados", "No se ha cargado ningun dato que se pueda eliminar")
            return
        
        respuesta = QMessageBox.question(self, "Eliminar Registro", "¿Esta seguro de eliminar definitivamente este Registro", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if respuesta == QMessageBox.Yes:
            sql.execute(f"SELECT ruta_imagen FROM participantes WHERE id = ?", (id,))
            rutas = sql.fetchone()

            if rutas[0] != None:
                if os.path.exists(rutas[0]):  # Verificar si el la imagen existe
                    os.remove(rutas[0])
            
            sql.execute(f"DELETE FROM participantes WHERE id = ?", (id,))
            conexion.commit()
            print("Filas afectadas:", sql.rowcount)
            
            self.vaciarCampos()
            QMessageBox.information(self, "Datos Eliminados", "Registro Borrado exitosamente", QMessageBox.Ok)
            self.buscador.setText("")
            self.cargar_todos_los_datos()
   
    def guardar_info(self):
        nombre = string.capwords(self.nombre.text().strip())
        apellido = string.capwords(self.apellido.text().strip())
        altura = int(self.altura.text())
        peso = int(self.peso.text())
        pais = self.pais.currentText()
        fecha_nacimiento = self.fecha_nacimiento.text()
        id = self.id.text()
        
        if nombre == "" or apellido == "" or altura == 0 or peso == 0 or fecha_nacimiento == "":
            QMessageBox.critical(self, "Datos Faltantes", "Al parecer hay campos en blanco, por favor rellenalos", QMessageBox.Ok)
        else:
            ruta_relativa = self.rutaRelativa(id)
                
            sql.execute(f"SELECT id FROM paises WHERE pais LIKE ?", (pais,))
            id_pais = sql.fetchone()
                
            if id == "" and self.estado.text() == "Registrar": # Crear Nuevo Registro
                
                if self.ruta_origen_imagen != "":
                    sql.execute("INSERT INTO participantes (nombre, apellido, id_nacionalidad, peso, altura, fecha_nacimiento) VALUES (?, ?, ?, ?, ?, ?)", (nombre, apellido, id_pais[0], peso, altura, fecha_nacimiento))
                    print("Filas afectadas:", sql.rowcount)
                    QMessageBox.information(self, "Datos Guardados", "Registro Creado exitosamente", QMessageBox.Ok)
                    self.buscador.setText("")
                    self.cargar_todos_los_datos()
                    
                    fila = self.tabla_participantes.rowCount() - 1
                    self.id.setText(str(self.tabla_participantes.item(fila, 4).text()))
                    ruta_relativa = self.rutaRelativa(self.id.text())
                    sql.execute(f"UPDATE participantes SET ruta_imagen = ? WHERE id = ?", (ruta_relativa, self.id.text()))
                    conexion.commit()
                                
                else:
                    sql.execute("INSERT INTO participantes (nombre, apellido, id_nacionalidad, peso, altura, fecha_nacimiento) VALUES (?, ?, ?, ?, ?, ?)",  (nombre, apellido, id_pais[0], peso, altura, fecha_nacimiento))
                    conexion.commit()
                    print("Filas afectadas:", sql.rowcount)
                    QMessageBox.information(self, "Datos Guardados", "Registro Creado exitosamente", QMessageBox.Ok)
                    self.buscador.setText("")
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
                self.buscador.setText("")
                self.cargar_todos_los_datos()
                
    def rutaRelativa(self, id):
        if self.ruta_origen_imagen != "" and id != "":
            ruta_destino = r"images\\participantes"
            os.makedirs(ruta_destino, exist_ok=True)
            nombre_base, extension = os.path.splitext(os.path.basename(self.ruta_origen_imagen))
            nuevo_nombre = f"ID-{id}{extension}"
            ruta_destino = os.path.join(ruta_destino, nuevo_nombre)
            shutil.copy(self.ruta_origen_imagen, ruta_destino)
            return f"images/participantes/{nuevo_nombre}"
            
    def asignar_participante(self, color):
        id = self.id.text()
        
        if id == "":
            QMessageBox.critical(self, "Sin Datos Cargados", "No hay datos cargados, si vas a ingresar uno nuevo, guarda el registro y vuelve a presionar este boton")
            return
        
        if id == self.idAzulAsignado or id == self.idRojoAsignado:
            QMessageBox.critical(self, "Datos en uso", "Estos datos ya estan asignados a un participante, intenta con otros datos")
            return

        sql.execute(f"SELECT ruta_imagen FROM paises WHERE pais LIKE  ?", (self.pais.currentText(),))
        datos = sql.fetchone()
        ruta = datos[0]
        
        sql.execute(f"SELECT ruta_imagen FROM participantes WHERE id = ?", (id,))
        datos2 = sql.fetchone()
        ruta_participante = "" if datos2[0] == None else datos2[0]
        
        nombre_completo = f"{self.nombre.text()} {self.apellido.text()}"

        if color == "A":
            self.WControl.participante_azul.setText(f"{nombre_completo}")
            self.WViewer.bandera_azul.setPixmap(QPixmap(f"{ruta}"))
            self.WViewer.bandera_azul.setScaledContents(True)
            self.WViewer.foto_azul.setPixmap(QPixmap(ruta_participante))
            self.WViewer.foto_azul.setScaledContents(True)
            self.WViewer.nombre_azul.setText(f"{nombre_completo}")
            self.idRojoAsignado = id
        elif color == "R":
            self.WControl.participante_rojo.setText(f"{nombre_completo}")
            self.WViewer.bandera_rojo.setPixmap(QPixmap(f"{ruta}"))
            self.WViewer.bandera_rojo.setScaledContents(True)
            self.WViewer.foto_rojo.setPixmap(QPixmap(ruta_participante))
            self.WViewer.foto_rojo.setScaledContents(True)
            self.WViewer.nombre_rojo.setText(f"{nombre_completo}")
            self.idAzulAsignado = id
            
    def busqueda(self):
        texto = self.buscador.text()
         # Obtener datos de la tabla
        sql.execute(f"SELECT nombre || ' ' || apellido, peso, altura, id, fecha_nacimiento FROM participantes WHERE nombre || ' ' || apellido LIKE ?", (f"%{texto}%",))
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
        else:
            self.tabla_participantes.setRowCount(0) 

if __name__ ==  "__main__":
    try:
        conexion = sqlite3.connect("BD.db")
        sql = conexion.cursor()
        app = QApplication(sys.argv)
        WViewer = ViewerWindow()
        WControl = ControlWindow(WViewer)
        WConfig = ConfigWindow(WViewer, WControl)
        
        # Configurar referencias cruzadas
        WViewer.WControl = WControl
        WControl.WConfig = WConfig

        WViewer.show()
        WControl.show()

        sys.exit(app.exec_())
        
    except Exception as e:
        print(e)
    