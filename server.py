from flask import Flask, request, Response
from datetime import datetime as dt
import time
import requests
app = Flask(__name__)
SERVER_NAME = 'Server of Mo'
# db = [{'author': 'Bill', 'time': time.time(), 'text': 'Some random text'},
#       {'author': 'Bill', 'time': time.time(), 'text': 'Some random text'}]
db = []
authors = set()

@app.route('/')
def hello_world():
    return "Hello, World!<br><a href='/status'>STATUS</a>"


@app.route('/status')
def status():
    time_now = (dt.now()).strftime('%Y.%m.%d %H:%M:%S')
    return {'server_name': SERVER_NAME, 'status': True, 'time':time_now, 'authors': len(authors)}


@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    if not isinstance(data, dict):
        return Response('not json', 400)
    text = data['text']
    author = data['author']
    authors.add(author)
    time_now = (dt.now()).strftime('%Y/%m/%d %H:%M:%S')
    if isinstance(text, str) and isinstance(author, str):
        db.append({'author': author, 'time': time.time(), 'text': text})
        if 'weather?' in text:
            response = requests.request('GET', 'http://wttr.in', params={'format': 2, 'M': ''})
            db.append({'author': 'AI', 'time': time.time(), 'text': response.text.rstrip()})
        return Response('Ok')
    else:
        return Response('NOT Ok',400)


@app.route('/get_messages')
def get_messages():
    after = request.args.get('after', '0')
    try:
        after = float(after)
    except:
        return Response('wrong format', 400)
    new_messages = [m for m in db if float(m['time']) > after]
    return {'messages': new_messages}



app.run()
