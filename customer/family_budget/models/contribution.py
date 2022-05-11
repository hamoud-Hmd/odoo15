from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import datetime, date


class FamilyContribution(models.Model):
    _name = "family.contribution"


    member_id = fields.Many2one('family.member', string='Member', required=True, store=True)
    amount = fields.Integer(string='Amount', required=True)
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    total = fields.Float(string='Total', compute="_compute_total", readonly=True)
    name = fields.Char(string='Reference', copy=False, required=True, readonly=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        enddate = self.caluclate_date_value(vals.get('amount'), vals.get('member_id'))
        vals['end_date'] = enddate
        if vals.get('member_id'):
            member = self.env["family.member"].search([('id', '=', vals.get('member_id'))])
            vals['start_date'] = member[0].last_contribution
            member[0].last_contribution = enddate
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('family.contribution') or ('New')
        res = super(FamilyContribution, self).create(vals)
        return res

    def caluclate_date_value(self, amount, member_id):
        value_monthly = 1000
        number_month = int(amount / value_monthly)
        date_format = '%Y-%m-%d'
        given_date = f'{date.today().day}/{date.today().month}/{date.today().year}'
        member = self.env["family.member"].search([('id', '=', member_id)])
        if member:
            given_date = str(member[0].last_contribution)

        dtObj = datetime.strptime(given_date, date_format)
        future_date = dtObj + relativedelta(months=number_month)
        return future_date

    def _compute_total(self):
        sum1 = 0
        for line in self:
            sum1 += line.amount
            line.total = sum1

    @api.constrains('amount')
    def check_amount(self):
        if self.amount<= 0:
            raise ValidationError("The amount can't 0 or negative")