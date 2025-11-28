from odoo import api, fields,tools, models, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from odoo.exceptions import Warning, UserError
from datetime import datetime, timedelta, date, time
# import MySQLdb
import calendar
import json
import requests
import urllib3
urllib3.disable_warnings()

class LaporanPenyelesaianWizard(models.TransientModel):
	_name = "laporan.penyelesaian.wiz"
	_rec_name ="name_report"
	_description = "Laporan Penyelesaian"
	
	company_id			= fields.Many2one('res.company',default=lambda self: self.env.user.company_id.id)
	company_title		= fields.Char(string="Title",related='company_id.name')
	name_report			= fields.Char("Nama Report", default='Laporan Penyelesaian')
	date_start			= fields.Date("Tanggal Mulai", required=True, default=fields.Date.context_today)
	date_end			= fields.Date("Tanggal Akhir", required=True, default=fields.Date.context_today)
	proses          	= fields.Many2one('proses',string='Proses')
	line_ids 			= fields.One2many('line.laporan.penyelesaian.wiz', 'penyelesaian_id','Details')

	date_range = fields.Selection(
		[('today', 'Hari Ini'),
		 ('this_week', 'Pekan Ini'),
		 ('this_month', 'Bulan Ini'),
		 ('this_quarter', 'Kwartal Ini'),
		 ('this_year', 'Tahun Ini'),
		 ('yesterday', 'Kemarin'),
		 ('last_week', 'Pekan Lalu'),
		 ('last_month', 'Bulan Lalu'),
		 ('last_quarter', 'Kwartal Lalu'),
		 ('last_year', 'Tahun Lalu')],
		string='Rentang Tanggal')

	@api.onchange('date_range')
	def onchange_date_range(self):
		if self.date_range:
			date = datetime.today()
			if self.date_range == 'today':
				self.date_start = date.strftime("%Y-%m-%d")
				self.date_end = date.strftime("%Y-%m-%d")
			if self.date_range == 'this_week':
				day_today = date - timedelta(days=date.weekday())
				self.date_start = (day_today - timedelta(days=date.weekday())).strftime("%Y-%m-%d")
				self.date_end = (day_today + timedelta(days=4)).strftime("%Y-%m-%d")
			if self.date_range == 'this_month':
				self.date_start = datetime(date.year, date.month, 1).strftime("%Y-%m-%d")
				self.date_end = datetime(date.year, date.month, calendar.mdays[date.month]).strftime("%Y-%m-%d")
			if self.date_range == 'this_quarter':
				if int((date.month - 1) / 3) == 0:  # First quarter
					self.date_start = datetime(date.year, 1, 1).strftime("%Y-%m-%d")
					self.date_end = datetime(date.year, 3, calendar.mdays[3]).strftime("%Y-%m-%d")
				if int((date.month - 1) / 3) == 1:  # Second quarter
					self.date_start = datetime(date.year, 4, 1).strftime("%Y-%m-%d")
					self.date_end = datetime(date.year, 6, calendar.mdays[6]).strftime("%Y-%m-%d")
				if int((date.month - 1) / 3) == 2:  # Third quarter
					self.date_start = datetime(date.year, 7, 1).strftime("%Y-%m-%d")
					self.date_end = datetime(date.year, 9, calendar.mdays[9]).strftime("%Y-%m-%d")
				if int((date.month - 1) / 3) == 3:  # Fourth quarter
					self.date_start = datetime(date.year, 10, 1).strftime("%Y-%m-%d")
					self.date_end = datetime(date.year, 12, calendar.mdays[12]).strftime("%Y-%m-%d")
			if self.date_range == 'this_year':
					self.date_start = datetime(date.year, 1, 1).strftime("%Y-%m-%d")
					self.date_end = datetime(date.year, 12, 31).strftime("%Y-%m-%d")

			date = (datetime.now() - relativedelta(days=1))
			if self.date_range == 'yesterday':
				self.date_start = date.strftime("%Y-%m-%d")
				self.date_end = date.strftime("%Y-%m-%d")
			date = (datetime.now() - relativedelta(days=7))
			if self.date_range == 'last_week':
				day_today = date - timedelta(days=date.weekday())
				self.date_start = (day_today - timedelta(days=date.weekday())).strftime("%Y-%m-%d")
				self.date_end = (day_today + timedelta(days=4)).strftime("%Y-%m-%d")
			date = (datetime.now() - relativedelta(months=1))
			if self.date_range == 'last_month':
				self.date_start = datetime(date.year, date.month, 1).strftime("%Y-%m-%d")
				self.date_end = datetime(date.year, date.month, calendar.mdays[date.month]).strftime("%Y-%m-%d")
			date = (datetime.now() - relativedelta(months=3))
			if self.date_range == 'last_quarter':
				if int((date.month - 1) / 3) == 0:  # First quarter
					self.date_start = datetime(date.year, 1, 1).strftime("%Y-%m-%d")
					self.date_end = datetime(date.year, 3, calendar.mdays[3]).strftime("%Y-%m-%d")
				if int((date.month - 1) / 3) == 1:  # Second quarter
					self.date_start = datetime(date.year, 4, 1).strftime("%Y-%m-%d")
					self.date_end = datetime(date.year, 6, calendar.mdays[6]).strftime("%Y-%m-%d")
				if int((date.month - 1) / 3) == 2:  # Third quarter
					self.date_start = datetime(date.year, 7, 1).strftime("%Y-%m-%d")
					self.date_end = datetime(date.year, 9, calendar.mdays[9]).strftime("%Y-%m-%d")
				if int((date.month - 1) / 3) == 3:  # Fourth quarter
					self.date_start = datetime(date.year, 10, 1).strftime("%Y-%m-%d")
					self.date_end = datetime(date.year, 12, calendar.mdays[12]).strftime("%Y-%m-%d")
			date = (datetime.now() - relativedelta(years=1))
			if self.date_range == 'last_year':
				self.date_start = datetime(date.year, 1, 1).strftime("%Y-%m-%d")
				self.date_end = datetime(date.year, 12, 31).strftime("%Y-%m-%d")

	def get_line_laporan(self):
		obj_line = self.env['line.laporan.penyelesaian.wiz']
		obj_line.search([]).unlink()
		dok = self.env['form.dokumen'].sudo().search([('tanggal_masuk', '>=', self.date_start),('tanggal_masuk', '<=', self.date_end),])
		for d in dok:
			data_dok = {
						"penyelesaian_id"		: self.id,
						"nama"					: d.nama,
						"sertifikat"            : d.sertifikat,
						"proses"				: d.proses,
						"berkas_pendukung"		: d.berkas_pendukung,
						"nama_berkas_pendukung"	: d.nama_berkas_pendukung,
						"akta"					: d.akta,
						"berkas_akta"			: d.berkas_akta,
						"nama_berkas_akta"		: d.nama_berkas_akta,
						"tanggal_masuk"			: d.tanggal_masuk,
						"tanggal_keluar"		: d.tanggal_keluar,
						"status"				: d.status,
					}
			obj_line.create(data_dok)

	def tampilkan(self):
		start_date = self.date_start.strftime("%Y-%m-%d")
		end_date = self.date_end.strftime("%Y-%m-%d")
		self.get_line_laporan()
		# return {
		# 	'domain': [('penyelesaian_id', '=', self.id)],
		# 	'name': _("PERIODE : " + start_date + ' S.D ' + end_date),
		# 	'view_type': 'form',
		# 	'view_mode': 'tree',
		# 	'res_model': 'line.laporan.penyelesaian.wiz',
		# 	'view_id': False,
		# 	'context': False,
		# 	'type': 'ir.actions.act_window'
		# }
			
class StockPenerimaanLineTPBWizard(models.TransientModel):
	_name = "line.laporan.penyelesaian.wiz"
	_description = "Stock Penerimaan Line"

	line_no 			= fields.Integer(string='No')
	penyelesaian_id		= fields.Many2one('line.laporan.penyelesaian.wiz', 'Penyelesaian ID', ondelete='cascade')
	nama            	= fields.Char('Nama')
	sertifikat      	= fields.Char('Sertifikat')
	proses          	= fields.Many2one('proses',string='Proses')
	berkas_pendukung 	= fields.Binary('Berkas Pendukung', store=True)  
	nama_berkas_pendukung = fields.Char('Nama Berkas Pendukung')
	akta            	= fields.Char('Akta')
	berkas_akta 		= fields.Binary('Berkas Akta', store=True)  
	nama_berkas_akta 	= fields.Char('Nama Berkas Akta')
	tanggal_masuk   	= fields.Date('Tanggal Masuk')
	tanggal_keluar  	= fields.Date('Tanggal Keluar')
	bukti_foto      = fields.Binary('Bukti Foto', store=True)  
	nama_bukti_foto = fields.Char('Nama Bukti Foto')
	status          	= fields.Char('Status')