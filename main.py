from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import * 
import sys, os, re

operators = {
  '+':'Op. Adición',
  '-':'Op. Sustracción',
  '/':'Op. División',
  '*':'Op. Producto'
}

digit_regex = r'(\d)'
alpha_regex = r'([a-z_])'
operator_regex = r'(\+|-|\*|/)'

variable_regex = r'^(_*[a-z]+[\d_]*(?! [+-]))$'
arithmetic_exp_regex = r'^[\+\-\/\*]?\d+(?=[\+\-\/\*])(\.\d+)?([\+\-\*\/]\d*(\.\d+)?)*$'
real_number_regex = r'(^[+-]?\d*\.\d+$)'
whole_number_regex = r'(^[+-]?\d+$)'
whole_exponent_regex = r'((?<!\.)\d+E(\+|-)\d+)'
real_exponent_regex = r'(\d*\.\d*E(\+|-)\d+)'

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
  9: 'q9',
  10: 'q10'
}

transition_table = [
    [6, 1, 2, -1, -1, -1],
    [6, 1, 4, 3, 7, -2],
    [-1, 1, -1, -1, -1, -1],
    [-1, 5, -1, -1, -1, -1],
    [-1, 1, -1, -1, -1, -1],
    [-1, 5, 4, -1, 7, -2],
    [6, 10, -1, -1, -1, -2],
    [-1, -1, 8, -1, -1, -1],
    [-1, 9, -1, -1, -1, -1],
    [-1, 9, 4, -1, -1, -2],
    [-1, 1, -1, -1, -1, -2]
  ]

token = ''
state = 0
class MainWindow(QtWidgets.QMainWindow):
  def __init__(self):
    QtWidgets.QMainWindow.__init__(self)
    
    ui_path = os.path.abspath("UI.ui")
    self.ui = uic.loadUi(ui_path, self)
    
    self.analizar_btn.clicked.connect(self.start_analyzer)
    
    header = self.tabla_tokens.horizontalHeader()       
    header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
    header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
    
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
              token = 'Exponente'
              return 4
            else: 
              if(char == ''):
                return 5
    
    print(char, 'no es un caracter válido')

  def determine_general_token(self, string):

    if re.match(arithmetic_exp_regex, string):
      return 'Expr. Aritmética'
    else:
      if re.match(real_exponent_regex, string):
        return 'Exp. Real'
      else:
        if re.match(whole_exponent_regex, string):
          return 'Exp. Entero'
        else:
          if re.match(variable_regex, string):
            return 'Id. Variable'
          else:
            if re.match(real_number_regex, string):
              return 'Num. Real'
            else:
              if re.match(whole_number_regex, string):
                return 'Num. Entero'
              else:
                if string == '':
                  return
            
    return 'no válida'  
    
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
        
        if character == 2:
          token = operators[char]
          
        if (state != -1) & (current != -1): data.append((char, token, states[current], states[state], "Válido"))
      
      data.append(('','','','',''))
      
    if state == -1:
      print("Cadena No Válida")

    self.print_analysis_table(data)
      
    if state == 9:
      print("Cadena Válida")
      
    self.start_tokenizer()
    
  def start_tokenizer(self): 
    data = []
    
    self.tabla_tokens.setRowCount(0)
    source_list = self.codigo_fuente.toPlainText().split('\n')
    
    for line in source_list:
    
        
      # if re.search('=',line):
        
      #   arith_exp = re.split('=', line)[1]
        
      #   new_line = re.sub(real_exponent_regex, '' , arith_exp)
      #   clean_line = re.sub(whole_exponent_regex, '' , new_line)
        
      #   full_line = re.split('=', line)[0]+'='+clean_line
      #   general_strings = re.split('=|\+|-|\*|/', full_line)
        
      #   for expr in general_strings:
      #     if expr != '':
      #       token = self.determine_general_token(expr)
      #       if expr != '': data.append((expr, token))           
      
      #   if re.search(real_exponent_regex, line):
      #     real_exponents = re.findall(real_exponent_regex, line)
      #     for exp in real_exponents:
      #       token = self.determine_general_token(exp[0])
      #       data.append((exp[0], token))

      #   if re.search(whole_exponent_regex, line):
      #     exponents = re.findall(whole_exponent_regex, line)
      #     for exp in exponents:
      #       token = self.determine_general_token(exp[0])
      #       data.append((exp[0], token))
            
      #   data.append((arith_exp, self.determine_general_token(arith_exp)))
      #   data.append(('','','','',''))
      # else:
      new_line = re.sub(real_exponent_regex, '' , line)
      clean_line = re.sub(whole_exponent_regex, '' , new_line)
      if re.search(arithmetic_exp_regex, clean_line):
        general_strings = re.split('\+|-|\*|/', clean_line)
        token = self.determine_general_token(clean_line)
        data.append((line, token))
        for expr in general_strings:
          if expr != '':
            token = self.determine_general_token(expr)
            if expr != '': data.append((expr, token))
      
      if re.search(real_exponent_regex, line):
        real_exponents = re.findall(real_exponent_regex, line)
        for exp in real_exponents:
          token = self.determine_general_token(exp[0])
          data.append((exp[0], token))
      
      if re.search(whole_exponent_regex, line):
        exponents = re.findall(whole_exponent_regex, line)
        for exp in exponents:
          token = self.determine_general_token(exp[0])
          data.append((exp[0], token))
      
      if re.search(whole_number_regex, line):
        token = self.determine_general_token(line)
        data.append((line, token))
      
      if re.search(real_number_regex, line):
        token = self.determine_general_token(line)
        data.append((line, token))
      
      if re.match(variable_regex, line):
        token = self.determine_general_token(line)
        data.append((line, token))
        
      data.append(('','','','',''))
  
    self.print_token_table(data)
    
  def print_token_table(self, data):
    
    row = 0
    
    for field in data:
      col = 0
      self.tabla_tokens.insertRow(row)
      for element in field:
        cell = QtWidgets.QTableWidgetItem(element)
        self.tabla_tokens.setItem(row, col, cell)
        col +=1
      row += 1
    
  def print_analysis_table(self, data):
    
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