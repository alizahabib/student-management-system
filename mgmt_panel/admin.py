from django.contrib import admin
from .models import Student, Course, Enrollment, GradeScale  # ✅ import all models

@admin.register(GradeScale)
class GradeScaleAdmin(admin.ModelAdmin):
    list_display = ('grade', 'min_marks', 'max_marks')  # ✅ shows columns
    list_filter = ('grade',)  # optional filter sidebar
    ordering = ('-min_marks',)  # newest first

# Optional: Register other models
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Enrollment)
