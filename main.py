
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.logger import Logger
from shutil import rmtree
from textwrap import fill
import time
import cv2
from os.path import exists, join
import numpy as np
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.graphics import Rotate, PushMatrix, PopMatrix
from kivy.uix.camera import Camera
from kivy.core.text import LabelBase
from androidstorage4kivy import SharedStorage, Chooser
from android_permissions import AndroidPermissions
from kivy.core.window import Window
from android import mActivity, autoclass, api_version


LabelBase.register(name="Roboto", 
                   fn_regular= "asset/Roboto/Montserrat-Bold.ttf")
LabelBase.register(name="Montserrat", 
                   fn_regular= "asset/Roboto/Montserrat-Light.ttf")
LabelBase.register(name="Rob", 
                   fn_regular= "asset/Roboto/Roboto-Regular.ttf")



class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen,self).__init__(**kwargs)
        self.start()

    def start(self):
        anim = Animation(opacity=1, duration=1)
        anim += Animation(opacity=1, duration=1)
        anim += Animation(opacity=0, duration=1)
        anim.bind(on_complete=self.start2)
        anim.start(self.ids["welcometxt1"])
        

    def start2(self,*args):
        anim = Animation(opacity=1, duration=1)
        anim += Animation(opacity=1, duration=0.5)
        anim += Animation(pos=(0, 60), t='in_quad')
        anim.bind(on_complete=self.start3)
        anim.start(self.ids["welcometxt2"])

    def start3(self,*args):
        anim = Animation(opacity=1, duration=1)
        anim += Animation(opacity=1, duration=0.5)
        anim.start(self.ids["startbtn"])


    def switch_screen(self, *args):
        
        self.manager.current = "another"
        

class CameraInstructionsScreen(Screen):
    
    def switch_screen(self, *args):
    
        self.camera_screen = CameraScreen(name="cam")
        
        self.manager.add_widget(self.camera_screen)
        #self.parent.get_screen('cam').start()
        self.manager.current = "cam"

class DisplayProcessedImageScreen(Screen):
    
    def start(self, contourlength,prediction,filename):
        predlbl = self.ids['predictlbl']
        infolbl = self.ids['infolbl']
        img = self.ids['dpimage']
        lbl = self.ids['contournumlbl']
        lbl.text="The image has "+contourlength+" contours found"
        
        
        img.source=filename
        predlbl.text="The image is "+prediction
        if prediction.lower()=="gingivitis":
            infolbl.text="Gum diseases such as Gingivitis can lead to complications. Please visit your dentist whenever you can"
        if prediction.lower()=="healthy":
            infolbl.text="Keep taking care of your teeth and gums!"

    def switch_screen(self, *args):
        self.manager.current = "mainmenu"



class ProcessScreen(Screen):
    
    def start(self,filename):
        self.filename=filename
        img = self.ids['takenimg']
        
        img.source=filename
    
    #confirm
    def image_process(self,*args):
        img2 = cv2.imread(self.filename)

        ORANGE_MIN = np.array([5, 145, 94],np.uint8)
        ORANGE_MAX = np.array([8, 255, 255],np.uint8)
        img=cv2.rotate(img2, cv2.ROTATE_90_COUNTERCLOCKWISE)
        hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        cv2.imwrite('res1.jpg', hsv_img)
        

        frame_threshed = cv2.inRange(hsv_img, ORANGE_MIN, ORANGE_MAX)
        cv2.imwrite('res.jpg', frame_threshed)
        

        kernel = np.ones((10, 10), np.uint8)
        closing = cv2.morphologyEx(frame_threshed, cv2.MORPH_CLOSE, kernel, iterations=1)
        cv2.imwrite('res2.jpg', closing)
        

        contours, hierarchy = cv2.findContours(image=closing, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

        image_copy = img.copy()
        contourlength=str(len(contours))

        cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=4, lineType=cv2.LINE_AA)
                
        cv2.imwrite('contour_point_simple.jpg', image_copy)

        predict="No prediction"
        self.parent.get_screen('dpimage').start(contourlength,predict,self.filename)
        self.manager.current = "dpimage"

    #retake
    def switch_screen(self, *args):
        self.manager.current = "mainmenu"


class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MainMenuScreen,self).__init__(**kwargs)
        self.dialog=None
    
    def start(self,*args):
        
        anim = Animation(opacity=1, duration=0.2)
        anim += Animation ( pos=(0,300), t="in_quad")
        anim.start(self.ids["cambtn"])

        anim2 = Animation(opacity=1, duration=0.2)
        anim2 += Animation ( pos=(0,200), t="in_quad")
        anim2.start(self.ids["gallerybtn"])

        anim3 = Animation(opacity=1, duration=0.2)
        anim3 += Animation ( pos=(0,100), t="in_quad")
        anim3.start(self.ids["howbtn"])

    def switch_screen2(self, *args):
        self.manager.current = "main"
            
    def switch_screen(self, *args):
        
        #self.camera_screen = CameraScreen(name="cam")
        
        #self.manager.add_widget(self.camera_screen)
        #self.parent.get_screen('cam').start()
        self.manager.current = "caminst"
        
    
        #self.chooser = Chooser(self.chooser_callback)
    #code for take from gallery
    
    def quit_app(self,window,key,*args):
        if key == 27:
            mActivity.finishAndRemoveTask() 
            return True   
        else:
            return False    

    def start_app(self):
        self.dont_gc = None
        ss = SharedStorage()
        app_title = str(ss.get_app_title())
        self.label_lines = []

    # Chooser interface
    def chooser_start(self,bt):
        self.chooser.choose_content("image/*")

    def chooser_callback(self,uri_list):
        try:
            ss = SharedStorage()
            for uri in uri_list:
                # copy to private
                path = ss.copy_from_shared(uri)
                filename=str(path).split("/")[-1]
                if path:
                    # then to app shared
                    shared = ss.copy_to_shared(path)
                
            
        except Exception as e:
            Logger.warning('SharedStorageExample.chooser_callback():')
            Logger.warning(str(e))
        
    def switch_screen3(self, *args):
        self.manager.current = "another"

class AnotherScreen(Screen):
    def switch_screen(self, *args):
        self.parent.get_screen('mainmenu').start()
        self.manager.current = "mainmenu"

class CameraScreen(Screen):
    def capture(self):

        
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        
        source=camera.export_to_png("IMG_{}.png".format(timestr))
        img2 = cv2.imread("IMG_{}.png".format(timestr))
        img=cv2.rotate(img2, cv2.ROTATE_90_COUNTERCLOCKWISE)
        cv2.imwrite('contour_point_simple.jpg', img)
        camera.play=False
        self.parent.get_screen('process').start("IMG_{}.png".format(timestr))
        
        self.manager.current = "process"

    
    def switch_screen(self, *args):
        self.manager.current = "mainmenu"
    #def start(self,*args):

class MainApp(MDApp):
    def build(self):
        temp = SharedStorage().get_cache_dir()
        if temp and exists(temp):
            rmtree(temp)
        self.dont_gc = None
        dont_gc = AndroidPermissions(self.start_app)
        self.screen_manager = ScreenManager()
        self.main_screen = MainScreen(name="main")
        self.another_screen = AnotherScreen(name="another")
        self.mainmenu_screen = MainMenuScreen(name="mainmenu")
        self.camerainst_screen = CameraInstructionsScreen(name="caminst")
        self.process_screen = ProcessScreen(name="process")
        self.dpimage_screen = DisplayProcessedImageScreen(name="dpimage")
        
        self.screen_manager.add_widget(self.main_screen)
        self.screen_manager.add_widget(self.another_screen)
        self.screen_manager.add_widget(self.mainmenu_screen)
        self.screen_manager.add_widget(self.camerainst_screen)
        self.screen_manager.add_widget(self.process_screen)
        self.screen_manager.add_widget(self.dpimage_screen)
        self.screen_manager.current = "main"
        return self.screen_manager
    
    

if __name__ == '__main__':
    MainApp().run()

