"""Django models."""

# -----------------------------------------------------------------------------
# Import
# ------
#
# - Python Standard Library

# - Other Libraries or Frameworks
from django.db import models
from django.contrib.auth.models import User

# - Local Application

# -----------------------------------------------------------------------------
# Module Metadata
# ---------------
#
__author__ = 'Dave Piché'
__version__ = '0.1'

class Athlete(models.Model):
    """A person."""

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)

    def __str__(self):
        """Full name of the person."""
        return '{0} {1}'.format(self.first_name, self.last_name)

class EmailAddress(models.Model):
    """Email address belonging to a person."""

    athlete = models.ForeignKey( Athlete
                               , on_delete=models.CASCADE
                               , related_name='emails'
                               )
    email_address = models.EmailField()

    def __str__(self):
        """Full name of the person."""
        return str(self.email_address)

class Team(models.Model):
    """A cheerleading team."""

    LEVELS = (
        ('MI', 'Mini'),
        ('YH', 'Youth'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
        ('OP', 'Open'),
    )

    name = models.CharField(max_length=200)
    level = models.CharField(max_length=10, choices=LEVELS)
    coaches = models.ManyToManyField( User
                                    , related_name='teams'
                                    , limit_choices_to=models.Q(user__groups__name='Coaches')
                                    )
    athletes = models.ManyToManyField(Athlete, related_name='teams')

    def __str__(self):
        """Full name of the person."""
        return str(self.name)

class Practice(models.Model):
    """A practice session."""

    date = models.DateField()
    team = models.ForeignKey(Team)

    def __str__(self):
        return '{} - {}'.format(self.date, self.team.name)

class Attendance(models.Model):
    """"""

    ATTENDANCES = (
        ('PR', 'Present'),
        ('AB', 'Absent'),
        ('OT', 'Other'),
    )

    pratice = models.ForeignKey(Practice, on_delete=models.CASCADE)
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    attendance = models.CharField(max_length=10, choices=ATTENDANCES)
