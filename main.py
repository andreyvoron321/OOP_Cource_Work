from PyQt5 import QtWidgets, QtCore, QtGui
import inter
import workcode
import sys

#F:\\test

class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)
    def write(self, text):
        self.textWritten.emit(str(text))

class ExampleApp(QtWidgets.QDialog, inter.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Инициализация
        self.pushButton.clicked.connect(self.output)
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)

    def __del__(self):
        # Restore sys.stdout
        sys.stdout = sys.__stdout__

    def normalOutputWritten(self, text):#   Перехват командной строки
        cursor = self.textEdit_2.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textEdit_2.setTextCursor(cursor)
        self.textEdit_2.ensureCursorVisible()

    def output(self):
        global data
        self.textEdit_2.setText('')#    Обновление окна
        data = self.textEdit.toPlainText()
        self.textEdit_2.insertPlainText(data)
        self.textEdit_2.insertPlainText('\n')
        workcode.main1(data)

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':
    main()