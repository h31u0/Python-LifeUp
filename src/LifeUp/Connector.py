from abc import ABC, abstractmethod

import dropbox

import os
import shutil

class Connector(ABC):
 
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def retrieve(self):
        pass
    
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def close(self):
        pass

class Dropbox_Connector(Connector):
    def __init__(self, app_key, app_sec, token, file, path):
        self.dbx = None
        self.app_key = app_key
        self.app_sec = app_sec
        self.token = token
        self.file = file
        self.path = path
        if(os.path.isdir(self.path) and len(os. listdir(self.path)) != 0):
            print("tmp dir must not have other files")
            exit(-1)

    def connect(self):
        if(self.dbx is None):
            self.dbx = dropbox.Dropbox(
            app_key = self.app_key,
            app_secret = self.app_sec,
            oauth2_refresh_token = self.token
        )
    
    def retrieve(self):
        os.makedirs(self.path, exist_ok=True)
        self.dbx.files_download_to_file(self.path+"LifeupBackup.zip", self.file)
        
        shutil.unpack_archive(self.path+"LifeupBackup.zip", self.path+"LifeupBackup", "zip")
        os.remove(self.path+"LifeupBackup.zip")

    def update(self):
        shutil.make_archive("tmp2/LifeupBackup", 'zip', "tmp2/LifeupBackup")        
        with open(self.path+"LifeupBackup.zip", "rb") as f:
            self.dbx.files_upload(f.read(), self.file, mode=dropbox.files.WriteMode('overwrite'))

    def close(self):
        if(self.dbx):
            self.dbx.close()
        if(os.path.isdir(self.path)):
            shutil.rmtree(self.path)

