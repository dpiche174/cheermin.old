"""Cheermin accounting models."""

# -----------------------------------------------------------------------------
# Import
# ------
#
# - Other Libraries or Frameworks
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import ugettext

# -----------------------------------------------------------------------------
# Module Metadata
# ---------------
#
__author__ = 'Dave Piché'

class Fee(models.Model):
    """Represent a fee an athlete must pay to be part of a team."""

    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='fees')
    name = models.CharField(max_length=256)
    amount = models.FloatField(verbose_name=ugettext('Amount'), default=0, validators=[MinValueValidator(0)])
    depot = models.FloatField(verbose_name=ugettext('Depot'), default=0)
    due_date = models.DateField(verbose_name=ugettext('Due Date'), null=True)

    # number_of_payments = models.IntegerField(
    #     verbose_name=ugettext('Number of payments'),
    #     blank=False,
    #     null=True,
    # )
    # monthly_payment = models.FloatField(verbose_name=ugettext('Monthly Payment'), max_length=128, null=True, blank=True)
    # start_date = models.DateField(
    #     verbose_name=ugettext('Start Date'),
    #     blank=False,
    #     null=True,
    # )
    # start_date = models.DateField(
    #     verbose_name=ugettext('Start Date'),
    #     blank=False,
    #     null=True,
    # )

    def clean(self):
        # Don't allow draft entries to have a pub_date.
        if self.depot > self.amount:
            raise ValidationError(ugettext('Depot cannot be greater than amount.'))

    class Meta:
        verbose_name = ugettext('fee')
        verbose_name_plural = ugettext('fees')

    def __str__(self):
        """Return name of the fee."""
        return self.name

# class Credit(models.Model):

#     name = models.CharField(max_length=128)
#     amount = models.FloatField(verbose_name=ugettext('Amount'))
#     fee = models.ForeignKey(
#         FeeBase,
#         on_delete=models.CASCADE,
#         related_name='credit',
#     )
#     athlete = models.ManyToManyField(
#         Athlete,
#         related_name='credit',
#         blank=True,
#     )

#     def __str__(self):
#         return self.name
