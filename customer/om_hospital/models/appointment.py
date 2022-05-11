# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

# create model Patient reference to table in the database


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    # inherit  to  mail so that we use mail chatter and activity so that we us schedule activity
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointment"
    _order = 'id desc'
    _rec_name = 'patient_id'

    patient_id = fields.Many2one('hospital.patient', string='Patient', tracking=True, required=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', tracking=True, required=True)
    age = fields.Integer(string='Age', related='patient_id.age', tracking=True)
    reference = fields.Char(string='Reference', required=True, readonly=True,
                            default=lambda self: _('New'))
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, default='male', related='patient_id.gender', tracking=True)
    note = fields.Text(string='Description', tracking=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirmed'), ('done', 'Done'), ('cancel', 'Cancelled')], default='draft',
        string="Status", tracking=True)
    date_appointment = fields.Date(string='Date')
    date_checkup = fields.Datetime(string='Date Check up Time')
    prescription = fields.Text(string='Prescription')
    prescription_line_ids = fields.One2many('appointment.prescription.lines', 'appointment_id',
                                           string='Prescription Lines')

    def action_url(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'new', #or self if you want to get opened in the same page
            'url': 'https://%s/' % self.prescription
        }
    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Appointment'
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or ('New')
        res = super(HospitalAppointment, self).create(vals)
        return res

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        if self.patient_id:
            if self.patient_id.gender:
                self.gender = self.patient_id.gender
            if self.patient_id.note:
                self.note = self.patient_id.note
        else:
            pass

    # Overide delete method
    def unlink(self):
        if self.state == 'done':
            raise ValidationError(_('You cannot delete %s as it is in done state'% self.state))
        return super(HospitalAppointment, self).unlink()


    class AppointmentPrescriptionLines(models.Model):
        _name = 'appointment.prescription.lines'
        _description = 'Appointment Prescription Lines'

        name = fields.Char(string='Name', required=True)
        qty = fields.Integer(string='Quantity')
        appointment_id = fields.Many2one('hospital.appointment', string='Appointment', tracking=True, readonly=True)
