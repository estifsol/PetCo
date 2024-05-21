from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt
from wtforms import StringField, PasswordField, SubmitField,Form,validators
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

bcrypt = Bcrypt()
db = SQLAlchemy()

# Create owner model to form database
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Fullname = db.Column(db.String(250),nullable=False)
    Email = db.Column(db.String(250), unique=True,nullable=False)
    Password = db.Column(db.String(250),nullable=False)
    
    def __init__(self,Fullname,Email,Password):
        self.Fullname = Fullname
        self.Email = Email
        self.Password = bcrypt.generate_password_hash(Password).decode('utf-8')

    def check_password(self,Password):
        return bcrypt.check_password_hash(self.Password, Password)


# Registration form
class RegistrationForm(FlaskForm):
    Fullname = StringField('Fullname', validators=[DataRequired()])
    Email = StringField('Email', [Email(),DataRequired()])
    Password = PasswordField('Password', validators=[Length(min=6)])
    Confirm_Password = PasswordField('Confirm_Password', validators=[DataRequired()])
    Submit = SubmitField('Create_Account')

    def validate_Email(self, field):
        if Users.query.filter_by(Email=field.data).first():
            raise ValidationError('Email already exists')
        
    def validate_Password(self, field):
        if field.data != self.Confirm_Password.data: 
            raise ValidationError('Passwords must match')

class LoginForm(FlaskForm):
    Email = StringField('Email', [DataRequired()])
    Password = PasswordField('Password', validators=[Length(min=6)])
    Submit = SubmitField('Login')
     
    def validate_Password(self, field):
        user = Users.query.filter_by(Email=self.Email.data).first()
        if not user or not user.check_password(field.data):
            raise ValidationError('Invalid email or password')