from django.db import models
from django.contrib.auth.models import User
from .base_models import Timestampable
from .base_models import AbstractArea
from .base_models import AbstractReview


'''Profile Section
        UserProfile
        TutorProfile
        StudentProfile
'''


class UserProfile(Timestampable, models.Model):
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


'''End of profile section ====================================================
'''


''' Course and curriculum section
        Course
        ImageToCourse
        Category
        SubCategory
        Curriculum
        CurriculumContents
        FileToCurriculum
        ImageToCurriculum
        IFrameLinkToCurriculum
'''


class Course(Timestampable, models.Model):
    """Course table

    Stores course information

    One to one relationship with Tutor
    Many to many relationship with SubCategory
    One to many relationship with Curriculum
    Many to many relationship with TutorAvailability


    tutor: reference to the tutor who created the course
    title: course title
    description: course description
    is_active: True if the course is available
    group_max: maximum number of people per session
    sub_category: subcategory of where the course belongs
    availability: availability of course set by tutor

    """
    tutor = models.ForeignKey(TutorProfile,
                              related_name="tutorprofile",
                              on_delete=models.CASCADE)
    sub_category = models.ManyToManyField(SubCategory)
    availability = models.ManyToManyField(TutorAvailability)
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


class Curriculum(Timestampable, models.Model):
    """SubCategory table

    Stores list of SubCategory

    One to many relationship with Category

    category: reference of Category
    sub_category: name of subcategory

    """
    course = models.ForeignKey(Course,
                               related_name="+",
                               on_delete=models.CASCADE)
    step_number = models.IntegerField()
    public_description = models.CharField(max_length=300)


class CurriculumContents(Timestampable, models.Model):
    """CurriculumContents table

    Stores private contents of curriculum

    One to one relationship with curriculum

    curriculum: reference to the Curriculum
    text_content: text content of curriculum
    has_file: indicator of having file
    has_image: indicator of having image
    has_iframe: indicator of having iframe
    """
    curriculum = models.OneToOneField(Curriculum,
                                      on_delete=models.CASCADE,
                                      primary_key=True)
    text_content = models.TextField()
    has_file = models.BooleanField(default=False)
    has_image = models.BooleanField(default=False)
    has_iframe = models.BooleanField(default=False)


class FileToCurriculum(models.Model):
    """FileToCurriculum table

    Stores mapping information between course related file and curriculum

    One to many relationship with curriculum

    curriculum: reference to the Curriculum
    file_path: path to course related file

    """
    curriculum = models.ForeignKey(Curriculum,
                                   related_name="+",
                                   on_delete=models.CASCADE)
    file_path = models.FilePathField(path='course/curriculum/file',
                                     help_text="Upload file")


class ImageToCurriculum(models.Model):
    """ImageToCurriculum table

    Stores mapping information between image and curriculum

    One to many relationship with curriculum

    curriculum: reference to the Curriculum
    curriculum_image_path: path to course image file

    """
    curriculum = models.ForeignKey(Curriculum,
                                   related_name="+",
                                   on_delete=models.CASCADE)
    curriculum_image_path = models.ImageField(upload_to='course/curriculum/pics')


class IFrameLinkToCurriculum(models.Model):
    """IFrameLinkToCurriculum table

    Stores mapping information between iFrameLink and curriculum

    One to many relationship with curriculum

    curriculum: reference to the Curriculum
    iframe_url: url of iframe
    source_from: video provider

    """
    curriculum = models.ForeignKey(Curriculum,
                                   related_name="+",
                                   on_delete=models.CASCADE)
    iframe_url = models.CharField(max_length=255)
    source_from = models.CharField(max_length=100)


'''End of course and curriculum section ======================================
'''


'''Calendar section
'''


class DayOfWeek(models.Model):
    """DayOfWeek table

    Stores Day of week information
    Available Day: Monday, Tuesday, Wednesday,
                    Thursday, Friday, Saturday, Sunday

    name: full name of day
    short_name: 3 characters shortened version for name of day
    """
    name = models.CharField(max_length=9,
                            unique=True,
                            primary_key=True)
    short_name = models.CharField(max_length=3, unique=True)


class TutorAvailability(models.Model):
    """TutorAvailability table

    Stores availability of tutor as in day based weekly schedule

    One to many relationship with TutorProfile
    One to many relationship with DayOfWeek (start,end day)

    tutor: reference to TutorProfile
    start_day: start day
    end_day: end day
    start_time: start time
    end_time: end time
    """
    tutor = models.ForeignKey(TutorProfile,
                              related_name="+",
                              on_delete=models.CASCADE)
    start_day = models.ForeignKey(DayOfWeek, related_name='+')
    end_day = models.ForeignKey(DayOfWeek, related_name='+')
    start_time = models.TimeField()
    end_time = models.TimeField()


class PendingBookingRequest(Timestampable, models.Model):
    """PendingBookingRequest table

    Stores all of created booking request by students

    One to many relationship with StudentProfile
    One to many relationship with TutorProfile
    One to many relationship with CourseProfile

    student: reference to student
    tutor: reference to tutor
    course: reference to course
    start_time: start time in DateTime form
    end_time: end time in DateTime form
    message: private message in the request
    request_status: status of request[P(ending(,R(ejected),A(pproved)]
    """
    student = models.ForeignKey(StudentProfile,
                                related_name="studentprofile")
    tutor = models.ForeignKey(TutorProfile,
                              related_name="tutorprofile")
    course = models.ForeignKey(Course,
                               related_name='+')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    message = models.CharField(max_length=300)
    # 3 status, P(ending), R(ejected), A(pproved)
    request_status = models.CharField(max_length=3)


class ApprovedBookingRequest(Timestampable, models.Model):
    """ApprovedBookingRequest table

    Stores reference of PendingBookingRequests when the request is approved

    One to One relationship with PendingBookingRequest

    request: approved request reference
    """
    request = models.OneToOneField(PendingBookingRequest,
                                   primary_key=True)


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


class CourseComment(Comment):
    course_id = models.ForeignKey(Course)


# period, dayOfWeek, location


class CourseReview(AbstractReview):
    course = models.ForeignKey(
        Course, related_name='+', on_delete=models.CASCADE)
