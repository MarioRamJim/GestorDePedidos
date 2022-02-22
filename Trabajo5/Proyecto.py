from cgitb import text
import json
import sys
from tkinter import DoubleVar
from turtle import color
from PySide6 import QtCore
from PySide6.QtWidgets import *
from PySide6.QtSql import *
from PySide6.QtCore import *
from MainWindow import Ui_MainWindow 
import GestionarProductos
import GestionarPedidos
from reportlab.pdfgen.canvas import Canvas
from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
import pyqtgraph as pg
import pyqtgraph.exporters
from pathlib import Path
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
import webbrowser

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.prod = {"id":"","nombre":"","precio":""}
        self.pedido = {"id":"","idProducto":"","cantidad":"","dia":""}

        #Configuración del Wizard de inserción de productos
        self.wizardInsert = QWizard()
        self.wizardInsert.setWizardStyle(QWizard.ModernStyle)
        self.insertPage1 = QWizardPage()
        self.insertPage1.setTitle('Inserción de un nuevo producto')
        self.insertPage1.setSubTitle('Escoge los siguientes datos a insertar')
        self.labelInsert1 = QLabel()
        self.labelInsert1.setText('Id del producto a insertar')
        self.lineEditInsert1 = QLineEdit()
        self.labelInsert2 = QLabel()
        self.labelInsert2.setText('Nombre del producto a insertar')
        self.lineEditInsert2 = QLineEdit()
        self.labelInsert3 = QLabel()
        self.labelInsert3.setText('Precio del producto a insertar')
        self.lineEditInsert3 = QLineEdit()
        self.formLayoutInsert1 = QFormLayout(self.insertPage1)
        self.formLayoutInsert1.addRow(self.labelInsert1,self.lineEditInsert1)
        self.formLayoutInsert1.addRow(self.labelInsert2,self.lineEditInsert2)
        self.formLayoutInsert1.addRow(self.labelInsert3,self.lineEditInsert3)
        self.insertPage1.registerField('Producto', self.lineEditInsert1,self.lineEditInsert1.text(),'textChanged')
        self.wizardInsert.addPage(self.insertPage1)
        self.insertPage1.setFinalPage(True)

        #Configuración del wizard de eliminación de productos
        self.wizardElim = QWizard()
        self.wizardElim.setWizardStyle(QWizard.ModernStyle)
        self.EliminarPage1 = QWizardPage()
        self.EliminarPage1.setTitle('Eliminación de un producto')
        self.EliminarPage1.setSubTitle('Escoge el producto a eliminar')
        self.labelElim = QLabel()
        self.labelElim.setText('ID del producto a eliminar')
        self.lineEditElim = QLineEdit()
        self.formLayoutElim = QFormLayout(self.EliminarPage1)
        self.formLayoutElim.addRow(self.labelElim,self.lineEditElim)
        self.EliminarPage1.registerField('Producto', self.lineEditElim,self.lineEditElim.text(),'textChanged')
        self.wizardElim.addPage(self.EliminarPage1)
        self.EliminarPage1.setFinalPage(True)

        #Configuración del wizard de consulta 
        self.wizardConsultarInf = QWizard()
        self.wizardConsultarInf.setWizardStyle(QWizard.ModernStyle)
        self.ConsultaPage1 = QWizardPage()
        self.ConsultaPage1.setTitle('Consulta de una tabla')
        self.ConsultaPage1.setSubTitle('Escoge una tabla a consultar')
        self.labelConsult = QLabel()
        self.labelConsult.setText('Tabla a consultar')
        self.ComboBoxEditConsult = QComboBox()
        self.ComboBoxEditConsult.addItem("Productos")
        self.ComboBoxEditConsult.addItem("Pedidos")
        self.listWidget = QTableWidget()
        self.labelConfirmConsult = QLabel()
        self.labelConfirmConsult.setText("Consultar tablas")
        self.consultaButton = QPushButton()
        self.consultaLabel = QLabel()
        self.consultaLabel.setText("Realizar consulta")
        self.formLayoutConsult = QFormLayout(self.ConsultaPage1)
        self.formLayoutConsult.addRow(self.labelConsult,self.ComboBoxEditConsult)
        self.formLayoutConsult.addRow(self.listWidget)
        self.formLayoutConsult.addRow(self.consultaLabel,self.consultaButton)
        self.ConsultaPage1.registerField('Producto', self.lineEditElim,self.lineEditElim.text(),'textChanged')
        self.wizardConsultarInf.addPage(self.ConsultaPage1)

        #Configuración del Wizard de inserción de pedidos
        self.wizardInsertPedido = QWizard()
        self.wizardInsertPedido.setWizardStyle(QWizard.ModernStyle)
        self.insertPedidoPage1 = QWizardPage()
        self.insertPedidoPage1.setTitle('Inserción de un nuevo pedido')
        self.insertPedidoPage1.setSubTitle('Escoge los datos del pedido')
        self.labelPedido1 = QLabel()
        self.labelPedido1.setText('Id del pedido')
        self.lineEditPedido1 = QLineEdit()
        self.labelPedido2 = QLabel()
        self.labelPedido2.setText('Id del producto a pedir')
        self.lineEditPedido2 = QLineEdit()
        self.labelPedido3 = QLabel()
        self.labelPedido3.setText('Cantidad del producto a pedir')
        self.lineEditPedido3 = QLineEdit()
        self.labelPedido4 = QLabel()
        self.labelPedido4.setText('Dia en el que se realizo el producto')
        self.lineEditPedido4 = QLineEdit()
        self.formLayoutPedido1 = QFormLayout(self.insertPedidoPage1)
        self.formLayoutPedido1.addRow(self.labelPedido1,self.lineEditPedido1)
        self.formLayoutPedido1.addRow(self.labelPedido2,self.lineEditPedido2)
        self.formLayoutPedido1.addRow(self.labelPedido3,self.lineEditPedido3)
        self.formLayoutPedido1.addRow(self.labelPedido4,self.lineEditPedido4)
        self.wizardInsertPedido.addPage(self.insertPedidoPage1)
        self.insertPedidoPage1.setFinalPage(True)

        #Configuración del wizard de eliminación de productos
        self.wizardElimPedido = QWizard()
        self.wizardElimPedido.setWizardStyle(QWizard.ModernStyle)
        self.EliminarPedidoPage1 = QWizardPage()
        self.EliminarPedidoPage1.setTitle('Eliminación de un pedido')
        self.EliminarPedidoPage1.setSubTitle('Escoge el pedido a eliminar')
        self.labelElimPedido = QLabel()
        self.labelElimPedido.setText('ID del pedido a eliminar')
        self.lineEditElimPedido = QLineEdit()
        self.formLayoutElimPedido = QFormLayout(self.EliminarPedidoPage1)
        self.formLayoutElimPedido.addRow(self.labelElimPedido,self.lineEditElimPedido)
        self.wizardElimPedido.addPage(self.EliminarPedidoPage1)
        self.EliminarPedidoPage1.setFinalPage(True)

        #Configuración del wizard de eliminación de dias
        self.wizardElimDia = QWizard()
        self.wizardElimDia.setWizardStyle(QWizard.ModernStyle)
        self.EliminarDiaPage1 = QWizardPage()
        self.EliminarDiaPage1.setTitle('Eliminación de todos los productos de un dia')
        self.EliminarDiaPage1.setSubTitle('Escoge de que dia se eliminaran los productos')
        self.labelElimDia = QLabel()
        self.labelElimDia.setText('Especifica el dia')
        self.lineEditElimDia = QLineEdit()
        self.formLayoutElimDia = QFormLayout(self.EliminarDiaPage1)
        self.formLayoutElimDia.addRow(self.labelElimDia,self.lineEditElimDia)
        self.wizardElimDia.addPage(self.EliminarDiaPage1)
        self.EliminarDiaPage1.setFinalPage(True)

        self.finishDiaElim = self.wizardElimDia.button(QWizard.FinishButton)
        self.finishDiaElim.clicked.connect(self.eliminarDia)
        self.pushButton_10.clicked.connect(self.wizardEliminarDia)

        self.finishProdElim = self.wizardElimPedido.button(QWizard.FinishButton)
        self.finishProdElim.clicked.connect(self.eliminarPedido)
        self.pushButton_4.clicked.connect(self.wizardEliminarPedido)

        self.finishPedido = self.wizardInsertPedido.button(QWizard.FinishButton)
        self.finishPedido.clicked.connect(self.insertarPedido)
        self.pushButton_3.clicked.connect(self.wizardInsertarPedido)

        self.finish = self.wizardInsert.button(QWizard.FinishButton)
        self.finish.clicked.connect(self.insertarProd)
        self.pushButton.clicked.connect(self.wizardInsertar)

        self.finishElim = self.wizardElim.button(QWizard.FinishButton)
        self.finishElim.clicked.connect(self.eliminarProd)
        self.pushButton_2.clicked.connect(self.wizardEliminar)

        self.pushButton_5.clicked.connect(self.wizardConsultarInformacion)
        self.consultaButton.clicked.connect(self.consultarInfo)

        #Configuración del wizard de generación de PDF
        self.wizardGenerarPDF = QWizard()
        self.wizardGenerarPDF.setWizardStyle(QWizard.ModernStyle)
        self.GenerarPDFPage1 = QWizardPage()
        self.GenerarPDFPage1.setTitle('Eliminación de todos los productos de un dia')
        self.GenerarPDFPage1.setSubTitle('Escoge las opciones para generar el PDF')
        self.GenerarPDFPage2 = QWizardPage()
        self.GenerarPDFPage2.setTitle('Eliminación de todos los productos de un dia')
        self.GenerarPDFPage2.setSubTitle('Escoge las opciones para generar el PDF')
        self.GenerarPDFPage3 = QWizardPage()
        self.GenerarPDFPage3.setTitle('Eliminación de todos los productos de un dia')
        self.GenerarPDFPage3.setSubTitle('Escoge las opciones para generar el PDF')
        self.GenerarPDFPage4 = QWizardPage()
        self.GenerarPDFPage4.setTitle('Eliminación de todos los productos de un dia')
        self.GenerarPDFPage4.setSubTitle('Escoge las opciones para generar el PDF')
        self.nombreTrabajadorPDF = QLineEdit()
        self.labelNombreTrabajadorPDF = QLabel()
        self.labelNombreTrabajadorPDF.setText("Nombre del trabajador que crea el informe")
        self.diaPDF = QSpinBox()
        self.labelDiaPDF = QLabel()
        self.labelDiaPDF.setText("Dia en que se crea este informe")
        self.colorGraficaPDF = QComboBox()
        self.colorGraficaPDF.addItem("Rojo")
        self.colorGraficaPDF.addItem("Azul")
        self.colorGraficaPDF.addItem("Negro")
        self.labelColorGraficaPDF = QLabel()
        self.labelColorGraficaPDF.setText("Color de la grafica")
        self.tienePrecioPDF = QCheckBox()
        self.labelTienePrecioPDF = QLabel()
        self.labelTienePrecioPDF.setText("Generar con/sin precio")
        self.formLayoutGenerarPDF1 = QFormLayout(self.GenerarPDFPage1)
        self.formLayoutGenerarPDF1.addRow(self.labelNombreTrabajadorPDF,self.nombreTrabajadorPDF)
        self.formLayoutGenerarPDF2 = QFormLayout(self.GenerarPDFPage2)
        self.formLayoutGenerarPDF2.addRow(self.labelDiaPDF,self.diaPDF)
        self.formLayoutGenerarPDF3 = QFormLayout(self.GenerarPDFPage3)
        self.formLayoutGenerarPDF3.addRow(self.labelColorGraficaPDF,self.colorGraficaPDF)
        self.formLayoutGenerarPDF4 = QFormLayout(self.GenerarPDFPage4)
        self.formLayoutGenerarPDF4.addRow(self.labelTienePrecioPDF,self.tienePrecioPDF)
        self.wizardGenerarPDF.addPage(self.GenerarPDFPage1)
        self.wizardGenerarPDF.addPage(self.GenerarPDFPage2)
        self.wizardGenerarPDF.addPage(self.GenerarPDFPage3)
        self.wizardGenerarPDF.addPage(self.GenerarPDFPage4)

        self.GenerarPDFButton = self.wizardGenerarPDF.button(QWizard.FinishButton)
        self.GenerarPDFButton.clicked.connect(self.genPdf)
        self.pushButton_6.clicked.connect(self.wizardGenPDF)

        self.pushButton_7.clicked.connect(self.generarpdf)
        self.pushButton_7.setEnabled(False)

        self.outfile = ""

        self.pushButton_11.clicked.connect(lambda:webbrowser.open("https://github.com/MarioRamJim/GestorDePedidos/blob/main/Manual%20de%20uso%20.md", new=2, autoraise=True))
   
    def generarpdf(self):
        self.nombreTrabajadorPDF.setText("Juan")
        self.diaPDF.setValue(self.spinBox.value())
        self.genPdf()

    def wizardGenPDF(self):
        self.wizardGenerarPDF.show()

    def wizardInsertarPedido(self):
        self.wizardInsertPedido.show()

    def wizardEliminarDia(self):
        self.wizardElimDia.show()

    def wizardInsertar(self):
        self.wizardInsert.show()

    def wizardEliminar(self):
        self.wizardElim.show()

    def wizardEliminarPedido(self):
        self.wizardElimPedido.show()

    def wizardConsultarInformacion(self):
        self.wizardConsultarInf.show()
    
    def FailureDialog(self):

        dialog = QMessageBox()
        dialog.setText("Todos los campos deben tener valores validos para poder continuar")
        dialog.exec()

    def insertarProd(self):

        fallo = False
        if(self.lineEditInsert1.text() == "" or self.lineEditInsert2 == "" or self.lineEditInsert3 == ""):
            self.FailureDialog()
        for x in GestionarProductos.productos.find():

            if(int(self.lineEditInsert1.text())==x["id"]):
                fallo = True
                self.FailureDialog()

        else: 

            if fallo == False:
                id = int(self.lineEditInsert1.text())
                nombre = self.lineEditInsert2.text()
                precio = float(self.lineEditInsert3.text())

                self.prod["id"] = id
                self.prod["nombre"] = nombre
                self.prod["precio"] = precio

                GestionarProductos.añadirProducto(self.prod)
    
    def insertarPedido(self):

        fallo = False
        if(self.lineEditPedido1.text() == "" or self.lineEditPedido2 == "" or self.lineEditPedido3 == ""):

            self.FailureDialog()
        fallo = True
        for x in GestionarProductos.productos.find():
            try:

                if(x["id"]==int(self.lineEditPedido2.text())):
                    fallo = False

            except Exception: 
                self.FailureDialog()

        if fallo == True:
            self.FailureDialog()
        for x in GestionarPedidos.pedidos.find():

            if(int(self.lineEditPedido1.text())==x["id"]):
                fallo = True
                self.FailureDialog()

        else: 
            if fallo == False:
                try:

                    id = int(self.lineEditPedido1.text())
                    idProducto = int(self.lineEditPedido2.text())
                    cantidad = int(self.lineEditPedido3.text())
                    dia = int(self.lineEditPedido4.text())

                    self.pedido["id"] = id
                    self.pedido["idProducto"] = idProducto 
                    self.pedido["cantidad"] = cantidad
                    self.pedido["dia"] = dia

                    GestionarPedidos.añadirPedido(self.pedido)
                    
                except Exception:
                    self.FailureDialog()

    def eliminarPedido(self):

        if(self.lineEditElimPedido.text() == ""):
            self.FailureDialog()
        else:
            isElim = False
            try:
                id = int(self.lineEditElimPedido.text())
            except Exception:
                self.FailureDialog()
            for i in GestionarPedidos.pedidos.find():
                if i["id"] == id:
                    GestionarPedidos.EliminarPedido(i)
                    isElim = True
            if(isElim == False):
                self.FailureDialog

    def eliminarDia(self):

        if(self.lineEditElimDia.text() == ""):
            self.FailureDialog()
        else:
            isElim = False
            try:
                dia = int(self.lineEditElimDia.text())
            except Exception:
                self.FailureDialog()
            for i in GestionarPedidos.pedidos.find():
                if i["dia"] == dia:
                    isElim = True
                    GestionarPedidos.EliminarPedido(i)
            if(isElim == False):
                self.FailureDialog
    
    def eliminarProd(self):
        if(self.lineEditElim.text() == ""):
            self.FailureDialog()
        else:
            try:
                id = int(self.lineEditElim.text())
            except Exception:
                self.FailureDialog()
            for i in GestionarProductos.productos.find():
                if int(i["id"]) == id:
                    GestionarProductos.EliminarProducto(i)

    def consultarInfo(self):

        row = 0
        self.listWidget.clear()
        if(self.ComboBoxEditConsult.currentText() == "Productos"):

            nombreColumnas = ("id","nombre","precio")
            self.listWidget.setColumnCount(3)
            self.listWidget.setHorizontalHeaderLabels(nombreColumnas)

            for x in GestionarProductos.productos.find():

                self.listWidget.setRowCount(row+1)
                self.listWidget.setItem(row,0,QTableWidgetItem(str(x["id"])))
                self.listWidget.setItem(row,1,QTableWidgetItem(x["nombre"]))
                self.listWidget.setItem(row,2,QTableWidgetItem(str(x["precio"])))
                row+=1

        elif(self.ComboBoxEditConsult.currentText() == "Pedidos"):

            nombreColumnas2 = ("id","idProducto","cantidad","dia")
            self.listWidget.setColumnCount(4)
            self.listWidget.setHorizontalHeaderLabels(nombreColumnas2)

            for x in GestionarPedidos.pedidos.find():

                self.listWidget.setRowCount(row+1)
                self.listWidget.setItem(row,0,QTableWidgetItem(str(x["id"])))
                self.listWidget.setItem(row,1,QTableWidgetItem(str(x["idProducto"])))
                self.listWidget.setItem(row,2,QTableWidgetItem(str(x["cantidad"])))
                self.listWidget.setItem(row,3,QTableWidgetItem(str(x["dia"])))
                row+=1

    def genGrafica(self):
        exporter = pg.exporters.ImageExporter(self.graphWidget.plotItem)
        exporter.parameters()['width'] = 500
        exporter.export('fileName.png')

    def genPdf(self):

            if(self.tienePrecioPDF.isChecked):
                self.data = {
                'NombreTrabajador': self.nombreTrabajadorPDF.text(),
                'DiaGenerado': self.diaPDF.text(),
                'ColorGrafica': self.colorGraficaPDF.currentText(),
                'tienePrecio': False
                }
            else:
                self.data = {
                    'NombreTrabajador': self.nombreTrabajadorPDF.text(),
                    'DiaGenerado': self.diaPDF.text(),
                    'ColorGrafica': self.colorGraficaPDF.currentText(),
                    'tienePrecio': True
                    }
           
            self.outfile = "Formulario" + self.nombreTrabajadorPDF.text() + "Dia" + self.diaPDF.text()+".pdf"
            template = PdfReader("Trabajo5/InformeBase.pdf", decompress=False).pages[0]
            template_obj = pagexobj(template)

            canvas = Canvas(self.outfile)

            xobj_name = makerl(canvas, template_obj)
            canvas.doForm(xobj_name)



            contPedidos = 0
            contProductos = 0
            celdasY = 543
            celdasX = 138
            
            pedidos = {}

            for x in GestionarPedidos.pedidos.find():
                if(x["dia"]==int(self.data["DiaGenerado"])):
                    if(contPedidos!=10):
                        canvas.drawString(celdasX,celdasY,str(x["id"]))
                        canvas.drawString(celdasX+150,celdasY,str(x["idProducto"]))
                        canvas.drawString(celdasX+300,celdasY,str(x["cantidad"]))
                        celdasY = celdasY - 23
                        contPedidos += 1
                        contProductos += x["cantidad"]

                        try:
                            pedidos[x["idProducto"]] += x["cantidad"]
                        except Exception:
                            pedidos[x["idProducto"]] = x["cantidad"]
            
            precioTotal = 0

            if(self.tienePrecioPDF.isChecked()):
                for y in pedidos.keys():
                    key = y
                    for x in GestionarProductos.productos.find():
                        if(x["id"]) == key:
                            precioTotal += (x["precio"]*pedidos[x["id"]])
                    
            canvas.drawString(288,313,"Pedidos con los que se creo el informe: " + str(contPedidos))
            canvas.drawString(288,292,"Total de productos pedidos: " + str(contProductos))
            canvas.drawString(288,271,"Precio Total del pedido: " + str(precioTotal))
            if(self.colorGraficaPDF.currentText()=="Rojo"):
                color=(255, 0, 0)

            elif(self.colorGraficaPDF.currentText()=="Azul"):
                color=(0,0,255)

            else:
                color=(0,0,0)

            ystart = 745

            canvas.drawString(300, ystart, self.data['NombreTrabajador'])
            canvas.drawString(270, ystart-135, self.data['DiaGenerado'])

          
            claves = []
            for x in pedidos.keys():
                claves.append(x)
            valores = []
            for x in pedidos.values():
                valores.append(x)

            self.graphWidget = pg.plot()
            self.graphWidget.setBackground('w')
            bargraph = pg.BarGraphItem(x = claves, height = valores, width = 0.6, brush = color)
            self.graphWidget.addItem(bargraph)

            self.genGrafica()
            
            self.graphWidget.hide()

            canvas.drawImage('fileName.png',100,50,400,200)

            canvas.save()
            
            QMessageBox.information(self, "Finalizado", "Se ha generado el PDF")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
