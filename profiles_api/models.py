from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""
    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database Model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of our user"""
        return self.email

class ProfileFeedItem(models.Model):
    """Profile status update"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the model as a string"""
        return self.status_text

###############################################################################

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        """Return string representation of category"""
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1023)
    overview = models.CharField(max_length=1023)
    price = models.IntegerField()
    created_at = models.DateField(auto_now=False, auto_now_add=True)
    updated_at = models.DateField(auto_now=True, auto_now_add=False)
    language = models.CharField(max_length=255)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        """Return string representation of a course"""
        return self.name

class Image(models.Model):
    IMAGE_CHOICES = [
        ('cover', 'cover'),
        ('overview', 'overview')
    ]
    name = models.CharField(max_length=255, choices=IMAGE_CHOICES)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    image_path = models.CharField(max_length=255)
    # images_path = models.FileField(upload_to='uploads/'+course.__str__()+'/images/')

    def __str__(self):
        """Return string representation of course image"""
        return self.name + " image for " + self.course.__str__()

class Video(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1023)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    video_path = models.CharField(max_length=255)
    # video_path = models.FileField(upload_to='uploads/'+course.__str__()+'/videos/')

    def __str__(self):
        """Return string representation of course video"""
        return self.name + " video for " + self.course.__str__()

class Review(models.Model):
    review = models.CharField(max_length=511)
    rating = models.IntegerField()
    created_at = models.DateField(auto_now=False, auto_now_add=True)
    user = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        """Return string representation of review"""
        return self.user.get_full_name() + "'s review of " + self.course.__str__()

class Instructor(models.Model):
    name = models.CharField(max_length=255)
    image_path = models.CharField(max_length=255)
    description = models.CharField(max_length=1023)
    rating = models.IntegerField()
    courses = models.ManyToManyField(Course)

    def __str__(self):
        """Return string representation of instructor"""
        return self.name
