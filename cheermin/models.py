"""Django models."""

# -----------------------------------------------------------------------------
# Import
# ------
#
# - Other Libraries or Frameworks
from django.db import models
from django.contrib.auth.models import User

# -----------------------------------------------------------------------------
# Module Metadata
# ---------------
#
__author__ = 'Dave Piché'

class Athlete(models.Model):
    """A person."""

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __str__(self):
        """Full name of the person."""
        return '{0} {1}'.format(self.first_name, self.last_name)

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
    coaches = models.ManyToManyField(
        User,
        related_name='teams',
        limit_choices_to=models.Q(groups__name='Coaches'),
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
