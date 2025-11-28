from odoo import _, api, fields, models, tools
from odoo.exceptions import Warning, UserError
from datetime import datetime, time

class FormDokumen(models.Model):
    _name = 'form.dokumen'
    _rec_name = 'sertifikat'
    _description = 'Form Dokumen'

    nama            = fields.Char('Nama')
    sertifikat      = fields.Char('Sertifikat')
    proses          = fields.Many2one('proses',string='Proses')
    berkas_pendukung = fields.Binary('Berkas Pendukung', store=True)  
    nama_berkas_pendukung = fields.Char('Nama Berkas Pendukung')
    akta            = fields.Char('Akta')
    berkas_akta = fields.Binary('Berkas Akta', store=True)  
    nama_berkas_akta = fields.Char('Nama Berkas Akta')
    tanggal_masuk   = fields.Date('Tanggal Masuk', default=fields.Date.context_today)
    tanggal_keluar  = fields.Date('Tanggal Keluar', default=fields.Date.context_today)
    bukti_foto      = fields.Binary('Bukti Foto', store=True)  
    nama_bukti_foto = fields.Char('Nama Bukti Foto')
    status          = fields.Char('Status')

class Proses(models.Model):
    _name = 'proses'
    _rec_name = 'nama_proses'
    _description = 'Form Proses'

    nama_proses     = fields.Char('Nama Proses')
    keterangan      = fields.Text('Keterangan')