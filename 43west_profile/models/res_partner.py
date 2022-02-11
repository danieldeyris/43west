# -*- coding: utf-8 -*-
# Copyright 2016 Syleam
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    country_id = fields.Many2one(default=lambda self: self.env['res.country'].search([('code', '=', 'FR')])[0])
