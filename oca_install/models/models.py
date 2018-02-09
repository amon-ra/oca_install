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
# from openerp.osv import fields as fields_old
# import openerp.addons.decimal_precision as dp
import subprocess, os
import logging,re

logger = logging.getLogger(__name__)


class GitInstaller(models.TransientModel):
    _name = 'oca.installer'
    _description = 'OCA addons installer'

    oca_download_path = fields.Char(required=True, string='Oca download path',help='Ensure you have permision in this directory')
    addon_symlink = fields.Boolean(required=True, string='Add module to system path')
    oca_addon_path = fields.Char(required=True, string='Odoo addon path' )

    oca_addon_base_url = fields.Char(string='Oca addon base url',required=True)

    system_addon_path = fields.Text(string='Config string addons path',help='Append this to configuration addons path')

    name = fields.Char(required=True, string='OCA Repo Name' )
    tree = fields.Char('Tree')

    def git_download(self, system_addon_path, name, path, tree=False, base_url=False):
        if name.startswith('http://') or name.startswith('https://') or name.startswith('git://'):
            l = name.split('/')
            url=name
            name = l[-1]
            if not base_url:
                base_url = '/'.join(l[:-1])          
        else:
            assert base_url, "no base url" 
            url=base_url+"/"+name

        #return if already downloaded
        destination = os.path.join(path,name)
        if destination in system_addon_path:
            return system_addon_path
        if not os.path.exists(destination):
            if tree:
                p = subprocess.Popen(['/usr/bin/git','clone','-b',tree,'--depth','1', url,
                                    os.path.join(path,name)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            else:
                p = subprocess.Popen(['/usr/bin/git','clone','--depth','1', url,
                                    os.path.join(path,name)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output, errors = p.communicate()
            logger.info("{}\n{}".format(output,errors))
            if os.path.exists(os.path.join(path,name,'__openerp__.py')):
                os.rename(os.path.join(path,name),os.path.join(path,name,'_'+name))
                os.mkdir(os.path.join(path,name))
                os.rename(os.path.join(path,name,'_'+name),os.path.join(path,name,name))
        if self.addon_symlink:
            tree_path = os.path.join(path,name)
            for f in os.listdir(tree_path):
                logger.info(self.oca_addon_path)
                logger.info(tree_path)
                logger.info(f)
                if not os.path.isfile(os.path.join(tree_path,f)) and not os.path.exists(os.path.join(
                self.oca_addon_path,f)) and not f.startswith('.'):
                    os.symlink(os.path.join(tree_path,f),os.path.join(self.oca_addon_path,f))
                                   
        try:
            system_addon_path.append(os.path.join(path,name))
            with open(os.path.join(path, name, 'oca_dependencies.txt'), 'r') as f:
                for line in f:
                    line=line.strip()
                    if line.startswith('#'):
                        continue
                    arr = re.split(r'\s+',line)
                    try:
                        if arr[1] != '':
                            line = arr[1]
                        else:
                            line = arr[0]
                    except:
                        line = arr[0] 
                    line = line.strip()
                    if line:
                        system_addon_path = self.git_download(system_addon_path,line,path,tree,base_url)
                    # if line.startswith('http://') or line.startswith('https://') or line.startswith('git://'):
                    #     system_addon_path = self.git_download(system_addon_path,line,path,tree,base_url)
                    # else:
                    #     system_addon_path = self.git_download(system_addon_path,line, path,tree,base_url)
        except IOError:
            pass
        return system_addon_path

    # @api.one
    # def create(self):
    #     #logger.error(str(self.name))
    #     #logger.error(str(self.oca_addon_base_url))
    #     #logger.error(str(self.oca_addon_path))
    #     self.git_download(self.name, self.oca_addon_path, self.oca_addon_base_url)
    #     return {
    #                  'name' : 'Modulos locales',
    #                  'view_type' : 'form',
    #                  'view_mode' : 'form',
    #                  'view_id': False,
    #                  'res_model' : 'ir.module.module',
    #                  'context' : self._context,
    #                  'type' : 'ir.actions.act_window',
    #                  'target' : 'current',
    #
    #                  }

    @api.one
    def action_install(self):
        #logger.error(str(self.name))
        #logger.error(str(self.oca_addon_base_url))
        #logger.error(str(self.oca_addon_path))

        self.system_addon_path =  ','.join(self.git_download([], self.name, self.oca_download_path, tree=self.tree,
                                                    base_url=self.oca_addon_base_url))
