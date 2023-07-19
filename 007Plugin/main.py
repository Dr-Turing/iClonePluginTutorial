import RLPy
from PySide2 import *
from shiboken2 import wrapInstance

import os
import json
import random

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
    add_button("Generate Talk", generate_talk)
    
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
  
def generate_talk():
    avatar = select_avatar()
    if avatar is None:
        return
    generate_talk_v0(avatar,1.0, 6.0)
    voice_file = 'D:/iClonePluginTut/Voice/compere-001.mp3'
    generate_viseme(avatar,1.0, voice_file)
    set_auto_blink(avatar)
    
def load_motion(time, filename):
    fps = RLPy.RFps.Fps60
    ft = fps.FrameTimeFromSecond(time)
    RLPy.RGlobal.SetTime( ft)
    RLPy.RFileIO.LoadFile(filename)
     
def generate_talk_v0(avatar, start_time, duration):
    motionlet_dir = RLPy.RApplication.GetCustomContentFolder(RLPy.ETemplateRootFolder_Motion)+'/Tutorial/'
    print(motionlet_dir)
    fps = RLPy.RFps.Fps60
    
    info = load_motionlet_info()
    name_list = list(info.keys())
    time = start_time
    end_time = start_time + duration
    while time < end_time:
        r = random.randint(0, len(name_list)-1)
        filename = name_list[r]
        current_len = info[filename]
        load_motion(time, motionlet_dir+filename)
        time += current_len
        if time > end_time:
            sk = avatar.GetSkeletonComponent() 
            sk.BreakClip(fps.FrameTimeFromSecond(end_time))
            load_motion(end_time-0.03, motionlet_dir+'End/End.rlMotion')
    return 
  
def generate_viseme(avatar, start_time, voice_file):
    viseme_component = avatar.GetVisemeComponent()
    audio_obj = RLPy.RAudio.CreateAudioObject()
    audio_obj.Load(voice_file)
    clip_name= "Talk_Clip"
    
    fps = RLPy.RFps.Fps60
    clip_start_time = fps.FrameTimeFromSecond(start_time)
    viseme_component.LoadVocal(audio_obj, clip_start_time,clip_name)
    return 
  
def set_auto_blink(avatar):
    time = RLPy.RTime.FromValue(0)
    RLPy.RGlobal.SetTime(time)
    face = avatar.GetFaceComponent()
    blinks = face.GetAutoBlinkNames()
    print(blinks)
    face.SetAutoBlinkName('Charming')

def add_menu_item(plugin_menu, caption, func ):
    # Check if the menu action already exists
    menu_actions = plugin_menu.actions()
    for i in range(len(menu_actions)):
        if menu_actions[i].text() == caption:
            plugin_menu.removeAction(menu_actions[i])  # Remove duplicate actions

    new_action = plugin_menu.addAction(caption)
    new_action.triggered.connect(func)   
    
def initialize_plugin():
    # Add menu
    ic_dlg = wrapInstance(int(RLPy.RUi.GetMainWindow()), QtWidgets.QMainWindow)
    plugin_menu = ic_dlg.menuBar().findChild(QtWidgets.QMenu, "turing_pytutorial_menu")
    if (plugin_menu == None):
        plugin_menu = wrapInstance(int(RLPy.RUi.AddMenu("Turing Python Tutorial", RLPy.EMenu_Plugins)), QtWidgets.QMenu)
        plugin_menu.setObjectName("turing_pytutorial_menu")
    
    add_menu_item(plugin_menu, 'Generate Talk', show_dialog )
    
#show_dialog()
initialize_plugin()