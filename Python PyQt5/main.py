import sys  # sys нужен для передачи argv в QApplication

from datetime import datetime
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import  QFileDialog ,  QStyle, QDialog, QMessageBox , QTableWidget,  QTableWidgetItem, QPushButton
import design  # Это наш конвертированный файл дизайна

GPSData = ""

class ExampleApp(QtWidgets.QMainWindow, design.Ui_Dialog):
    
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.toolButton.clicked.connect(self.BrowseFile)
        self.pushButton.clicked.connect(self.ConvertFile)
        self.exitButton.clicked.connect(self.close)

    def BrowseFile(self):
        global GPSData
        GPSData = QFileDialog.getOpenFileName(self,"Выберите GPSData000001.txt", "","GPSData000001 (*.txt)")[0]
        self.label.setText(GPSData)
        self.pushButton.setEnabled(True)
        self.textBrowser.clear()

    def ConvertFile(self):
        self.textBrowser.clear()
        self.textBrowser.setText("Начинаю конвертацию...")
        time_correct = 60*60*(8);                                                   # Поправка на часовой пояс, в секундах
        time_correct_name_file = 60*60*(8+int(self.Time_line.currentText()));       # Поправка на часовой пояс в названии файла, в секундах
        folder_done = "done/";                                                      # Папка для готовых gpx файлов, "./" - текущая дериктория
        
        #Значения по умолчанию
        f = open(GPSData)
        f.close()
        
        
        if not self.Author_line.text():
            header_autor = 'Author';
            header_name = 'Author';
            print("qwe")
        else:
            header_autor = self.Author_line.text()
            header_name = self.Author_line.text()


        if not self.Desc_line.text():
            header_desc = 'Description';           
        else:
            header_desc = self.Desc_line.text()

        header_time = '2011-09-22T18:56:51Z';
        header_trk_name = 'Track Name';
        
        os.makedirs(folder_done,exist_ok=True)
        
        def header(header_autor, header_time, header_name, header_desc, header_trk_name):
            header = '''<?xml version="1.0" encoding="UTF-8"?>
            <gpx
            xmlns="http://www.topografix.com/GPX/1/1"
            version="1.1"
            creator="Sc0rpion"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">
              <time>'''+header_time+'''</time>
              <metadata>
                <name>'''+header_name+'''</name>
                <desc>'''+header_desc+'''</desc>
                <author>
                 <name>'''+header_autor+'''</name>
                </author>
              </metadata>
              <trk>
                <name>'''+header_trk_name+'''</name>
                <trkseg>'''
            return header
        
        footer = '''
            </trkseg>
          </trk>
        </gpx>''';
        
        with open(GPSData, "r") as file1:
            for line in file1:
                if ('$V02' in line.strip()):
                    flag = 1
                else:
                    pieces = line.strip().split(",")
                    timedone = int(pieces[0])+int(time_correct)
                    iso8601 = str(datetime.utcfromtimestamp(timedone).isoformat())+".0Z"
                    stroka = '''
                    <trkpt lat="'''+pieces[2]+'''" lon="'''+pieces[3]+'''">
                      <time>'''+iso8601+'''</time>
                    </trkpt>'''
                    
                    if (flag == 1):
                        if f.closed == False:
                            f.writelines(footer)
                            f.close()
                        
                        iso860_name = str(datetime.utcfromtimestamp(int(pieces[0])+int(time_correct_name_file)).isoformat())
                        file_name = folder_done+iso860_name.replace(':','_').replace('T',' ') +'.gpx'
                        self.textBrowser.append(file_name)
                        f = open(file_name, "w")
                        f.writelines(header(header_autor, iso8601, iso8601, header_desc, iso8601))
                        flag = 0
                    
                    f.writelines(stroka)
        f.writelines(footer)
        f.close()
        self.textBrowser.append("Конвертация окончена")

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()