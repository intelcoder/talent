from django.db import models
from django.contrib.auth.models import User
from .base_models import Timestampable
from .base_models import AbstractArea
from .base_models import AbstractReview


class UserProfile(models.Model):
    """UserProfile table

    Stores user's profile information

    One to one relationship with Django provided User model

    user: Foreign key from the User table to match the user
          profile and user account
    profile_image_path: Path to user's profile image file
    pref_location: Preferred location given by user (long,lat,radius)
    """
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True)
    profile_image_path = models.ImageField(upload_to='profile/pics')
    pref_location = models.CharField()


class TutorProfile(Timestampable, UserProfile):
    """TutorProfile table

    Stores tutor specific profile information

    Extends UserProfile table

    brief_intro: brief introduction of Tutor
    resume_path: Path to user's resume file
    is_verified: True if the tutor is verified
    """
    # user = models.OneToOneField(UserProfile)
    brief_intro = models.TextField(max_length=300,
                                   blank=True,
                                   help_text="Brief introduction of yourself")
    resume_path = models.FilePathField(path='profile/resume',
                                       help_text="Upload your resume")
    is_verified = models.BooleanField(default=False)


class StudentProfile(Timestampable, UserProfile):
    """StudentProfile table

    Stores student specific profile information

    Extends UserProfile table

    """
    favorite_animal = models.CharField(max_length=3,
                                       blank=True,
                                       default="Cat",
                                       help_text="CAT CAT CAT")


class Course(Timestampable, models.Model):
    """Course table

    Stores course information

    One to one relationship with Tutor
    Many to many relationship with SubCategory
    One to many relationship with Curriculum

    tutor: reference to the tutor who created the course
    title: course title
    description: course description
    is_active: True if the course is available
    group_max: maximum number of people per session
    sub_category: subcategory of where the course belongs

    """
    tutor = models.ForeignKey(TutorProfile,
                              related_name="tutorprofile",
                              on_delete=models.CASCADE)
    sub_category = models.ManyToManyField(SubCategory)
    title = models.CharField(max_length=255, help_text="Course title")
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    group_max = models.IntegerField()


class ImageToCourse(models.Model):
    """ImageToCourse table

    Stores mapping information between image and course

    One to many relationship with Course

    course: reference to the Course
    course_image_path: path to course image file

    """
    course = models.ForeignKey(Course,
                               related_name="+",
                               on_delete=models.CASCADE)
    course_image_path = models.ImageField(upload_to='course/pics')


class IframeLinkToCourse(models.Model):
    """IframeLinkToCourse table

    Stores mapping information between iFrameLink and course

    One to many relationship with Course

    course: reference to the Course
    iframe_url: url of iframe
    source_from: video provider

    """
    course = models.ForeignKey(Course,
                               related_name="+",
                               on_delete=models.CASCADE)
    iframe_url = models.CharField(max_length=255)
    source_from = models.CharField(max_length=100)


class Category(models.Model):
    """Category table

    Stores list of category

    name: name of category

    """
    name = models.CharField(max_length=50, unique=True)


class SubCategory(models.Model):
    """SubCategory table

    Stores list of SubCategory

    One to many relationship with Category

    category: reference of Category
    sub_category: name of subcategory

    """
    category = models.ForeignKey(Category, related_name="category")
    sub_category = models.CharField(max_length=50, unique=True)


# End of Timothy's work


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
    preparation_rating = models.FloatField()
    teaching_rating = models.FloatField()
    onTime_rating = models.FloatField()
    tutor = models.ForeignKey(
        TutorProfile, related_name='+', on_delete=models.CASCADE)


class Comment(Timestampable, models.Model):
    creator = models.ManyToManyField(UserProfile, related_name='+')
    comment = models.ForeignKey('self')

    class Meta:
        abstract = True


class DayOfWeek(models.Model):
    name = models.CharField(max_length=50)


class CourseComment(Comment):
    course_id = models.ForeignKey(Course)


# period, dayOfWeek, location


class CourceSchedule(models.Model):
    time_from = models.DateTimeField()
    time_to = models.DateTimeField()
    day_of_week = models.ForeignKey(DayOfWeek)
    course = models.ForeignKey(Course)


class CourseReview(AbstractReview):
    course = models.ForeignKey(
        Course, related_name='+', on_delete=models.CASCADE)
