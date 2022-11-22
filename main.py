from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import * 
import sys, os, re

operators = {
  '=':'Asignación',
  '+':'Adición',
  '-':'Sustracción',
  '/':'División',
  '*':'Producto'
}

digit_regex = r'([0-9])'
alpha_regex = r'([a-z_])'
operator_regex = r'(\+|-|\*|/|=)'
# real_number_regex = r'(^[0-9]*\.[0-9]+[^a-z])'
# whole_number_regex = r'(^[0-9]+[^a-z])'
# whole_exponent_regex = r'(([0-9]+)(e|E)(\+|-)+([0-9])+)'

states = {
  0: 'q0',
  1: 'q1',
  2: 'q2',
  3: 'q3',
  4: 'q4',
  5: 'q5',
  6: 'q6',
  7: 'q7',
  8: 'q8',
  9: 'q9'
}

transition_table = [
    [6, 1, 2, -1, -1, -1],
    [-1, 1, 4, 3, 7, -2],
    [-1, 1, -1, -1, -1, -1],
    [-1, 5, -1, -1, -1, -1],
    [-1, 1, -1, -1, -1, -1],
    [-1, 5, 4, -1, 7, -2],
    [6, 6, 1, -1, -1, -2],
    [-1, -1, 8, -1, -1, -1],
    [-1, 9, -1, -1, -1, -1],
    [-1, 9, -1, -1, -1, -2],
  ]

token = ''
state = 0
class MainWindow(QtWidgets.QMainWindow):
  def __init__(self):
    QtWidgets.QMainWindow.__init__(self)
    
    ui_path = os.path.dirname(os.path.abspath(__file__))
    self.ui = uic.loadUi(os.path.join(ui_path, 'UI.ui'), self)
    
    self.analizar_btn.clicked.connect(self.start_analyzer)
    
  def determine_variable_id_state(self, char):
    global token
    
    if re.match(alpha_regex, char):
      token = 'Letra'
      return 0
    else:
      if re.match(digit_regex, char):
        token = 'Digito'
        return 1
      else:
        if re.match(operator_regex, char):
          token = 'Operador'
          return 2
        else:
          if re.match(r'\.', char):
            token = 'Punto'
            return 3
          else:
            if re.match(r'(E|e)', char):
              token = 'Exponetne'
              return 4
            else: 
              if(char == ''):
                return 5
    
    print(char, 'no es un caracter válido')

    
  def start_analyzer(self):
    global transition_table, token, state
    
    data = []
    self.tabla_analisis.setRowCount(0)
    source_list = self.codigo_fuente.toPlainText().split('\n')
    
    for line in source_list:  
      state = 0
      token = ''
      print(line)
      for char in line:
        current = state
        
        character = self.determine_variable_id_state(char)
        
        state = transition_table[state][character]

        if state == -1: 
          print(char, 'No es un caracter válido')
          data.append((char, token, "-", "-", "No Válido"))
          self.print_table(data)
          break
        
        data.append((char, token, states[current], states[state], "Válido"))
      
        print('Estado actual:', states[current], 'Siguiente:', states[state], '| Caracter:', char, '| Token:', token)
      if state == -1: break  
       
      data.append(('','','',''))
      
    if state == -1:
      print("Cadena No Válida")
    else:
      self.print_table(data)
      
    if state == 9:
      print("Cadena Válida")
      
 
  def print_table(self, data):
    
    row = 0
    
    for field in data:
      col = 0
      self.tabla_analisis.insertRow(row)
      for element in field:
        cell = QtWidgets.QTableWidgetItem(element)
        self.tabla_analisis.setItem(row, col, cell)
        col +=1
      row += 1

#Función main
if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  mainWindow = MainWindow()
  mainWindow.show()
  sys.exit(app.exec_())