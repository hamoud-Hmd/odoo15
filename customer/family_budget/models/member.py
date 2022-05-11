from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import datetime, date

from odoo.odoo.api import depends


class FamilyMember(models.Model):
    _name = "family.member"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Full Name', default=lambda self: _('Name'), translate=True, compute='_compute_name', store=True)
    first_name = fields.Char(string='First Name', required=True, translate=True, store=True)
    last_name = fields.Char(string='Last Name', required=True, translate=True, store=True)
    middle_name = fields.Char(string='Middle Name', translate=True, store=True)
    image = fields.Binary(string='Image')
    birthdate = fields.Date(string='Birth Date')
    age = fields.Integer(string='Age', compute='_compute_calculate_age')
    last_contribution = fields.Date(string='Last Contribution', default=date(2020, 1, 1))
    nni = fields.Char(string='NNI', required=False)
    debt = fields.Float(string="Debt", compute='_compute_debt')
    position = fields.Char(string='Position (Job)', translate=True)
    tel = fields.Char(string='Tel')
    is_active = fields.Boolean(string='Active', default=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], required=True, default='male', translate=True)
    note = fields.Text(string='Description', translate=True)
    contribution_count = fields.Integer(string='Contribution Count', compute='_compute_contribution_count')
    total_cost = fields.Float(string='Total Cost', readonly=True, compute='_compute_contribution_count')

    # @api.model
    # def create(self, vals):
    #     middle_name = ''
    #     if vals.get('middle_name'):
    #         middle_name = vals.get('middle_name')
    #     vals['name'] = self.first_name + ' ' + middle_name + ' ' + self.last_name
    #     res = super(FamilyMember, self).create(vals)
    #     return res



    @api.depends('first_name', 'middle_name', 'last_name')
    def _compute_name(self):
        for rec in self:
            middle_name = ''
            if rec.middle_name:
                middle_name = rec.middle_name
            name = f'{rec.first_name} {middle_name} {rec.last_name}'
            rec.name = name

    # def _value_search(self, operator, value):
    #     if operator == 'like':
    #         operator = 'ilike'
    #         name = self.env['family.member'].search([('name', operator, value)], limit=None)
    #     return [(self.name, operator, value)]

    


    def _compute_calculate_age(self):
        today = date.today()
        for rec in self:
            if rec.birthdate:
                age = today.year - rec.birthdate.year - (
                        (today.month, today.day) < (rec.birthdate.month, rec.birthdate.day))
                rec.age = age
            else:
                rec.age = 0

    @api.constrains('birthdate')
    def check_birthdate(self):
        if self.birthdate >= date.today():
            raise ValidationError("a member can't be born in future")




    def name_get(self):
        result = []
        for rec in self:
            middle_name = ''
            if rec.middle_name:
                middle_name = rec.middle_name
            name = rec.first_name + ' ' + middle_name + ' ' + rec.last_name
            result.append((rec.id, name))
        return result

    def _compute_debt(self):
        for rec in self:
            rec.debt = 0
            last_contribution = rec.last_contribution
            current_date = date.today()

            diff_date = (current_date.year - last_contribution.year) * 12 + (
                    current_date.month - last_contribution.month)

            if diff_date > 0:
                rec.debt = 1000 * diff_date

    #
    # def name_get(self):
    #     result = []
    #     for rec in self:
    #         middle_name = ''
    #         if rec.middle_name:
    #             middle_name = rec.middle_name
    #
    #         name = f'{rec.first_name} {middle_name} {rec.last_name}'
    #         rec.name = name
    #         result.append((rec.id, name))
    #     return result

    @api.constrains('nni')
    def _check_nni(self):
        for rec in self:

            if rec.nni:

                if len(rec.nni) != 10:
                    raise ValidationError('NNI must be 10 digits')

    def _compute_contribution_count(self):
        for rec in self:
            rec.total_cost = 0
            contribution_count = rec.env['family.contribution'].search_count([('member_id', '=', rec.id)])
            contributions = rec.env['family.contribution'].search([('member_id', '=', rec.id)])
            total_cost = 0
            if contributions:
                for c in contributions:
                    total_cost += c.amount
            rec.contribution_count = contribution_count
            rec.total_cost = total_cost

    def action_open_contributions(self):
        return {
            'name': _("Contributions"),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'family.contribution',
            'domain': [('member_id', '=', self.id)],
            'target': 'current',
        }
