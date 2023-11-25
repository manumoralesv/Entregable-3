#Integrantes: -Miguel Zapata miguel.zapata1@udea.edu.co
# -Manuela Morales - manuela.moralesv@udea.edu.co#

import pydicom
import os
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QLineEdit, QFileDialog
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import sys 

class VentanaPrincipal(QMainWindow):
    def __init__(self, ppal =None):
        super().__init__()
        loadUi('interfaces/ventana_principal.ui',self)
        self.setup()
    
    def setup(self):
        #se programa la señal para el boton
        self.boton_ingreso.clicked.connect(self.entrada)
    
    def asignarControlador(self,control):
        #Se asigna el controlador
        self.__controlador = control

    def entrada(self):
        #Función que nos servirá para llevar a cabo el funcionamiento del botón de ingreso
        self.edit_password = QLineEdit(self)
        user = self.usuario.text()
        password = self.clave.text()
        #esta informacion la debemos pasar al controlador
        resultado = self.__controlador.verificar_usuario(user,password)
        #se crea la ventana de resultado
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Resultado")
        if resultado == True:
            ventana_vista= Ingreso(self)
            self.hide()
            ventana_vista.show()
            resultado = False 
        else:
            msg.setText("Usuario o contraseña no validos")
            msg.show()

class Ingreso(QDialog):
    def __init__(self,ppal=None):
        super().__init__(ppal)
        loadUi('interfaces/vista_imagenes.ui',self)
        self.img()
        
    def img(self):
        #se organizan los botones 
        self.boton_cargar.clicked.connect(self.cargar_img)
        self.canvas = FigureCanvas(plt.Figure())
        self.vista_imagenes.addWidget(self.canvas)
        self.slider_img.valueChanged.connect(self.actualizar_imagen)
        self.boton_salir.clicked.connect(lambda:self.close()) 
        #self.vista_imagenes.addWidget(self.actualizar_imagen)
        
    def asignarControlador(self,c):
        self.__controlador = c

    def cargar_img(self):
        self.path = []
        #se abre el cuadro de dialogo para cargar
        self.archivo_cargado = QFileDialog.getExistingDirectory(self, "Abrir imagenes")
        self.archivos = os.listdir(self.archivo_cargado)
        for i in self.archivos:
            self.path.append(f'{self.archivo_cargado}/{i}')
        if self.path:
            self.slider_img.setRange(0, len(self.path) - 1)
            self.slider_img.setValue(0)
            self.actualizar_imagen()
            
    def actualizar_imagen(self):
        indice = self.slider_img.value()
        if 0 <= indice < len(self.path):
            imagen_dicom_path = self.path[indice]
            dataset = pydicom.dcmread(imagen_dicom_path)
            
            # Convertir la imagen DICOM a formato numpy
            imagen_array = dataset.pixel_array
            self.canvas.figure.clf()
            ax = self.canvas.figure.add_subplot(111)
            ax.imshow(imagen_array, cmap='gray')
            ax.axis("off")
            self.canvas.draw()
            
            #Sacamos la información y creamos el label
            name = dataset[0x0010,0x0010].value
            doc = dataset[0x0010,0x0020].value
            sex = dataset[0x0010,0x0040].value
            mod = dataset[0x0008,0x0060].value
            study_desc = dataset[0x0008,0x1030].value
            self.info_data.setText(f'''
                                   Nombre: {name}
                                   Id: {doc}
                                   Sexo: {sex}
                                   Modalidad: {mod}
                                   Descripción del estudio: {study_desc}''')