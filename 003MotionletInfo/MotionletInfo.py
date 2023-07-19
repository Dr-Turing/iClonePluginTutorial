import RLPy
from PySide2 import *
from shiboken2 import wrapInstance

import os
import json

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
    global tutorial_layout
    tutorial_layout = pyside_dialog.layout()
 

    #-- Add PushButton --#
    add_button("Select Avatar", select_avatar)
    add_button("Generate Info", generate_motionlet_info)
    add_button("Load Info", load_motionlet_info)
    
    tutorial_dialog.Show()
    
def add_button(caption, func):
    global tutorial_layout
    button = QtWidgets.QPushButton(caption)
    button.clicked.connect(func)
    tutorial_layout.addWidget(button)

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
        
def avatar_auto_select(avatar_name):
    avatar_object = RLPy.RScene.FindObject(RLPy.EObjectType_Avatar, avatar_name)
    if avatar_object!= None:
        RLPy.RScene.SelectObject(avatar_object)
        return avatar_object
    else:
        print(f'Can not find avatar:{avatar_name}')
        return None
        
def select_avatar():
    avatar = avatar_auto_select('Camila')
    if avatar is not None:
        print(f'{avatar.GetName()} is selected')
    return avatar
    
info_file_name= 'D:/iClonePluginTut/MotionletInfo/MotionletInfo.json'
def generate_motionlet_info():
    motionlet_dir = RLPy.RApplication.GetCustomContentFolder(RLPy.ETemplateRootFolder_Motion)+'/Tutorial/'
    print(motionlet_dir)
    avatar = select_avatar()
    if avatar is None:
        return
    fps = RLPy.RFps.Fps60
    info = {}
    for f in os.scandir(motionlet_dir):
        if f.is_file():
            filename = f.name
            #print(filename)
            RLPy.RGlobal.SetTime( RLPy.RTime.FromValue(0))
            RLPy.RFileIO.LoadFile(motionlet_dir+filename)
            sk = avatar.GetSkeletonComponent()
            aclip = sk.GetClip(0)
            length = aclip.GetClipLength()
            time = fps.SecondFromFrameTime(length)
            info[filename] = time
    print(info)
    with open(info_file_name,'w', encoding='utf-8') as fl:
        json.dump(info, fl, ensure_ascii = False, indent = 4)
    return

def load_motionlet_info():
    if not os.path.exists(info_file_name):
        generate_motionlet_info()
    fl = open(info_file_name)
    info = json.load(fl)
    fl.close()
    print(info)
    return info
    
   
show_dialog()