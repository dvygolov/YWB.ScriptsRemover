from ntpath import join
import os, sys, shutil
from zipfile import ZipFile
from os.path import dirname,realpath,basename, join


def get_working_path() -> str:
    if len(sys.argv) > 1:
        dirPath = sys.argv[1]
    else:
        dirPath = get_currentscript_path() 
    return dirPath

def get_currentscript_path()->str:
    return dirname(realpath(__file__))

def copy_file(src:str,dst:str)->None:
    shutil.copy(src,dst)

def get_files():
    dirPath = get_working_path()
    print(f"Working directory: {dirPath}")

    if os.path.isdir(join(dirPath,'__macosx')):
        shutil.rmtree(join(dirPath,'__macosx'))

    files = []
    for root, _, filenames in os.walk(dirPath):
        for filename in filenames:
            if (
                "index.html" in filename or
                "index.htm" in filename or
                "index.php" in filename
            ):
                fname = os.path.join(root, filename)
                print("Found file: {}".format(fname))
                files.append(fname)
    if len(files) == 0:
        print(
            "No HTML/PHP files found! Start script in a directory WITH HTML/PHP files!"
        )
        sys.exit()
    else:
        print(f"Found {len(files)} HTML/PHP files!")
        return files


def zip_file():
    dirPath = get_working_path()
    archivePath = join(dirPath, "prelanding.zip")
    if os.path.isfile(archivePath):
        os.remove(archivePath)
    with ZipFile(archivePath, "w") as z:
        for root, dirs, files in os.walk(dirPath):
            for f in files:
                if f=="prelanding.zip": 
                    continue
                z.write(os.path.join(root, f), 
                           os.path.relpath(os.path.join(root, f), 
                                           os.path.join(dirPath, '..')))

    print("Zip file prelanding.zip created!")
