# coding:utf-8

import sys
import os
import json
import requests
import urllib

apikey = os.environ.get("GOOGLE_API_KEY")
TIMEOUT = 30

def stt_google_wav(filename):
    q = {"output": "json", "lang": "ja-JP", "key": apikey}

    url = "http://www.google.com/speech-api/v2/recognize?%s" % (urllib.parse.urlencode(q))

    headers = {"Content-Type": "audio/l16; rate=16000"}
    data = open(filename, "rb").read()

    response = requests.post(
        url,
        headers=headers,
        data=data,
        timeout=TIMEOUT
    )

    jsonunits = response.text.split(os.linesep)
    res = ""

    for unit in jsonunits:
        if not unit:
            continue
        obj = json.loads(unit)
        alternatives = obj["result"]

        if len(alternatives) > 0:
            breakflag = False
            for obj in alternatives:
                results = obj["alternative"]
                for result in results:
                    res = result["transcript"]
                    breakflag = True
                    break

                if breakflag:
                    break

    return res

if __name__ == '__main__':
    print(stt_google_wav(sys.argv[1]))
