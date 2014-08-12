<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
		<link rel='stylesheet' href='addons/account_webkit_report_library/webkit_headers/main.css' />
        <style>
            ${css}
        </style>
    </head>
    <body class = "data">
        <% 
        	student_selected=data['form']['student_id']
        	student = get_student_by_id(cr, uid, student_selected) 
        %>
        <div style="font-size: 20px; font-weight: bold; text-align: center;"> ${company.partner_id.name}</div>
        <div style="font-size: 25px; font-weight: bold; text-align: center;"> ${_('Courses by Student')}</div>
        <br></br>
        <div style="font-size: 25px; font-weight: bold; text-align: left;"> ${_('Identification:')} ${student.identification}</div>
        <div style="font-size: 25px; font-weight: bold; text-align: left;"> ${_('Student Name:')} ${student.name}</div>
		<br></br>
        <%
        	courses_student=get_course_by_student(cr, uid, student_selected)
        %>
        <table class="table list" style="width: 70%; margin-left: auto; margin-right: auto;">
        	<tr class="table-cell" style="text-align:left; border:silver 1px solid;" style="text-align:left; border:silver 1px solid;">
        		<td class="table-cell" style="text-align:left; border:silver 1px solid;font-size: 28px" style="text-align:left; border:silver 1px solid;font-size: 28px">Curso</td>
        		<td class="table-cell" style="text-align:left; border:silver 1px solid;font-size: 28px" style="text-align:left; border:silver 1px solid;font-size: 28px">Calificación</td>
        	</tr>
        
        	%for course in courses_student:
        		
        	<tr class="table-cell" style="text-align:left; border:silver 1px solid;" style="text-align:left; border:silver 1px solid;">
        		<td class="table-cell" style="text-align:left; border:silver 1px solid;" style="text-align:left; border:silver 1px solid;"><b>${course.name}</b></td>
        		<td class="table-cell" style="text-align:left; border:silver 1px solid;" style="text-align:left; border:silver 1px solid;"><b>${formatLang(get_qualify_course(cr, uid, student_selected,course.id)) or '0'}</b></td>
        	</tr>
        		<%
        		tasks_student=get_task_by_student_course(cr, uid, student_selected,course.id)
        		%>
        		%for task in tasks_student:
        		<tr class="table-cell" style="text-align:left; border:silver 1px solid;" style="text-align:left; border:silver 1px solid;">
        			<td class="table-cell" style="text-align:left; border:silver 1px solid;" style="text-align:left; border:silver 1px solid;">${task.name}</td>
        			<td class="table-cell" style="text-align:left; border:silver 1px solid;" style="text-align:left; border:silver 1px solid;">${formatLang(get_qualify_task(cr, uid, student_selected,course.id,task.id)) or '0'}</td>
        		</tr>
        		%endfor
        	%endfor
        </table>	
			

    </body>
</html>