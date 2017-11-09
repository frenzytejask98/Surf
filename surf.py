import sys, pickle
from PyQt5 import QtCore
from PyQt5.QtWebEngineWidgets import *
from PyQt5 import QtWidgets
from PyQt5 import QtWebEngineWidgets

b = open("bookmarks","w+")
try:
        bookmarks = pickle.loads(b.read())
except EOFError:
        bookmarks=[]
b.close()

url = ""
 
class Main(QtWidgets.QMainWindow):
 
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.initUI()
 
    def initUI(self):
 
        global bookmarks
         
        self.centralwidget = QtWidgets.QWidget(self)
 
        self.line = QtWidgets.QLineEdit(self)
        self.line.setMinimumSize(1150,30)
        self.line.setStyleSheet("font-size:15px;")
 
        self.enter = QtWidgets.QPushButton(self)
        self.enter.resize(0,0)
        self.enter.clicked.connect(self.Enter)
        self.enter.setShortcut("Return")
 
        self.reload = QtWidgets.QPushButton("↻",self)
        self.reload.setMinimumSize(35,30)
        self.reload.setShortcut("F5")
        self.reload.setStyleSheet("font-size:23px;")
        self.reload.clicked.connect(self.Reload)
 
        self.back = QtWidgets.QPushButton("◀",self)
        self.back.setMinimumSize(35,30)
        self.back.setStyleSheet("font-size:23px;")
        self.back.clicked.connect(self.Back)
 
        self.forw = QtWidgets.QPushButton("▶",self)
        self.forw.setMinimumSize(35,30)
        self.forw.setStyleSheet("font-size:23px;")
        self.forw.clicked.connect(self.Forward)
 
        self.book = QtWidgets.QPushButton("☆",self)
        self.book.setMinimumSize(35,30)
        self.book.clicked.connect(self.Bookmark)
        self.book.setStyleSheet("font-size:18px;")
 
        self.pbar = QtWidgets.QProgressBar()
        self.pbar.setMaximumWidth(120)
 
        self.web = QWebEngineView(loadProgress = self.pbar.setValue, loadFinished = self.pbar.hide, loadStarted = self.pbar.show, titleChanged = self.setWindowTitle)
        self.web.setMinimumSize(1360,700)
 
        self.list = QtWidgets.QComboBox(self)
        self.list.setMinimumSize(35,30)
 
        for i in bookmarks:
            self.list.addItem(i)
 
        self.list.activated[str].connect(self.handleBookmarks)
        self.list.view().setSizePolicy(QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Minimum)
 
        self.web.urlChanged.connect(self.UrlChanged)
         
        self.web.page().linkHovered.connect(self.LinkHovered)
 
        grid = QtWidgets.QGridLayout()
 
        grid.addWidget(self.back,0,0, 1, 1)
        grid.addWidget(self.line,0,3, 1, 1)
        grid.addWidget(self.book,0,4, 1, 1)
        grid.addWidget(self.forw,0,1, 1, 1)
        grid.addWidget(self.reload,0,2, 1, 1)
        grid.addWidget(self.list,0,5, 1, 1)
        grid.addWidget(self.web, 2, 0, 1, 6)
 
        self.centralwidget.setLayout(grid)
 
        self.setGeometry(50,50,1360,768)
        self.setWindowTitle("PySurf")
        # self.setWindowIcon(QtWidgets.QIcon(""))
        self.setStyleSheet("background-color:")
         
        self.status = self.statusBar()
        self.status.addPermanentWidget(self.pbar)
        self.status.hide()
 
        self.setCentralWidget(self.centralwidget)
 
    def Enter(self):
        global url
        global bookmarks
         
        url = self.line.text()
 
        https = "https://"
        www = "www."
         
        if www in url and https not in url:
            url = https + url
             
        elif "." not in url:
            url = "https://www.google.com/search?q="+url
             
        elif https in url and www not in url:
            url = url[:7] + www + url[7:]
 
        elif https and www not in url:
            url = https + www + url
 
 
        self.line.setText(url)
 
        self.web.load(QtCore.QUrl(url))
 
        if url in bookmarks:
            self.book.setText("★")
             
        else:
            self.book.setText("☆")
             
        self.status.show()
         
    def Bookmark(self):
        global url
        global bookmarks
 
        bookmarks.append(url)
 
        b = open("bookmarks","wb")
        pickle.dump(bookmarks,b)
        b.close()
         
        self.list.addItem(url)
        self.book.setText("★")
 
    def handleBookmarks(self,choice):
        global url
 
        url = choice
        self.line.setText(url)
        self.Enter()
 
    def Back(self):
        self.web.back()
        
    def Forward(self):
        self.web.forward()
 
    def Reload(self):
        self.web.reload()
 
    def UrlChanged(self):
        self.line.setText(self.web.url().toString())
 
    def LinkHovered(self,l):
        self.status.showMessage(l)
 
def main():
    app = QtWidgets.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
