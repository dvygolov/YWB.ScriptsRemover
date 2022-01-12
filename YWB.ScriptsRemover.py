import sys, os, time, re, chardet
from bs4 import BeautifulSoup, Comment
from urllib.parse import urlparse

jquery = "//ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js" #Change JQuery version if you need

php_sig = '!!!PHP!!!'
php_elements = []
def php_remove(m):
    php_elements.append(m.group())
    return php_sig

def php_add(m):
    return php_elements.pop(0)

def remove_all_scripts(soup):
    for s in soup.select('script'):
        print('Found script tag, removing...')
        s.extract()
    for s in soup.select('noscript'):
        print('Found noscript tag, removing...')
        s.extract()

def is_local_jquery(str):
    if str == None:
       return False
    if bool(urlparse(str).netloc):
        return False
    if str.endswith('jquery.js') or str.endswith('jquery.min.js'):
        return True
    return False

def is_google_tag(tag):
    if tag.string== None:
        return False
    if "gtag('config" in tag.string:
        return True
    if "googletagmanager" in tag.string:
        return True
    if tag.get('src') == None:
        return False
    if "googletagmanager" in tag.get('src'):
        return True

def is_facebook_tag(tag):
    if tag.string==None:
        return False
    if "fbq('init'" in tag.string or "fbq('track" in tag.string:
        return True

def is_yandex_tag(tag):
    if tag.string==None:
        return False
    if "mc.yandex.ru" in tag.string:
        return True

def modify_scripts(soup):
    for s in soup.select('noscript'):
        print('Found noscript tag, removing...')
        s.extract()
    googlemeta = soup.find_all("meta", attrs={"name":"google-site-verification"})
    for tag in googlemeta:
        print('Found google meta tag, removing...')
        tag.extract()
    for s in soup.select('script'):
        if is_facebook_tag(s):
            print('Found FB pixel\'s tag, removing...')
            s.extract()
        elif is_yandex_tag(s):
            print('Found Yandex Metrika\'s tag, removing...')
            s.extract()
        elif is_google_tag(s):
            print('Found Google tag, removing...')
            s.extract()
        elif is_local_jquery(s.get('src')):
            print(f'Found local JQuery {s.get("src")}, modifying...')
            s['src'] = jquery
            
print()
print('                      HTML Scripts Remover v.0.6 ')
print('   _            __     __  _ _             __          __  _     ')
print('  | |           \ \   / / | | |            \ \        / / | |    ')
print('  | |__  _   _   \ \_/ /__| | | _____      _\ \  /\  / /__| |__  ')
print("  | '_ \| | | |   \   / _ \ | |/ _ \ \ /\ / /\ \/  \/ / _ \ '_ \ ")
print('  | |_) | |_| |    | |  __/ | | (_) \ V  V /  \  /\  /  __/ |_) |')
print('  |_.__/ \__, |    |_|\___|_|_|\___/ \_/\_/    \/  \/ \___|_.__/ ')
print('          __/ |                                                  ')
print('         |___/             https://yellowweb.top                 ')
print()
print('If you like this script, PLEASE DONATE!')
print('WebMoney: Z182653170916')
print('Bitcoin: bc1qqv99jasckntqnk0pkjnrjtpwu0yurm0qd0gnqv')
print('Ethereum: 0xBC118D3FDE78eE393A154C29A4545c575506ad6B')
print()
time.sleep(3)

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


print('What do you want to do?')
print('1.Remove ALL scripts')
print('2.Remove Facebook and Google scripts and change JQuery to CDN')
print('Enter your choice: ',end='')
menu = input()

for fname in files:
    print(f'Processing {fname}...')
    try:
        with open(fname, 'rb') as detect_file_encoding:
            detection = chardet.detect(detect_file_encoding.read())
        print('Detected encoding:', detection)
        with open(fname, encoding=detection['encoding'],errors='ignore') as f:
            html = f.read()
        # Pre-parse HTML to remove all PHP elements
        html = re.sub(r'<\?.*?\?>', php_remove, html, flags=re.S + re.M)
        soup = BeautifulSoup(html, 'html.parser')
        match menu:
            case '1':
                remove_all_scripts(soup)
            case '2':
                modify_scripts(soup)
                
        print('Removing all HTML comments...')
        comments = soup.findAll(text=lambda text:isinstance(text, Comment))
        for comment in comments:
            comment.extract()
        html = re.sub(php_sig, php_add, soup.prettify(formatter="html"))
    except Exception as e:
        print(f"Error processing file {fname}!{e} Skipping...")
    finally:
        f.close()
    with open(fname,'w',encoding="utf-8") as f:
        f.write(html)

print('All Done! Press any key to exit and... thank you for your support!')


