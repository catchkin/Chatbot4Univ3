import sys
sys.path.append('F:\dev\Chatbot4Univ2')

from flask import Flask, render_template

from flask_cors import CORS

# Flask 애플리케이션
app = Flask(__name__)
CORS(app)



@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050)







