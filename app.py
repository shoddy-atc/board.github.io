from flask import Flask, request, render_template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# データベース設定
db_uri = os.environ.get('DATABASE_URL', 'sqlite:///test.db')
if db_uri.startswith("postgres://"):
    db_uri = db_uri.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    threadname = db.Column(db.String(80), unique=True)
    articles = db.relationship('Article', backref='thread', lazy=True)

    def __init__(self, threadname, articles=[]):
        self.threadname = threadname
        self.articles = articles

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.String(80))
    article = db.Column(db.Text())
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)

    def __init__(self, pub_date, name, article, thread_id):
        self.pub_date = pub_date
        self.name = name
        self.article = article
        self.thread_id = thread_id

@app.route("/")
def main():
    threads = Thread.query.all()
    return render_template("index.html", threads=threads)

@app.route("/thread", methods=["POST"])
def thread():
    thread_get = request.form["thread"]
    thread = Thread.query.filter_by(threadname=thread_get).first()
    if not thread:
        thread = Thread(thread_get)
        db.session.add(thread)
        db.session.commit()
    articles = Article.query.filter_by(thread_id=thread.id).all()
    return render_template("thread.html", articles=articles, thread=thread_get)

@app.route("/result", methods=["POST"])
def result():
    date = datetime.now()
    article = request.form["article"]
    name = request.form["name"]
    thread_name = request.form["thread"]
    thread = Thread.query.filter_by(threadname=thread_name).first()
    admin = Article(pub_date=date, name=name, article=article, thread_id=thread.id)
    db.session.add(admin)
    db.session.commit()
    return render_template("result.html", article=article, name=name, now=date)

def init_db():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
