from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker

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
    User_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)  # 外键字段


class User(db.Model):
    """用户表"""
    __tablename__ = "User"  # 指明数据库表名
    id = db.Column(db.Integer, primary_key=True)  # 主键 整型的主键默认设置为自增
    accountId = db.Column(db.String(64), unique=True)  # 唯一性
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    Card = db.relationship("Card", backref="User")


# 创建数据表
# 使用drop_all清除数据库中的所有数据
# db.drop_all()
# 创建所有的表
# db.create_all()


@app.route('/login/')
def login():
    return render_template('login.html')



if __name__ == '__main__':
    app.run()
