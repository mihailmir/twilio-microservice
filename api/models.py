from peewee import Model, CharField, BooleanField, IntegerField, DateTimeField, TextField, ForeignKeyField
from config import Envs
import peewee_async

locker_db = peewee_async.PostgresqlDatabase(
    Envs.DB_NAME,
    user=Envs.DB_USER,
    password=Envs.DB_PASS,
    host=Envs.DB_HOST,
    port=Envs.DB_PORT
)
locker_db.set_allow_sync(False)
objects = peewee_async.Manager(locker_db)


hearing_source_choices = (
    ('Google Maps', 'Google Maps'),
    ('Google Search', 'Google Search'),
    ('Facebook or Instagram Post/Ad', 'Facebook or Instagram Post/Ad'),
    ('Signage/Walked by', 'Signage/Walked by'),
    ('Friend/Family', 'Friend/Family'),
    ('Flyer', 'Flyer'),
    ('Yelp', 'Yelp'),
    ('Other', 'Other'),
)


class SupportPhone(Model):
    id = IntegerField()
    number = CharField(max_length=31)
    active = BooleanField(default=True)
    priority = IntegerField(default=0)
    created = DateTimeField(null=True)
    updated = DateTimeField(null=True)

    class Meta:
        db_table = 'portal_supportphone'
        database = locker_db


class Tenant(Model):
    id = IntegerField()
    acc_info = TextField(null=True)
    first_name = CharField(max_length=130, null=True)
    last_name = CharField(max_length=150, null=True)
    business_name = CharField(max_length=256, null=True)
    phone = CharField(max_length=64)
    address_line_1 = CharField(max_length=512, null=True)
    apartment = CharField(max_length=512, null=True)
    address_line_2 = CharField(max_length=512, null=True)
    city = CharField(max_length=128, null=True)
    state = CharField(max_length=128, null=True)
    postal = CharField(max_length=128, null=True)
    hubspot_contact_id = CharField(max_length=128, null=True)
    email = CharField(unique=True)
    heard_about_us = CharField(choices=hearing_source_choices, max_length=64, null=True)
    stripe_id = CharField(max_length=128, null=True)
    created = DateTimeField(null=True)
    updated = DateTimeField(null=True)

    class Meta:
        db_table = 'portal_tenant'
        database = locker_db

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'


class TwilioNumber(Model):
    id = IntegerField()
    number = CharField(max_length=31)

    def __str__(self):
        return f"{self.number}"

    class Meta:
        db_table = 'calls_twillionumber'
        database = locker_db


class Location(Model):
    id = IntegerField()
    title = CharField(max_length=512, null=True)
    address = CharField(max_length=512, null=True)
    telephone = CharField(max_length=64, null=True)
    zip_code = CharField(max_length=32, null=True)
    access_instructions = TextField(null=True)
    my_business_location_name = CharField(max_length=256, null=True)
    google_place_id = CharField(max_length=128, null=True)
    twillio_phone = ForeignKeyField(TwilioNumber, null=True)

    details = TextField()
    created = DateTimeField(null=True)
    updated = DateTimeField(null=True)
    three_minimum_months_required = BooleanField(default=False)
    emails_disabled = BooleanField(default=False)
    hubspot_location = CharField(default='Unknown', max_length=256)
    is_hidden = BooleanField(default=False)

    class Meta:
        db_table = 'portal_location'
        database = locker_db


class Site(Model):
    id = IntegerField()
    domain = CharField(max_length=100)
    name = CharField(max_length=50, null=True)

    class Meta:
        db_table = 'django_site'
        database = locker_db

