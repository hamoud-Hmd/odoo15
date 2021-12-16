# -*- coding: utf-8 -*-
from odoo import api, fields, models, _





class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    # inherit  to  mail so that we use mail chatter and activity so that we us schedule activity
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Doctor"
    _rec_name = 'doctor_name'
    _order = 'id desc'

    doctor_name = fields.Char(string='Doctor Name', required=True, tracking=True)
    reference = fields.Char(string='Order Reference', required=True, readonly=True,
                            default=lambda self: _('New'))
    age = fields.Integer(string='Age', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, default='male', tracking=True)
    note = fields.Text(string='Description', tracking=True)
    image = fields.Binary(string="Image")

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Docotr'
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.doctor') or ('New')
        res = super(HospitalDoctor, self).create(vals)
        return res


    def copy(self, default=None):
        default = dict(default or {})
        if ('doctor_name' not in default):
            default['doctor_name'] = _("%s (copy)", self.doctor_name)
        return super(HospitalDoctor, self).copy(default)
