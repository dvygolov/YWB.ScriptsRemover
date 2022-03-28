import re, chardet, os
from copyright import show
from files import copy_file, get_currentscript_path, get_files, get_working_path, zip_file
from bs4 import BeautifulSoup, Comment
from urllib.parse import urlparse
from settings import SoftSettings, load_settings
from collections import Counter
from PIL import Image
from pytesseract import pytesseract
from os.path import join
from copy import copy

path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
php_sig = '!!!PHP!!!'
php_elements = []

def php_remove(m):
    php_elements.append(m.group())
    return php_sig

def php_add(m):
    return php_elements.pop(0)

# Pre-parse HTML to remove all PHP elements
def php_save(html:str)->str:
    html = re.sub(r'<\?.*?\?>', php_remove, html, flags=re.S + re.M)
    return html

#return all PHP elements to their places
def php_load(html:str)->str:
    html = re.sub(php_sig, php_add, html)
    return html

def remove_junk(soup:BeautifulSoup)->None:
    print('Removing all HTML comments...')
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    for comment in comments:
        comment.extract()
    print('Removing all meta tags...')
    metatags = soup.select('meta')
    for meta in metatags:
        if 'name' in meta.attrs and meta['name']=='viewport':
            continue
        if 'http-equiv' in meta.attrs:
            continue
        meta.extract()
    base = soup.find('base')
    if base!=None:
        base.extract()

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

def modify_scripts(soup:BeautifulSoup, settings:SoftSettings)->None:
    for s in soup.select('noscript'):
        print('Found noscript tag, removing...')
        s.extract()
    jqueryFound=False
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
            if not jqueryFound:
                print(f'Found local JQuery {s.get("src")}, modifying...')
                fullJqueryPath=join(get_working_path(),s['src'])
                if os.path.isfile(fullJqueryPath):
                    os.remove(fullJqueryPath)
                s['src'] = settings.jquery
                jqueryFound=True
            else:
                print('Removing duplicate JQuery...')
                s.extract()

def choose_vertical()->str:
    verticals=["diet","joints","potency","prostatitis"]
    for i,v in enumerate(verticals):
        print(f'{i+1}. {v}')
    chosen=input('Choose your vertical (Enter if none):')
    return None if not chosen else verticals[int(chosen)-1]

def choose_pp()->str:
    pps=["m1","lucky","leadbit","shakes","kma","lemonad"]
    for i,pp in enumerate(pps):
        print(f'{i+1}. {pp}')
    chosen=input('Choose your program (Enter if none):')
    return None if not chosen else pps[int(chosen)-1]

def change_offer(soup:BeautifulSoup, settings:SoftSettings, encoding:str)->str:
    dirPath=get_working_path()

    htm=soup.find('html')
    if 'data-scrapbook-create' in htm.attrs:
        del htm.attrs['data-scrapbook-create']
    if 'data-scrapbook-source' in htm.attrs:
        del htm.attrs['data-scrapbook-source']
    defaultCountry='ES'
    if 'lang' in htm.attrs:
        defaultCountry=htm['lang'].upper()
    vertical = choose_vertical()
    pp = choose_pp()


    defaultOffer=find_probable_offer(soup)
    currentOffer=input(f'Current offer name (or {defaultOffer} if Enter):') or defaultOffer
    newOffer=input('New offer name (Enter if the same):') or currentOffer
    
    country=input(f'Enter country code (or {defaultCountry} if Enter):') or defaultCountry

    formId='form'
    isModalForm=False
    allForms=soup.select('form')

    if len(allForms)==0:
        isModalForm=True
        print('No forms found! Inserting modal form...')
        head=soup.select_one('head')
        curPath=get_currentscript_path()
        fCssPath=join(curPath,'form','form.css')
        copy_file(fCssPath,dirPath)
        linkTag=soup.new_tag('link',rel='stylesheet',href='form.css')
        head.append(linkTag)
        body = soup.select_one('body')
        with open(join(curPath,'form','form.html'), errors='ignore') as f:
            formHtml = f.read()
        fSoup=BeautifulSoup(formHtml, 'html.parser')
        soup.body.append(copy(fSoup.select_one('body :first-child')))
        allForms=soup.select('form')

    for form in allForms:
        if 'id' in form.attrs:
            print('Found form ID!')
            formId=form['id']
        print('Removing unnecessary inputs...')
        for inpt in form.select('input'):
            if 'name'in inpt.attrs:
                if inpt['name'] not in ['name','phone','tel']:
                    if 'type' in inpt.attrs and inpt['type'] not in ['button','submit']:
                        inpt.extract()
                        continue
                    inpt.extract()
                    continue
                elif( inpt['name'] in ['phone','tel'] and 
                     'placeholder' in inpt.attrs and 
                     re.match('^[\s\d\+]+$',inpt['placeholder'])
                     ):
                    del inpt['placeholder']
                    continue
                else:
                    continue
            if 'type' in inpt.attrs and inpt['type'] not in ['button','submit']:
                inpt.extract()
                continue
            else:
                continue
            inpt.extract()

                
        print('Adding necessary inputs...')
        for inpt in settings.inputs:
            newInput=soup.new_tag('input',attrs=inpt)
            form.insert(0,newInput)
        print('Changing form action...')
        fAction=f'../common/order/{country.lower()}/{newOffer.lower().replace(" ","").replace("-","")}'
        if vertical!=None:
            fAction+=f'_{vertical}'
        if pp!=None:
            fAction+=f'_{pp}'
        fAction+='.php'
        form['action']=fAction

        

    print('Changing product images...')
    for img in soup.findAll('img'):
        if 'scrapbook' in img['src']:
            continue
        if settings.fix_image_path:
            img['src']=img['src'].split('/')[-1]
            if 'onerror' in img.attrs:
                del img['onerror']

        if newOffer==currentOffer:
            continue
        m=re.match(f'product.*(\.png|\.jpg|\.jpeg)|prod\.png|{currentOffer}\.png', img['src'])
        if m!=None:
            imgName=m.group()
            print(f'Found product image: {imgName}')
            img['src']=f'../common/products/{newOffer.lower().replace(" ","").replace("-","")}.png'
        else:
            imgFullPath=join(dirPath,img['src'])
            if not os.path.isfile(imgFullPath) or img['src'].split('.')[-1] not in ['png','jpg','jpeg']:
                continue
            bImage=Image.open(imgFullPath)
            pytesseract.tesseract_cmd=path_to_tesseract
            imgText = pytesseract.image_to_string(bImage)
            if currentOffer.lower() in imgText.lower():
                print(f'Found product image using OCR: {img["src"]}')
                img['src']=f'../common/products/{newOffer.lower().replace(" ","").replace("-","")}.png'
    if settings.remove_webp:
        print('Removind all webp images...')
        for src in soup.select('source', type='image/webp'):
            src.extract()
            if src['srcset'].endswith('.webp'):
                fullSrcPath=join(dirPath,src['srcset'])
                if os.path.isfile(fullSrcPath):
                    os.remove(fullSrcPath)



    for link in soup.findAll('a'):
        if 'onclick' in link.attrs:
            del link['onclick']
        if isModalForm:
            link['onclick']=f'document.getElementById("{formId}").style.display="block";'
        elif 'href' in link.attrs and 'http' in link['href']:
            print('Found link with absolute url, changing...')
            link['href']=f'#{formId}'



    html=soup.prettify()
    print('Replacing offer...')
    html=html.replace(currentOffer, newOffer)
    if ' ' in currentOffer:
        spl=currentOffer.split()
        html=html.replace('&nbsp;'.join(spl),newOffer)
    if '&' in currentOffer:
        spl=currentOffer.split('&')
        html=html.replace('&amp;'.join(spl),newOffer)
    return html

def find_probable_offer(soup:BeautifulSoup)->str:
    texts=soup.findAll(text=True)
    txt=' '.join(t.strip() for t in texts)
    txt= ' '.join(t.strip(',.:?!;') for t in txt.split() if len(t)>4 and re.match('^[A-Za-z&]+$',t))
    c=Counter(txt.split())
    probable,_= c.most_common(1)[0] 
    if probable=='Cannabis':
        probable+=' Oil'
    return probable

def main():
    show()
    s = load_settings()
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
            html=php_save(html)
            soup = BeautifulSoup(html, 'html.parser')
            remove_junk(soup)


            match menu:
                case '1':
                    remove_all_scripts(soup)
                    html=soup.prettify()
                case '2':
                    modify_scripts(soup,s)
                    html=soup.prettify()
                case '3':
                    modify_scripts(soup,s)
                    html=change_offer(soup,s,detection['encoding'])


            html=php_load(html)

        except Exception as e:
            print(f"Error processing file {fname}! Skipping... Error: {e}")
        finally:
            f.close()
        with open(fname,'w',encoding=detection['encoding']) as f:
            f.write(html)

    openAnswer=input("Do you want to open index.htm file in your browser?(Y/N)")
    if openAnswer in ['Y','y'] or not openAnswer:
        import webbrowser
        webbrowser.open('file://'+os.path.realpath(files[0]))

    zipAnswer=input("Do you want to zip all the folder's content?(Y/N)")
    if zipAnswer in ['Y','y'] or not zipAnswer:
        zip_file()
    print('All Done! Press any key to exit and... thank you for your support!')



if __name__ == "__main__":
    main()
