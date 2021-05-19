# -*- coding: utf-8 -*-

"""
Snippet based on pydrive allowing to upload full folders to Google Drive, replicating the same subfolders hierarchy.
Settings are set in the yaml files; don't forget to generate google api credentials and to put the client_secrets.json in the folder.

You should get first the id of the parent folder (the gdrive folder where you want to copy your folders), which is the
end of its url.

If the destination folder does not exist, it will be created.
"""

# Enable Python3 compatibility
from __future__ import (unicode_literals, absolute_import, print_function,
                        division)

# Import general libraries
from argparse import ArgumentParser
import os
from sys import exit
import ast
import yaml

# Import Google libraries
from pydrive.auth import GoogleAuth, ServiceAccountCredentials
from pydrive.drive import GoogleDrive
from pydrive.files import GoogleDriveFileList
import googleapiclient.errors

def authenticate():
    """
    Authenticate to Google API
    """

    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    return GoogleDrive(gauth)


def get_folder_id(drive, parent_folder_id, folder_name):
    """
    Check if destination folder exists and return it's ID
    :param drive: An instance of GoogleAuth
    :param parent_folder_id: the id of the parent of the folder we are uploading the files to
    :param folder_name: the name of the folder in the drive
    """

    # Auto-iterate through all files in the parent folder.
    file_list = GoogleDriveFileList()

    try:
        file_list = drive.ListFile(
            {'q': "'{0}' in parents and trashed=false".format(parent_folder_id)}
                                  ).GetList()
    # Exit if the parent folder doesn't exist
    except googleapiclient.errors.HttpError as err:
        # Parse error message
        message = ast.literal_eval(err.content)['error']['message']
        if message == 'File not found: ':
            print(message + folder_name)
            exit(1)
        # Exit with stacktrace in case of other error
        else:
            raise

    # Find the the destination folder in the parent folder's files
    for file in file_list:
        if file['title'] == folder_name:
            print('title: %s, id: %s' % (file['title'], file['id']))
            return file['id']


def create_folder(drive, folder_name, parent_folder_id):
    """
    Create folder on Google Drive
    :param drive: An instance of GoogleAuth
    :param folder_id: the id of the folder we are uploading the files to
    :param parent_folder_id: the id of the parent of the folder we are uploading the files to
    """
    folder_metadata = {
        'title': folder_name,
        # Define the file type as folder
        'mimeType': 'application/vnd.google-apps.folder',
        # ID of the parent folder
        'parents': [{'id':parent_folder_id}]
    }

    folder = drive.CreateFile(folder_metadata)
    folder.Upload()

    # Return folder informations
    print('title: %s, id: %s' % (folder['title'], folder['id']))
    return folder['id']


def upload_files_in_folder(drive, folder_id, src_folder_name):
    """
    Recursively upload files from a folder and its subfolders to Google Drive
    :param drive: An instance of GoogleAuth
    :param folder_id: the id of the folder we are uploading the files to
    :param src_folder_name: the path to the source folder to upload
    """
    print("\n Folder:", src_folder_name)

    # Iterate through all files in the folder.
    for object_name in os.listdir(src_folder_name):
        filepath = src_folder_name+'/'+object_name

        # Check the file's size
        statinfo = os.stat(filepath)
        if statinfo.st_size > 0:
            # Upload file to folder.
            f = drive.CreateFile(
                {"parents": [{'id':folder_id}],
                'title': object_name}
                )
            if os.path.isdir(filepath):

                child_folder_id = get_folder_id(drive, folder_id, object_name)

                # Create the folder if it doesn't exists
                if not child_folder_id:
                    child_folder_id = create_folder(drive, object_name, folder_id)
                else:
                    print('folder {0} already exists'.format(object_name))

                upload_files_in_folder(drive, child_folder_id, filepath)
            else:
                print('Uploading file: ', object_name)
                f.SetContentFile(filepath)
                f.Upload()

        # Skip the file if it's empty
        else:
            print('file {0} is empty'.format(file))
    print("DONE UPLOADING")


def main():
    """
    Main
    """
    #args = parse_args()

    src_folder_names = ["raw_data","encrypted"] #args.source
    dst_folder_names = ["raw_data","encrypted"] #args.destination
    parent_folder_id = "1t5fMTq0z8xEhYlaHCj4Sa2utpjCburDu" #args.parent_id
    # print("Running with parameters: source = " + src_folder_names[0]+" destination = "+dst_folder_names[i]+"  parent_id = "+parent_folder_id)

    # Authenticate to Google API
    drive = authenticate()

    for i in range(2):
        folder_id = get_folder_id(drive, parent_folder_id, dst_folder_names[i])

        # Create the folder if it doesn't exists
        if not folder_id:
            folder_id = create_folder(drive, dst_folder_names[i], parent_folder_id)
            print("Folder id is "+folder_id)
        else:
            print('folder {0} already exists'.format(dst_folder_names[i]))

        # Upload the files
        upload_files_in_folder(drive, folder_id, src_folder_names[i])

if __name__ == "__main__":
    main()
