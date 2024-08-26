import os
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# データベース設定
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///test.db')
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# モデル定義（変更なし）
class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    threadname = db.Column(db.String(80), unique=True)
    articles = db.relationship('Article', backref='thread', lazy=True)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.String(80))
    article = db.Column(db.Text())
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)

# データベース初期化関数
def init_db():
    with app.app_context():
        db.create_all()

# ルートの実装（変更なし）
@app.route("/")
def main():
    threads = Thread.query.all()
    return render_template("index.html", threads=threads)

@app.route("/thread", methods=["POST"])
def thread():
    thread_get = request.form["thread"]
    thread = Thread.query.filter_by(threadname=thread_get).first()
    if not thread:
        thread = Thread(threadname=thread_get)
        db.session.add(thread)
        db.session.commit()
    articles = Article.query.filter_by(thread_id=thread.id).all()
    return render_template("thread.html", articles=articles, thread=thread_get)

@app.route("/", methods=['GET', 'POST'])
def result():
    date = datetime.now()
    article = request.form["article"]
    name = request.form["name"]
    thread_name = request.form["thread"]
    thread = Thread.query.filter_by(threadname=thread_name).first()
    new_article = Article(pub_date=date, name=name, article=article, thread_id=thread.id)
    db.session.add(new_article)
    db.session.commit()
    return render_template("result.html", article=article, name=name, now=date)

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
else:
    init_db()
