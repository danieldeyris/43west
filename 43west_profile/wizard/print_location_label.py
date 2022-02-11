# -*- coding: utf-8 -*-
# Copyright 2016 Syleam
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields


class PrintLocationLabel(models.TransientModel):
    _name = 'wizard.print.location.label'
    _description = 'Print Location Label'

    printer_id = fields.Many2one(comodel_name='printing.printer', string='Printer', required=True, help='Printer used to print the labels.')
    label_id = fields.Many2one(comodel_name='printing.label.zpl2', string='Label', required=True, domain=lambda self: [('model_id.model', '=', self.env.context.get('active_model'))], help='Label to print.')

    def print_label(self):
        """
        Prints a label per selected location
        """
        for location_id in self.env['stock.location'].browse(self.env.context['active_ids']):
            self.label_id.print_label(self.printer_id, location_id)
