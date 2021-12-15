# -*- coding: utf-8 -*-
from odoo import api, fields, models

# create model Patient reference to table in the database


class SaleOrder(models.Model):
    # on veut heriter du module existe déjà
    _inherit = "sale.order"

    sale_description = fields.Char(string='Sale Description')


