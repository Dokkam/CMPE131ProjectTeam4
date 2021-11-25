from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators= [DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Sign in")

class RegisterForm(FlaskForm):
    username = StringField("Username",validators = [DataRequired()])
    password = PasswordField("Password",validators =[DataRequired()])
    submit = SubmitField("Register")

class FileForm(FlaskForm):
    file = FileField('File', validators=[
        FileRequired(),
        FileAllowed(['md'], '.md only!')
    ])
    submit = SubmitField('Upload')

class uploadForm(FlaskForm):
    file = FileField('Document', validators = [FileRequired(), FileAllowed(['md', 'markdown'], 'Markdown document only!')])
    submit = SubmitField('Upload')