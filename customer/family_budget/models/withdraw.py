from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import datetime, date


class FamilyWithdraw(models.Model):
    _name = "family.withdraw"


    reason = fields.Text(string='Reason', required=True)
    amount = fields.Integer(string='Amount', required=True)
    total = fields.Float(string='Total', compute="_compute_total", readonly=True)
    name = fields.Char(string='Reference', required=True, readonly=True, default=lambda self: _('New'))
    user_id = fields.Many2one('res.users', string='Member', default=lambda self: self.env.user.id, readonly=True)

    @api.model
    def create(self, vals):
        budget = self.env['family.budget'].search([])
        for b in budget:
            total_cont = b.active_total
            if (total_cont - vals['amount']) < 0:
                raise ValidationError(f"The active amount is {total_cont}, Not sufficient to do the operation")

        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('family.withdraw') or ('New')
        res = super(FamilyWithdraw, self).create(vals)
        return res


    def _compute_total(self):
        sum1 = 0
        for line in self:
            sum1 += line.amount
            line.total = sum1

    @api.constrains('amount')
    def check_amount(self):
        if self.amount<= 0:
            raise ValidationError("The amount can't 0 or negative")