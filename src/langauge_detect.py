import json
import urllib.request

def detectLang(text):

    client_id = "JHrkGnHiqgpYUvAlaZbH"
    client_secret = "s4klABFmBY"
    encQuery = urllib.parse.quote(text)
    data = "query=" + encQuery
    url = "https://openapi.naver.com/v1/papago/detectLangs"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        return json.loads(response_body.decode('utf-8'))["langCode"]
    else:
        print("Error Code:" + rescode)

