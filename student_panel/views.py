from django.shortcuts import render, redirect
from student_panel.models import Student
import jwt
from mgmt_panel.models import Student, Enrollment, Course
from django.conf import settings
from django.http import HttpResponse
from datetime import datetime, timedelta

from django.http import JsonResponse


def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
   

        try:
            student = Student.objects.get(username=username)
            if student.password == password:
                # Save student ID in session
                request.session['student_id'] = student.id

                # Generate JWT token with expiry
                payload = {
                             'student_id': student.id,
                             'exp': datetime.utcnow() + timedelta(minutes=30),
                             'iat': datetime.utcnow()
                          }

            
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

                # Store token in session (or frontend can store in localStorage)
                request.session['jwt_token'] = token

                response = redirect('student_dashboard')
                response.set_cookie('jwt_token', token, max_age=300, httponly=True)  # Optional: cookie-based
                return response
            else:
                return render(request, 'student_panel/student_login.html', {
                    'error': 'Invalid username or password'
                })
        except Student.DoesNotExist:
            return render(request, 'student_panel/student_login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'student_panel/student_login.html')


def student_dashboard(request):
    token = request.session.get('jwt_token')
    student_id = request.session.get('student_id')

    if not token or not student_id:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Session expired'}, status=401)
        return redirect('student_login')

    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        student_id = decoded['student_id']

        if str(decoded.get('student_id')) != str(student_id):
            return JsonResponse({'error': 'Invalid token'}, status=403)

        student = Student.objects.get(id=student_id)
        enrollments = Enrollment.objects.filter(student=student)

        for e in enrollments:
            if e.marks >= 90:
                e.grade = 'A+'
            elif e.marks >= 80:
                e.grade = 'A'
            elif e.marks >= 70:
                e.grade = 'B'
            elif e.marks >= 60:
                e.grade = 'C'
            elif e.marks >= 50:
                e.grade = 'D'
            else:
                e.grade = 'F'

        # Respond with normal HTML on direct page load
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'ok'})  # ✅ for JS to continue

        return render(request, 'student_panel/student_dashboard.html', {
            'student': student,
            'enrollments': enrollments,
            'token': token
        })

    except jwt.ExpiredSignatureError:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Expired'}, status=401)
        return redirect('student_login')

    except jwt.InvalidTokenError:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Invalid'}, status=401)
        return redirect('student_login')


def student_logout(request):
    request.session.flush()
    return redirect('/')
