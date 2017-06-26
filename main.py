from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

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
            'ping': self.ping,
            'speed': self.speed
        }


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data/")
def get_data():
    data = Obs.query.order_by(Obs.dt)

    return jsonify(json_list=[i.serialize for i in data.all()])


if __name__ == "__main__":
    app.run(debug=True)
