# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrLeaveInherit(models.Model):
    _inherit = 'hr.leave'

    def _compute_remaining(self):
        for rec in self:
            allocation = self.env['hr.leave.allocation'].search([('holiday_status_id', '=', rec.holiday_status_id.id)], limit=1)

            if allocation.type_request_unit == 'day':
                rec.remaining = str(int(allocation.max_leaves - allocation.leaves_taken)) + ' days'
            elif allocation.type_request_unit == 'half_day':
                rec.remaining = str(int(allocation.max_leaves - allocation.leaves_taken)) + ' days'
            elif allocation.type_request_unit == 'hour':
                rec.remaining = str(int(allocation.max_leaves - allocation.leaves_taken)) + ' hours'
            else:
                rec.remaining = 'None'

    remaining = fields.Char(string='Remaining (Days/Hours)', compute='_compute_remaining')
