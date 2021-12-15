# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


# create model Patient reference to table in the database


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    # inherit  to  mail so that we use mail chatter and activity so that we us schedule activity
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patient"

    name = fields.Char(string='Name', required=True, tracking=True)
    reference = fields.Char(string='Order Reference', required=True, readonly=True,
                            default=lambda self: _('New'))
    age = fields.Integer(string='Age', tracking=True)
    appointment_count = fields.Integer(string='Appointment Count', compute='_compute_appontment_count')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, default='male', tracking=True)
    note = fields.Text(string='Description', tracking=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirmed'), ('done', 'Done'), ('cancel', 'Cancelled')], default='draft',
        string="Status", tracking=True)
    responsible_id = fields.Many2one('res.partner', string='Responsible', tracking=True)

    def _compute_appontment_count(self):
        for rec in self:
            appointment_count = rec.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
            rec.appointment_count = appointment_count

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New patient'
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.patient') or ('New')
        res = super(HospitalPatient, self).create(vals)
        return res

    @api.model
    def default_get(self, fields):
        res = super(HospitalPatient, self).default_get(fields)
        return res
