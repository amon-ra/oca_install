# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from openerp import models, fields, api, tools, _
import os
# from openerp.osv import fields as fields_old
# import openerp.addons.decimal_precision as dp


class OcaGitInstallSettings(models.TransientModel):
    _name = 'oca.install.settings'
    _inherit = 'res.config.settings'


    def _default_oca_addon_path(self):
        if os.environ.get('XDG_DATA_HOME',False):
            return  os.path.join(os.environ['XDG_DATA_HOME'],'Odoo','addons','10.0')
            # os.path.join(os.environ['XDG_DATA_HOME'],'src'))
        else:
            return os.path.join(os.environ.get('HOME','/var/lib/odoo'),'addons','10.0')
            # default_oca_download_path = fields.Char(default_model='oca.installer',default=os.path.join(os.environ.get('HOME','/var/lib/odoo'),'src'))

    def _default_oca_download_path(self):
        if os.environ.get('XDG_DATA_HOME',False):
            return os.path.join(os.environ['XDG_DATA_HOME'],'src') 
        else:
            return os.path.join(os.environ.get('HOME','/var/lib/odoo'),'src') 

    default_oca_addon_base_url = fields.Char(default_model='oca.installer',default='https://github.com/OCA')

    default_oca_addon_path = fields.Char(default_model='oca.installer',default=_default_oca_addon_path)

    default_oca_download_path = fields.Char(default_model='oca.installer',default=_default_oca_download_path)


    default_addon_symlink = fields.Boolean(default_model='oca.installer',default=True)
