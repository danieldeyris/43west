# -*- coding: utf-8 -*-
# Copyright 2016 Syleam
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields


class PrintProductLabel(models.TransientModel):
    _name = 'wizard.print.product.label'
    _description = 'Print Product Label'

    printer_id = fields.Many2one(comodel_name='printing.printer', string='Printer', required=True, help='Printer used to print the labels.')
    label_id = fields.Many2one(comodel_name='printing.label.zpl2', string='Label', required=True, domain=lambda self: [('model_id.model', '=', self.env.context.get('active_model'))], help='Label to print.')

    @api.model
    def default_get(self, fields_list):
        """
        Pre-populate wizard lines on creation, depending on the selected picking
        """
        values = super(PrintProductLabel, self).default_get(fields_list)
        printers = self.env['printing.printer'].search([])
        if len(printers) == 1:
            values['printer_id'] = printers.id

        labels = self.env['printing.label.zpl2'].search([('model_id.model', '=', 'product.product')])
        if len(labels) == 1:
            values['label_id'] = labels.id

        return values

    def print_label(self):
        """
        Prints a label per selected location
        """
        for product in self.env['product.product'].browse(self.env.context['active_ids']):
            self.label_id.print_label(self.printer_id, product, page_count=1, lot=False)
