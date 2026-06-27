import PyQt6.QtWidgets as qw
import PyQt6.QtGui as gui
from PyQt6.QtCore import Qt
import os
from src import calculator
assets = __file__.replace(r"src\ui.py", "") + "assets"
class mainWindow(qw.QMainWindow):
    def __init__(self, width, height, params):
        # make window
        super().__init__()
        screenSize = qw.QApplication.primaryScreen().size()
        self.setWindowTitle("epik text")
        self.setWindowIcon(gui.QIcon(os.path.join(assets, "icon.png")))

        # --formatting window 'n stuf
        self.resize(width, height)
        xcent = (screenSize.width() - width) // 2
        ycent = (screenSize.height() - height) // 2
        self.move(xcent, ycent)
        self.show()
        print(f"created mainWindow: {width}, {height}, {xcent}, {ycent}")
        # --set up file system!
        self.files = []
        # --check for file params
        if len(params) > 1:
            print("param detected!")
            name = os.path.basename(params[1])
            file = open(params[1], "r")
            self.files.append({"name": name, "dir": params[1], "content": file.read()})
            self.tabs.addTab(name)
            self.tabs.setCurrentIndex(self.tabs.count() - 1)
            self.field.setText(file.read())
            file.close()

        self.ui()
    def ui(self):
        # setting up layout and workspace
        self.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #fcf7fc, stop:1 #fad2f8);")
        workspace = qw.QWidget()
        layout = qw.QHBoxLayout(workspace)
        layout.setContentsMargins(20, 20, 20, 50)
        editor_layout = qw.QVBoxLayout()
        editor_widget = qw.QWidget()
        editor_widget.setLayout(editor_layout)
        calc_layout = qw.QVBoxLayout()
        calc_widget = qw.QWidget()
        calc_widget.setLayout(calc_layout)
        self.menu = self.menuBar()
        self.tabrow = qw.QHBoxLayout()
        # adding stuff to workspace :D

        fileMenu = self.menu.addMenu("File")
        self.actionSave = fileMenu.addAction("Save")
        self.actionSave.setShortcut("Ctrl+S")
        self.actionOpen = fileMenu.addAction("Open")
        self.actionOpen.setShortcut("Ctrl+O")

        # ***editor***
        self.newTab = qw.QPushButton()
        self.newTab.setText("+")
        self.newTab.setFixedSize(int(self.size().width() / 100), int(self.size().width() / 100))

        self.tabs = qw.QTabBar()
        self.tabrow.addWidget(self.newTab)
        self.tabrow.addWidget(self.tabs)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.closeTab)
        self.tabs.setMovable(True)

        self.field = qw.QTextEdit()
        font = gui.QFont()
        font.setPointSize(15)
        self.field.setFont(font)
        self.field.setPlaceholderText("select a file please")
        self.field.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.field.setStyleSheet("background-color: #e2bcf5;")

        # **calculator**
        self.calcQuery = qw.QLineEdit()
        calc_layout.addWidget(self.calcQuery)
        self.calcResponse = qw.QLabel()
        calc_layout.addWidget(self.calcResponse)
        self.calcResponse.setText("0")
        font = gui.QFont()
        font.setPointSize(24)
        self.calcResponse.setFont(font)
        self.calcQuery.textChanged.connect(self.calc)


        # **tools**
        self.toolTabs = qw.QTabWidget()
        self.toolTabs.setTabPosition(qw.QTabWidget.TabPosition.West)
        self.toolTabs.addTab(editor_widget, "editor")
        self.toolTabs.addTab(calc_widget, "calculator")
        self.toolTabs.setMovable(True)
        # code for functionality
        self.actionSave.triggered.connect(self.save)
        self.actionOpen.triggered.connect(self.openFile)
        self.newTab.clicked.connect(self.askForName)
        self.tabs.currentChanged.connect(self.changeTab)
        self.field.textChanged.connect(self.textChanged)
        # add all the stuff to layout/workspace
        layout.addWidget(self.toolTabs)
        editor_layout.addLayout(self.tabrow)
        editor_layout.addWidget(self.field)
        self.setCentralWidget(workspace)

    def resizeEvent(self, event):
        w = event.size().width()
        h = event.size().height()

        super().resizeEvent(event)
    def askForName(self):
        new = qw.QLineEdit()
        new.setPlaceholderText("insert file name")
        self.tabrow.insertWidget(1, new)
        def finish():
            name = new.text()
            new.deleteLater()
            tab = self.tabs.addTab(name)
            self.files.append({"name": name, "dir": None, "content": ""}) # i'm not even gonna bother commenting any of this
        new.returnPressed.connect(finish)
    def save(self):
        content = self.field.toPlainText()
        current = self.currentFile()
        try:
            if current["dir"] == None:
                path, _ = qw.QFileDialog.getSaveFileName(self, "Save or Replace File", current["name"], "Text Files (*.txt);;All Files (*)")
                file = open(path, "w")
                file.write(content)
                file.close()
                self.currentFile()["dir"] = path
            else:
                file = open(current["dir"], "w")
                file.write(content)
                file.close()
            self.currentFile()["content"] = content
            self.tabs.setTabText(self.tabs.currentIndex(), current["name"])
        except:
            print("save cancelled")
    def openFile(self):
        try:
            directory, _ = qw.QFileDialog.getOpenFileName(self, "Open file", "", "Text Files (*.txt);;All Files (*)")
            file = open(directory, "r")
            content = file.read()
            self.files.append({"name": os.path.basename(file.name), "dir": file.name, "content": content})
            self.tabs.addTab(os.path.basename(file.name))
            self.tabs.setCurrentIndex(self.tabs.count() - 1)
            self.field.setText(content)
            file.close()
            currentIndex = self.tabs.currentIndex()
            self.changeTab(currentIndex)
            self.tabs.setTabText(currentIndex, self.tabs.tabText(currentIndex))
        except:
            print("open cancelled")
    def changeTab(self, index):
        print(self.tabs.tabText(index))
        eurika = False
        for i in self.files:
            if i["name"] == self.tabs.tabText(index):
                self.field.setText(i["content"])
                eurika = True
        if eurika == False:
            self.field.setText("")
    def closeTab(self, index):
        file = self.currentFile()
        try:
            self.files.pop(self.files.index(file))
            self.tabs.removeTab(index)
        except:
            print("GHOST FILE?!?!?!")
            self.tabs.removeTab(index)
    def textChanged(self):
        try:
            index = self.tabs.currentIndex()
            content = self.currentFile()["content"]
            if self.field.toPlainText() != content:
                self.tabs.setTabText(index, self.tabs.tabText(index).replace("*", "") + "*")
        except:
            print("it looks like theres probably no tabs open")
    def currentFile(self):
        for i in self.files:
                if i["name"] == self.tabs.tabText(self.tabs.currentIndex()).replace("*", ""):
                    return i
        print("could not find file!")
        return None
    def calc(self):
        try:
            res = calculator.calculate(self.calcQuery.text())
            self.calcResponse.setText(str(res))
        except IndexError:
            pass
        return None
