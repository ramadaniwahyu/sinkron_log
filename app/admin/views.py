from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
from . import admin
from ..models import PengadilanNegeri, PengadilanTinggi, Sinkronisasi
from .forms import PNForm, PTForm, SyncForm
from .. import db

from datetime import datetime

### Pengadilan Tinggi
@admin.route('/beranda/pengadilan-tinggi', methods=['GET', 'POST'])
@login_required
def pengadilan_tinggi():
    
    data = PengadilanTinggi.query.first()
    form = PTForm(obj=data)
    if not data and form.validate_on_submit():
        item = PengadilanTinggi(jenis_pengadilan = form.jenis.data, kelas = form.kelas.data,
                                nama = form.nama.data, alamat = form.alamat.data,
                                city = form.city.data, prov=form.prov.data,
                                website = form.website.data, email = form.email.data)
        
        db.session.add(item)
        db.session.commit()
        flash('Data Pengadilan Tinggi telah ditambahkan.')
        return redirect(url_for('dashboard'))
    
    elif data and form.validate_on_submit():
        data.jenis_pengadilan = form.jenis.data
        data.kelas = form.kelas.data
        data.nama = form.nama.data
        data.alamat = form.alamat.data
        data.city = form.city.data
        data.prov = form.prov.data
        data.website = form.website.data
        data.email = form.email.data
        
        db.session.commit()
        flash('Data Pengadilan Tinggi telah diubah.')
        return redirect(url_for('dashboard'))
    
    form.jenis.data = data.jenis_pengadilan
    form.kelas.data = data.kelas
    form.nama.data = data.nama
    form.alamat.data = data.alamat
    form.city.data = data.city
    form.prov.data = data.prov
    form.website.data = data.website
    form.email.data = data.email
    
    return render_template("admin/pengadilan-tinggi.html", title="Pengadilan Tinggi", form=form)

### Pengadilan Negeri
@admin.route('/beranda/pengadilan-negeri', methods=['GET', 'POST'])
@login_required
def pengadilan_negeri():
    pt = PengadilanTinggi.query.first()
    list = enumerate(PengadilanNegeri.query.all(), start=1)
    form = PNForm()
    if form.validate_on_submit():
        item = PengadilanNegeri(pt_id = pt.id, kode = form.kode.data, nama = form.nama.data,
                                alamat = form.alamat.data, city = form.city.data, prov = form.prov.data,
                                jenis_pengadilan = form.jenis.data, kelas = form.kelas.data,
                                website = form.website.data, email = form.email.data, kode_pn = form.kode_pn.data)
        db.session.add(item)
        db.session.commit()
        flash('Data telah ditambahkan.')
        return redirect(url_for('admin.pengadilan_negeri'))
    
    return render_template('admin/pengadilan-negeri.html', list=list, title='Pengadilan Negeri', form=form)

@admin.route('/beranda/pengadilan-negeri/<id>', methods=['GET', 'POST'])
@login_required
def pengadilan_negeri_edit(id):
    
    pn = PengadilanNegeri.query.get_or_404(id)
    form = PNForm(obj=pn)
    if form.validate_on_submit():
        pn.pengadilan_tinggi = form.pt.data
        pn.kode = form.kode.data
        pn.kode_pn = form.kode_pn.data
        pn.nama = form.nama.data
        pn.alamat = form.alamat.data
        pn.city = form.city.data
        pn.prov = form.prov.data
        pn.jenis_pengadilan = form.jenis.data
        pn.kelas = form.kelas.data
        pn.website = form.website.data
        pn.email = form.email.data
        
        print(pn)
        db.session.commit()
        flash('Data telah diubah')
        return redirect(url_for('admin.pengadilan_negeri'))
    
    form.pt.data = pn.pt_id
    form.kode.data = pn.kode
    form.kode_pn.data = pn.kode_pn
    form.nama.data = pn.nama
    form.alamat.data = pn.alamat
    form.city.data = pn.city
    form.prov.data = pn.prov
    form.jenis.data = pn.jenis_pengadilan
    form.kelas.data = pn.kelas
    form.website.data = pn.website
    form.email.data = pn.email
    
    return render_template('admin/pengadilan-negeri-edit.html', form=form, pn=pn, title='Edit')

@admin.route('/beranda/pengadilan-negeri/<id>/hapus', methods=['GET', 'POST'])
@login_required
def pengadilan_negeri_del(id):
    
    pn = PengadilanNegeri.query.get_or_404(id)
    db.session.delete(pn)
    db.session.commit()
    flash('Data telah dihapus.')
    return redirect(url_for('admin.pengadilan_negeri'))

@admin.route('/beranda/sinkronisasi', methods=['GET', 'POST'])
@login_required
def sinkronisasi():
    
    list = enumerate(Sinkronisasi.query.all(), start=1)
    form = SyncForm()
    if form.validate_on_submit():
        item = Sinkronisasi(pengadilan_negeri = form.pn.data, kode_pn = form.kode_pn.data)
        db.session.add(item)
        db.session.commit()
        flash('Data telah ditambahkan')
        
        return redirect(url_for('admin.sinkronisasi'))
    
    return render_template('admin/sinkronisasi.html', list=list, form=form, title='Sinkronisasi')

@admin.route('/beranda/sinkronisasi/<id>', methods=['GET', 'POST'])
@login_required
def sinkronisasi_edit(id):
    item = Sinkronisasi.query.get_or_404(id)
    form = SyncForm(obj=item)
    if form.validate_on_submit():
        item.pengadilan_negeri = form.pn.data
        item.kode_pn = form.kode_pn.data
        
        db.session.commit()
        flash('Data telah diubah')
        
        return redirect(url_for('admin.sinkronisasi'))
    
    form.pn.data = item.pengadilan_negeri
    form.kode_pn.data = item.kode_pn
    
    return render_template('admin/sinkronisasi-edit.html', item=item, form=form, title='Edit')

@admin.route('/beranda/sinkronisasi/<id>/hapus', methods=['GET', 'POST'])
@login_required
def sinkronisasi_del(id):
    item = Sinkronisasi.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Data telah dihapus.')
    return redirect(url_for('admin.sinkronisasi'))