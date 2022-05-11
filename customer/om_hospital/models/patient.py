# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


# create model Patient reference to table in the database


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    # inherit  to  mail so that we use mail chatter and activity so that we us schedule activity
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patient"
    _order = 'id desc'
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
    image = fields.Binary(string="Image")
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirmed'), ('done', 'Done'), ('cancel', 'Cancelled')], default='draft',
        string="Status", tracking=True)
    responsible_id = fields.Many2one('res.partner', string='Responsible', tracking=True)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string='Appointments', required=True)

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


    @api.constrains('name')
    def check_name(self):
        for rec in self:
            patients = self.env['hospital.patient'].search([('name', '=', rec.name), ('id', '!=', rec.id)])
            if patients:
                raise ValidationError('Name %s is Already Exists'% rec.name)

    @api.constrains('age')
    def check_age(self):
        if self.age <= 0:
            raise ValidationError('%s is not a valide age ' % self.age)


    def name_get(self):
        result = []
        for rec in self:
            name = '[' + rec.reference + '] ' + rec.name
            result.append((rec.id, name))
        return result

    def action_open_appointments(self):
        return {
            'name': _("Appointment"),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hospital.appointment',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
            'target': 'current',
        }