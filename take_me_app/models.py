from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.


class BusinessType(models.Model):

    class Meta:
        db_table = 'business_type'
        ordering = ['id']

    name = models.CharField(db_column='name', max_length=256, null=False, blank=False)


class Business(models.Model):

    class Meta:
        db_table = 'business'
        ordering = ['id']

    name = models.CharField(db_column='name', max_length=64, null=False, blank=False)
    description = models.CharField(db_column='description', null=True, blank=True)
    phone_num = models.IntegerField(db_column='phone_num', validators=[MinValueValidator()], null=False, blank=False)
    menu_url = models.URLField(db_column='menu_url', null=True, blank=True)
    rush_hour = models.TimeField(db_column='rush_hour')
    create_date = models.DateField(db_column='create_date', auto_now=True)
    views_num = models.IntegerField(db_column='views_num') # TODO: ask how i can do automation when someone view it
                                                            # TODO: will add 1 automatic

    business_type = models.ManyToManyField(BusinessType, through='BusinessAndType')

    # addres_id =
    # opening_hours = models.ForeignKey()
    #

class Address(models.Model):

    class Meta:
        db_table = 'address'
        ordering = ['id']

    business = models.ForeignKey(Business, on_delete=models.RESTRICT, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    city = models.CharField(db_column='city', max_length=256, null=False, blank=False)
    street = models.CharField(db_column='street', max_length=256, null=False, blank=False)
    number = models.SmallIntegerField(db_column='number', null=False, blank=False)
    zip_code = models.IntegerField(db_column='zip_code', null=True, blank=True)
    floor = models.SmallIntegerField(db_column='floor', null=True, blank=True)
    apartment_num = models.SmallIntegerField(db_column='apartment_num', null=True, blank=True)
    is_business = models.BooleanField(db_column='is_business')

    # Must be one of the two User or Business

class BusinessAndType(models.Model):

    class Meta:
        db_table = 'business_and_type'
        ordering = ['id']

    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    business_type = models.ForeignKey(BusinessType, on_delete=models.CASCADE)


class OpeningHours(models.Model):

    class Meta:
        db_table = 'opening_hours'

    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    sun_open = models.TimeField(db_column='sun_open', null=True, blank=True)
    sun_close = models.TimeField(db_column='sun_close', null=True, blank=True)
    mon_open = models.TimeField(db_column='mon_open', null=True, blank=True)
    mon_close = models.TimeField(db_column='mon_close', null=True, blank=True)
    tues_open = models.TimeField(db_column='tues_open', null=True, blank=True)
    tues_close = models.TimeField(db_column='tues_close', null=True, blank=True)
    wed_open = models.TimeField(db_column='wed_open', null=True, blank=True)
    wed_close = models.TimeField(db_column='wed_close', null=True, blank=True)
    thurs_open = models.TimeField(db_column='sun_open', null=True, blank=True)
    thurs_close = models.TimeField(db_column='sun_close', null=True, blank=True)
    fri_open = models.TimeField(db_column='sun_open', null=True, blank=True)
    fri_close = models.TimeField(db_column='sun_close', null=True, blank=True)
    sat_open = models.TimeField(db_column='sun_open', null=True, blank=True)
    sat_close = models.TimeField(db_column='sun_close', null=True, blank=True)


class BusinessChallenge(models.Model):

    class Meta:
        db_table = 'business_challenge'
        ordering = ['id']

    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    challenge_type = models.ForeignKey()  # TODO: table
    challenge_name = models.CharField(db_column='challenge_name', max_length=256, null=False, blank=False)
    date = models.DateField(db_column='date', null=False, blank=False) # check about auto field if I need to write false
    text_on_challenge = models.CharField(db_column='text_on_challenge', null=True, blank=True)










