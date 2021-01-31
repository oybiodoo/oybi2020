from  psycopg2 import ProgrammingError,OperationalError,InterfaceError,DatabaseError,DataError,IntegrityError,InternalError,NotSupportedError
from odoo import models, fields, api,_
from odoo.exceptions import except_orm,UserError
import re

class SqlQueryControl(models.Model):
    _name = 'sql.query.control'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name='sql_instruction'

    msgs={
            'select':_('You do not have permission for the select command, contact the administrator.'),
            'insert':_('You do not have permission for the insert command, contact the administrator.'),
            'update':_('You do not have permission for the update command, contact the administrator.'),
            'delete':_('You do not have permission for the delete command, contact the administrator.'),
            'replace':_('You do not have permission for the replace command, contact the administrator.'),
            'truncate':_('You do not have permission for the truncate command, contact the administrator.'),
            }

    sql_instruction = fields.Text(
                                string="SQL Instruction",
                                default="select * from res_partner;",
                                track_visibility='onchange')

    msg=fields.Char(string=' ',readonly=True)

    html_field = fields.Html(
                            string='sql result',
                            readonly=True,
                            help="Enter an sql statement to execute in the Postgres database")

    alias_id = fields.Many2one('mail.alias', string='Alias', ondelete="restrict", required=False,
        help=_("Internal email associated with this project. Incoming emails are automatically synchronized "
             "with Tasks (or optionally Issues if the Issue Tracker module is installed)."))

    def excute_select(self):
        try:
            result_row = self.env.cr.dictfetchall()
            thead="<tr>"
            tds=""
            table="""
                <div style="height:400px; overflow-y:hidden; overflow: scroll;">
                <table class="table">
                    %s
                    <tbody class="body-dark">
                    %s
                    </tbody>
                    </table>
                """
            cant=len(result_row)
            if cant:
                check_query=True
                thead+="<thead><tr><th scope='col'>#</th>"
                theadkeys = result_row[0].keys()
                for key in theadkeys:
                    thead+="""
                    <th scope="col">%s</th>
                    """ % key
                thead+="</tr></thead>"
            self.msg=cant
            cant=1
            for row in result_row:
                tds+="<tr><td>%s</td>" % cant
                cant+=1
                for value in row:
                    tds+="<td>%s</td>" % row[value]
                tds+="</tr>"
            table_out=table % (thead,tds)
            self.html_field=table_out
        except (ProgrammingError,OperationalError,InterfaceError,
        DatabaseError,DataError,IntegrityError,InternalError,
        NotSupportedError) as e:
            raise UserError(e.pgerror)

    def capture_sql_field(self):
        if self.sql_instruction:
            query="%s"%self.sql_instruction
            lower_query=query.lower()
            convert_lower_query=lower_query.split(' ')
            evaluate=[
                        'select',
                        'insert',
                        'update',
                        'delete',
                        'replace',
                        'truncate',
                        'create',
                        'drop',
                        'alter'  ]

            grupo=self.env.user.has_group('sql_query_excecute.select_sql_user')
            if self.env.user.has_group('sql_query_excecute.select_sql_user'):
                evaluate.remove("select")
            if self.env.user.has_group('sql_query_excecute.insert_sql_user'):
                evaluate.remove("insert")
            if self.env.user.has_group('sql_query_excecute.update_sql_user'):
                evaluate.remove("update")
            if self.env.user.has_group('sql_query_excecute.delete_sql_user'):
                evaluate.remove("delete")

            for i in convert_lower_query:
                if i in evaluate:
                    raise UserError(_(self.msgs[i]))
            for retrict in evaluate:
                patron = re.compile(retrict)
                match = patron.search(lower_query)
                if match:
                    raise UserError(_(self.msgs[retrict]))
            try:
                self._cr.execute(query)
            except (ProgrammingError,OperationalError,InterfaceError,
            DatabaseError,DataError,IntegrityError,InternalError,
            NotSupportedError) as e:
                code_error='Code Error: %s'%e.pgcode
                error=e.pgerror
                error_message="""%s
                %s""" % (code_error,error)
                raise UserError(error_message)
                return
            for i in convert_lower_query:
                if i == 'select':
                    self.excute_select()
                    return

            self.message()

    def message(self):
        convert_lower_list_query=(self.sql_instruction.lower()).split(' ')
        for i in convert_lower_list_query:
            if i == 'insert':
                type_query='Insert'

            elif i == 'update':
                type_query='Update'

            elif i == 'delete':
                type_query='Delete'

        msg=_('%s - successful consultation!') % type_query
        self.html_field='<div class="alert alert-success">%s</div>' % msg
