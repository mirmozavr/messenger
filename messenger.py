from PyQt5 import QtWidgets, QtCore
import simpui
import requests
from datetime import datetime as dt


class ExampleApp(QtWidgets.QMainWindow, simpui.Ui_MainWindow):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.setupUi(self)

        self.pushButton.pressed.connect(self.send_message)

        self.after = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_messages)
        self.timer.start(1000) #1000

    def get_messages(self):
        try:
            print(self.url,'selfurl')
            response = requests.get(self.url+'get_messages', params={'after': self.after})
            print(response.status_code)
            print(response.text)
        except:
            self.textBrowser.append('System: connection problem')
            return

        if response.status_code == 200:
            messages = response.json()['messages']

            for message in messages:
                self.after = message['time']
                ftime = dt.fromtimestamp(message['time']).strftime('%Y.%m.%d %H:%M:%S')
                self.textBrowser.append(message['author'] + ' ' + ftime)
                self.textBrowser.append(message['text'])
                self.textBrowser.append('')

    def send_message(self):
        print('button  press')
        name = self.lineEdit.text()
        text = self.plainTextEdit.toPlainText()
        try:
            response = requests.post(self.url+'send_message',
                                     json={'author': name,
                                           'text': text})
        except:
            self.textBrowser.append('Server not available')
            self.textBrowser.append('')
            self.textBrowser.repaint()
            return
        if response.status_code != 200:
            self.textBrowser.append('Validation error')
            self.textBrowser.append('')
            self.textBrowser.repaint()
            return

        self.plainTextEdit.clear()
        self.plainTextEdit.repaint()


app = QtWidgets.QApplication([])
# insert URL given by ngrok.exe
window = ExampleApp('http://127.0.0.1:5000/')
window.show()
app.exec_()
