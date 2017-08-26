import re
import tempfile
import urllib.request
import urllib.parse
from lxml import etree
import PIL.Image
import discord

def get_embed_reply(text):
    match = re.search(r"xkcd\.com/(\d+)", text)
    if match:
        return xkcd_embed(match.group(1))
    return None, None, None

def xkcd_embed(comic_id):
    try:
        webpage = urllib.request.urlopen('https://xkcd.com/' + str(comic_id))
        image_url, title_text, title = xkcd_extract(webpage.read().decode())
        return discord.Embed().set_image(url = image_url), title_text, title
    except:
        return None, None, None
    
def xkcd_extract(html):
    root = etree.HTML(html)
    url = root.xpath("//div[@id='comic']//img/@src")[0]
    title_text = root.xpath("//div[@id='comic']//img/@title")[0]
    title = root.xpath("//div[@id='ctitle']//text()")[0]
    if not url.startswith('http'):
        url = 'https:' + url
    return url, title_text, title

def get_tex_image(texcode):
    request = urllib.request.urlopen('http://www.tlhiv.org/ltxpreview/ltxpreview.cgi', ('width=872&height=672&ltx=&ltxsource=$' + urllib.parse.quote_plus(texcode) + '$&result=pnghq&int=0').encode('utf-8'))
    t1 = tempfile.NamedTemporaryFile()
    t1.write(request.read())
    t1.seek(0)
    if t1.read(8) != b'\x89PNG\r\n\x1a\n':
        t1.close()
        return None
    t1.seek(0)
    im = PIL.Image.open(t1)
    background = PIL.Image.new('RGBA', im.size, (255, 255, 255, 255))
    comp = PIL.Image.alpha_composite(background, im.convert('RGBA'))
    t2 = tempfile.NamedTemporaryFile(delete=False)
    comp.save(t2, 'PNG')
    t2.close()
    return t2.name
