import re, chardet
from copyright import show
from files import get_files
from bs4 import BeautifulSoup, BeautifulStoneSoup, Comment
from urllib.parse import urlparse


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

def modify_scripts(soup:BeautifulSoup):
    for s in soup.select('noscript'):
        print('Found noscript tag, removing...')
        s.extract()
    for s in soup.select('script'):
        match s:
            case is_facebook_tag(s):
                print('Found FB pixel\'s tag, removing...')
                s.extract()
                break
            case is_yandex_tag(s):
                print('Found Yandex Metrika\'s tag, removing...')
                s.extract()
                break
            case is_google_tag(s):
                print('Found Google tag, removing...')
                s.extract()
                break
            case is_local_jquery(s.get('src')):
                print(f'Found local JQuery {s.get("src")}, modifying...')
                s['src'] = jquery
                break


def change_offer(soup:BeautifulSoup,s:json):
    currentOffer=input('Current offer name:')
    newOffer=input('New offer name:')

    for form in soup.select('form'):
        for inpt in form.select('input'):
            if not inpt.has_attr('name') or inpt['name'] not in ['name','phone','tel']:
                inpt.extract()
        for inpt in s.inputs:
            newInput=soup.new_tag('input',attrs=inpt)
            form.insert(0,newInput)



show()
files = get_files()

print('What do you want to do?')
print('1.Remove ALL scripts')
print('2.Remove Facebook and Google scripts and change JQuery to CDN')
print('3.Add form inputs and change offer')
menu = input('Enter your choice(s):')

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
            case '3':
                change_offer(soup)

        print('Removing all HTML comments...')
        comments = soup.findAll(text=lambda text:isinstance(text, Comment))
        for comment in comments:
            comment.extract()
        #return all PHP elements to their places
        html = re.sub(php_sig, php_add, soup.prettify(formatter="html"))
    except Exception as e:
        print(f"Error processing file {fname}! Skipping... Error: {e}")
    finally:
        f.close()
    with open(fname,'w',encoding="utf-8") as f:
        f.write(html)

print('All Done! Press any key to exit and... thank you for your support!')
