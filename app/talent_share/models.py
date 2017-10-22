from django.db import models
from django.contrib.auth.models import User
from .base_models import Timestampable
from .base_models import AbstractArea
from .base_models import AbstractReview


''' Profile Section
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
    display_name = models.CharField(max_length=20,
                                    blank=False)
    phone_number = models.CharField(max_length=15,
                                    blank=True)
    profile_image_path = models.ImageField(upload_to='profile/pics',
                                           blank=True)
    pref_location = models.CharField(blank=True)


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
    price_per_session = models.IntegerField()


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


class IFrameLinkToCourse(models.Model):
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


class FileToCurriculumContents(models.Model):
    """FileToCurriculumContents table

    Stores mapping information between course contents related file
        and curriculum contents

    One to many relationship with CurriculumContents

    contents: reference to the CurriculumContents
    file_path: path to course related file

    """
    contents = models.ForeignKey(CurriculumContents,
                                 related_name="+",
                                 on_delete=models.CASCADE)
    file_path = models.FilePathField(path='course/curriculum/file',
                                     help_text="Upload file")


class ImageToCurriculumContents(models.Model):
    """ImageToCurriculumContents table

    Stores mapping information between image and curriculum contents

    One to many relationship with curriculum contents

    contents: reference to the CurriculumContents
    image_path: path to course image file

    """
    contents = models.ForeignKey(CurriculumContents,
                                 related_name="+",
                                 on_delete=models.CASCADE)
    image_path = models.ImageField(upload_to='course/curriculum/pics')


class IFrameLinkToCurriculumContents(models.Model):
    """IFrameLinkToCurriculumContents table

    Stores mapping information between iFrameLink and curriculum contents

    One to many relationship with CurriculumContents

    contents: reference to the CurriculumContents
    iframe_url: url of iframe
    source_from: video provider

    """
    contents = models.ForeignKey(CurriculumContents,
                                   related_name="+",
                                   on_delete=models.CASCADE)
    iframe_url = models.CharField(max_length=255)
    source_from = models.CharField(max_length=100)


'''End of course and curriculum section ======================================
'''


''' Calendar section
        DayOfWeek
        TutorAvailability
        PendingRequest
        ApprovedRequest
'''


class DayOfWeek(models.Model):
    """DayOfWeek table

    Stores Day of week information
    Available Day: Monday, Tuesday, Wednesday,
                    Thursday, Friday, Saturday, Sunday

    country: country
    name: full name of day
    short_name: 3 characters shortened version for name of day
    """
    country = models.ForeignKey(Country, related_name="+")
    name = models.CharField(max_length=20,
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


class PendingRequest(Timestampable, models.Model):
    """PendingRequest table

    Stores all of created request by users

    One to many relationship with StudentProfile
    One to many relationship with TutorProfile
    One to many relationship with CourseProfile

    student: reference to student
    tutor: reference to tutor
    course: reference to course
    request_type: Type of the request [ Booking,
                                        Cancel,
                                        Modification ]
    start_time: start time in DateTime form
    end_time: end time in DateTime form
    message: private message in the request
    request_status: status of request [ P(ending),
                                        R(ejected),
                                        A(pproved),
                                        M(odified) ]
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
    request_status = models.CharField(max_length=1)


class ApprovedRequest(Timestampable, models.Model):
    """ApprovedBookingRequest table

    Stores reference of PendingRequests when the request is approved

    One to One relationship with PendingRequest
    One to Many relationship with TutorProfile
    One to Many relationship with StudentProfile

    request: approved request reference
    tutor: Tutor profile reference
    student: Studetn profile reference
    """
    request = models.OneToOneField(PendingRequest,
                                   primary_key=True)
    tutor = models.ForeignKey(TutorProfile,
                              related_name="tutorprofile")
    student = models.ForeignKey(StudentProfile,
                                related_name="studentprofile")

'''End of calendar section ===================================================
'''


''' Resume section
        ResumeEducation
        ResumeSkill
        ResumeExperience
        ResumeEducationToCourse
        ResumeSkillToCourse
        ResumeExperienceToCourse
    Note:
        Resume information is desired to be pulled from LinkedIn
'''


class ResumeEducation(Timestampable, models.Model):
    """ResumeEducation table

    Stores tutor's education detail

    One to Many relationship with TutorProfile

    tutor: tutor profile reference
    school: name of school
    degree: name of degree
    study_field: field of study
    grade: GPA
    start_month: started month of education
    start_year: started year of education
    end_month: ended month of education
    end_year: ended year of education
    extra: extracurricular activity detail
    description: extra description
    """
    tutor = models.ForeignKey(TutorProfile,
                              on_delete=models.CASCADE,
                              related_name='+')
    school = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    study_field = models.CharField(max_length=100)
    grade = models.CharField(max_length=10,
                             blank=True)
    start_month = models.CharField(max_length=25)
    start_year = models.CharField(max_length=4)
    end_month = models.CharField(max_length=25,
                                 blank=True)
    end_year = models.CharField(max_length=4,
                                blank=True)
    extra = models.TextField()
    description = models.TextField()


class ResumeSkill(Timestampable, models.Model):
    """ResumeSkill table

    Stores tutor's skill

    One to Many relationship with TutorProfile

    tutor: tutor profile reference
    skill: name of skill
    """
    tutor = models.ForeignKey(TutorProfile,
                              on_delete=models.CASCADE,
                              related_name='+')
    skill = models.CharField(max_length=20)


class ResumeExperience(Timestampable, models.Model):
    """ResumeExperience table

    Stores tutor's experience detail

    One to Many relationship with TutorProfile

    tutor: tutor profile reference
    title: name of title
    company: name of company
    location: location of company
    grade: GPA
    start_month: started month of experience
    start_year: started year of experience
    end_month: ended month of experience
    end_year: ended year of experience
    description: extra description
    """
    tutor = models.ForeignKey(TutorProfile,
                              on_delete=models.CASCADE,
                              related_name='+')
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    start_month = models.CharField(max_length=25)
    start_year = models.CharField(max_length=4)
    end_month = models.CharField(max_length=25,
                                 blank=True)
    end_year = models.CharField(max_length=4,
                                blank=True)
    description = models.TextField()


class ResumeEducationToCourse(Timestampable, models.Model):
    """ResumeEducationToCourse table

    Maps related education information to course

    Many to Many relationship with Course
    Many to Many relationship with ResumeEducation

    """
    course = models.ManyToManyField(Course)
    education = models.ManyToManyField(ResumeEducation)


class ResumeSkillToCourse(Timestampable, models.Model):
    """ResumeSkillToCourse table

    Maps related skill information to course

    Many to Many relationship with Course
    Many to Many relationship with ResumeSkill

    """
    course = models.ManyToManyField(Course)
    skill = models.ManyToManyField(ResumeSkill)


class ResumeExperienceToCourse(Timestampable, models.Model):
    """ResumeExperienceToCourse table

    Maps related experience information to course

    Many to Many relationship with Course
    Many to Many relationship with ResumeExperience

    """
    course = models.ManyToManyField(Course)
    experience = models.ManyToManyField(ResumeExperience)


'''End of resume section =====================================================
'''


''' Review section
        ReviewStudent
        ReviewCourse
        ReviewTutor
'''


class ReviewStudent(Timestampable, models.Model):
    student = models.ForeignKey(StudentProfile,
                                related_name="+",
                                on_delete=models.CASCADE)
    author = models.ForeignKey(TutorProfile,
                               related_name="+")
    description = models.TextField()
    # need to add review criteria


class ReviewCourse(Timestampable, models.Model):
    course = models.ForeignKey(Course,
                               related_name="+",
                               on_delete=models.CASCADE)
    author = models.ForeignKey(StudentProfile,
                               related_name="+")
    description = models.TextField()
    contents_rating = models.IntegerField()
    knowledge_rating = models.IntegerField()
    # need to add review criteria


class ReviewTutor(Timestampable, models.Model):
    tutor = models.ForeignKey(TutorProfile,
                              related_name="+",
                              on_delete=models.CASCADE)
    author = models.ForeignKey(StudentProfile,
                               related_name="+")
    description = models.TextField()
    preparation_rating = models.IntegerField()
    teaching_rating = models.IntegerField()
    onTime_rating = models.IntegerField()
    # need to add review criteria


'''End of review section =====================================================
'''


''' Administration section

'''

# user should upload photo of their credentials (User uploaded documents)
# each document will be verified using 3rd party web/non-web services
# user can upload multiple documents


class ReceivedTutorApplication(Timestampable, models.Model):
    applicant = models.OneToOneField(UserProfile)
    phone_number = models.CharField(max_length=15)
    # gov issueed id will be verified through 3rd party web service
    is_gov_issued_id_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    is_info_verified = models.BooleanField(default=False)


class ReportCategory(models.Model):
    category = models.CharField(max_length=20,
                                blank=False,
                                unique=True)


class ReportSubCategory(models.Model):
    category = models.ForeignKey(ReportCategory,
                                 related_name="reportcategory")
    sub_category = models.CharField(max_length=30,
                                    blank=False,
                                    unique=True)

# need to store report as threads gets stored in db


class ReportFromUser(Timestampable, models.Model):
    sender = models.ForeignKey(UserProfile,
                               related_name="userprofile",
                               blank=False)
    sub_category = models.ForeignKey(ReportSubCategory,
                                     related_name="+",
                                     blank=False)
    message = models.TextField(blank=False)
    status = models.CharField(max_length=1, blank=False)


'''End of administration section =============================================
'''


''' Region section

'''


class Country(AbstractArea):
    short_name = models.CharField(max_length=55, unique=True)
    full_name = models.CharField(max_length=60, unique=True)
    alpha_two_code = models.CharField(max_length=2, unique=True)
    alpha_three_code = models.CharField(max_length=3, unique=True)


class Province(AbstractArea):

    pass


class City(AbstractArea):
    pass


class Address(AbstractArea):
    suburban = models.CharField(max_length=150)
    postal_code = models.CharField(max_length=150)


class Location(models.Model):
    country = models.ForeignKey(Country)
    # province and city is not needed since address has postal code
    # province = models.ForeignKey(Province)
    # city = models.ForeignKey(City)
    address = models.ForeignKey(Address)


'''End of region section =============================================
'''

# End of Timothy's work


class Role(models.Model):
    title = models.CharField(max_length=50, unique=True)