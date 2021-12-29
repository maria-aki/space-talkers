from google.cloud import dialogflow
from flask import Flask, request
import os
from random import randint

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'config.json'

app = Flask(__name__)

session_client = dialogflow.SessionsClient()
project_id = 'fedor-335607'


def ask(text):
    global project_id
    if text != '':
        session = session_client.session_path(project_id,
                                              str(randint(0, 10000)))
        text_input = dialogflow.TextInput(text=text, language_code='ru-RU')
        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(request={
            "session": session,
            "query_input": query_input
        })
        return response.query_result.fulfillment_text
    else:
        return ''


@app.route('/')
def main():
    if request.args.get('text') != None:
      return ask(request.args.get('text'))
    else:
      return ''


app.run(host='0.0.0.0', port=8080)
