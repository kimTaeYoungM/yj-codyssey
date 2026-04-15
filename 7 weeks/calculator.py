import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.expression = ''
        self.init_ui()

    def init_ui(self):
        # 메인 레이아웃 설정
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 디스플레이 창 설정 (아이폰 계산기 스타일의 출력 형태)
        self.display = QLineEdit('0')
        self.display.setFixedHeight(80)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFont(QFont('Arial', 30))
        self.display.setStyleSheet('border: none; background-color: transparent; color: black;')
        main_layout.addWidget(self.display)

        # 버튼 배치 구성을 위한 그리드 레이아웃
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        # 버튼 텍스트와 위치 정의 (아이폰 계산기 배치 기준)
        buttons = [
            ('AC', 0, 0), ('+/-', 0, 1), ('%', 0, 2), ('/', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('*', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('0', 4, 0, 1, 2), ('.', 4, 2), ('=', 4, 3)
        ]

        for btn_info in buttons:
            text = btn_info[0]
            row = btn_info[1]
            col = btn_info[2]
            
            button = QPushButton(text)
            button.setFixedSize(70, 70)
            button.setFont(QFont('Arial', 18))
            
            # '0' 버튼은 2칸을 차지하도록 설정
            if text == '0':
                button.setFixedSize(150, 70)
                grid_layout.addWidget(button, row, col, 1, 2)
            else:
                grid_layout.addWidget(button, row, col)
            
            # 버튼 클릭 이벤트 연결
            button.clicked.connect(self.on_button_clicked)

        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)
        
        self.setWindowTitle('Calculator')
        self.setFixedSize(340, 500)
        self.show()

    def on_button_clicked(self):
        button = self.sender()
        key = button.text()

        if key == 'AC':
            self.expression = ''
            self.display.setText('0')
        elif key == '=':
            try:
                # 보너스 과제: 사칙연산 기능 구현
                # eval 함수 사용 시 안전을 위해 문자열 정제 후 계산
                result = str(eval(self.expression.replace('x', '*')))
                self.display.setText(result)
                self.expression = result
            except Exception:
                self.display.setText('Error')
                self.expression = ''
        elif key == '+/-':
            if self.expression:
                if self.expression.startswith('-'):
                    self.expression = self.expression[1:]
                else:
                    self.expression = '-' + self.expression
                self.display.setText(self.expression)
        elif key == '%':
            if self.expression:
                try:
                    result = str(float(self.expression) / 100)
                    self.display.setText(result)
                    self.expression = result
                except ValueError:
                    pass
        else:
            # 숫자 및 연산자 입력 처리
            if self.expression == '0' and key.isdigit():
                self.expression = key
            else:
                self.expression += key
            self.display.setText(self.expression)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Calculator()
    sys.exit(app.exec_())