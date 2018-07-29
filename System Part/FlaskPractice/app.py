from flask import Flask, render_template, request, redirect, abort
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import User, Polution, Register


app = Flask(__name__)
app.config.update({'SECRET_KEY': '이재현'})
app.config['SQLALCHEMY_DATABASE_URI'] = ['sqlite:///test.db', 'sqlite:///air.db']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


db = SQLAlchemy(app)
admin = Admin(app)


class TestModelView(ModelView):
    can_create = False
    can_edit = False
    can_delete = False
    can_view_details = True


admin.add_view(TestModelView(User, db.session))
admin.add_view(ModelView(Register, db.session))
admin.add_view(ModelView(Polution, db.session))


class MyForm(FlaskForm):
    text = StringField('text1', validators=[DataRequired()])
    # form.html의 form2의 label.
    password = PasswordField('password1')
# flaskform을 인터페이싱해주는 클래스.


class SearchForm(FlaskForm):
    search = StringField('검색', validators=[DataRequired()])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/graph')
def graph():
    from data import plotdata
    script, div = plotdata()
    return render_template('graph.html', script=script, div=div)


@app.route('/hws/<name>')
def homeworks(name=None):
    if name == '2':
        return render_template('Exercise#2.html')
    elif name == '3':
        return render_template('Exercise#3.html')
    elif name == '4':
        return render_template('Exercise#4.html')
    elif name == '5':
        return render_template('Exercise#5.html')
    elif name == '6':
        return render_template('Exercise#6.html')


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


if __name__ == '__main__':
    app.run()
