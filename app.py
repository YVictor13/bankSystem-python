from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost:3306/banksystem?charset=utf8'
app.config["SECRET_KEY"] = "12345678"
db = SQLAlchemy(app)


# 用户类
class Card(db.Model):
    """银行卡表"""
    __tablename__ = "Card"
    CardId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    money = db.Column(db.String(20), default=0)
    accountId = db.Column(db.String(64), db.ForeignKey("User.accountId"))  # 外键字段


class User(db.Model):
    """用户表"""
    __tablename__ = "User"  # 指明数据库表名
    id = db.Column(db.Integer, primary_key=True)  # 主键 整型的主键默认设置为自增
    accountId = db.Column(db.String(64), unique=True)  # 唯一性
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    Card = db.relationship("Card", backref="User")


class UserFrom(FlaskForm):
    """用户表单数据验证"""
    accountId = StringField(label='用户账号', validators=[DataRequired('请输入用户账号')],
                            description='请输入用户账号', render_kw={'required': 'required', 'class': 'form-control'})
    email = EmailField(label='用户邮箱', validators=[DataRequired('请输入用户邮箱')],
                       description='请输入用户邮箱', render_kw={'required': 'required', 'class': 'form-control'})
    password = PasswordField(label='用户密码', validators=[DataRequired('请输入正确的秘密')],
                             description='请输入密码邮箱', render_kw={'required': 'required', 'class': 'form-control'})
    submit = SubmitField('提交')


# 创建数据表
# # 使用drop_all清除数据库中的所有数据
# db.drop_all()
# # 创建所有的表
# db.create_all()


# 登录界面
@app.route('/')
def login():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('404.html')


# 验证登录
@app.route('/login', methods=['POST'])
def do_admin_login():
    password = request.form['password']
    accountId = request.form['accountId']
    obj = User.query.filter_by(accountId=accountId).first()
    if obj and password == obj.password:
        session['logged_in'] = True
        return index()
    else:
        flash('wrong password!')
        return login()



@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def do_register():
    password = request.form['password']
    accountId = request.form['accountId']
    email = request.form['email']
    user_obj = User(
        accountId=accountId,
        password=password,
        email=email
    )
    try:
        db.session.add(user_obj)
        db.session.commit()
        flash('注册成功')
        return login()
    except:
        flash('注册失败')
        return register()


@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/index', methods=['POST'])
def update_index():
    CardId = request.form['CardId']
    password = request.form['password']
    accountId = request.form['accountId']
    email = request.form['email']
    Card_obj = Card(
        password=password,
        accountId=accountId,
        email=email,
        CardId=CardId
    )
    try:
        db.session.add(Card_obj)
        db.session.commit()
        flash('用户账号有误，请核实再输入')
        return home()
    except:
        return index()


@app.route('/login', methods=['GET'])
def quite():
    session['logged_in'] = False
    return login()


if __name__ == '__main__':
    app.run(debug=True)
