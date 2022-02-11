# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

import logging

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'

    def fix_for_version_15(self):

        _logger.info("Fix unit")
        for unit in self.env['uom.uom'].search([('measure_type', '=', False)]):
            sql_request = "UPDATE uom_uom set measure_type = 'unit', category_id = 1 where id = %s" % unit.id
            self.env.cr.execute(sql_request)
        self.env.cr.commit()

        for product in self.env['product.product'].search([('type', '=', 'product')]):
            fix = False
            for move in self.env['stock.move.line'].search([('product_id', '=', product.id), ('product_uom_id', '!=', product.uom_id.id)]):
                sql_request = "UPDATE stock_move_line set product_uom_id = %s where id = %s" % (product.uom_id.id, move.id)
                self.env.cr.execute(sql_request)
                fix = True

            for move in self.env['stock.move'].search([('product_id', '=', product.id), ('product_uom', '!=', product.uom_id.id)]):
                sql_request = "UPDATE stock_move set product_uom = %s where id = %s" % (product.uom_id.id, move.id)
                self.env.cr.execute(sql_request)
                fix = True

            if fix:
                _logger.error("Fix product %s" % product.name)
        self.env.cr.commit()

        #
        # # suprimer action serveur de modification de la osition fiscale
        # self.env['ir.actions.server'].browse(999).unlink()
        # self.env['base.automation'].browse(34).unlink()
        #
        # # fix fiscal position France
        # self.env['account.fiscal.position'].browse(1).write({'vat_required': False})
        #
        # self.env.cr.commit()
        #
        # for company in self.env['res.company'].search([('id', '=', 1)]):
        #     # Correction des compte comptables client
        #     nb_partner_fix = 0
        #     nb_partner_processed = 0
        #     account_receivable = self.env['account.account'].with_company(company).search([('code', '=', '411100')], limit=1)
        #
        #     account_payable = self.env['account.account'].with_company(company).search([('code', '=', '401100')], limit=1)
        #     if not account_receivable:
        #         _logger.error("Account 411100 not found for company : %s" % company.name)
        #         return
        #
        #     if not account_payable:
        #         _logger.error("Account 401100 not found for company : %s" % company.name)
        #         return
        #     # veepee
        #     account_receivable_veepee = self.env['account.account'].with_company(company).search([('code', '=', '411110')], limit=1)
        #     if not account_receivable_veepee:
        #         account_receivable_veepee = account_receivable.copy({'code': '411110', 'name': 'Ventes de biens ou de prestations de services VEEPEE'})
        #     category_weepee = self.env["res.partner.category"].browse(4)
        #
        #     _logger.info("process company : %s" % company.name)
        #
        #     partners_to_fix = self.env['res.partner'].search([])
        #     for partner in partners_to_fix:
        #         nb_partner_processed += 1
        #         # re init fiscal position
        #         if partner.with_company(company).property_account_position_id:
        #             partner.with_company(company).property_account_position_id = False
        #
        #         partner_account_receivable = partner.with_company(company).property_account_receivable_id
        #         partner_account_payable = partner.with_company(company).property_account_payable_id
        #
        #         customer_account = account_receivable
        #         # Clients
        #         if partner_account_receivable.code != customer_account.code and partner_account_receivable.code > '999999':
        #             nb_partner_fix += 1
        #             # if nb_partner_fix > 10:categ
        #             #     return
        #             _logger.info("Fix customer : %s" % partner.name)
        #             #chagement de compte des écritures
        #             move_lines = self.env['account.move.line'].with_company(company).search([('account_id', '=', partner_account_receivable.id)])
        #             for move_line in move_lines:
        #                 sql_request = 'UPDATE account_move_line set account_id = %s where id = %s' % (customer_account.id, move_line.id)
        #                 self.env.cr.execute(sql_request)
        #             partner_account_receivable.deprecated = True
        #             partner.with_company(company).property_account_receivable_id = customer_account
        #             if nb_partner_fix % 10 == 0:
        #                 self.env.cr.commit()
        #
        #         # Fournisseurs
        #         if partner_account_payable.code != account_payable.code and partner_account_payable.code > '999999':
        #             nb_partner_fix += 1
        #             _logger.info("Fix vendor : %s" % partner.name)
        #             #chagement de compte des écritures
        #             move_lines = self.env['account.move.line'].with_company(company).search([('account_id', '=', partner_account_payable.id)])
        #             for move_line in move_lines:
        #                 sql_request = 'UPDATE account_move_line set account_id = %s where id = %s' % (account_payable.id, move_line.id)
        #                 self.env.cr.execute(sql_request)
        #             partner_account_payable.deprecated = True
        #             partner.with_company(company).property_account_payable_id = account_payable
        #             if nb_partner_fix % 10 == 0:
        #                 self.env.cr.commit()
        #
        #         if nb_partner_processed % 1000 == 0:
        #             _logger.info("Partner processed : %s" % nb_partner_processed)
        #             self.env.cr.commit()
        #     self.env.cr.commit()
        #
        #     accounts = self.env['account.account'].with_company(company).search([('code', '>', '999999'), ('deprecated', '=', False ), ('group_id', '=', 87)])
        #     # suppression des compte inutiles,
        #     #accounts.filtered(lambda c: not c.used).unlink()
        #     for account in accounts:
        #         _logger.info("process account : %s" % account.code)
        #         move_lines = self.env['account.move.line'].with_company(company).search([('account_id', '=', account.id)])
        #         for move_line in move_lines:
        #             sql_request = 'UPDATE account_move_line set account_id = %s where id = %s' % (account_receivable.id, move_line.id)
        #             self.env.cr.execute(sql_request)
        #         account.deprecated = True
        #         self.env.cr.commit()
        #
        #     accounts = self.env['account.account'].with_company(company).search([('id', '=', 14715)])
        #     # suppression des compte inutiles,
        #     #accounts.filtered(lambda c: not c.used).unlink()
        #     for account in accounts:
        #         _logger.info("process account : %s" % account.code)
        #         move_lines = self.env['account.move.line'].with_company(company).search([('account_id', '=', account.id)])
        #         for move_line in move_lines:
        #             sql_request = 'UPDATE account_move_line set account_id = %s where id = %s' % (account_receivable.id, move_line.id)
        #             self.env.cr.execute(sql_request)
        #         account.deprecated = True
        #         self.env.cr.commit()
        #
        #     # Fix vepee
        #     for partner in partners_to_fix:
        #         if category_weepee in partner.with_company(company).category_id and partner.with_company(company).property_account_receivable_id.id != account_receivable_veepee.id:
        #             _logger.info("Vepee customer : %s" % partner.name)
        #             partner.with_company(company).property_account_receivable_id = account_receivable_veepee
        #     self.env.cr.commit()
        #
        #     # transfert vepee
        #     move_lines = self.env['account.move.line'].with_company(company).search([('account_id', '=', account_receivable.id)])
        #     for move in move_lines:
        #         partner_account = move.partner_id.with_company(company).property_account_receivable_id
        #         if move.partner_id and partner_account.id != move.account_id.id and partner_account.id == account_receivable_veepee.id:
        #             _logger.info("Vepee move : %s" % move.id)
        #             sql_request = 'UPDATE account_move_line set account_id = %s where id = %s' % ( account_receivable_veepee.id, move.id)
        #             self.env.cr.execute(sql_request)
        #     self.env.cr.commit()
