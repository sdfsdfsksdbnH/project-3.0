import pickle
from PyQt5 import uic, QtCore
from PyQt5.QtCore import QDate
import os
from PyQt5.QtWidgets import QApplication

print(os.path.realpath(__file__))
dirname, filename = os.path.split(os.path.realpath(__file__))
print(dirname)
Form, Window = uic.loadUiType(dirname+"\\trck.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()


def save_to_file():
    global start_date, calc_date, description, dirname
    data_to_save = {"start": start_date, "end": calc_date, "desc": description}
    file1 = open(dirname+"\\config.txt", "wb")
    pickle.dump(data_to_save, file1)
    file1.close()
    task = """schtasks /create /tr "python """+os.path.realpath(__file__)+"""" /tn "Трекер события" /sc MINUTE /mo 120 /ed 31/12/2020 /F"""
    task = """schtasks /create /tr "python """ + os.path.realpath(
        __file__) + """" /tn "Трекер события" /sc MINUTE /mo 120 /ed """+calc_date.toString("dd/MM/yyyy")+""" /F"""
    print(task)
    os.system('chcp 65001')
    os.system(task)


def read_from_file():
    global start_date, calc_date, description, now_date, dirname
    try:
        file1 = open(dirname+"\\config.txt", "rb")
        data_to_load = pickle.load(file1)
        file1.close()
        start_date = data_to_load["start"]
        calc_date = data_to_load["end"]
        description = data_to_load["desc"]
        form.calendarWidget.setSelectedDate(calc_date)
        form.dateEdit.setDate(calc_date)
        form.plainTextEdit.setPlainText(description)
        delta_days_left = start_date.daysTo(now_date)  # прошло дней
        delta_days_right = now_date.daysTo(calc_date)  # осталось дней
        days_total = start_date.daysTo(calc_date)      # всего дней
        procent = int(delta_days_left * 100 / days_total)
        form.progressBar.setProperty("value", procent)
    except:
        print("Не могу прочитать файл конфигурации")


def on_click():
    global calc_date, description, start_date
    start_date = now_date
    calc_date = form.calendarWidget.selectedDate()
    description = form.plainTextEdit.toPlainText()
    save_to_file()


def on_click_calendar():
    global start_date, calc_date
    form.dateEdit.setDate(form.calendarWidget.selectedDate())
    calc_date = form.calendarWidget.selectedDate()
    delta_days = now_date.daysTo(calc_date)
    days = ['день', 'дня', 'дней']
    if delta_days % 10 == 1 and delta_days % 100 != 11:
        p = 0
    elif 2 <= delta_days % 10 <= 4 and (delta_days % 100 < 10 or delta_days % 100 >= 20):
        p = 1
    else:
        p = 2
    form.label_3.setText(f"До выбранной даты: {str(delta_days) + ' ' + days[p]}")



def on_dateedit_change():
    global start_date, calc_date
    form.calendarWidget.setSelectedDate(form.dateEdit.date())
    calc_date = form.dateEdit.date()
    delta_days = now_date.daysTo(calc_date)
    if (delta_days == 1):
        p ='день'
    if (2 <= delta_days < 5):
        p = 'дня'
    else:
        p = 'дней'
    form.label_3.setText(f"До выбранной даты: {str(delta_days) + ' ' + p}")

form.pushButton.clicked.connect(on_click)
form.calendarWidget.clicked.connect(on_click_calendar)
form.dateEdit.dateChanged.connect(on_dateedit_change)

form.label.setGeometry(QtCore.QRect(100, 0, 500, 51))
form.label.setGeometry(QtCore.QRect(50, 0, 550, 51))
form.label_2.setGeometry(QtCore.QRect(15, 50, 300, 41))
form.calendarWidget.setGeometry(QtCore.QRect(300, 50, 350, 250))
form.pushButton.setGeometry(QtCore.QRect(130, 260, 150, 36))
form.dateEdit.setGeometry(QtCore.QRect(15, 260, 111, 36))


_translate = QtCore.QCoreApplication.translate
form.pushButton.setText(_translate("MainWindow", "Следить"))

start_date = form.calendarWidget.selectedDate()
now_date = form.calendarWidget.selectedDate()
calc_date = form.calendarWidget.selectedDate()
description = form.plainTextEdit.toPlainText()
read_from_file()

form.label.setText("Трекер события от %s" % start_date.toString('dd-MM-yyyy'))
on_click_calendar()

app.exec_()