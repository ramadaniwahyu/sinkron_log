from flask import Flask, render_template, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
login_manager = LoginManager()

app = Flask(__name__)

# Configuration of application, see configuration.py, choose one and uncomment.
#app.config.from_object('config.ProductionConfig')
app.config.from_object('config.DevelopmentConfig')
#app.config.from_object('config.TestingConfig')

Bootstrap(app)
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "auth.login"
migrate = Migrate(app, db)

from app import models
from .models import PengadilanTinggi, Sinkronisasi

@app.route('/')
def index():
    pt = PengadilanTinggi.query.first()
    list = Sinkronisasi.query.all()
    
    return render_template('home.html', pt=pt, list=list, title='Monitoring Sinkronisasi SIPP')

@app.route('/beranda')
@login_required
def dashboard():
    pt = PengadilanTinggi.query.first()
    
    return render_template("dashboard.html", pt=pt, title="Dashboard")

@app.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)

# Register blueprints
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from .admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint)

# Errors Handling
@app.errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html', title='Akses Ditolak'), 403

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html', title='Halaman Tidak Ditemukan'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html', title='Server Internal Eror'), 500