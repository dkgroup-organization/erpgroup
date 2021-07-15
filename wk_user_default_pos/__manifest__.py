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
  "name"                 :  "Restrict User To Default POS",
  "summary"              :  "Provide access to a single specific POS to the user using the is module. Once restricted, the user can see and use only his designated POS in Odoo.",
  "category"             :  "Point of Sale",
  "version"              :  "1.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Restrict-User-To-Default-POS.html",
  "description"          :  """Odoo Restrict User To Default POS
Odoo POS Restrict User To Default POS
User access POS
POS user access
Allow POS access
Assign default POS""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=wk_user_default_pos",
  "depends"              :  ['point_of_sale'],
  "data"                 :  [
                             'views/res_user_view.xml',
                             'security/default_pos_security.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  17,
  "currency"             :  "EUR",
}