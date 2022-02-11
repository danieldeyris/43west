# -*- coding: utf-8 -*-
# Copyright 2016 Syleam
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_quotation_send(self):
        '''  Override to use a modified template that includes a portal signup link '''
        action_dict = super(SaleOrder, self).action_quotation_send()
        try:
            template_id = self.env['ir.model.data'].get_object_reference('43west_profile', 'email_template_edi_sale')[1]
            # assume context is still a dict, as prepared by super
            ctx = action_dict['context']
            ctx['default_template_id'] = template_id
            ctx['default_use_template'] = True
        except Exception:
            pass
        return action_dict

    def action_confirm(self):
        StockWarehouseOrderpoint = self.env['stock.warehouse.orderpoint']
        for order in self:
            for line in order.order_line.filtered('product_id.countermark_ok'):
                product = line.product_id.copy(default={
                    'name': line.name,
                    'description_sale': line.name,
                    'sale_ok': False,
                    'purchase_ok': False,
                    'use_as_countermark': True,
                })
                suppliers_info = line.product_id.product_tmpl_id.seller_ids[-1]
                if suppliers_info:
                    suppliers_info.copy(default={
                        'product_tmpl_id': product.product_tmpl_id.id,
                    })
                orderpoints = StockWarehouseOrderpoint.search([('product_id', '=', line.product_id.id)])
                for orderpoint in orderpoints:
                    orderpoint.copy(default={
                        'product_id': product.id,
                        'product_min_qty': 0.,
                        'product_max_qty': 0.,
                    })

                line.product_id = product.id
        super(SaleOrder, self).action_confirm()
