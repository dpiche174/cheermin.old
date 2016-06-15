"""Athlete model."""
# -----------------------------------------------------------------------------
# Import
# ------
#
# - Python Standard Library
import os

# - Local application

# - Other Libraries or Frameworks
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext

# -----------------------------------------------------------------------------
# Module Metadata
# ---------------
#
__author__ = 'Dave Piché'

PROVINCES_CHOICES = (
    ('QC', 'Québec'),
    ('ON', 'Ontario'),
)

class Athlete(models.Model):
    """An athlete."""

    app_label = 'cheermin'
    model_name = 'athlete'
    verbose_name = ugettext('Athlete')

    # Name
    first_name = models.CharField(max_length=200, verbose_name=ugettext('First name'))
    last_name = models.CharField(max_length=200, verbose_name=ugettext('Last name'))

    # Address
    street = models.CharField(
        max_length=200,
        null=True,
        blank=False,
        verbose_name=ugettext('Street'),
    )
    city = models.CharField(
        max_length=200,
        null=True,
        blank=False,
        verbose_name=ugettext('City'),
    )
    province = models.CharField(
        max_length=200,
        choices=PROVINCES_CHOICES,
        default='QC',
        null=True,
        blank=False,
        verbose_name=ugettext('Province'),
    )
    country = models.CharField(
        max_length=200,
        editable=False,
        default='Canada',
        null=True,
        blank=False,
        verbose_name=ugettext('Country'),
    )
    postal_code = models.CharField(
        max_length=200,
        null=True,
        blank=False,
        verbose_name=ugettext('Postal code'),
    )

    # Age
    birthday = models.DateField(null=True, blank=False, verbose_name=ugettext('Birthday'))

    # Contact
    phone_number = models.CharField(max_length=200, null=True, blank=False, verbose_name=ugettext('Phone number'))
    email = models.EmailField(null=True, blank=True, verbose_name=ugettext('Email address'))

    photo = models.ImageField(
        upload_to=os.path.normpath('cheermin/athletes/'),
        null=True,
        blank=True,
        verbose_name=ugettext('Photo'),
    )

    # Personal Health Record
    health_insurance_card_photo = models.ImageField(
        upload_to=os.path.normpath('cheermin/athletes/health_insurance_card/'),
        null=True,
        blank=True,
        verbose_name=ugettext('Health Insurance Card'),
    )
    health_insurance_number = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )
    health_insurance_expiration_date = models.DateField(
        null=True,
        blank=True,
    )
    secondary_id_card = models.ImageField(
        upload_to=os.path.normpath('cheermin/athletes/secondary_id_card/'),
        null=True,
        blank=True,
        verbose_name=ugettext('Secondary ID Card'),
    )

    # TODO: Add checkbox to tell no health issue.
    health_problems = models.TextField(
        null=True,
        blank=True,
    )
    allergies = models.TextField(
        null=True,
        blank=True,
    )
    father_name = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )
    father_phone_number = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )
    mother_name = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )
    mother_phone_number = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )
    other_contact_name = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )
    other_contact_phone_number = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    def __str__(self):
        """Full name of the person."""
        return '{0} {1}'.format(self.first_name, self.last_name)

photo_height = 265  # px
photo_width = 206  # px
