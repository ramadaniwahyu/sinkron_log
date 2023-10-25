from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField, IntegerField, SelectField, EmailField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField

from datetime import date

from app.models import PengadilanTinggi, PengadilanNegeri

class PNForm(FlaskForm):
    jenis = SelectField('Jenis Pengadilan', choices=[('', 'Belum ada pilihan'),('umum', 'Peradilan Umum'),('agama', 'Peradilan Agama'),('militer', 'Peradilan Militer'),('tun', 'Peradilan Tata Usaha Negara')])
    kelas = SelectField('Kelas Pengadilan', choices=[('0', 'Belum ada pilihan'),('1', 'IA-Khusus'),('2', 'IA'),('3', 'IB'),('4', 'II')])
    pt = QuerySelectField('Wilayah Hukum Pengadilan Tinggi', validators=[DataRequired()], 
                           query_factory=lambda: PengadilanTinggi.query.order_by(PengadilanTinggi.nama.asc()).all(), 
                           get_label='nama', allow_blank=True, blank_text='Belum ada pilihan')
    kode = StringField('Kode Pengadilan')
    nama = StringField('Nama Pengadilan')
    kode_pn = IntegerField('Kode Sinkronisasi Pengadilan')
    alamat = TextAreaField('Alamat')
    city = StringField('Kota/Kabupaten')
    prov = StringField('Provinsi')
    email = EmailField('Email Pengadilan')
    website = StringField('Alamat Web Pengadilan')
    submit = SubmitField('Simpan')
    
class PTForm(FlaskForm):
    jenis = SelectField('Kategori Pengadilan', choices=[('', 'Belum ada pilihan'),('umum', 'Peradilan Umum'),('agama', 'Peradilan Agama'),('militer', 'Peradilan Militer'),('tun', 'Peradilan Tata Usaha Negara')])
    kelas = SelectField('Tipe Pengadilan', choices=[('0', 'Belum ada pilihan'),('1', 'Tipe A'),('2', 'Tipe B')])
    kode = StringField('Kode Pengadilan')
    nama = StringField('Nama Pengadilan')
    alamat = TextAreaField('Alamat')
    city = StringField('Kota/Kabupaten')
    prov = StringField('Provinsi')
    email = EmailField('Email Pengadilan')
    website = StringField('Alamat Web Pengadilan')
    submit = SubmitField('Simpan')
    
class SyncForm(FlaskForm):
    pn = QuerySelectField('Nama Pengadilan Negeri', validators=[DataRequired()],
                          query_factory=lambda: PengadilanNegeri.query.order_by(PengadilanNegeri.nama.asc()).all(),
                          get_label='nama', allow_blank='True', blank_text='Belum ada pilihan')
    kode_pn = IntegerField('Kode Sinkronisasi Pengadilan Negeri')
    submit = SubmitField('Simpan')