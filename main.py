from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtGui import * 
import sys, os, re

operators = {
  '=':'Asignación',
  '+':'Adición',
  '-':'Sustracción',
  '/':'División',
  '*':'Producto'
}

variable_name_regex = r'(^[a-zA-z_][_a-zA-Z0-9]*)'
real_number_regex = r'([0-9]*\.[0-9]+)'
whole_number_regex = r'([0-9]+)'
real_exponent_regex = r'(([0-9]+)(e|E)(\+|-)+([0-9])+)'

tokens = {
  'id_variable': 'Identificador de Variable',
  'num_entero': 'Numero Entero',
  'num_real': 'Numero Real',
  'exp_entero' : 'Exponente Entero',
  'exp_real' : 'Exponente Real'
}

class MainWindow(QtWidgets.QMainWindow):
  def __init__(self):
    QtWidgets.QMainWindow.__init__(self)
    ui_path = os.path.dirname(os.path.abspath(__file__))
    self.ui = uic.loadUi(os.path.join(ui_path, 'UI.ui'), self)
    
    self.analizar_btn.clicked.connect(self.start_analyzer)
    
  def start_analyzer(self):
    source_list = self.codigo_fuente.toPlainText().split('\n')
    
    for line in source_list:
      if re.search(variable_name_regex, line):
        print(line, 'valido')
      else:
        print(line, 'no valido')
    pass

#Función main
if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  mainWindow = MainWindow()
  mainWindow.show()
  sys.exit(app.exec_())