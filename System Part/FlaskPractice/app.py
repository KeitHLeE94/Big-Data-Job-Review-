from flask import Flask, render_template, request, redirect, abort
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
#from models import User, Polution, Register
from flask_moment import Moment
from datetime import datetime
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask_googlemaps import GoogleMaps, Map


app = Flask(__name__)


app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '이재현'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECURITY_REGISTERABLE'] = True
# 자동으로 127.0.0.1:5000/register 페이지가 만들어진다.
# 로그아웃: 127.0.0.1:5000/logout으로 이동.
app.config['SECURITY_PASSWORD_SALT'] = '이재현'
app.config['SECURITY_PASSWORD_HASH'] = 'sha512_crypt'
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['GOOGLEMAPS_KEY'] = 'AIzaSyA5pvygq6OIt2iPKryeqnV0i4RkLGtpCgc'


db = SQLAlchemy(app)
admin = Admin(app)
moment = Moment(app)
GoogleMaps(app)


roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))
# 다대다 관계 의미 => 연관된 db도 전부 만들어준다.


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    # 입력받을 사용자 정보는 여기다 추가하면됨.


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


class TestModelView(ModelView):
    can_create = False
    can_edit = False
    can_delete = False
    can_view_details = True


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Role, db.session))
#admin.add_view(ModelView(Register, db.session))
#admin.add_view(ModelView(Polution, db.session))


class MyForm(FlaskForm):
    text = StringField('text1', validators=[DataRequired()])
    # form.html의 form2의 label.
    password = PasswordField('password1')
# flaskform을 인터페이싱해주는 클래스.


class SearchForm(FlaskForm):
    search = StringField('검색', validators=[DataRequired()])


@app.route('/')
def index():
    now = datetime.utcnow()
    # 윗줄 안쓰면 서버시간 기준으로 나옴.
    return render_template('index.html', dt=now)


@app.route('/graph')
@login_required
def graph():
    from data import plotdata
    script, div = plotdata()
    return render_template('graph.html', script=script, div=div)


@app.route('/hws/<name>')
def homeworks(name=None):
    if name == '2':
        dt = datetime(2018, 7, 4)
        return render_template('Exercise#2.html', dt=dt)
    elif name == '3':
        dt = datetime(2018, 7, 5)
        return render_template('Exercise#3.html', dt=dt)
    elif name == '4':
        dt = datetime(2018, 7, 9)
        return render_template('Exercise#4.html', dt=dt)
    elif name == '5':
        dt = datetime(2018, 7, 21)
        return render_template('Exercise#5.html', dt=dt)
    elif name == '6':
        dt = datetime(2018, 7, 23)
        return render_template('Exercise#6.html', dt=dt)


@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['search']
    if search_term == '이재현':
        return render_template('index.html')


@app.route('/sample')
def p_index():
    from pandastohtml import pandas_index
    pandas_index()
    return render_template('a.html')


@app.route('/form', methods=['GET', 'POST'])
# methods: 디폴트값 = GET.
# form이 post이고 methods가 GET이면 에러난다.
def form():
    form = MyForm()
    if request.method == 'GET':
        if form.validate_on_submit():
            return render_template('index.html')
        # 입력이 제대로 됐으면 index.html로 이동.

        # request.args는 dict이기 때문에 get대신 dict 인덱싱으로도 접근 가능.
        # .get 장점: 디폴트값을 줄 수 있다.

        return render_template("form.html", form2=form)
        # input tag에서 입력된 값을 form.html에 전달하여 form.html에서 name이라는 이름으로 사용할 수 있다.
        # 보안형태이므로 csrf 반드시 사용해야 한다.
    else:
        if form.validate_on_submit():
            return render_template('index.html')
        return render_template("index.html", form2=form)


@app.route('/form2', methods=['POST'])
def form2():
    return render_template("form.html")
# post방식만 동작하게 하였으므로 주소 직접 입력해서 넘어오면 에러남.(form 입력만으로만 넘어갈 수 있음)


# @app.before_first_request
# def create_user():
#     db.create_all()
#     user_datastore.create_user(email='wogus4187@naver.com', password='password')
#     db.session.commit()
# # 자동으로 superuser를 생성하기 위한 함수.(초기화에 사용)
# # 자동으로 127.0.0.1:5000/login 페이지가 만들어진다.


@app.route('/map')
def googlemap():
    mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)]
    )
    sndmap = Map(
        identifier="sndmap",
        lat=37.566535,
        lng=126.97796919999996,
        zoom=13,
        markers=[
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                'lat': 37.5132612,
                'lng': 127.10013359999994,
                'infobox': "<b>잠실역</b>"
            },
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                'lat': 37.49794199999999,
                'lng': 127.02762099999995,
                'infobox': "<b>강남역</b>"
            },
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
                'lat': 37.5850193,
                'lng': 127.0263559,
                'infobox': "<b>고려대학교 안암캠퍼스 우정정보관</b>"
            }
        ],
        style=(
            "height:100%;"
            "width:100%;"
            "top:64;"
            "left:0;"
            "position:absolute;"
            "z-index:200;"
        ),
        language='ko',
    )
    sndmap.add_circle(37.5132612, 127.10013359999994, 1000)
    sndmap.add_polygon
    return render_template('map.html', sndmap=sndmap)


if __name__ == '__main__':
    app.run()
