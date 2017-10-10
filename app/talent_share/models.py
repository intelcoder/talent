from django.db import models
from django.contrib.auth.models import User
from .base_models import Timestampable
from .base_models import AbstractArea
from .base_models import AbstractReview


class UserProfile(models.Model):
    """UserProfile table

    Stores user's profile information

    user: Foreign key from the User table to match the user profile and user account
    profile_image_path: Path to user's profile image file
    brief_intro: Brief introduction of user given by user
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True)
    # cell = models.CharField(max_length=150, blank=True)
    profile_image_path = models.ImageField(upload_to='profile/pics')
    brief_intro = models.TextField(max_length=300, blank=True,
                                   help_text="Brief introduction of yourself")


class TutorProfile(Timestampable, UserProfile):
    """TutorProfile table

    Stores tutor specific profile information
    Extends UserProfile table

    resume: Path to user's resume file
    """
    # user = models.OneToOneField(UserProfile)
    resume_path = models.FilePathField(path='profile/resume')



class StudentProfile(Timestampable, UserProfile):
    """StudentProfile table
    Stores student specific profile information
    Extends UserProfile table

    """
    student_pref_location = models.CharField()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)


class SubCategory(models.Model):
    """
    SubCategory is to define specific category
    Language - korea, english

    """
    sub_category = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category)


# Create your models here.
class Role(models.Model):
    title = models.CharField(max_length=50, unique=True)


class Country(AbstractArea):
    pass


class Province(AbstractArea):
    pass


class City(AbstractArea):
    pass


class Address(AbstractArea):
    suburban = models.CharField(max_length=150)
    postal_code = models.CharField(max_length=150)


class Location(models.Model):
    country = models.ForeignKey(Country)
    province = models.ForeignKey(Province)
    city = models.ForeignKey(City)
    address = models.ForeignKey(Address)





class TutorReview(AbstractReview):
    express_rating = models.FloatField()
    contents_rating = models.FloatField()
    prepration_rating = models.FloatField()
    teaching_rating = models.FloatField()
    onTime_rating = models.FloatField()
    tutor = models.ForeignKey(
        Tutor, related_name='+', on_delete=models.CASCADE)


class Comment(Timestampable, models.Model):
    creator = models.ManyToManyField(UserProfile, related_name='+')
    comment = models.ForeignKey('self')

    class Meta:
        abstract = True


class DayOfWeek(models.Model):
    name = models.CharField(max_length=50)


class Course(Timestampable, models.Model):
    title = models.CharField(max_length=255)
    about = models.TextField()  # will contain html
    course_period = models.IntegerField()  # how many hour per session
    group_max = models.IntegerField()  # Max number of people in the group
    curriculum = models.TextField()

    # category also can break down to sub category
    category = models.ManyToManyField(Category)


class CourseComment(Comment):
    course_id = models.ForeignKey(Course)


# period, dayOfWeek, location


class CourceSchedule(models.Model):
    time_from = models.DateTimeField()
    time_to = models.DateTimeField()
    day_of_week = models.ForeignKey(DayOfWeek)
    course = models.ForeignKey(Course)


class CourseIframeLink(models.Model):
    course = models.ForeignKey(Course)
    iframe_url = models.CharField(max_length=255)
    source_from = models.CharField(max_length=100)


class CourseImage(models.Model):
    image = models.ImageField(upload_to='course/pics')
    course = models.ForeignKey(
        Course, related_name='+', on_delete=models.CASCADE)


class CourseReview(AbstractReview):
    course = models.ForeignKey(
        Course, related_name='+', on_delete=models.CASCADE)
