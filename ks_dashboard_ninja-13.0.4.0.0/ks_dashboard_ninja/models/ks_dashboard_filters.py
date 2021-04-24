from odoo import models, fields, api, _


class KsDashboardNinjaTemplate(models.Model):
    _name = 'ks_dashboard_ninja.board_defined_filters'
    _description = 'Dashboard Ninja Defined Filters'

    name = fields.Char("Filter Label")
    ks_dashboard_board_id = fields.Many2one('ks_dashboard_ninja.board', string="Dashboard")
    ks_model_id = fields.Many2one('ir.model', string='Model',
                                  domain="[('access_ids','!=',False),('transient','=',False),"
                                         "('model','not ilike','base_import%'),('model','not ilike','ir.%'),"
                                         "('model','not ilike','web_editor.%'),('model','not ilike','web_tour.%'),"
                                         "('model','!=','mail.thread'),('model','not ilike','ks_dash%')]",
                                  help="Data source to fetch and read the data for the creation of dashboard items. ")
    ks_domain = fields.Char(string="Domain", help="Define conditions for filter. ")
    ks_domain_temp = fields.Char(string="Domain Substitute")
    ks_model_name = fields.Char(related='ks_model_id.model', string="Model Name")
    display_type = fields.Selection([
        ('line_section', "Section")], default=False, help="Technical field for UX purpose.")
    sequence = fields.Integer(default=10,
                              help="Gives the sequence order when displaying a list of payment terms lines.")
    ks_is_active = fields.Boolean(string="Active")


class KsDashboardNinjaTemplate(models.Model):
    _name = 'ks_dashboard_ninja.board_custom_filters'
    _description = 'Dashboard Ninja Custom Filters'

    name = fields.Char("Filter Label")
    ks_dashboard_board_id = fields.Many2one('ks_dashboard_ninja.board', string="Dashboard")
    ks_model_id = fields.Many2one('ir.model', string='Model',
                                  domain="[('access_ids','!=',False),('transient','=',False),"
                                         "('model','not ilike','base_import%'),('model','not ilike','ir.%'),"
                                         "('model','not ilike','web_editor.%'),('model','not ilike','web_tour.%'),"
                                         "('model','!=','mail.thread'),('model','not ilike','ks_dash%')]",
                                  help="Data source to fetch and read the data for the creation of dashboard items. ")
    ks_domain_field_id = fields.Many2one('ir.model.fields',
                                         domain="[('model_id','=',ks_model_id),"
                                                "('name','!=','id'),('store','=',True),"
                                                "('ttype', 'in', ['boolean', 'char', "
                                                "'date', 'datetime', 'float', 'integer', 'html', 'many2many', "
                                                "'many2one', 'monetary', 'one2many', 'text', 'selection'])]",
                                         string="Domain Field")
