from datetime import datetime

from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import declared_attr

from app import db, login_manager

class Pengguna(db.Model, UserMixin):
    __tablename__= 'pengguna'
    
    id = db.Column(db.Integer, primary_key=True)
    dibuat_pada = db.Column(db.DateTime, default=datetime.now)
    diubah_pada = db.Column(db.DateTime, onupdate=datetime.now)
    name = db.Column(db.String(60))
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password  
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '{}'.format(self.name)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Pengguna.query.get(int(user_id))

class Sinkronisasi(db.Model):
    __tablename__ = 'sinkronisasi'
    
    id = db.Column(db.Integer, primary_key=True)    
    pn_id = db.Column(db.Integer, db.ForeignKey('pengadilan_negeri.id'))
    kode_pn = db.Column(db.Integer)
    mulai = db.Column(db.DateTime, default=datetime.now)
    selesai = db.Column(db.DateTime, default=datetime.now)
    
class PengadilanNegeri(db.Model):
    __tablename__= 'pengadilan_negeri'
    
    id = db.Column(db.Integer, primary_key=True)
    kode_pn = db.Column(db.Integer)
    pt_id = db.Column(db.Integer, db.ForeignKey('pengadilan_tinggi.id'))
    kode = db.Column(db.String(50))
    nama = db.Column(db.String(100), nullable=False)
    alamat = db.Column(db.String(500))
    city = db.Column(db.String(50))
    prov = db.Column(db.String(50))
    jenis_pengadilan = db.Column(db.String(50), default='umum')
    kelas = db.Column(db.String(5))
    website = db.Column(db.String(100))
    email = db.Column(db.String(100))
    sinkron = db.relationship('Sinkronisasi', backref='pengadilan_negeri')
    dibuat_pada = db.Column(db.DateTime, default=datetime.now)
    diubah_pada = db.Column(db.DateTime, onupdate=datetime.now)
    
    def __repr__(self):
        return '{}'.format(self.nama)
    
class PengadilanTinggi(db.Model):
    __tablename__= 'pengadilan_tinggi'
    
    id = db.Column(db.Integer, primary_key=True)
    kode = db.Column(db.String(50))
    nama = db.Column(db.String(100), nullable=False)
    alamat = db.Column(db.String(500))
    city = db.Column(db.String(50))
    prov = db.Column(db.String(50))
    jenis_pengadilan = db.Column(db.String(50), default='umum')
    website = db.Column(db.String(100))
    email = db.Column(db.String(100))
    kelas = db.Column(db.String(5))
    pn = db.relationship('PengadilanNegeri', backref='pengadilan_tinggi')
    dibuat_pada = db.Column(db.DateTime, default=datetime.now)
    diubah_pada = db.Column(db.DateTime, onupdate=datetime.now)
    
    def __repr__(self):
        return '{}'.format(self.nama)