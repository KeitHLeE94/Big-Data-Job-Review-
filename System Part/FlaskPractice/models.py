# coding: utf-8
from sqlalchemy import Column, Text
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Polution(db.Model):
    __tablename__ = 'Polution'

    Datatime = db.Column(db.Text, primary_key=True)
    so2Value = db.Column(db.Text)
    coValue = db.Column(db.Text)
    o3Value = db.Column(db.Text)
    no2Value = db.Column(db.Text)
    pm10Value = db.Column(db.Text)
    pm10Value24 = db.Column(db.Text)
    pm25Value = db.Column(db.Text)
    pm25Value24 = db.Column(db.Text)
    khaiValue = db.Column(db.Text)
    khaiGrade = db.Column(db.Text)
    so2Grade = db.Column(db.Text)
    coGrade = db.Column(db.Text)
    o3Grade = db.Column(db.Text)
    no2Grade = db.Column(db.Text)
    pm10Grade = db.Column(db.Text)
    pm25Grade = db.Column(db.Text)
    pm10Grade1h = db.Column(db.Text)
    pm25Grade1h = db.Column(db.Text)


class Register(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    pw = db.Column(db.String(120), nullable=False)
    pnum = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username





# 터미널 -> flask-sqlacodegen 'sqlite:///air.db' --flask > models.py 입력하면 자동으로 생성된다.