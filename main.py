from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog, QWidget, QPushButton, QMessageBox         # не знаю почему, но иначе импорт диалогового окна не происходил,
from PyQt5.QtWidgets import QListWidget                     # хотя эти модули был подключены выше
import inter3
import sys
import os
import hashlib


class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)
    def write(self, text):
        self.textWritten.emit(str(text))


class ExampleApp(QtWidgets.QDialog, inter3.Ui_Dialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Инициализация
        #self.state = None
        self.SearchButton.clicked.connect(self.inp_dir)
        self.DeleteButton.clicked.connect(self.inp_dir2)
        self.ExitButton.clicked.connect(self.exit_f)
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)


    def normalOutputWritten(self, text):#   Перехват командной строки
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textEdit.setTextCursor(cursor)
        self.textEdit.ensureCursorVisible()

    def inp_dir(self):
        self.textEdit.setText('')
        data = QFileDialog.getExistingDirectory(self, "Select directory", ".")
        self.main1(data)

    def inp_dir2(self):
        self.textEdit.setText('')
        data = QFileDialog.getExistingDirectory(self, "Select directory", ".")
        self.main2(data)


# --------------------------------- from workcode.py ---------------------------------------------------------
    @classmethod
    def hashfile(self, path, blocksize = 65536):
        afile = open(path, 'rb')
        hasher = hashlib.md5()
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)
        afile.close()
        return hasher.hexdigest()

    @classmethod
    def findDup(self, parentFolder):
        dups = {}
        for dirName, subdirs, fileList in os.walk(parentFolder):
            for filename in fileList:
                path = os.path.join(dirName, filename)  # Полный путь к файлу
                file_hash = self.hashfile(path) # Вычисление хэша
                if file_hash in dups:
                    dups[file_hash].append(path) # добавление дубликата
                else:
                    dups[file_hash] = [path]    # добавление нового типа дубликата
        return dups

    @classmethod
    def findDup_del(self, parentFolder):
        dups = {}
        for dirName, subdirs, fileList in os.walk(parentFolder):
            for filename in fileList:
                path = os.path.join(dirName, filename)  # Полный путь к файлу
                file_hash = self.hashfile(path)  # Вычисление хэша
                if file_hash in dups:
                    dups[file_hash].append(path)  # добавление дубликата
                    os.remove(path)
                else:
                    dups[file_hash] = [path]  # добавление нового типа дубликата
        return dups

    @classmethod
    def joinDicts(self, dict1, dict2):
        for key in dict2.keys():
            if key in dict1:
                dict1[key] = dict1[key] + dict2[key]
            else:
                dict1[key] = dict2[key]

    @classmethod
    def main1(self, data1):
        dups = {}
        self.joinDicts(dups, self.findDup(data1))
        self.printResults(dups)

    @classmethod
    def main2(self, data1):
        dups = {}
        self.joinDicts(dups, self.findDup_del(data1))
        self.printResults(dups)

    @classmethod
    def printResults(self, dict1):
        results = list(filter(lambda x: len(x) > 1, dict1.values()))
        if len(results) > 0:
            print('Duplicates Found:')
            print('The following files are identical. The name could differ, but the content is identical')
            print('___________________')
            for result in results:
                for subresult in result:
                    print(subresult)
                print('___________________')
        else:
            print('No duplicate files found.')

    @classmethod
    def exit_f(cls):
        sys.exit()

# ------------------------------------------------------------------------------------------------------------


def main():
    #global status #                                                                 <--- обьявление переменной
    #status = False
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':
    main()
