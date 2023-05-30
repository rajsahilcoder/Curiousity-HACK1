from flask import Flask, render_template, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qna.db'
app.config['SQLALCHEMY_BINDS'] = {'ans': 'sqlite:///ans.db'}
app.config['SQLALCHEMY_BINDS'] = {'upload': 'sqlite:///upload.db'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class QnA(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
# adminapprove create

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


class Answer(db.Model):
    __bind_key__ = 'ans'
    sno = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(200), nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


class FileContents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    data = db.Column(db.LargeBinary)


@app.route('/')
def Home():
    return render_template("index.html")


@app.route('/templates/clubs.html')
def CLub():
    return render_template("clubs.html")


@app.route('/templates/adrenaline_racing.html')
def adrenaline_racing():
    return render_template("adrenaline_racing.html")


@app.route('/templates/blackpearl.html')
def blackpearl():
    return render_template("blackpearl.html")


@app.route('/templates/about.html')
def about():
    return render_template("about.html")


@app.route('/templates/QnA.html', methods=['GET', 'POST'])
def heloqna():
    if request.method == 'POST':

        title = request.form['title']
        desc = request.form['desc']
        qna = QnA(title=title, desc=desc)
        db.session.add(qna)
        db.session.commit()
        return redirect("/templates/QnA.html")
        #boolean -false

    allqna = QnA.query.all()

    return render_template("QnA.html", allqna=allqna)


@app.route('/templates/answer.html', methods=['GET', 'POST'])
def heloans():
    if request.method == 'POST':

        title = request.form['title']
        desc = request.form['desc']
        ans = Answer(title=title, desc=desc)
        db.session.add(ans)
        db.session.commit()
        return redirect("/templates/answer.html")

    allans = Answer.query.all()

    return render_template("answer.html", allans=allans)


@app.route('/templates/AIDS.html')
def aids():
    return render_template("AIDS.html")


@app.route('/templates/mentorship.html')
def mentor():
    return render_template("mentorship.html")


@app.route('/templates/join.html')
def join():
    return render_template("join.html")


@app.route('/templates/guide.html')
def guide():
    return render_template("guide.html")


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['inputFile']
    newFile = FileContents(name=file.filename, data=file.read())
    db.session.add(newFile)
    db.session.commit()

    return 'Saved' + file.filename + 'to the database !!!'


# app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
if __name__ == "__main__":
    app.run(debug=True, port=8300)
