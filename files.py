import os,sys
def get_files():
    if len(sys.argv)>1:
        dir_path=sys.argv[1]
    else:
        dir_path = os.path.dirname(os.path.realpath(__file__))
    print(f"Working directory: {dir_path}")
    files = []
    for root, dirnames, filenames in os.walk(dir_path):
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

