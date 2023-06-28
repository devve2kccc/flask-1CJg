from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import Float
from sqlalchemy.orm import object_session
from sqlalchemy import event


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    total_cash = db.Column(db.Float, nullable=False, default=0.0)

    #  um urilizador pode ter muitas transações
    mains = db.relationship('Main', back_populates='user')

    savings = db.relationship('Saving', back_populates='user')

    # um utilizador pode ter muitos bancos
    banks = db.relationship('Bank', back_populates='user')
    cash = db.relationship('CashSources', back_populates='user')
    
    @property
    def total_money(self):
        bank_balances = sum([bank.ammout for bank in self.banks])
        cash_balance = sum([cash.balance for cash in self.cash]) if self.cash else 0.0
        total = cash_balance + bank_balances
        return total
    
    @staticmethod
    def update_user_cash_balance(mapper, connection, target):
        session = object_session(target)
        total_cash = session.query(func.coalesce(func.sum(CashSources.balance), 0.0)).filter_by(
            user_id=target.id).scalar()
        target.total_cash = total_cash



class Main(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer)  # Unique transaction ID
    transaction_name = db.Column(db.String(10000))
    transaction_type = db.Column(db.String(10000))
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date)
    category = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    payment_method = db.Column(db.String(20))
    bank_id = db.Column(db.Integer, db.ForeignKey('bank.id'))
    cash_id = db.Column(db.Integer, db.ForeignKey('cash_sources.id'))


    user = db.relationship('User', back_populates='mains')
    bank = db.relationship('Bank', back_populates='mains')
    cash = db.relationship('CashSources', back_populates='mains')

    @staticmethod
    def generate_transaction_id(mapper, connection, target):
        session = object_session(target)
        max_transaction_id = session.query(func.max(Main.transaction_id)).filter_by(
            user_id=target.user_id).scalar()

        if max_transaction_id is not None:
            target.transaction_id = max_transaction_id + 1
        else:
            target.transaction_id = 1

    def serialize(self):
        return {
            'transaction_id': self.id,
            'transaction_name': self.transaction_name,
            'amount': self.amount,
            'category': self.category,
            'date': self.date.strftime('%Y-%m-%d'),
            'transaction_type': self.transaction_type
        }
# Associate the event listener to generate transaction ID
event.listen(Main, 'before_insert', Main.generate_transaction_id)
event.listen(User, 'before_insert', User.update_user_cash_balance)



class Bank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bankname = db.Column(db.String(10000), nullable=False)
    ammout = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', back_populates='banks')
    mains = db.relationship('Main', back_populates='bank')

class CashSources(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cashname = db.Column(db.String(10000), nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0.0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', back_populates='cash')
    mains = db.relationship('Main', back_populates='cash')



class Saving(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    safename = db.Column(db.String(10000), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', back_populates='savings')

class GeneratedReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    generated_at = db.Column(db.DateTime, nullable=False, default=func.now())

    user = db.relationship('User', backref=db.backref('generated_reports', lazy=True))