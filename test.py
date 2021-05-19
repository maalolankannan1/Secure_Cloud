import subprocess
outp = subprocess.Popen(". ~/venv1/bin/activate; python3 gdrive_upload_folder_with_subfolders.py",shell=True,stdout = subprocess.PIPE)
subproc_return = outp.stdout.read()
out_str = str(subproc_return)
print(out_str)
#subprocess.Popen("deactivate",shell=True,stdout = subprocess.PIPE)
