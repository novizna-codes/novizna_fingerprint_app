import uvicorn
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from main import start_fast_api
import sys
from multiprocessing import Process

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow,self).__init__(*args, **kwargs)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://127.0.0.1:8000"))

        self.setCentralWidget(self.browser)

        self.show()

class TrayIcon(QSystemTrayIcon):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.activated.connect(self.showMenuOnTrigger)

    def showMenuOnTrigger(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            display_main_window(window)
        else:
            self.contextMenu().popup(QCursor.pos())

def display_main_window(window):
    window.setWindowState(window.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
    window.activateWindow()
    window.show()



if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = MainWindow()
    window.resize(400,600)



    api = Process(target=start_fast_api, args=(display_main_window,window), daemon=True)
    api.start()
    def quit_app():
        api.kill()
        app.quit()

    icon = QIcon("icon.png")

    tray = TrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)


    # Creating the options
    menu = QMenu()

    open_window_action=QAction("Open")
    open_window_action.triggered.connect(display_main_window)
    quit = QAction("Quit")
    quit.triggered.connect(quit_app)
    menu.addAction(open_window_action)
    menu.addAction(quit)

    # Adding options to the System Tray
    tray.setContextMenu(menu)
    app.exec_()