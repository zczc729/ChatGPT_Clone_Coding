import pandas as pd
import requests
import folium
from flask import *
from openai import OpenAI # openai==1.2.0

with open ("api_key.txt", "r", encoding="utf-8") as file:
    my_api_key = file.readline()



# Flask 애플리케이션 설정
app = Flask(__name__)

# Flask 라우팅 설정
@app.route('/')
def index():
    return render_template('gpt.html')

@app.route('/user_input/<user_input>')
def get_answer(user_input):
    client = OpenAI(
    api_key = my_api_key,
    base_url="https://api.upstage.ai/v1/solar"
    )
    stream = client.chat.completions.create(
    model="solar-1-mini-chat",
    messages=[
        {
        "role": "system",
        "content": "You are a helpful assistant."
        },
        {
        "role": "user",
        "content": user_input
        }
    ],
    stream=True,
    )

    ai_response = ''
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
            ai_response += chunk.choices[0].delta.content
    return jsonify({'response': ai_response})


# Flask 애플리케이션 실행
if __name__ == '__main__':
    app.run(debug=True)