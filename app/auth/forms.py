from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
# from wtforms.ext.sqlalchemy.fields import QuerySelectField

# from ..models import Group

class LoginForm(FlaskForm):

    name = StringField('Nama Pengguna', validators=[DataRequired()])
    password = PasswordField('Kata Kunci', validators=[DataRequired()])
    submit = SubmitField('Masuk')

# class PenggunaForm(FlaskForm):
#     name = StringField('Nama Pengguna', validators=[DataRequired()])
#     fullname = StringField('Nama Lengkap', validators=[DataRequired()])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     group = QuerySelectField('Organisasi', query_factory=lambda: Group.query.all(), get_label='name', allow_blank=True)
#     submit = SubmitField('Simpan')

class PasswordForm(FlaskForm):
    password_lama = PasswordField('Password Lama', validators=[DataRequired()])
    password = PasswordField('Password Baru', validators=[DataRequired()])
    confirm_password = PasswordField('Konfirmasi Password Baru', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Ganti Password')