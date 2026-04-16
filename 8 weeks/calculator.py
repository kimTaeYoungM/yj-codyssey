import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class Calculator:
    '''계산기의 핵심 연산 로직을 담당하는 클래스입니다.'''
    
    def __init__(self):
        self.reset()

    def reset(self):
        '''모든 데이터를 초기화합니다.'''
        self.current_value = '0'
        self.first_operand = None
        self.operator = None
        self.waiting_for_second_operand = False

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            return 'Error'
        return a / b

    def negative_positive(self):
        '''현재 숫자의 부호를 반전시킵니다.'''
        if self.current_value != '0':
            if self.current_value.startswith('-'):
                self.current_value = self.current_value[1:]
            else:
                self.current_value = '-' + self.current_value

    def percent(self):
        '''현재 숫자를 100으로 나눕니다.'''
        try:
            val = float(self.current_value) / 100
            self.current_value = self.format_number(val)
        except ValueError:
            self.current_value = 'Error'

    def format_number(self, value):
        '''보너스 과제: 소수점 6자리 반올림 및 문자열 변환을 처리합니다.'''
        if isinstance(value, str):
            return value
        
        # 소수점 6자리까지 반올림
        rounded_val = round(value, 6)
        
        # 정수형으로 표현 가능하면 정수로 변환 (예: 5.0 -> 5)
        if rounded_val == int(rounded_val):
            return str(int(rounded_val))
        return str(rounded_val)

    def calculate(self):
        '''연산자에 따라 최종 결과를 계산합니다.'''
        if self.operator and self.first_operand is not None:
            second_operand = float(self.current_value)
            
            if self.operator == '+':
                result = self.add(self.first_operand, second_operand)
            elif self.operator == '-':
                result = self.subtract(self.first_operand, second_operand)
            elif self.operator == '×':
                result = self.multiply(self.first_operand, second_operand)
            elif self.operator == '÷':
                result = self.divide(self.first_operand, second_operand)
            
            self.current_value = self.format_number(result)
            self.first_operand = None
            self.operator = None
            self.waiting_for_second_operand = False


class CalculatorApp(QWidget):
    '''PyQt5를 이용한 계산기 UI 및 컨트롤러 클래스입니다.'''
    
    def __init__(self):
        super().__init__()
        self.core = Calculator()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Calculator')
        self.setFixedSize(350, 500)
        self.setStyleSheet('background-color: black;')

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        # 디스플레이 설정
        self.label = QLabel('0')
        self.label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label.setStyleSheet('color: white; padding: 10px;')
        self.update_font_size()
        self.main_layout.addWidget(self.label)

        # 버튼 레이아웃
        self.grid_layout = QGridLayout()
        buttons = [
            ('AC', 0, 0, 'gray'), ('+/-', 0, 1, 'gray'), ('%', 0, 2, 'gray'), ('÷', 0, 3, 'orange'),
            ('7', 1, 0, 'dark_gray'), ('8', 1, 1, 'dark_gray'), ('9', 1, 2, 'dark_gray'), ('×', 1, 3, 'orange'),
            ('4', 2, 0, 'dark_gray'), ('5', 2, 1, 'dark_gray'), ('6', 2, 2, 'dark_gray'), ('-', 2, 3, 'orange'),
            ('1', 3, 0, 'dark_gray'), ('2', 3, 1, 'dark_gray'), ('3', 3, 2, 'dark_gray'), ('+', 3, 3, 'orange'),
            ('0', 4, 0, 'dark_gray', 2), ('.', 4, 2, 'dark_gray'), ('=', 4, 3, 'orange')
        ]

        for btn_text, r, c, color, *span in buttons:
            button = QPushButton(btn_text)
            button.setFixedSize(70 if not span else 155, 70)
            button.clicked.connect(self.on_button_click)
            
            # 스타일 시트 적용 (이미지 UI와 유사하게 설정)
            style = self.get_button_style(color)
            button.setStyleSheet(style)
            
            if span:
                self.grid_layout.addWidget(button, r, c, 1, span[0])
            else:
                self.grid_layout.addWidget(button, r, c)

        self.main_layout.addLayout(self.grid_layout)
        self.setLayout(self.main_layout)

    def get_button_style(self, color):
        base_style = 'border-radius: 35px; font-size: 22px; font-weight: bold;'
        if color == 'gray':
            return base_style + 'background-color: #A5A5A5; color: black;'
        elif color == 'orange':
            return base_style + 'background-color: #FF9F0A; color: white;'
        else: # dark_gray
            return base_style + 'background-color: #333333; color: white;'

    def update_font_size(self):
        '''보너스 과제: 글자 길이에 따라 폰트 크기를 조절합니다.'''
        text_len = len(self.label.text())
        if text_len <= 6:
            font_size = 50
        elif text_len <= 10:
            font_size = 35
        else:
            font_size = 25
        self.label.setFont(QFont('Arial', font_size))

    def on_button_click(self):
        sender = self.sender().text()

        if sender.isdigit():
            if self.core.waiting_for_second_operand:
                self.core.current_value = sender
                self.core.waiting_for_second_operand = False
            else:
                if self.core.current_value == '0':
                    self.core.current_value = sender
                else:
                    self.core.current_value += sender
        
        elif sender == '.':
            # 소수점이 이미 존재하지 않을 때만 추가
            if '.' not in self.core.current_value:
                self.core.current_value += '.'
        
        elif sender == 'AC':
            self.core.reset()
        
        elif sender == '+/-':
            self.core.negative_positive()
        
        elif sender == '%':
            self.core.percent()
        
        elif sender in ['+', '-', '×', '÷']:
            self.core.first_operand = float(self.core.current_value)
            self.core.operator = sender
            self.core.waiting_for_second_operand = True
        
        elif sender == '=':
            self.core.calculate()

        # UI 업데이트
        self.label.setText(self.core.current_value)
        self.update_font_size()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CalculatorApp()
    ex.show()
    sys.exit(app.exec_())