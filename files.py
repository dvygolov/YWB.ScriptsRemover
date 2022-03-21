from ntpath import join
import os, sys
from zipfile import ZipFile
from os.path import dirname,realpath,basename, join


def get_working_path() -> str:
    if len(sys.argv) > 1:
        dirPath = sys.argv[1]
    else:
        dirPath = dirname(realpath(__file__))
    return dirPath


def get_files():
    dirPath = get_working_path()
    print(f"Working directory: {dirPath}")

    if os.path.isdir(join(dirPath,'__macosx')):
        import shutil
        shutil.rmtree(join(dirPath,'__macosx'))

    files = []
    for root, dirnames, filenames in os.walk(dirPath):
        for filename in filenames:
            if (
                filename.endswith(".html")
                or filename.endswith(".htm")
                or filename.endswith(".php")
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
    with ZipFile(archivePath, "w") as zipObj:
        for folderName, subfolders, filenames in os.walk(dirPath):
            for filename in filenames:
                if filename == "prelanding.zip":
                    continue
                filePath = join(folderName, filename)
                zipObj.write(filePath, basename(filePath))
                os.remove(filePath)

    print("Zip file prelanding.zip created!")
