# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


# create model Patient reference to table in the database


class CreateAppointmentWiz(models.TransientModel):
    _name = "create.appointment.wizard"
    _description = "Create Appointment Wizard"

    date_appointment = fields.Date(string='Date', required=True)
    patient_id = fields.Many2one('hospital.patient', string='Patient', tracking=True)

    def action_create_appointment(self):
        vals = {
            'patient_id': self.patient_id.id,
            'date_appointment': self.date_appointment
        }
        self.env['hospital.appointment'].create(vals)
