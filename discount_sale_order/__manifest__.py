# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "Discount On Sale Order",
  "summary"              :  "Discount on order line and sales order along with global discount",
  "category"             :  "Website",
  "version"              :  "1.3.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Discount-On-Sale-Order.html",
  "description"          :  """Discount with fixed type on order line and global discount on order""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=discount_sale_order&version=12.0",
  "depends"              :  ['sale_management', 'account'],
  "data"                 :  [
                             'views/sale_views.xml',
                             'views/account_invoice_view.xml',
                             'views/sale_config_setting_view.xml',
                             'report/sale_report_templates.xml',
                             'report/report_invoice.xml',
                             'security/discount_security.xml',
                            ],
  "demo"                 :  [
                             'data/discount_data.xml',
                             'data/discount_demo.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  25,
  "currency"             :  "EUR",
#  "pre_init_hook"        :  "pre_init_check",
}
