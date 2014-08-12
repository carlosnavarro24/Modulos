import pooler
from report import report_sxw
from tools.translate import _
from openerp.addons.account_report_lib.account_report_base import accountReportbase

class Parser(accountReportbase):

    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context=context)
        self.pool = pooler.get_pool(self.cr.dbname)
        self.cursor = self.cr

        self.localcontext.update({
            'cr': cr,
            'uid': uid,
            'storage':{},
            'display_student_id': self.display_student_id, 
            'display_courses_student':self.display_courses_student,
            'display_tasks_student':self.display_tasks_student,
            'display_qualify_course':self.display_qualify_course,
            'display_qualify_task':self.display_qualify_task,
            'get_student_id':self.get_student_id,
        })



     #====Extract data from wizard==============================================    
    def get_student_id(self, data):
        return self._get_form_param('student_id', data)
    

        
    #==========================================================================
    #====Display data==========================================================
    
    def display_student_id(self,cr,uid, data):
        student_id = self.get_student_id(data)
        student_obj = self.pool.get('module1.student')
        student = student_obj.browse(cr, uid, student_id)
        return student
    
    def display_courses_student(self, cr, uid,data):
        field=[]
        student_id = self.get_student_id(data)
        enrollments = self.pool.get('module1.enrollment').search(cr, uid,[('student_id','=',student_id)])
        for enrollment in self.pool.get('module1.enrollment').browse(cr, uid, enrollments):
            field.append(enrollment.course_id.id)
        courses = self.pool.get('module1.course').browse(cr, uid,field)
        return courses
    def display_tasks_student(self, cr, uid,data,course_id):
        field=[]
        student_id = self.get_student_id(data)
        results= self.pool.get('module1.result').search(cr, uid,[('student_id','=',student_id),('course_id','=',course_id)])
        for result in self.pool.get('module1.result').browse(cr, uid, results):
            field.append(result.task_id.id)
        tasks = self.pool.get('module1.task').browse(cr, uid,field)
        return tasks
    def display_qualify_course(self, cr, uid,data, course_id):
        res = 0.00
        student_id = self.get_student_id(data)
        results= self.pool.get('module1.result').search(cr, uid,[('student_id','=',student_id),('course_id','=',course_id)])
        for result in self.pool.get('module1.result').browse(cr, uid, results):
            res+=result.qualify
        return res
    
    def display_qualify_task(self, cr, uid,data, course_id,task_id):
        res = 0.00
        student_id = self.get_student_id(data)
        results= self.pool.get('module1.result').search(cr, uid,[('student_id','=',student_id),('course_id','=',course_id),('task_id','=',task_id)])
        for result in self.pool.get('module1.result').browse(cr, uid, results):
            res+=result.qualify
        return res
  
