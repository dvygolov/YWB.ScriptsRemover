import os,time,re
from bs4 import BeautifulSoup, Doctype

jquery="//ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js" #Change JQuery version if you need
php_sig = '!!!PHP!!!'
php_elements = []
def php_remove(m):
    php_elements.append(m.group())
    return php_sig

def php_add(m):
    return php_elements.pop(0)

def remove_all_scripts(soup):
    for s in soup.select('script','noscript'):
        print('Found script or noscript tag, removing...')
        s.extract()

def modify_scripts(soup):
    for s in soup.select('noscript'):
        print('Found noscript tag, removing...')
        s.extract()
    for s in soup.select('script'):
        if (s.string!=None and ("fbq('init'" in s.string or "fbq('track" in s.string)):
            print('Found FB pixel\'s tag, removing...')
            s.extract()
        elif s.string!=None and "mc.yandex.ru" in s.string:
            print('Found Yandex Metrika\'s tag, removing...')
            s.extract()
        elif (s.string!=None and "gtag('config" in s.string) or (s.get('src')!=None and "googletagmanager" in s.get('src')):
            print('Found Google tag, removing...')
            s.extract()
        elif s.get('src')!=None and "jquery" in s.get('src'):
            print('Found JQuery tag, modifying...')
            s['src']=jquery

print('HTML Scripts Remover ver. 0.2 by Yellow Web')
print('If you like this script, PLEASE DONATE!')
print("WebMoney: Z182653170916")
print("Bitcoin: bc1qqv99jasckntqnk0pkjnrjtpwu0yurm0qd0gnqv")
print("Ethereum: 0xBC118D3FDE78eE393A154C29A4545c575506ad6B")
print()
time.sleep(5)

dir_path = os.path.dirname(os.path.realpath(__file__))
files = []
for root, dirnames, filenames in os.walk(dir_path):
    for filename in filenames:
        if filename.endswith('.html') or filename.endswith('.htm') or filename.endswith('.php'):
            fname = os.path.join(root, filename)
            print('Found file: {}'.format(fname))
            files.append(fname)
if files.count==0:
    print('No HTML/PHP files found! Start script in a directory WITH HTML/PHP files!')
    exit


print('What do you want to do?')
print('1.Remove ALL scripts')
print('2.Remove Facebook and Google scripts and change JQuery to CDN')
print('Enter your choice:',end='')
menu = input()

for fname in files:
    print(f'Processing {fname}...')
    f=open(fname,'r')
    html=f.read()
    # Pre-parse HTML to remove all PHP elements
    html = re.sub(r'<\?.*?\?>', php_remove, html, flags=re.S+re.M)
    soup = BeautifulSoup(html, 'html.parser')
    match menu:
        case '1':
            remove_all_scripts(soup)
        case '2':
            modify_scripts(soup)
    html = re.sub(php_sig, php_add, soup.prettify())
    f.close()
    with open(fname,'w') as f:
        f.write(html)

print('All Done! Press any key to exit and... thank you for your support!')


