# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectProjectInherit(models.Model):
    _inherit = 'project.project'

    @api.model
    def create(self, values):
        res = super(ProjectProjectInherit, self).create(values)
        sale_order = self.env['sale.order'].search([('name', '=', res.name)])
        if sale_order:
            if sale_order.user_id:
                res.user_id = sale_order.user_id
                print('USER IS: ', res.user_id.name)
        else:
            sale_order = self.env['sale.order'].search([])
            for order in sale_order:
                if res.name.find(order.name) != -1:
                    if order.user_id:
                        res.user_id = order.user_id
                        print('USER IS: ', res.user_id.name)
                        break
        return res
