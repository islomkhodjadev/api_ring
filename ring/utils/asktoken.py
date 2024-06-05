import os
import requests
import json
from dotenv import load_dotenv
from django.conf import settings
from pathlib import Path

settings.configure()

load_dotenv()
def req_token():
    params = {
        'yandexPassportOauthToken': os.getenv("yandexPassportOauthToken")
    }
    url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
    
    try:
        resp = requests.post(url, params=params)
        if resp.status_code != 200:
            raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))
        
        data = resp.json()

        iam_token = data.get('iamToken')
        expires_at = data.get('expiresAt')
        
        if iam_token and expires_at:
             data_to_save = {
        'iamToken': iam_token,
        'expiresAt': expires_at
    }
    
        with open(Path(__file__).resolve().parent/"auth.json", 'w', encoding='utf-8') as file:
            json.dump(data_to_save, file, indent=4)
                
            return 'Successful synthesis'
        

    except Exception as e:
        return str(e)

import time

while True:
    print(req_token())
    time.sleep(28800)
    