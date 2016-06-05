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

class Team(models.Model):
    """A cheerleading team."""

    verbose_name = ugettext('Team')

    LEVELS = (
        ('MI', 'Mini'),
        ('YH', 'Youth'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
        ('OP', 'Open'),
    )

    name = models.CharField(max_length=200)
    level = models.CharField(max_length=10, choices=LEVELS)
    coaches = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='teams',
        limit_choices_to=models.Q(groups__name='Coaches'),
    )
    athletes = models.ManyToManyField(Athlete, related_name='teams')

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
