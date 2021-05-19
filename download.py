from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import GoogleDriveFileList
import os

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)
parent_folder_id = "1t5fMTq0z8xEhYlaHCj4Sa2utpjCburDu"
file_list = GoogleDriveFileList()
file_list = drive.ListFile({'q': "'{0}' in parents and trashed=false".format(parent_folder_id)}).GetList()
cwd = os.getcwd()
for file in file_list:
	print(file['title']+" with ID: "+file['id'])
	os.chdir(cwd)
	os.mkdir(file['title'])
	os.chdir(file['title'])
	file_list1 = drive.ListFile({'q': "'{0}' in parents and trashed=false".format(file['id'])}).GetList()
	for fl in file_list1:
		print(fl['title'])
		file6 = drive.CreateFile({'id': fl['id']})
		file6.GetContentFile(fl['title'])
