# -*- coding: utf-8 -*-
# Copyright 2016 Syleam
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    type = fields.Selection(default='product')
    countermark_ok = fields.Boolean(string='Is a Countermak', default=False, copy=False, help='If set, this product will be replace by new one before confirm sale order.')
    use_as_countermark = fields.Boolean(string='Use as Countermark', default=False, copy=False, help='Is set, this product is used in sale order')
