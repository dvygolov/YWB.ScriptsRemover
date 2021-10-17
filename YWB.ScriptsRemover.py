import os 
from bs4 import BeautifulSoup, Doctype
dir_path = os.path.dirname(os.path.realpath(__file__))
files=[]
for root, dirnames, filenames in os.walk(dir_path):
    for filename in filenames:
        if filename.endswith('.html'):
            fname = os.path.join(root, filename)
            print('Found file: {}'.format(fname))
            files.append(fname)

print('What do you want to do?')
print('1.Remove ALL scripts')
print('2.Remove Facebook and Google scripts and change JQuery to CDN')
print('Enter your choice:',end='')
menu=input()

if menu=='1':
    print(menu)
elif menu=='2':
    print(menu)

