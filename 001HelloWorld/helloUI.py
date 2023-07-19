import RLPy
from PySide2 import *
from shiboken2 import wrapInstance

rl_plugin_info = {"ap": "iClone", "ap_version": "8"}


tutorial_dialog = None
def show_dialog():
    global tutorial_dialog
    
    tutorial_dialog = RLPy.RUi.CreateRDialog()
    tutorial_dialog.SetWindowTitle("Turing Tutorial")

    #-- Create Pyside layout for RDialog --#
    global pyside_dialog
    pyside_dialog = wrapInstance(int(tutorial_dialog.GetWindow()), QtWidgets.QDialog)
    pyside_dialog.setFixedWidth(300)
    tutorial_layout = pyside_dialog.layout()
 

    #-- Add PushButton --#
    hello_button = QtWidgets.QPushButton("Hello")
    hello_button.clicked.connect(hello_world)
    tutorial_layout.addWidget(hello_button)
    
    tutorial_dialog.Show()

def hello_world():
    print("Hello World!")
    
show_dialog()