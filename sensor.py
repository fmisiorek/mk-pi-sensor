import RPi.GPIO as GPIO
import json
import requests
from time import sleep
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# set GPIO to read data from sensor
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# open connection to server
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

url = 'https://mk-kaffee.azurewebsites.net/automat'
send = False
last = -1
id = 8083

while True:
    print(' '+str(GPIO.input(25) != last)+' '+str(GPIO.input(25))+' '+str(last))
    if GPIO.input(25) != last:
        last = GPIO.input(25)
        print(last)
        if send == False:
            send = True
            payload = {'state': last, 'id': id}
            print('sending...')
            try:
                httpresponse = session.post(url, data=json.dumps(payload))
                continue
            except requests.ConnectionError as exc:
                print(exc)
                continue
            except:
                print('it is bad...')
                continue
    print('send set to false')
    send = False
    print(httpresponse)
    print(httpresponse.text)
    sleep(10)
