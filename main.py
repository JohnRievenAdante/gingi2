"""from kivy.app import App
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
import uri
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
        media=autoclass('android.media.MediaScannerConnection')
        logging.info(f"{p}/Screenshot_2023-02-09-20-08-13-569_org.adblockplus.browser.jpg") 
        #base = URI(f"{path}/mac.jpg")
        base=media.scanFile(self.selection[0].getAbsolutePath(), None)
        self.b_t.ii = base
        self.box.ii = base
        #self.b_t.ii = f"{path}/mac.jpg"
        #self.box.ii = f"{path}/mac.jpg"
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
    
"""
from kivy.uix.image import Image
from kivy.uix.label import Label
import os.path
from kivy.app import App
from android import activity, mActivity
from jnius import autoclass
import logging
from kivy.uix.widget import Widget
Intent = autoclass('android.content.Intent')
DocumentsContract = autoclass('android.provider.DocumentsContract')
Document = autoclass('android.provider.DocumentsContract$Document')

class RunApp(App):
    REQUEST_CODE = 42 # unique request ID
   
    def set_intent(self):
        #intent = Intent(Intent.ACTION_OPEN_DOCUMENT_TREE)
        intent = Intent(Intent.ACTION_OPEN_DOCUMENT)
        #intent = Intent(Intent.ACTION_GET_CONTENT)
        #intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
        intent.addCategory(Intent.CATEGORY_OPENABLE)
        intent.setType("image/*")
        mActivity.startActivityForResult(intent, self.REQUEST_CODE)        

    def intent_callback(self, requestCode, resultCode, intent):
        if requestCode == self.REQUEST_CODE:
            msg = ""
            name=""
            try:
                root_uri = intent.getData()
               
                #root_id = DocumentsContract.getTreeDocumentId(root_uri)
                #children = DocumentsContract.buildChildDocumentsUriUsingTree(root_uri,root_id)
                contentResolver = mActivity.getContentResolver()
                c = contentResolver.query(root_uri, None, None, None, None)
                logging.info(str(c)+" what the fuck") 
                c.moveToNext()
                name = str(c.getString(0))
                    
                
                #Widget.add_widget(Widget.box)
                #pfd=contentResolver.openFileDescriptor(content_uri,"r")
                #info = [Document.COLUMN_DISPLAY_NAME]
                #logging.info(str(children)+" what the fuck")  
                #logging.info(str(info)+" what the fuck") 
                #c = contentResolver.query(children, info, None, None, None)
                #logging.info(str(c)+" what the fuck") 
                #while c.moveToNext():
                   # name = str(c.getString(0))
                    #if 'rce_plugin' not in name:  # junk from Kindle App
                        #msg += name + '\n'
                #c.close()
            except Exception as e:
                msg += str(e) + '\n'
                logging.info(str(e)) 
            logging.info(str(name))
            self.box.source = str(name)

    def on_start(self):
        self.set_intent()

    def build(self):
        activity.bind(on_activity_result=self.intent_callback)
        self.label = Label()
        self.box=Image()
        return self.label

if __name__ == '__main__':
    RunApp().run()
