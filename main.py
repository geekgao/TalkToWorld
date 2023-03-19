import sys
import subprocess
import threading
import requests
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QCursor, QPixmap
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer


# Google Input Tools API
API_URL = 'https://inputtools.google.com/request?text={text}&itc={itc}&num={num}'
solagn = "Giving voice to the deaf community(为聋哑人社群发声)"


def input_method_conversion(query, num=10):
    url = API_URL.format(text=query, itc='zh-t-i0-pinyin', num=num)
    try:
        response = requests.post(url)
        if response.status_code == 200:
            print(response.json()[1][0][1])
            data = response.json()[1][0][1]
            return data
        else:
            return None
    except Exception as e:
        print(e)
        return None


def get_platform():
    platforms = {
        'linux1': 'Linux',
        'linux2': 'Linux',
        'darwin': 'OS X',
        'win32': 'Windows'
    }
    if sys.platform not in platforms:
        return sys.platform

    return platforms[sys.platform]


def speak(text):
    platform = get_platform()
    if platform == 'Windows':
        subprocess.call(
            ['powershell', 'Add-Type –AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("{0}")'.format(text)])
    elif platform == 'Linux':
        subprocess.call(['espeak', text])
    elif platform == 'OS X':
        subprocess.call(['say', text])


class Keyboard(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "TalkToWorld中文语音键盘 Giving voice to the deaf community")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 创建显示区域
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background-color: white;")
        self.label.setFont(QFont("Arial", 32))
        self.label.setStyleSheet(
            "background-color:rgb(227, 227, 227); border-radius:10px; padding: 10px;")
        self.layout.addWidget(self.label)

        self.label.setText(solagn)

        def blink():
            self.label.setStyleSheet(
                "color:green")
            QTimer.singleShot(100, lambda: self.label.setStyleSheet(
                "color:blue"))

        timer = QTimer()
        timer.timeout.connect(blink)
        timer.start(100)

        QTimer.singleShot(4000, lambda: (timer.stop(), self.label.setText("")))

        self.row_layout = QHBoxLayout()
        self.layout.addLayout(self.row_layout)

        pixmap = QPixmap("cursor.png").scaled(64, 64)
        cursor = QCursor(pixmap, hotX=-1, hotY=-1)
        self.setCursor(cursor)
# 创建键盘按钮
        keys = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
            ['z', 'x', 'c', 'v', 'b', 'n', 'm']
        ]

        for row in keys:
            row_layout = QHBoxLayout()
            for key in row:
                button = QPushButton(key)
                button.setMaximumWidth(128)
                button.setMaximumHeight(128)
                button.setFont(QFont("Arial", 64))
                button.setStyleSheet(
                    "QPushButton{background-color:rgb(255,255,255);border-radius:10px;}"
                    "QPushButton:hover{background-color:rgb(240,240,240);}"
                )
                button.clicked.connect(self.button_clicked)
                row_layout.addWidget(button)
            self.layout.addLayout(row_layout)

        # 添加特殊功能键
        special_keys_layout = QHBoxLayout()
        clear_button = QPushButton("🧹")
        clear_button.setMaximumWidth(200)
        clear_button.setMaximumHeight(200)
        clear_button.setFont(QFont("Arial", 64))
        clear_button.setStyleSheet(
            "QPushButton{background-color:rgb(227, 227, 227);border-radius:10px;}"
            "QPushButton:hover{background-color:rgb(240,240,240);}"
        )
        clear_button.clicked.connect(self.clear_clicked)
        special_keys_layout.addWidget(clear_button)

        backspace_button = QPushButton("DEL")
        backspace_button.setMaximumWidth(200)
        backspace_button.setMaximumHeight(200)
        backspace_button.setFont(QFont("Arial", 48))
        backspace_button.setStyleSheet(
            "QPushButton{background-color:rgb(227, 227, 227);border-radius:10px;}"
            "QPushButton:hover{background-color:rgb(240,240,240);}"
        )
        backspace_button.clicked.connect(self.backspace_clicked)
        special_keys_layout.addWidget(backspace_button)

        speak_button = QPushButton("🗣️")
        speak_button.setMaximumWidth(200)
        speak_button.setMaximumHeight(200)
        speak_button.setFont(QFont("Arial", 64))
        speak_button.setStyleSheet(
            "QPushButton{background-color:rgb(227, 227, 227);border-radius:10px;}"
            "QPushButton:hover{background-color:rgb(240,240,240);}"
        )
        speak_button.clicked.connect(self.speak_clicked)
        special_keys_layout.addWidget(speak_button)

        self.layout.addLayout(special_keys_layout)
        self.continue_typing_cache = ''

    def speak_clicked(self):
        text = self.label.text()
        speak(text)

    def button_clicked(self):
        button = self.sender()
        text = button.text()
        self.continue_typing_cache = self.continue_typing_cache + text
        if text.isdigit():
            self.label.setText(self.label.text() + ' ' + text)
            speak(text)
            return
        if self.continue_typing_cache:
            print(self.continue_typing_cache)
            self.remove_buttons()
            hanzi = input_method_conversion(self.continue_typing_cache)
        else:
            hanzi = input_method_conversion(text)

        if self.continue_typing_cache:
            max_width = 200
            font_size = 24
        else:
            max_width = 128
            font_size = 64
        for key in hanzi:
            self.candidate_button = QPushButton(key)
            self.candidate_button.setMaximumWidth(max_width)
            self.candidate_button.setMaximumHeight(100)
            self.candidate_button.setFont(QFont("Arial", font_size))
            self.candidate_button.setStyleSheet(
                "QPushButton{background-color:rgb(255,255,200);border-radius:10px;font-weight:bold;}"
                "QPushButton:hover{background-color:rgb(240,240,240);}"
            )
            self.candidate_button.clicked.connect(
                self.button_candidate_clicked)
            self.row_layout.addWidget(self.candidate_button)
        self.layout.addLayout(self.row_layout)

    def clear_clicked(self):
        self.label.clear()

    def backspace_clicked(self):
        text = self.label.text()
        self.label.setText(text[:-1])
        self.remove_buttons()
        self.continue_typing_cache = ''

    def button_candidate_clicked(self):
        self.continue_typing_cache = ''
        button = self.sender()
        self.label.setText(self.label.text() + button.text())
        speak(button.text())
        self.remove_buttons()

    def remove_buttons(self):
        for i in reversed(range(self.row_layout.count())):
            item = self.row_layout.itemAt(i)
            if isinstance(item.widget(), QPushButton):
                btn = item.widget()
                self.row_layout.removeWidget(btn)
                btn.setVisible(False)
                btn.deleteLater()


if __name__ == "__main__":
    app = QApplication([])
    keyboard = Keyboard()
    keyboard.showFullScreen()
    # Create a thread
    solagn = threading.Thread(target=speak, args=(solagn,))
    # Start the thread
    solagn.start()
    app.exec_()
