# Secure Storage On Google Drive Using Hybrid Cryptography

# Methodology

1. Load the file on the server.</br>
2. Dividing the uploaded file into N parts.</br>
3. Encrypting all the parts of the file using any one of the selected algorithms (Algorithm is changed with every part in round robin fashion).</br>
4. The keys for cryptography algorithms is then secured using a different algorithm and the key for this algorithm is provided to the user as public key.</br>

After the above 4 steps you will have a N files which are in encrypted form which are stored on the server and a key which is downloaded as public key for decrypting the file and downloading it.</br>

To restore the file, follow the following steps:</br>
1. Load the key on the server.</br>
2. Decrypt the keys of the algorithms.</br>
3. Decrypt all the N parts of the file using the same algorithms which were used to encrypt them.</br>
4. Combine all the N parts to form the original file and provide it to the user for downloading.</br>

# How to Run

**NOTE:** The project is based on Python 2.7.15 plateform running it on any other plateform might create some issues.</br>
Create a python3 virtual environment to run the file that helps in uploading and downloading file from the google drive.

Step 1: Install Requirements</br>
`pip install -r requirements.txt`</br>

Step 2: Run the application</br>
`python app.py`</br>

Step 3: Visit the localhost from your browser</br>

Step 4: Enjoy :)


