"""Cheermin team models."""

# -----------------------------------------------------------------------------
# Import
# ------
#
# - Other Libraries or Frameworks
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext

# - Local application
from . import accounting
from .athlete import Athlete

# -----------------------------------------------------------------------------
# Module Metadata
# ---------------
#
__author__ = 'Dave Piché'

class Team(models.Model):
    """A cheerleading team."""

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
        through='Membership',
        through_fields=('team', 'athlete'),
    )

    class Meta:
        verbose_name = ugettext('team')
        verbose_name_plural = ugettext('teams')

    def __str__(self):
        """Return name of the team."""
        return self.name

class Membership(models.Model):
    """Represent the membership of an athlete in a team."""

    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    primary = models.BooleanField()
