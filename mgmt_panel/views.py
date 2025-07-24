from django.shortcuts import render
from django.http import JsonResponse
from .models import Student, Course, Enrollment

def save_enrollment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        password = request.POST.get('password') 
        course_names = request.POST.getlist('course_name[]')
        course_marks = request.POST.getlist('course_marks[]')

        student = Student.objects.create(name=name, username=username, password=password)

        for cname, mark in zip(course_names, course_marks):
            course, _ = Course.objects.get_or_create(name=cname)
            Enrollment.objects.create(student=student, course=course, marks=int(mark))

        return JsonResponse({'message': 'Enrollment and courses saved successfully', 'password': password})

    return render(request, 'mgmt_panel/mgmt.html')
