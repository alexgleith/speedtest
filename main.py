from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
import datetime

SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(
    __name__
)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)


class Obs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dt = db.Column(db.DateTime)
    ping = db.Column(db.Integer)
    speed = db.Column(db.Integer)

    def __init__(self, dt, ping, speed):
        self.dt = dt
        self.ping = ping
        self.speed = speed

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'dt': self.dt.strftime("%Y-%m-%d %H:%M:%S"),
            'ping': round(self.ping, 0),
            'speed': round(self.speed/1024/1024, 2)
        }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/data/")
def get_data():
    days = 30
    try:
        days = int(request.args.get('days')) 
    except (TypeError, ValueError):
        # Do nothing
        print("Failed to convert to int")
    from_date = datetime.datetime.today() - datetime.timedelta(days=days)
    data = Obs.query.filter(Obs.dt > from_date).order_by(Obs.dt)

    return jsonify(json_list=[i.serialize for i in data.all()])


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
