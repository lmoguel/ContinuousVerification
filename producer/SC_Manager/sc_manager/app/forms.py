from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from django.utils.crypto import get_random_string #POSTERIORMENTE CAMBIAR A CADENA GENERADA POR NOSOTROS

class contract_form(FlaskForm):
    ip = StringField('IP', validators=[DataRequired()])
    port = StringField('Port', validators=[DataRequired(), Length(max=5)])
    bb_id = StringField('Building Block identifier', validators=[DataRequired(), Length(max=80), Length(min=80)])
    folder_path = StringField('Output folder path', validators=[DataRequired()])
    #password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Is this the initial organization of the sc?')
    submit = SubmitField('Validate request')