from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, session, redirect, url_for, flash
from datetime import datetime
from flask_wtf import FlaskForm
from sqlalchemy import null
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
    Deposit = db.relationship("Deposit", backref="User")
    Transfer = db.relationship("Transfer", backref="User")


class Transfer(db.Model):
    """转账表"""
    __tablename__ = "Transfer"  # 指明数据库表名

    id = db.Column(db.Integer, primary_key=True)  # 主键 整型的主键默认设置为自增
    accountId = db.Column(db.String(64), db.ForeignKey("User.accountId"))  # 外键字段
    my_CardId = db.Column(db.Integer, db.ForeignKey("Card.CardId"))  # 外键字段
    other_CardId = db.Column(db.Integer, db.ForeignKey("Card.CardId"))  # 外键字段
    datetime = db.Column(db.DateTime, nullable=False)
    money = db.Column(db.String(64), nullable=False)


class Deposit(db.Model):
    """存款表"""
    __tablename__ = "Deposit"
    id = db.Column(db.Integer, primary_key=True)  # 主键 整型的主键默认设置为自增
    accountId = db.Column(db.String(64), db.ForeignKey("User.accountId"))  # 外键字段
    CardId = db.Column(db.Integer, db.ForeignKey("Card.CardId"))  # 外键字段
    datetime = db.Column(db.DateTime, nullable=False)
    money = db.Column(db.String(64), nullable=False)
#
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
        db.session.rollback()
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
            db.session.rollback()
            flash('用户账号有误，请核实再输入')
            return index()


# 退出功能
@app.route('/login', methods=['GET'])
def quite():
    session['logged_in'] = False
    session['login_ok'] = False
    session['information_ok'] = False
    session['accountId'] = False
    session['deposit_flash'] = False
    session['transfer_flash'] = False
    session['update_user_flash'] = False
    session['update_card_flash'] = False
    return login()


# 银行首页
@app.route('/home', methods=['GET'])
def home():
    if session.get('login_ok'):
        return render_template('home.html')
    else:
        return render_template('404.html')


# 充值功能
@app.route('/home/deposit', methods=['POST'])
def deposit():
    accountId = session.get('accountId')
    CardId = request.form['CardId']
    money = request.form['money']
    now_time = datetime.now()
    Card_obj = Card.query.filter_by(CardId=CardId).first()
    if not Card_obj:
        flash('卡号不存在，请添加后再进行充值！！')
        return redirect('/home')
    if money == "":
        flash('金额不能为空！！')
        return redirect('/home')
    if money.isdigit():
        deposit_obj = Deposit(
            accountId=accountId,
            CardId=CardId,
            money=money,
            datetime=now_time
        )
        session['deposit_flash'] = True
        session['transfer_flash'] = False
        try:
            db.session.query(Card).filter(Card.CardId == CardId).update(
                {'money': int(money) + int(Card_obj.money)})
            db.session.add(deposit_obj)
            db.session.commit()
            flash("充值成功！！")
            return redirect('/home')
        except:
            db.session.rollback()
            flash("充值失败！！")
            return redirect('/home')
    else:
        flash("金额必须为整数！！")
        return redirect('/home')


@app.route('/home/transfer', methods=['POST'])
def transfer():
    accountId = session.get('accountId')
    now_time = datetime.now()
    my_CardId = request.form['my_CardId']
    other_CardId = request.form['other_CardId']
    money = request.form['money']
    password = request.form['password']
    Card_obj = Card.query.filter_by(CardId=my_CardId).first()
    Card_obj_other = Card.query.filter_by(CardId=other_CardId).first()
    if not Card_obj:
        flash("此银行卡不存在，请添加后再尝试！！")
        return redirect('/home')
    if not Card_obj_other:
        flash("此银行卡不存在，请确认后再尝试！！")
        return redirect('/home')
    if int(Card_obj.money) < int(money):
        flash("余额不足！！")
        return redirect('/home')
    if password == Card_obj.password:
        transfer_obj = Transfer(
            accountId=accountId,
            datetime=now_time,
            my_CardId=my_CardId,
            other_CardId=other_CardId,
            money=money
        )
        session['deposit_flash'] = False
        session['transfer_flash'] = True
        try:
            db.session.query(Card).filter(Card.CardId == my_CardId).update({'money':
                                                                                int(Card_obj.money) - int(money)})
            db.session.query(Card).filter(Card.CardId == other_CardId).update({'money':
                                                                                   int(Card_obj_other.money) + int(
                                                                                       money)})
            db.session.add(transfer_obj)
            db.session.commit()
            flash("转账成功！！")
            return redirect('/home')
        except:
            db.session.rollback()
            flash("转账失败，请核实信息后再尝试！！")
            return redirect('/home')
    else:
        flash("密码不正确，请核实后再尝试！！")
        return redirect('/home')


@app.route('/home/mine')
def mine():
    accountId = session.get('accountId')
    User_obj = User.query.filter_by(accountId=accountId).first()
    Card_obj_list = Card.query.filter_by(accountId=accountId)
    Transfer_obj_list = Transfer.query.filter_by(accountId=accountId)
    Deposit_obj_list = Deposit.query.filter_by(accountId=accountId)
    return render_template('mine.html', User_obj=User_obj, Card_obj_list=Card_obj_list,
                           Transfer_obj_list=Transfer_obj_list, Deposit_obj_list=Deposit_obj_list)


@app.route('/home/mine/update/<name>', methods=['GET'])
def update(name):
    if name == 'user':
        accountId = session.get('accountId')
        new_obj = User.query.filter_by(accountId=accountId).first()
        return render_template('update_user.html', new_obj=new_obj)
    if name == 'card':
        accountId = session.get('accountId')
        new_obj_list = Card.query.filter_by(accountId=accountId)
        return render_template('update_card.html', new_obj_list=new_obj_list)


@app.route('/home/mine/update/user', methods=['POST'])
def update_user():
    accountId = session.get('accountId')
    email = request.form['email']
    password = request.form['password']
    sure_password = request.form['sure_password']
    if (not email and password) or email == '':
        if password == sure_password:
            try:
                db.session.query(User).filter(User.accountId == accountId).update({'password': password})
                db.session.commit()
                return redirect('/home/mine')
            except:
                db.session.rollback()
                flash("修改失败！！")
                session['update_user_flash'] = True
                return redirect('/home/mine/update/user')
        else:
            flash("两次输入密码不正确，请核实后再输入！！！")
            session['update_user_flash'] = True
            return redirect('/home/mine/update/user')

    else:
        if not password:
            try:
                db.session.query(User).filter(User.accountId == accountId).update({'email': email})
                db.session.commit()
                return redirect('/home/mine')
            except:
                db.session.rollback()
                session['update_user_flash'] = True
                flash("修改失败！！")
                return redirect('/home/mine/update/user')
        else:
            if password == sure_password:
                try:
                    db.session.query(User).filter(User.accountId == accountId).update(
                        {'email': email, 'password': password})
                    db.session.commit()
                    return redirect('/home/mine')
                except:
                    db.session.rollback()
                    flash("修改失败！！")
                    session['update_user_flash'] = True
                    return redirect('/home/mine/update/user')
            else:
                flash("两次输入密码不正确，请核实后再输入！！！")
                session['update_user_flash'] = True
                return redirect('/home/mine/update/user')


@app.route('/home/mine/update/card', methods=['POST'])
def update_card():
    accountId = session.get('accountId')
    password = request.form['password']
    sure_password = request.form['sure_password']

    if not password:
        try:
            db.session.query(Card).filter(Card.accountId == accountId).update({'accountId': accountId})
            db.session.commit()
            return redirect('/home/mine')
        except:
            db.session.rollback()
            flash("修改失败！！")
            session['update_card_flash'] = True
            return redirect('/home/mine/update/card')
    else:
        if password == sure_password:
            try:
                db.session.query(Card).filter(Card.accountId == accountId).update(
                    {'accountId': accountId, 'password': password})
                db.session.commit()
                return redirect('/home/mine')
            except:
                db.session.rollback()
                flash("修改失败！！")
                session['update_card_flash'] = True
                return redirect('/home/mine/update/card')
        else:
            flash("两次输入密码不正确，请核实后再输入！！！")
            session['update_card_flash'] = True
            return redirect('/home/mine/update/card')


@app.route('/home/mine/add', methods=['GET'])
def add():
    return render_template('add.html')


@app.route('/home/mine/add', methods=['POST'])
def add_card():
    accountId = session.get('accountId')
    CardId = request.form['CardId']
    password = request.form['password']
    name = request.form['name']
    if password == '' or CardId == '' or name == '':
        session['add_ok'] = False
        flash("所填内容不能为空！！")
        return redirect('/home/mine/add')
    Card_obj = Card.query.filter_by(CardId=CardId).first()
    if Card_obj:
        session['add_ok'] = False
        flash("此银行卡已添加！！")
        return redirect('/home/mine/add')
    new_obj = Card(
        money=0,
        accountId=accountId,
        CardId=CardId,
        password=password,
        name=name
    )
    try:
        db.session.add(new_obj)
        db.session.commit()
        return redirect('/home/mine')
    except:
        db.session.rollback()
        session['add_ok'] = False
        flash("添加失败！！")
        return redirect('/home/mine/add')


@app.route('/admin')
@app.route('/admin/index', methods=['GET'])
def index_admin():
    obj_list = User.query.all()
    return render_template('admin/index.html', obj_list=obj_list)


@app.route('/admin/card', methods=['GET'])
def card_admin():
    obj_list = Card.query.all()
    return render_template('admin/card.html', obj_list=obj_list)


@app.route('/admin/deposit', methods=['GET'])
def deposit_admin():
    obj_list = Deposit.query.all()
    return render_template('admin/deposit.html', obj_list=obj_list)


@app.route('/admin/transfer', methods=['GET'])
def transfer_admin():
    obj_list = Transfer.query.all()
    return render_template('admin/transfer.html', obj_list=obj_list)


if __name__ == '__main__':
    app.run(debug=True)
