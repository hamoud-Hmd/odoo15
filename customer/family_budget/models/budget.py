from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import datetime, date


class FamilyBudget(models.Model):
    _name = "family.budget"
    _rec_name = 'id'

    active_total = fields.Float(string='Active Total', readonly=True, compute='_compute_total')
    contribution_total = fields.Float(string='Contribution Total', readonly=True, compute='_compute_contribution_total')
    withdraw_total = fields.Float(string='Withdraw Total', readonly=True, compute='_compute_withdraw_total')

    def _compute_total(self):
        for line in self:
            line.active_total = line.contribution_total - line.withdraw_total

    def _compute_contribution_total(self):
        for line in self:
            total_cont = 0
            conttrs = self.env['family.contribution'].search([])
            for c in conttrs:
                total_cont += c.amount
            line.contribution_total = total_cont

    def _compute_withdraw_total(self):
        for line in self:
            total_withdarws = 0
            withdraws = self.env['family.withdraw'].search([])
            for c in withdraws:
                total_withdarws += c.amount
            line.withdraw_total = total_withdarws
