from flask import Flask, render_template, request
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account
import requests
import csv
app = Flask(__name__)

chatbot_api_url = 'https://api-url.com/chatbot'

# Load credentials from JSON file
credentials = service_account.Credentials.from_service_account_file('API-KEY.json')

# Authenticate the Translation API client
translate_client = translate.Client(credentials=credentials)

@app.route('/', methods=['GET', 'POST'])
def home():
    data = []
    input_lang = 'en'
    user_input = ''
    if request.method == 'POST':
        user_input = request.form['text-input']

        

        response = requests.post(chatbot_api_url, json={'input': user_input})
        chatbot_response = response.json()['response']
        data.append([user_input, chatbot_response])

        input_lang = translate_client.detect_language(chatbot_response)['language']
        with open('static/data/data.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Inputs', 'Response'])
                for row in data:
                    writer.writerow(row)
        
    else:
        chatbot_response = ''
    if input_lang == 'ur':
        return render_template('index.html', chatbot_response_urd=chatbot_response)
    else:
        return render_template('index.html', chatbot_response=chatbot_response)


if __name__ == '__main__':
    app.run(debug=True, port=8130)

