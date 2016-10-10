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
from django.utils.translation import ugettext_lazy
from multi_email_field.fields import MultiEmailField

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

    class Meta:
        verbose_name = ugettext_lazy('Athlete')

    # Name
    first_name = models.CharField(max_length=200, verbose_name=ugettext_lazy('First name'))
    last_name = models.CharField(max_length=200, verbose_name=ugettext_lazy('Last name'))

    active = models.BooleanField( null=False, blank=False, default=True
                                , verbose_name=ugettext_lazy('Active')
                                , help_text=ugettext_lazy("If the athlete is not active he won't show up in the forms and he won't receive emails.")
                                )

    # Address
    street = models.CharField(
        max_length=200,
        null=True,
        blank=False,
        verbose_name=ugettext_lazy('Street'),
    )
    city = models.CharField(
        max_length=200,
        null=True,
        blank=False,
        verbose_name=ugettext_lazy('City'),
    )
    province = models.CharField(
        max_length=200,
        choices=PROVINCES_CHOICES,
        default='QC',
        null=True,
        blank=False,
        verbose_name=ugettext_lazy('Province'),
    )
    country = models.CharField(
        max_length=200,
        editable=False,
        default='Canada',
        null=True,
        blank=False,
        verbose_name=ugettext_lazy('Country'),
    )
    postal_code = models.CharField(
        max_length=200,
        null=True,
        blank=False,
        verbose_name=ugettext_lazy('Postal code'),
    )

    # Age
    birthday = models.DateField(null=True, blank=False, verbose_name=ugettext_lazy('Birthday'))

    # Contact
    phone_number = models.CharField(max_length=200, null=True, blank=False, verbose_name=ugettext_lazy('Phone number'))
    email = MultiEmailField(null=True, blank=True, verbose_name=ugettext_lazy('Email addresses'))

    photo = models.ImageField(
        upload_to=os.path.normpath('cheermin/athletes/'),
        null=True,
        blank=True,
        verbose_name=ugettext_lazy('Photo'),
    )

    # Personal Health Record
    health_insurance_card_photo = models.ImageField(
        upload_to=os.path.normpath('cheermin/athletes/health_insurance_card/'),
        null=True,
        blank=True,
        verbose_name=ugettext_lazy('Health Insurance Card'),
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
        verbose_name=ugettext_lazy('Secondary ID Card'),
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

    @property
    def email_addresses(self):
        """Return althetes email addresses."""
        return self.email.split('\n')

    @email_addresses.setter
    def email_addresses(self, addreses):
        """Set athlete email addresses."""
        self.email = '\n'.join(addresses)

photo_height = 265  # px
photo_width = 206  # px
