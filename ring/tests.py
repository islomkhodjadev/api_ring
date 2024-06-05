# from django.test import TestCase

# Create your tests here.


import requests


response = requests.get(url="http://127.0.0.1:8000/api/v1/voice/", data=
    {
    "request": "You are google assistant",
    "assistant": "Alice"
})