from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.validators import *
from django.db import models

# Create your models here.


class ChallengeType(models.Model):
    # TODO: need to write a list of the types of challenges and insert it into the database
    class Meta:
        db_table = 'challenge_type'
        ordering = ['id']

    name = models.CharField(db_column='name', max_length=256, null=False, blank=False)
    url_img = models.URLField(db_column='url_img')  # TODO: default


class BusinessAccessibility(models.Model):

    class Meta:
        db_table = 'business_accessibility'

    business = models.ForeignKey('Business', on_delete=models.CASCADE, null=False, blank=False,
                                 related_name='accessibilities')
    is_free = models.BooleanField(db_column='is_free', null=False, blank=False)
    is_accessible = models.BooleanField(db_column='is_accessible',
                                        null=False, blank=False)  # is accessible for people with disabilities
    is_kosher = models.BooleanField(db_column='is_kosher', null=False, blank=False)
    is_baby_carriage = models.BooleanField(db_column='is_baby_carriage', null=False, blank=False)


class BusinessType(models.Model):
    # TODO: need to write a list of the types of business and insert it into the database
    class Meta:
        db_table = 'business_type'
        ordering = ['id']

    name = models.CharField(db_column='name', max_length=256, null=False, blank=False)


class Business(models.Model):

    class Meta:
        db_table = 'business'
        ordering = ['id']

    name = models.CharField(db_column='name', max_length=64, null=False, blank=False, db_index=True)  # index = True
    description = models.TextField(db_column='description', null=True, blank=True)
    phone_num = models.IntegerField(db_column='phone_num', null=True, blank=True)  # TODO: add validation
    menu_url = models.URLField(db_column='menu_url', null=True, blank=True)

    # TODO: To check whether I need to calculate the load hours or the client writes them,
    #  or if there is an option to leave it blank.
    load_hour = models.TimeField(db_column='load_hour', null=True, blank=True)
    create_date = models.DateField(db_column='create_date', auto_now_add=True)
    views_num = models.IntegerField(db_column='views_num',
                                    default=0) # TODO: How can I automate a process where each time someone
                                    # TODO: views it, the view count increases by 1 automatically?
    is_active = models.BooleanField(db_column='is_active', null=False, blank=False, default=True)
    logo = models.URLField(db_column='logo_url', null=True, blank=True)
    cover = models.URLField(db_column='cover_url', null=True, blank=True)
    # bn_number =  # TODO: add bn_number

    business_types = models.ManyToManyField(BusinessType, through='BusinessAndType')
    users = models.ManyToManyField(User, through='BusinessAndUser', related_name='business')
    users_histories = models.ManyToManyField(User, through='UserViewHistory', related_name='business_histories')
    users_likes = models.ManyToManyField(User, through='UserLike', related_name='business_likes')

    # TODO: add facebook, and insta.

    # addres_id
    # opening_hours


class Address(models.Model):

    class Meta:
        db_table = 'address'
        ordering = ['id']

    business = models.ForeignKey(Business, on_delete=models.RESTRICT, null=True, blank=True,
                                 related_name='business_address')
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True, related_name='user_address')
    city = models.CharField(db_column='city', max_length=256, null=False, blank=False, db_index=True)  # index = True
    street = models.CharField(db_column='street', max_length=256, null=True, blank=True)
    number = models.SmallIntegerField(db_column='number', null=True, blank=True)
    zip_code = models.IntegerField(db_column='zip_code', null=True, blank=True)
    floor = models.SmallIntegerField(db_column='floor', null=True, blank=True)
    apartment_num = models.SmallIntegerField(db_column='apartment_num', null=True, blank=True)
    is_business = models.BooleanField(db_column='is_business')

    # TODO: Must be one of the two User or Business


class BusinessAndType(models.Model):

    class Meta:
        db_table = 'business_and_type'
        ordering = ['id']

    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=False, blank=False)
    business_type = models.ForeignKey(BusinessType, on_delete=models.CASCADE, null=False, blank=False)


class OpeningHours(models.Model):

    class Meta:
        db_table = 'opening_hours'
#
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=False, blank=False,
                                 related_name='opening_hours')
    day = models.SmallIntegerField(db_column='day', null=False, blank=False)
    opening_time = models.TimeField(db_column='opening_time', null=False, blank=False)
    closing_time = models.TimeField(db_column='closing_time', null=False, blank=False)


class BusinessAndUser(models.Model):

    class Meta:
        db_table = 'business_and_user'
        ordering = ['id']

    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.business.name + " " + self.user.first_name
    # date?


class Challenge(models.Model):

    class Meta:
        db_table = 'challenge'
        ordering = ['id']

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(db_column='challenge_name', max_length=256, null=False, blank=False)
    challenge_type = models.ForeignKey(ChallengeType, on_delete=models.CASCADE, null=False, blank=False)
    date = models.DateField(db_column='date', null=True, blank=True)  # TODO: default date.now()
    challenge_time = models.TimeField(db_column='challenge_time', null=False, blank=False)
    text_on_challenge = models.TextField(db_column='text_on_challenge', null=True, blank=True)
    is_business_challenge = models.BooleanField(db_column='is_business_challenge', null=False, blank=False)


class BusinessChallengeDetails(models.Model):

    class Meta:
        db_table = 'business_challenge_details'

    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, null=False, blank=False,
                                  related_name='business_details')
    # start_date = models.DateField(db_column='start_date', null=False,
    #                               blank=False)  # check about auto field if I need to write false
    end_date = models.DateField(db_column='end_date', null=False,
                                blank=False)  # check about auto field if I need to write false


class WhoToChallenge(models.Model):

    class Meta:
        db_table = 'who_to_challenge'

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='accepts_challenge')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, null=False, blank=False, related_name='who_challenged')
    answer = models.BooleanField(db_column='answer', null=True, blank=True)
    who_challenge = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False,
                                      related_name='Sender_challenge')
    is_read = models.BooleanField(db_column='is_read', default=False)


class UserViewHistory(models.Model):

    class Meta:
        db_table = 'user_view_history'
        ordering = ['view_date']

    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    view_date = models.DateField(db_column='view_date', auto_now=True, null=False, blank=False)
    num_click = models.IntegerField(db_column='num_click', null=True, blank=True)


class UserLike(models.Model):
    class Meta:
        db_table = 'user_like'
        ordering = ['add_date']

    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    add_date = models.DateField(db_column='add_date', auto_now=True, null=False, blank=False)


class UserProfile(models.Model):

    class Meta:
        db_table = 'user_profile'

    user = models.OneToOneField(User, on_delete=models.RESTRICT)
    profile_pic_url = models.CharField(max_length=1024, null=True, blank=True)
    is_google_login = models.BooleanField(db_column='is_google_login', null=True, blank=True)







