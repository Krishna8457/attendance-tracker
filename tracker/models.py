from django.db import models

# tracker/models.py

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    # Add blank=True and null=True to make these fields optional
    last_name = models.CharField(max_length=50, blank=True, null=True)
    # The unique=True on email must be removed if it can be null
    email = models.EmailField(unique=False, blank=True, null=True)

    def __str__(self):
        # This new version checks if last_name exists before adding it
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.first_name

class Course(models.Model):
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(Student, related_name='courses')

    def __str__(self):
        return self.name

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} - {self.course} - {self.date}"