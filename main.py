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

"""
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.image import Image
from kivy.uix.label import Label
import os.path
from kivy.app import App
from android import activity, mActivity
from jnius import autoclass
import logging
from kivy.uix.widget import Widget
from jnius import cast

Intent = autoclass('android.content.Intent')
DocumentsContract = autoclass('android.provider.DocumentsContract')
Document = autoclass('android.provider.DocumentsContract$Document')
PythonActivity = autoclass("org.kivy.android.PythonActivity")
Environment = autoclass("android.os.Environment")
Settings = autoclass("android.provider.Settings")
Uri=autoclass('android.net.Uri')

class bro(Widget):
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
            name2=""
            try:
                root_uri = intent.getData()
               
                #root_id = DocumentsContract.getTreeDocumentId(root_uri)
                #children = DocumentsContract.buildChildDocumentsUriUsingTree(root_uri,root_id)
                contentResolver = mActivity.getContentResolver()
                c = contentResolver.query(root_uri, None, None, None, None)
                logging.info(str(c)+" what the fuck") 
                c.moveToNext()
                name = c.getString(0)
                intent_image = Intent(Intent.ACTION_VIEW)
                intent_image.setData(Uri.parse("Primary:///DCIM/Screenshots/IMG_20210305_150147.jpg"))
                intent_image.setClassName("org.gingidetect.gingidetect","org.gingidetect.media.Gallery")
                mActivity.startActivityForResult(intent_image) 
                
                try: 
                    InputStream inputStream = mContext.getContentResolver().openInputStream(uri)
                    FileOutputStream outputStream = new FileOutputStream(output)
                    read = 0
                    bufferSize = 1024
                    buffers = new byte[bufferSize]
                    while (read = inputStream.read(buffers) != -1):
                        outputStream.write(buffers, 0, read)
                    

                    inputStream.close()
                    outputStream.close()

                except Exception as e: 
                    msg += str(e) + '\n'  
                
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
            name2=Uri.parse((name))
            logging.info(type(name2))
            logging.info((name2))
            #self.box.source = name
class RunApp(App):
    

    #def on_start(self):
       # self.set_intent()

    def build(self):
        #activity.bind(on_activity_result=self.intent_callback)
        try:
            activity = mActivity.getApplicationContext()
            uri = Uri.parse("package:" + activity.getPackageName())
            intent = Intent()
            intent.setAction(Settings.ACTION_MANAGE_ALL_FILES_ACCESS_PERMISSION)
            #intent = Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION, uri)
            SharedStorage().retrieve('test.txt')
            currentActivity = cast(
            "android.app.Activity", PythonActivity.mActivity
            )
            currentActivity.startActivityForResult(intent, 101)
        except:
            intent = Intent()
            intent.setAction(Settings.ACTION_MANAGE_ALL_FILES_ACCESS_PERMISSION)
            currentActivity = cast(
            "android.app.Activity", PythonActivity.mActivity
            )
            currentActivity.startActivityForResult(intent, 101) 
        self.label = Label()
        self.box=Image()
        #self.filechooser = FileChooserListView(size_hint=(1,0.8),pos_hint={"top":0.9},rootpath='/data/user/0/org.test.myapp/')
        self.filechooser = FileChooserListView(size_hint=(1,0.8),pos_hint={"top":0.9},rootpath='/storage/emulated/0/')
        return self.filechooser

if __name__ == '__main__':
    RunApp().run()
"""
from kivy.uix.filechooser import FileChooserListView
from kivy.app import App
from kivy.clock import mainthread
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.logger import Logger
from os.path import exists, join
from shutil import rmtree
from textwrap import fill
import logging
from android import mActivity, autoclass, api_version
from kivy.uix.image import Image

from androidstorage4kivy import SharedStorage, Chooser
from android_permissions import AndroidPermissions

Environment = autoclass('android.os.Environment')

#######################################################################
# Not a real world example, this is the unit tests.
#
# One test (8) depends on Pictures/CHART_4.jpg belonging to another app
# Expect this test to likely fail on some random device.
#######################################################################

class SharedStorageExample(App):

    def build(self):
        Window.bind(on_keyboard = self.quit_app)
        # create chooser listener
        self.chooser = Chooser(self.chooser_callback)
  
        # cleanup from last time if Android didn't
        """temp = SharedStorage().get_cache_dir()
        if temp and exists(temp):
            rmtree(temp)"""

        # layout
        self.label = Label(text = 'Greetings Earthlings')
        self.button = Button(text = 'Choose an image file',
                             on_press = self.chooser_start,
                             size_hint=(1, .15))
        #self.filechooser = Image(size_hint=(1,0.8),pos_hint={"top":0.9},rootpath='/data/user/0/org.test.myapp/')
        self.filechooser = Image(source='/storage/emulated/0/Android/data/org.test.myapp/cache/FromSharedStorage/test.jpg')
        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.button)
        self.layout.add_widget(self.filechooser)
        return self.layout

    def on_start(self):
        self.dont_gc = AndroidPermissions(self.start_app)

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
        self.display()
        self.append("Cache Dir Exists:  " + str(ss.get_cache_dir()))

        ############################################################
        # copy to app shared storage   copy_to_shared(private_file)
        ############################################################
        
        """share0 = ss.copy_to_shared('./test.txt')
        share1 = ss.copy_to_shared('test.txt',
                                   filepath = 'a/b/test1.txt')"""
        """share2 = ss.copy_to_shared('test.jpg',
                                   filepath = join('c','test1.jpg'))"""
        #share3 = ss.copy_to_shared('test.mp3')
        # For .ogg, collection depends on the Android version
        # On newer devices default is DIRECTORY_MUSIC, so DIRECTORY_ALARMS
        # is a legal place.
        # On older devices default is DIRECTORY_DOCUMENTS, so DIRECTORY_ALARMS
        # is not legal and will go to the default, see test 'path4' below.
        """share4 = ss.copy_to_shared('test.ogg', 
                                   collection = Environment.DIRECTORY_ALARMS)
        share5 = ss.copy_to_shared('test.mp4')
        # Illegal collection names for .mp4 default to the automatic
        # collection name DIRECTORY_MOVIES
        share6 = ss.copy_to_shared('test.mp4',
                                   collection = 'Video',
                                   filepath = 'renamed.mp4')
        share7 = ss.copy_to_shared('test.mp4',
                                   collection = None,
                                   filepath = 'newname.mp4')"""

        ################################################################
        # copy from app shared storage    copy_from_shared(shared_file)         SAKA KA NA  BOY SAKA KA NA BOY   SAKA KA NA BOY  SAKA KA NA BOY  SAKA KA NA BOY
        ################################################################
        
        #path0 = ss.copy_from_shared(share0)
        #path1 = ss.copy_from_shared(share1)
        """path2 = ss.copy_from_shared(join(Environment.DIRECTORY_PICTURES,
                                         app_title, 'c', 'test.jpg'))"""
        #path3 = ss.copy_from_shared(share3)

        # See note above about .ogg
        # Not certain the change is exactly Androoid 10, but close enough.
        """if api_version > 29:
            path4 = ss.copy_from_shared(join(Environment.DIRECTORY_ALARMS,
                                             app_title, 'test.ogg'))
        else:
            path4 = ss.copy_from_shared(join(Environment.DIRECTORY_DOCUMENTS,
                                             app_title, 'test.ogg'))
            
        path5 = ss.copy_from_shared(share5)
        path6 = ss.copy_from_shared(join(Environment.DIRECTORY_MOVIES,
                                         app_title, 'renamed.mp4'))
        path7 = ss.copy_from_shared(share7)"""

        ###############################################################
        # Delete from App Shared Storage    delete_shared(shared_file)
        ###############################################################
        
        # Keep two (share0, share1) to test persistence between app installs
        #del2 = ss.delete_shared(share2)
        """del3 = ss.delete_shared(share3)
        del4 = ss.delete_shared(share4)
        del5 = ss.delete_shared(join(Environment.DIRECTORY_MOVIES,
                                     app_title, 'test.mp4'))
        del6 = ss.delete_shared(share6)
        del7 = ss.delete_shared(join(Environment.DIRECTORY_MOVIES,
                                     app_title,'newname.mp4'))"""

        #############################################################
        # Copy file created by other app to this app then delete copy
        #############################################################
        
        # on my phones CHART_4.jpg exists
        path8 = ss.copy_from_shared(join(Environment.DIRECTORY_PICTURES,
                                         'test.jpg'))
        logging.info("copy from shared storage ok")
        share8 = ss.copy_to_shared(path8)
        logging.info("copy to app package ok")
        #del8 = ss.delete_shared(share8)

        #################################
        # Report Results
        #################################
        #self.append("copy_to_shared test.txt       " + str(share0 != None))
        #self.append("copy_to_shared a/b/test.txt:  " + str(share1 != None))
        #self.append("copy_to_shared c/test.jpg     " + str(share2 != None))
        """self.append("copy_to_shared test.mp3:      " + str(share3 != None))
        self.append("copy_to_shared test.ogg:      " + str(share4 != None))
        self.append("copy_to_shared test.mp4:      " + str(share5 != None))
        self.append("copy_to_shared renamed.mp4:   " + str(share6 != None))
        self.append("copy_to_shared newname.mp4:   " + str(share7 != None))
        
        self.append("copy_from_shared test.txt     " + str(path0 != None and\
                                                           exists(path0)))
        self.append("copy_from_shared a/b/test.txt " + str(path1 != None and\
                                                           exists(path1)))
        self.append("copy_from_shared c/test1.jpg  " + str(path2 != None and\
                                                           exists(path2)))"""
        """self.append("copy_from_shared test.mp3     " + str(path3 != None and\
                                                           exists(path3)))
        self.append("copy_from_shared test.ogg     " + str(path4 != None and\
                                                           exists(path4)))
        self.append("copy_from_shared test.mp4     " + str(path5 != None and\
                                                           exists(path5)))
        self.append("copy_from_shared renamed.mp4  " + str(path6 != None and\
                                                           exists(path6)))
        self.append("copy_from_shared newname.mp4  " + str(path7 != None and\
                                                           exists(path6)))"""
        
        #self.append("deleted c/test.jpg     " + str(del2))
        """self.append("deleted test.mp3       " + str(del3))
        self.append("deleted test.ogg       " + str(del4))
        self.append("deleted test.mp4       " + str(del5))
        self.append("deleted renamed.mp4    " + str(del6))
        self.append("deleted newname.mp4    " + str(del7))

        self.append("copy_from_shared other app    " + str(path8 != None and\
                                                    exists(path8)))
        self.append("copy_to_shared this app       " + str(share8 != None))"""
        #self.append("delete copy from other " + str(del8))
        self.display()

    # Chooser interface
    def chooser_start(self,bt):
        self.chooser.choose_content("image/*")

    def chooser_callback(self,uri_list):
        try:
            ss = SharedStorage()
            Logger.warning(str(uri_list)+" urilistttttt+++++++++")
            for uri in uri_list:
                # copy to private
                Logger.warning(str(uri)+" uriiiiiiiiii+++++++++")
                path = ss.copy_from_shared(uri)
                Logger.warning(str(path)+" pathhhhhhhhhhh+++++++++")
                if path:
                    # then to app shared
                    shared = ss.copy_to_shared(path)
                    Logger.warning(str(shared)+" sharedddddddd+++++++++")
                    self.append("Result copied to app shared "+\
                                str(exists(path) and shared != None))
                    contentResolver = mActivity.getContentResolver()
                    c = contentResolver.query(shared, None, None, None, None)
                    c.moveToNext()
                    name = c.getString(0)
                    Logger.warning(name+" file putanginaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/////////////-----------")
                    #self.filechooser.source="/storage/emulated/0/Android/data/org.test.myapp/cache/FromSharedStorage/"+
            self.display()
        except Exception as e:
            Logger.warning('SharedStorageExample.chooser_callback():')
            Logger.warning(str(e))

    # Label text
    def append(self, name):
        self.label_lines.append(name)

    @mainthread
    def display(self):
        if self.label:
            self.label.text = ''
            for r in self.label_lines:
                self.label.text += fill(r, 40) + '\n'

SharedStorageExample().run()