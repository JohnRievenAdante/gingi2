from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from kivy.lang import Builder
from kivy.uix.image import AsyncImage
from android.permissions import request_permissions, Permission
from plyer import filechooser
from kivy.properties import ListProperty
from kivy.uix.button import Button
from kivy import platform
import logging
#import cv2
from jnius import autoclass
from android.storage import primary_external_storage_path
Environment=autoclass('android.os.Environment')
path=Environment.getExternalStorageDirectory().getAbsolutePath()
logging.info(path) 

from android.storage import app_storage_path
settings_path = app_storage_path() 
p=primary_external_storage_path() 
from android.storage import secondary_external_storage_path
secondary_ext_storage = secondary_external_storage_path()

#logging.info(settings_path)  
if platform == "android":
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.CAMERA, Permission.WRITE_EXTERNAL_STORAGE, 
Permission.READ_EXTERNAL_STORAGE,Permission.READ_MEDIA_IMAGES])

class Main(Widget):

    selection = ListProperty([])

    def choose(self):
        '''
        Call plyer filechooser API to run a filechooser Activity.
        '''
        filechooser.open_file(on_selection=self.handle_selection)
        #filechooser.open_file(path=primary_external_storage_path())
       

    def handle_selection(self, selection):
        '''
        Callback function for handling the selection response from Activity.
        '''
        logging.info(selection)
        self.selection = selection
        #bro=cv2.imread(selection)
        #cv2.imwrite('res1.jpg', bro)
        #print(str(selection))


    def on_selection(self, *a, **k):
        '''
        Update TextInput.text after FileChoose.selection is changed
        via FileChoose.handle_selection.
        '''
        logging.info(f"{p}/Screenshot_2023-02-09-20-08-13-569_org.adblockplus.browser.jpg") 
        self.b_t.ii = f"{path}/mac.jpg"
        self.box.ii = f"{path}/mac.jpg"
        #self.b_t.ii = f"{secondary_ext_storage}/q.jpg"
        #self.box.ii = f"{secondary_ext_storage}/q.jpg"
class RunApp(App):
    def build(self):
        if platform == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.CAMERA,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE,Permission.READ_MEDIA_IMAGES
            ])
            from android.storage import primary_external_storage_path
            settings_path = app_storage_path()  
            logging.info(str(path)+" what the fuck")  
        game = Main()
        return game

if __name__ == '__main__':
    RunApp().run()