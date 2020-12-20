import os
import shutil
path = "./Cough dataset/Labeled audio"
subfolders = [ f.path for f in os.scandir(path) if f.is_dir() ]

for subfolder in subfolders:
    subfolders2 = [ f.path for f in os.scandir(subfolder) if f.is_dir() ]
    for subfolder2 in subfolders2:
        files = print(os.listdir(subfolder2))
        id = subfolder.split('/')[-1]
        print(subfolder2)
        try:
            src_file = os.path.join(subfolder2,'cough-heavy.wav')
            dest_dir = os.path.join("./DataParsed", id)
            shutil.copy(src_file, dest_dir)
            dst_file = os.path.join(dest_dir,"cough-heavy.wav")
            new_dst_file = os.path.join(dest_dir, str(subfolder2.split('/')[-1])+"-cough-heavy.wav")
            os.rename(dst_file, new_dst_file)
        except:
            print(str(src_file)+" no existe")
        try:
            src_file = os.path.join(subfolder2,'cough-shallow.wav')
            dest_dir = os.path.join("./DataParsed", id)
            shutil.copy(src_file, dest_dir)
            dst_file = os.path.join(dest_dir,"cough-shallow.wav")
            new_dst_file = os.path.join(dest_dir, str(subfolder2.split('/')[-1])+"-cough-shallow.wav")
            os.rename(dst_file, new_dst_file) 
        except:
            print(str(src_file)+" no existe")