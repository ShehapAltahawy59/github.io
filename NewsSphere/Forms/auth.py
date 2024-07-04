
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,EmailField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from NewsSphere.models.Models import User
class regestration(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min = 2, max = 20)])
    email = EmailField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('confirmed_password')])
    confirmed_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password',message='Passwords must match')])
    submit = SubmitField('Sign Up')

    def validate_email(self,email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            print("here")
            raise ValidationError('the Email is Already exist !')

            

    

    

class Login(FlaskForm):
    email = EmailField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(),])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
