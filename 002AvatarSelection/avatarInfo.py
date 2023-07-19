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
    hello_button = QtWidgets.QPushButton("Avatar Info")
    hello_button.clicked.connect(avatar_info)
    tutorial_layout.addWidget(hello_button)
    
    tutorial_dialog.Show()

def hello_world():
    print("Hello World!")
    
def current_avatar():
    items = RLPy.RScene.GetSelectedObjects()
    if len(items) == 1:
        object_type = items[0].GetType()
        if object_type == RLPy.EObjectType_Avatar:
            return items[0]
    return None
    
def avatar_info():
    avatar = current_avatar()
    if avatar is not None:
        print(f'{avatar.GetName()} is selected!')
    else:
        print('No avatar is selected!')
    
    
show_dialog()