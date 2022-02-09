import sys
from multiprocessing import Process
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow,self).__init__(*args, **kwargs)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://127.0.0.1:8000"))

        self.setCentralWidget(self.browser)

        self.show()


class TrayIcon(QSystemTrayIcon):

    def __init__(self,app,window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.window = window
        self.activated.connect(self.showMenuOnTrigger)
        self.icon = QIcon("icon.png")
        self.setIcon(self.icon)
        self.setVisible(True)
        self.add_menu()

    def add_menu(self):
        menu=QMenu()
        open_window_action = QAction("Open")
        open_window_action.triggered.connect(self.display_main_window)
        self.quit = QAction("Quit")
        self.quit.triggered.connect(self.quit_app)
        menu.addAction(open_window_action)
        menu.addAction(self.quit)
        self.setContextMenu(menu)

    def quit_app(self):
        # api.kill()
        self.app.quit()

    def showMenuOnTrigger(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.display_main_window()
        else:
            self.contextMenu().popup(QCursor.pos())

    def display_main_window(self):
        self.window.setWindowState(self.window.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        self.window.activateWindow()
        self.window.show()


class UiProcess(Process):

    def __init__(self, *args, **kwargs):
        super(UiProcess, self).__init__(*args, **kwargs)


    def run(self) -> None:
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        self.window = MainWindow()
        self.window.resize(400, 600)
        self.trayIcon = TrayIcon(self.app, self.window)
        self.app.exec_()

