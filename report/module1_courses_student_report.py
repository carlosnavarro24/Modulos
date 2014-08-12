import pooler
from report import report_sxw
from tools.translate import _

class Courses_Student(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(Courses_Student, self).__init__(cr, uid, name, context=context)
        self.pool = pooler.get_pool(self.cr.dbname)
        
        self.localcontext.update({
            'cr' : cr,
            'uid': uid,
            'get_student_by_id': self.get_student_by_id, 
            'get_course_by_student':self.get_course_by_student,
            'get_task_by_student_course':self.get_task_by_student_course,
            'get_qualify_task':self.get_qualify_task,
            'get_qualify_course':self.get_qualify_course,
        })    
        #====Display data in mako==========================================================
    def get_student_by_id(self, cr, uid,student_id):
        student_obj = self.pool.get('module1.student')
        student = student_obj.browse(cr, uid, [student_id])[0]
        return student
    def get_course_by_student(self, cr, uid,student_id):
        field=[]
        enrollments = self.pool.get('module1.enrollment').search(cr, uid,[('student_id','=',student_id)])
        for enrollment in self.pool.get('module1.enrollment').browse(cr, uid, enrollments):
            field.append(enrollment.course_id.id)
        courses = self.pool.get('module1.course').browse(cr, uid,field)
        return courses
    def get_task_by_student_course(self, cr, uid,student_id,course_id):
        field=[]
        results= self.pool.get('module1.result').search(cr, uid,[('student_id','=',student_id),('course_id','=',course_id)])
        for result in self.pool.get('module1.result').browse(cr, uid, results):
            field.append(result.task_id.id)
        tasks = self.pool.get('module1.task').browse(cr, uid,field)
        return tasks
    def get_qualify_course(self, cr, uid,student_id, course_id):
        res = 0.00
        results= self.pool.get('module1.result').search(cr, uid,[('student_id','=',student_id),('course_id','=',course_id)])
        for result in self.pool.get('module1.result').browse(cr, uid, results):
            res+=result.qualify
        return res
    
    def get_qualify_task(self, cr, uid,student_id, course_id,task_id):
        res = 0.00
        results= self.pool.get('module1.result').search(cr, uid,[('student_id','=',student_id),('course_id','=',course_id),('task_id','=',task_id)])
        for result in self.pool.get('module1.result').browse(cr, uid, results):
            res+=result.qualify
        return res
                
report_sxw.report_sxw(
    'report.test_1',
    'module1.student',
    'addons/module1/report/module1/report/test2_ods.ods',
    parser=Courses_Student)

