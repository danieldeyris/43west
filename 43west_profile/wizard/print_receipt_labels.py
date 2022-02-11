# -*- coding: utf-8 -*-
# Copyright 2016 Syleam
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields


class PrintReceiptLabelsLine(models.TransientModel):
    _name = 'wizard.print.receipt.labels.line'
    _description = 'Print Receipt Line'

    wizard_id = fields.Many2one(comodel_name='wizard.print.receipt.labels', string='Print Wizard', required=True, help='Printing wizard linked to this line.')
    product_id = fields.Many2one(comodel_name='product.product', string='Product', required=True, help='Product to print on the label.')
    prodlot_id = fields.Many2one(comodel_name='stock.production.lot', string='Lot', readonly=True, help='Lot to print on the label, if defined.')
    count = fields.Integer(string='Labels Count', default=1, help='Number of labels to print for this product/lot.')


class PrintReceiptLabels(models.TransientModel):
    _name = 'wizard.print.receipt.labels'
    _description = 'Print Receipt Labels'

    printer_id = fields.Many2one(comodel_name='printing.printer', string='Printer', required=True, help='Printer used to print the labels.')
    label_id = fields.Many2one(comodel_name='printing.label.zpl2', string='Label', required=True, domain=lambda self: [('model_id.model', '=', 'product.product')], help='Label to print.')
    line_ids = fields.One2many(comodel_name='wizard.print.receipt.labels.line', inverse_name='wizard_id', string='Lines', help='Lines to print on labels.')

    def print_labels(self):
        """
        Prints a label per product/lot in the selected receipt
        """
        for wizard in self:
            for line in wizard.line_ids:
                if line.prodlot_id:
                    self.label_id.print_label(self.printer_id, line.product_id, page_count=line.count, lot=line.prodlot_id)
                else:
                    self.label_id.print_label(self.printer_id, line.product_id, page_count=line.count, lot=False)

    @api.model
    def default_get(self, fields_list):
        """
        Pre-populate wizard lines on creation, depending on the selected picking
        """
        values = super(PrintReceiptLabels, self).default_get(fields_list)
        printers = self.env['printing.printer'].search([])
        if len(printers) == 1:
            values['printer_id'] = printers.id

        labels = self.env['printing.label.zpl2'].search([('model_id.model', '=', 'product.product')])
        if len(labels) == 1:
            values['label_id'] = labels.id

        values['line_ids'] = []
        for picking in self.env['stock.picking'].browse(self.env.context['active_ids']):
            for operation in picking.move_line_ids_without_package:
                line_data = {'product_id': operation.product_id.id, 'count': 1}
                if operation.lot_id:
                    line_data['prodlot_id'] = operation.lot_id.id
                values['line_ids'].append((0, 0, line_data))

        return values
