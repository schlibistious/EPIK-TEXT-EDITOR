from src import ui
import PyQt6.QtWidgets as qt
import sys
app = qt.QApplication(sys.argv)
screen = app.primaryScreen()
screenSize = screen.size()

window = ui.mainWindow(int(screenSize.width() / 1.1), int(screenSize.height() / 1.1))

app.exec()