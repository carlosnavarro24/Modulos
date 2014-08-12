from openerp.osv import osv, fields
import datetime
from openerp import tools

class student(osv.Model):
    _name='module1.student'
    
    def create(self, cr, uid, vals, context=None):
        sequence=self.pool.get('ir.sequence').get(cr, uid, 'module1.student')
        vals['student_code']=sequence
        return super(student, self).create(cr, uid, vals, context=context)
    _columns={
              'student_code' : fields.char('Student Code', size=64,readonly=True),
              'identification': fields.integer(string="Identification",required=True,help="Number Identification"),
              'name': fields.char(string="Full Name",size=128,required=True),
              'photo': fields.binary(string="Photo",filters='*.png,*.bmp,*.jpg'),
              'course_ids': fields.one2many('module1.enrollment','student_id', string="Course Assigned"),
              'result_ids': fields.one2many('module1.result','student_id',string="Tasks by Student"),
              'enrollment_ids': fields.one2many('module1.enrollment','student_id',string="Courses by Student")

              }
    #_defaults={
    #         'student_code':lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid,'module1.student'),
    #    }
    _sql_constraints=[
                     ('student_unique',
                      'UNIQUE(student_code)',
                      'Unique student_code'),
                       ('identification_unique',
                      'UNIQUE(identification)',
                      'Unique Identification')
                      
                     ]
    
    _order="identification,name"
    
class course(osv.Model):
    _name='module1.course'
    _columns={
              'code_course':fields.char(string="Course Code",size=3,required=True),
              'name':fields.char(string="Course Name",size=40,required=True),
              'teacher_id':fields.many2one('res.partner', string="Assigned Teacher",required=True,domain="[('teacher','=',True)]"),
              'task_ids': fields.one2many('module1.task','course_id', string="Task Assigned"),                   
              'enrollment_ids': fields.one2many('module1.enrollment','course_id',string="Students by Course"),
              'result_ids': fields.one2many('module1.result','course_id',string="Tasks by Course")
              }
    
    _sql_constraints=[
                      ('code_course',
                       'UNIQUE(code_course)',
                       'Unique code_course') 
                      
                    ]

    _order="code_course,name"

class resPartner(osv.Model):
     _inherit="res.partner"
     
     _columns = {
        'teacher':    fields.boolean(string="Teacher"),
        'course_ids':     fields.one2many('module1.course', 'teacher_id', string="Courses Asigned"),
    }

class task(osv.Model):
    _name='module1.task'
    
    def create(self, cr, uid, vals, context=None):
        new_task=super(task, self).create(cr, uid, vals, context=context)
        
        result_obj=self.pool.get('module1.result')
        enrollment_obj=self.pool.get('module1.enrollment')
        
        enrollments=enrollment_obj.search(cr, uid,[('course_id','=',vals['course_id'])])
        for enrollment  in enrollment_obj.browse(cr,uid,enrollments):
            new_result=result_obj.create(cr,uid,{
               'course_id': vals['course_id'],
               'student_id':enrollment.student_id.id,
               'task_id':new_task,
               'qualify':'0.00',
               'state':'assigned'
            },context=context)  
        return new_task
    
    _columns={
              'code_task':fields.char(string="Task Code",size=20,required=True),
              'name':fields.char(string="Task Name",size=40,required=True),
              'description':fields.text(string="Description",required=True),
              'assigned_date': fields.date(string="Assigned Date",required=True),
              'delivery_date': fields.datetime(string="Delivery Date Time",required=True),
              'qualify': fields.float(string="Qualify", size=3),
              'course_id': fields.many2one('module1.course', string="Course Assigned",required=True),
              'result_ids': fields.one2many('module1.result','task_id',string="Result Assigned")
              }
    
    _sql_constraints=[
                      ('code_task',
                       'UNIQUE(code_task)',
                       'Unique code_task') 
                      
                     ]
    
    _defaults = {
        'assigned_date':   fields.date.today,
        'delivery_date':   fields.date.today      
    }
    
    _order="code_task,name,course_id"

class enrollment(osv.Model):
    _name='module1.enrollment'
    
    def create(self, cr, uid, vals, context=None):
        new_enrollment=super(enrollment, self).create(cr, uid, vals, context=context)
        return new_enrollment
        #result_obj=self.pool.get('module1.result')
        #task_obj=self.pool.get('module1.task')
        
        #tasks=task_obj.search(cr, uid,[('course_id','=',vals['course_id'])])
        #for task  in task_obj.browse(cr,uid,tasks):
        #    new_result=result_obj.create(cr,uid,{
        #       'course_id': vals['course_id'],
        #       'student_id':vals['student_id'],
        #       'task_id':vals['id'],
        #       'qualify':'0.00',
        #       'state':'assigned'
        #    },context=context)  
        #return new_enrollment
                                                                                          
#Get sum of the qualifies of task by course and student
    def _get_qualifies(self, cr, uid, ids, fields, arg, context={}):
        res={}
        for enrollment in self.browse(cr,uid,ids,context=context):
                total=0.0
                results_obj = self.pool.get('module1.result')
                results=results_obj.search(cr, uid,[('student_id','=',enrollment.student_id.id),('course_id','=',enrollment.course_id.id)])
                for result in results_obj.browse(cr,uid,results):
                    total+=result.qualify
                res[enrollment.id]=total
        return res
#         for enrollment in self.browse(cr, uid, ids, context=context):
#             if enrollment.course_id and enrollment.student_id:
#                 sql_req= """
#                 select sum(r.qualify) as qualify from module1_result r 
#                 inner join module1_task t on r.task_id=t.id 
#                 where r.student_id=%d and t.course_id=%d
#                 """ % (enrollment.student_id,enrollment.course_id)
#                 cr.execute(sql_req)
#                 sql_res = cr.dictfetchone()
#                 if sql_res: 
#                     res[enrollment.id] = sql_res['qualify']
#                 else:
#                             
#                     res[enrollment.id] = 0
#         return res
    
    _columns={
              'course_id':fields.many2one('module1.course',string="Course Name",required=True),
              'student_id':fields.many2one('module1.student',string="Student Name",required=True),
              'qualify': fields.function(_get_qualifies,type="float", string="Course Qualify", readonly=True),          
              'color': fields.integer('Color'),
              }
    
    _sql_constraints = [
        ('enrollment_unique',
        'UNIQUE(course_id,student_id)',
        'The same student for the same course')
    ]
    _orders="course_id,student_id"
class result(osv.Model):
    _name='module1.result'
        
#    def get_domain_student(self, cr, uid, course):
#        field={}
#        enrollments = self.pool.get('module1.enrollment').search(cr, uid,[('course_id','=',course)])
#        for enrollment in self.pool.get('module1.enrollment').browse(cr, uid, enrollments):
#            v={'student_id':enrollment.student_id}
#        return {'domain':{'student_id':[('id','in',v)]}}
    
    #Domain: Obtain students and tasks by course 
    def action_assigned(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'assigned'}, context=context)
    
    def action_revised(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'revised'}, context=context)
    
    def action_done(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'done'}, context=context)
    
    def onchange_get_domain_course(self, cr, uid, ids, course):
        field=[]
        tasks = self.pool.get('module1.task').search(cr, uid,[('course_id','=',course)])
        enrollment_obj=self.pool.get('module1.enrollment')
        enrollments = enrollment_obj.search(cr, uid,[('course_id','=',course)])
        for enrollment in enrollment_obj.browse(cr, uid, enrollments):
            field.append(enrollment.student_id.id)
        students=self.pool.get('module1.student').search(cr,uid,[('id','in',field)])
        return {'domain':{'task_id':[('id','in',tasks)],'student_id':[('id','in',students)]}}  
        
    _columns={
              'course_id':fields.many2one('module1.course',string="Course Name",required=True),
              'task_id':fields.many2one('module1.task',string="Task Name",required=True),
              'student_id':fields.many2one('module1.student',string="Student Name",required=True),
              'qualify': fields.float(string="Qualify", size=3), 
              'state': fields.selection([('assigned','Assigned'),('revised','Revised'),('done','Done')], string="State"),
              }
    _defaults={
        'state':'assigned',
        }
    #constraint: the qualify by result no must not exceed the qualify by task
    def _check_qualify_task(self, cr, uid, ids, context={}):
        for result in self.browse(cr, uid, ids, context=context):
            if result.qualify>result.task_id.qualify:
                return False
        return True
    def _check_qualify_no_negative(self, cr, uid, ids, context={}):
        for result in self.browse(cr, uid, ids, context=context):
            if result.qualify<0:
                return False
        return True
    def _check_delivery_date(self, cr, uid, ids, context={}):
        for result in self.browse(cr, uid, ids, context=context):
            if result.task_id.delivery_date<datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"):
                return False
        return True
                
    _constraints = [
        (_check_qualify_no_negative,'Negatives results not allowed',['qualify']
         ),
        (
         _check_qualify_task,'It has exceeded the maximum qualify',['qualify']
         ),
         (_check_delivery_date,'It has exceeded the delivery date',['delivery_date]']
          )           
                    
    ]
    
    _sql_constraints = [
        ('result_unique',
        'UNIQUE(task_id,student_id)',
        'The same student for the same task')
     ]
    _order="course_id,student_id,task_id"
   