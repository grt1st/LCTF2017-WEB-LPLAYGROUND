import re
from lxml import etree

def get_html_content(text):
    try:
        html = etree.HTML(text)
        title = html.xpath("//title")[0].text
        content = text
    except Exception as e:
        title = None
        content = None

    return title, content