

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("The Email field must be set")
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):  # Inherit from PermissionsMixin
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # You can add any additional fields that are required for user creation

    objects = CustomUserManager()

    def is_alumni(self):
        return Alumni.objects.filter(email=self.email).exists()

    def __str__(self):
        return self.email



class Comment(models.Model):
    user = models.ForeignKey('comments.CustomUser', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', related_name='comments', on_delete=models.CASCADE)  # Add this line
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Course(models.Model):
    title = models.CharField(max_length=200, default="Untitled Course")
    description = models.TextField(default="No description available")
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='courses/images/', blank=True, null=True)

    def __str__(self):
        return self.title

class Rating(models.Model):
    course = models.ForeignKey(Course, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)  # Rating from 1 to 5

    def __str__(self):
        return f"Rating for {self.course.title} by {self.user.email}"

class Assignment(models.Model):
    course = models.ForeignKey(Course, related_name='assignments', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)  # Avoid null=True for TextField
    image = models.ImageField(upload_to='assignments/images/', blank=True, null=True)  # Optional image field
    file = models.FileField(upload_to='assignments/files/', blank=True, null=True)  # Optional file field

    def __str__(self):
        return self.title

class Quizz(models.Model):
    course = models.ForeignKey(Course, related_name='quizz', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='quizz/images/', blank=True, null=True)  # Optional image field
    file = models.FileField(upload_to='quizz/files/', blank=True, null=True)  # File field for documents

    def __str__(self):
        return self.title

class PastPaper(models.Model):
    course = models.ForeignKey(Course, related_name='pastPaper', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='pastPaper/images/', blank=True, null=True)  # Optional image field
    file = models.FileField(upload_to='pastPaper/files/', blank=True, null=True)  # File field for documents

    def __str__(self):
        return self.title

class CourseMaterial(models.Model):
    course = models.ForeignKey(Course, related_name='courseMaterial', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='courseMaterial/images/', blank=True, null=True)  # Optional image field
    file = models.FileField(upload_to='courseMaterial/files/', blank=True, null=True)  # File field for documents

    def __str__(self):
        return self.title


class Alumni(models.Model):
    email = models.EmailField(
        unique=True,
        max_length=255,
        validators=[
            RegexValidator(
                regex=r"^l\d{6}@lhr\.nu\.edu\.pk$",
                message="Email must be in the format lnnnnnn@lhr.nu.edu.pk",
            )
        ],
    )
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
