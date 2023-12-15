# -*- coding: euc-kr -*-
import urllib
import urllib.parse
import urllib.request


def translate(orig_lang_text, lang):
    
    client_id = "AGmMOuTdIomWk6JrDn19"      # Client ID
    client_secret = "kWD_DB0kbm"            # Client Secret
    
    encText = urllib.parse.quote(orig_lang_text)
    data = "source=" + lang + "&target=es&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    response_body = response.read()
    sub1 = '"translatedText"'
    sub2 = ',"engineType"'
    
    idx1 = (response_body.decode('utf-8')).find(sub1)
    idx2 = (response_body.decode('utf-8')).find(sub2)
    res = response_body[idx1 + len(sub1) + 1: idx2].decode('utf-8')
    new_lang_text = res[1:-1]

    return new_lang_text

# test
# print(translate("Hola", "es"))
print(translate("Hello", "en"))