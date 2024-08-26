from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    message = "Bitcon is the most valuable currency in the world!"  # ここでメッセージを定義
    return render_template('index.html', message=message)  # messageをテンプレートに渡す

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
