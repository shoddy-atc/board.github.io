from flask import Flask, request, render_template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# データベース設定
db_uri = os.environ.get('DATABASE_URL', 'sqlite:///test.db')
if db_uri.startswith("postgres://"):
    db_uri = db_uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.Text())
    article = db.Column(db.Text())

@app.route("/")
def bbs():
    text = Article.query.all()
    return render_template("index.html", lines=text)

@app.route("/result", methods=["POST"])
def result():
    date = datetime.now()
    article = request.form["article"]
    name = request.form["name"]
    admin = Article(pub_date=date, name=name, article=article)
    db.session.add(admin)
    db.session.commit()
    return render_template("result.html", article=article, name=name, now=date)

with app.app_context():
    inspector = db.inspect(db.engine)
    if not inspector.has_table("article"):
        db.create_all()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
