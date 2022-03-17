import os,sys
from zipfile import ZipFile
from os.path import basename

def get_files():
    if len(sys.argv)>1:
        dirPath=sys.argv[1]
    else:
        dirPath = os.path.dirname(os.path.realpath(__file__))
    print(f"Working directory: {dirPath}")
    files = []
    for root, dirnames, filenames in os.walk(dirPath):
        for filename in filenames:
            if filename.endswith('.html') or filename.endswith('.htm') or filename.endswith('.php'):
                fname = os.path.join(root, filename)
                print('Found file: {}'.format(fname))
                files.append(fname)
    if len(files)== 0:
        print('No HTML/PHP files found! Start script in a directory WITH HTML/PHP files!')
        sys.exit()
    else:
        print(f"Found {len(files)} HTML/PHP files!")
        return files

def zip_file():
    if len(sys.argv)>1:
        dirPath=sys.argv[1]
    else:
        dirPath = os.path.dirname(os.path.realpath(__file__))
    archivePath=os.path.join(dirPath,'prelanding.zip')
    with ZipFile(archivePath, 'w') as zipObj:
       for folderName, subfolders, filenames in os.walk(dirPath):
           for filename in filenames:
               if filename=='prelanding.zip':
                   continue
               filePath = os.path.join(folderName, filename)
               zipObj.write(filePath, basename(filePath))
               os.remove(filePath)

    print('Zip file prelanding.zip created!')

