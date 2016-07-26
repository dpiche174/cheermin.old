"""Configuration of the Django admin application."""
# -----------------------------------------------------------------------------
# Import
# ------
#
# - Other libraries and frameworks
from django import forms
from django.contrib import admin
from django.contrib.admin import options
from django.contrib.admin import site
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext

# - Local application
from .models import accounting
from .models.athlete import Athlete
from .models.team import Team, Membership

# -----------------------------------------------------------------------------
# Module Metadata
# ---------------
#
__author__ = 'Dave Piché'

site.site_title = 'Cheermin'
site.site_header = ugettext('Cheermin Administration')

class TeamInline(admin.TabularInline):
    """Representation of attendance list."""

    model = Team.athletes.through

class AthleteAdminForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = Athlete
        widgets = {'birthday': admin.widgets.AdminDateWidget(attrs={'placeholder': ugettext('DD/MM/YYYY')})}

# class CreditInline(admin.TabularInline):
#     """Representation of attendance list."""

#     model = Credit.athlete.through

class MembershipInline(admin.TabularInline):

    model = Membership

@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    """Representation of an athlete in the Django admin interface."""

    form = AthleteAdminForm

    # inlines = [TeamInline, CreditInline]

    ordering = ('first_name', 'last_name')
    readonly_fields = ('country',)
    fieldsets = (
        (ugettext('Personal Information'), {
            'fields': (
                'first_name',
                'last_name',
                'street',
                'city',
                'province',
                'country',
                'postal_code',
                'birthday',
                'phone_number',
                'email',
                'photo',
            )
        }),
        # (ugettext('Team Choice'), {
        #     'fields': (
        #         'team',
        #     )
        # }),
        (ugettext('Personal Health Record'), {
            'classes': ('collapse',),
            'fields': (
                'health_insurance_card_photo',
                'health_insurance_number',
                'health_insurance_expiration_date',
                'secondary_id_card',
                'health_problems',
                'allergies',
                'father_name',
                'father_phone_number',
                'mother_name',
                'mother_phone_number',
                'other_contact_name',
                'other_contact_phone_number',
            )
        }),
    )
    inlines = [MembershipInline]

    def get_list_display(self, request):
        return self.ordering

    def get_list_display_links(self, request, list_display):
        return list_display

    def get_absolute_url(self):
        return '/athletes/%i/' % self.id

    def view_on_site(self, athlete):
        return '/athletes/%i/' % athlete.id

class FeeInline(admin.TabularInline):

    model = accounting.Fee

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Representation of an athlete in the Django admin interface."""

    inlines = [FeeInline]
