"""Django models."""

# -----------------------------------------------------------------------------
# Import
# ------
#
# - Other Libraries or Frameworks
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext

# - Local application
from .athlete import Athlete

# -----------------------------------------------------------------------------
# Module Metadata
# ---------------
#
__author__ = 'Dave Piché'

class Membership(models.Model):
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    primary = models.BooleanField()

class Team(models.Model):
    """A cheerleading team."""

    verbose_name = ugettext('Team')

    CATEGORIES = (
        ('RC', 'Récréatif'),
        ('MI', 'Mini'),
        ('YH', 'Youth'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
        ('OI', 'Open International'),
        ('OP', 'Open'),
        ('MD', 'Mom & Dad'),
    )

    LEVELS = (
        ('1', '1'),
        ('2.0', '2.0'),
        ('2', '2'),
        ('3', '3'),
        ('4.2', '4.2'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
    )

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=10, choices=CATEGORIES, null=True, blank=True)
    level = models.CharField(max_length=10, choices=LEVELS, null=True, blank=True)
    coaches = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='teams',
        limit_choices_to=models.Q(groups__name='Coaches'),
    )
    athletes = models.ManyToManyField(
        Athlete,
        related_name='teams',
        through=Membership,
        through_fields=('team', 'athlete'),
    )

    def __str__(self):
        """Full name of the person."""
        return str(self.name)

class Practice(models.Model):
    """A practice session."""

    verbose_name = ugettext('Practice')

    date = models.DateField()
    team = models.ForeignKey(Team)

    def __str__(self):
        """Return the date of the practice and the name of the team."""
        return '{} - {}'.format(self.date, self.team.name)

class Attendance(models.Model):
    """Presence status of an athlete at a practice."""

    ATTENDANCES = (
        ('PR', 'Present'),
        ('AB', 'Absent'),
        ('OT', 'Other'),
    )

    pratice = models.ForeignKey(Practice, on_delete=models.CASCADE)
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    attendance = models.CharField(max_length=10, choices=ATTENDANCES)
    note = models.CharField(max_length=4096)

class UserPreferences(models.Model):
    """Preference of a Cheermin user."""

    FIELDS = (
        ('FN', ugettext('First name')),
        ('LN', ugettext('Last name')),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='preferences',
        primary_key=True,
    )
    athletes_list_first_column = models.CharField(max_length=8, choices=FIELDS)

class FeeBase(models.Model):

    def __str__(self):
        return self.name

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='fee')
    name = models.CharField(max_length=128)
    amount = models.FloatField(verbose_name=ugettext('Amount'))
    depot = models.FloatField(verbose_name=ugettext('Depot'), null=True, blank=True)

class Fee(FeeBase):

    verbose_name = ugettext('Fee')
    due_date = models.DateField(verbose_name=ugettext('Due Date'), null=True, blank=True)

class MonthlyFee(FeeBase):
    """docstring for MonthlyPayment"""

    verbose_name = ugettext('Monthly Fee')
    monthly_payment = models.FloatField(verbose_name=ugettext('Monthly Payment'), max_length=128, null=True, blank=True)
    start_date = models.DateField(
        verbose_name=ugettext('Start Date'),
        blank=False,
        null=True,
    )

class MonthlyFeeVariable(FeeBase):
    """docstring for MonthlyPayment"""

    verbose_name = ugettext('Variable Monthly Fee')
    start_date = models.DateField(
        verbose_name=ugettext('Start Date'),
        blank=False,
        null=True,
    )
    number_of_payments = models.IntegerField(
        verbose_name=ugettext('Number of payments'),
        blank=False,
        null=True,
    )

class Credit(models.Model):

    name = models.CharField(max_length=128)
    amount = models.FloatField(verbose_name=ugettext('Amount'))
    fee = models.ForeignKey(
        FeeBase,
        on_delete=models.CASCADE,
        related_name='credit',
    )
    athlete = models.ManyToManyField(
        Athlete,
        related_name='credit',
        blank=True,
    )

    def __str__(self):
        return self.name
