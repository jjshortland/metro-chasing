import requests
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='.env')
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')

payload = {
    'client_id': client_id,
    'client_secret': client_secret,
    'code': '53db25c4e570ec55240882516b1d66116a9230ab',
    'grant_type': 'authorization_code'
}

res = requests.post("https://www.strava.com/oauth/token", data=payload)
res.raise_for_status()

print(res.json())