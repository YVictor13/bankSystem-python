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


# 银行卡类
class Card(db.Model):
    """银行卡表"""
    __tablename__ = "Card"
    CardId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    money = db.Column(db.String(20), default=0)
    accountId = db.Column(db.String(64), db.ForeignKey("User.accountId"))  # 外键字段
    Transfer = db.relationship("Transfer", backref="Card", primaryjoin='Card.CardId == Transfer.my_CardId')
    Deposit = db.relationship("Deposit", backref="Card")


# 用户类
class User(db.Model):
    """用户表"""
    __tablename__ = "User"  # 指明数据库表名
    id = db.Column(db.Integer, primary_key=True)  # 主键 整型的主键默认设置为自增
    accountId = db.Column(db.String(64), unique=True)  # 唯一性
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    Card = db.relationship("Card", backref="User")


class Transfer(db.Model):
    """转账表"""
    __tablename__ = "Transfer"  # 指明数据库表名
    id = db.Column(db.Integer, primary_key=True)  # 主键 整型的主键默认设置为自增
    my_CardId = db.Column(db.Integer, db.ForeignKey("Card.CardId"))  # 外键字段
    other_CardId = db.Column(db.Integer, db.ForeignKey("Card.CardId"))  # 外键字段
    datetime = db.Column(db.DateTime, nullable=False)
    money = db.Column(db.String(64), nullable=False)


class Deposit(db.Model):
    """存款表"""
    __tablename__ = "Deposit"
    id = db.Column(db.Integer, primary_key=True)  # 主键 整型的主键默认设置为自增
    CardId = db.Column(db.Integer, db.ForeignKey("Card.CardId"))  # 外键字段
    datetime = db.Column(db.DateTime, nullable=False)
    money = db.Column(db.String(64), nullable=False)


class UserFrom(FlaskForm):
    """用户表单数据验证"""
    accountId = StringField(label='用户账号', validators=[DataRequired('请输入用户账号')],
                            description='请输入用户账号', render_kw={'required': 'required', 'class': 'form-control'})
    email = EmailField(label='用户邮箱', validators=[DataRequired('请输入用户邮箱')],
                       description='请输入用户邮箱', render_kw={'required': 'required', 'class': 'form-control'})
    password = PasswordField(label='用户密码', validators=[DataRequired('请输入正确的秘密')],
                             description='请输入密码邮箱', render_kw={'required': 'required', 'class': 'form-control'})
    submit = SubmitField('提交')


# # 创建数据表
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
    User_obj = User.query.filter_by(accountId=accountId).first()
    Card_obj = Card.query.filter_by(accountId=accountId).first()
    if Card_obj:
        session['information_ok'] = True

    if User_obj and password == User_obj.password:
        session['accountId'] = accountId
        session['logged_in'] = True
        if session.get('information_ok'):
            session['login_ok'] = True
            return redirect('/home')
        else:
            return redirect('/index')
    else:
        flash('wrong password!')
        return login()


# 注册
@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')


# 完成注册
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
        return redirect('/login')
    except:
        flash('注册失败')
        return register()


# 完善信息
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


# 实现完善信息功能
@app.route('/index', methods=['POST'])
def update_index():
    CardId = request.form['CardId']
    password = request.form['password']
    accountId = request.form['accountId']
    name = request.form['name']
    Card_obj = Card(
        password=password,
        accountId=accountId,
        name=name,
        CardId=CardId
    )

    Card_one_obj = Card.query.filter_by(CardId=CardId).first()
    if Card_one_obj:
        flash('此银行卡已被绑定，请核实再输入')
        return index()
    else:
        try:
            db.session.add(Card_obj)
            db.session.commit()
            session['login_ok'] = True
            return redirect('/home')
        except:
            flash('用户账号有误，请核实再输入')
            return index()


# 退出功能
@app.route('/login', methods=['GET'])
def quite():
    session['logged_in'] = False
    session['login_ok'] = False
    session['information_ok'] = False
    session['accountId'] = ''
    return login()


# 银行首页
@app.route('/home', methods=['GET'])
def home():
    if session.get('login_ok'):
        return render_template('home.html')
    else:
        return render_template('404.html')


@app.route('/home/mine')
def mine():
    accountId = session.get('accountId')
    User_obj = User.query.filter_by(accountId=accountId).first()
    Card_obj_list = Card.query.filter_by(accountId=accountId)
    return render_template('mine.html', User_obj=User_obj, Card_obj_list=Card_obj_list)


if __name__ == '__main__':
    app.run(debug=True)
