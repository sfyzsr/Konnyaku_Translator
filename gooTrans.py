import re

# import urllib2
# import urllib
# mport HTMLParser

import html
import urllib.request
import urllib.parse

agent = {'User-Agent':
         "Mozilla/4.0 (\
compatible;\
MSIE 6.0;\
Windows NT 5.1;\
SV1;\
.NET CLR 1.1.4322;\
.NET CLR 2.0.50727;\
.NET CLR 3.0.04506.30\
)"}


def unescape(text):
    parser = html
    return (parser.unescape(text))


def translate(to_translate, to_language="auto", from_language="auto"):   #auto
    
    base_link = "http://translate.google.com/m?tl=%s&sl=%s&q=%s"

    to_translate = urllib.parse.quote(to_translate)
    link = base_link % (to_language, from_language, to_translate)
    request = urllib.request.Request(link, headers=agent)
    raw_data = urllib.request.urlopen(request).read()
    data = raw_data.decode("utf-8")
    expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
    re_result = re.findall(expr, data)
    if (len(re_result) == 0):
        result = ""
    else:
        result = unescape(re_result[0])
    return (result)


# r= translate("「おはようございます」にはきちんと敬意(尊敬)がありますが",from_language="ja")
# print(translate("「おはようございます」にはきちんと敬意(尊敬)がありますが","zh-CN","ja"))
# print(r)
# print(translate(r,"zh-CN"))