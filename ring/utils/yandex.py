import time
import requests
from django.conf import settings
from pathlib import Path
import uuid

import os

    
#================================================


import requests
import json


def yandex_tts(text="Sample text"):
    try:
        with open(Path(__file__).resolve().parent/"auth.json", 'r') as file:
            data = json.load(file)
            
        iam_token = data.get("iamToken")
        
        folder_id = 'b1gk37s07uch69snmioo'

        url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
        headers = {'Authorization': 'Bearer ' + iam_token}
        data = {
            'text': text,
            'lang': 'uz-UZ',
            'voice': 'nigora',
            'folderId': folder_id,
            'format': 'mp3'
        }

        with requests.post(url, headers=headers, data=data, stream=True) as resp:
            if resp.status_code != 200:
                raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))
            
            
            return resp.content

    except Exception as e:
        return str(e)




def yandex_stt(audio):
        print(len(audio))
        folder_id = "b1gk37s07uch69snmioo"
        with open(Path(__file__).resolve().parent/"auth.json", 'r') as file:
            data = json.load(file)
            
        iam_token = data.get("iamToken")
        
        
        url = 'https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?topic=general&folderId=b1gk37s07uch69snmioo&lang=uz-UZ'
        params = "&".join([
            "topic=general",
            "folderId=%s" % folder_id,
            "lang=uz-UZ"
        ])
        headers = {'Authorization': 'Bearer %s' % iam_token, 'Content-Type': 'audio/mpeg'}
        try:
            with requests.post(url, params=params, data=audio, headers=headers,stream=True) as resp:
                if resp.status_code != 200:
                    raise RuntimeError(
                        "Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))
                result = json.loads(resp.content).get("result")

                print(result, 'result')
                return result
        except Exception as e:
            print(e)
            return "Error occured"











   
import requests
import json

import requests
import json

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
    
        with open("auth.json", 'w', encoding='utf-8') as file:
            json.dump(data_to_save, file, indent=4)
                
            return 'Successful synthesis'
        

    except Exception as e:
        return str(e)
