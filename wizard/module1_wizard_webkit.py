from osv import fields,osv

class report_wizard_webkit(osv.TransientModel):
    _name='module1.report_wizard_webkit'
    _columns={
              'student_id':fields.many2one('module1.student',string="Student Name" ,required=True),
              }
    
    def pre_print_report_webkit(self, cr, uid, ids, data, context=None):       
        if context is None:
            context = {}
        data = {}
        data['ids'] = context.get('active_ids', [])
        data['model'] = context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(cr, uid, ids, ['student_id'], context=context)[0]
        for field in ['student_id']:
            if isinstance(data['form'][field], tuple):
                data['form'][field] = data['form'][field][0]         
        return data

    
    def _print_report_webkit(self, cr, uid, ids, data, context={}):
        data = self.pre_print_report_webkit(cr, uid, ids, data, context=context)
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'test_1',
            'datas': data
            }

    def action_go_report(self, cr, uid, ids, context={}):        
            data={}
            report=self.read(cr,uid,ids,['report_type'],context=context)[0]
            return self._print_report_webkit(cr, uid, ids, data, context=context)
           
            
    
    