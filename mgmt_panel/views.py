from django.shortcuts import render
from django.http import JsonResponse
from .models import Student, Course, Enrollment, GradeScale
from django.core.exceptions import ObjectDoesNotExist


def save_enrollment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        course_names = request.POST.getlist('course_name[]')
        course_marks = request.POST.getlist('course_marks[]')

        # ✅ Create new student
        student = Student.objects.create(name=name, username=username, password=password)

        # ✅ Loop through courses and marks
        for cname, mark in zip(course_names, course_marks):
            mark = int(mark)
            course, _ = Course.objects.get_or_create(name=cname)

            # ✅ Get grade from GradeScale table
            grade_obj = GradeScale.objects.filter(min_marks__lte=mark, max_marks__gte=mark).first()
            grade = grade_obj.grade if grade_obj else "N/A"

            # ✅ Save enrollment
            Enrollment.objects.create(student=student, course=course, marks=mark, grade=grade)

        return JsonResponse({'message': 'Enrollment and courses saved successfully', 'password': password})

    return render(request, 'mgmt_panel/mgmt.html')
