# -*- coding: utf-8 -*-
# Copyright 2016 Syleam
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': '43 West Profile',
    'version': '12.0.1.0.0',
    'category': 'Custom',
    'summary': 'Profile for 43 West',
    'author': 'Sebastien LANGE',
    'website': 'http://www.syleam.fr',
    'depends': [
        'base',
        'sale',
        'purchase',
        'stock',
        'account',
        'mail',
    ],
    'data': [
        'security/43west_security.xml',
        'data/base.xml',
        'data/printing_label_zpl2.xml',
        'data/mail_template.xml',
        'views/product_supplierinfo.xml',
        'views/stock.xml',
        'views/product_template.xml',
        'wizard/print_location_label.xml',
        'wizard/print_receipt_labels.xml',
        'wizard/print_product_label.xml',
        'data/report_paperformat.xml',
        'reports/header.xml',
        'reports/footer.xml',
        'reports/saleorder.xml',
        'reports/invoices.xml',
        'reports/stock_picking.xml',
        'reports/purchaseorder.xml',
        'reports/purchasequotation.xml',
        'reports/delivery_slip.xml'
    ],
    'installable': True,
    'auto_install': False,
    'license': 'AGPL-3',
}
