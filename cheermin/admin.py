"""Configuration of the Django admin application."""
# -----------------------------------------------------------------------------
# Import
# ------
#
# - Other libraries and frameworks
from django.contrib import admin
from django.contrib.admin import site
from django.utils.translation import ugettext

# - Local application
from .models import Attendance, Team, Practice
from .models.athlete import Athlete

# -----------------------------------------------------------------------------
# Module Metadata
# ---------------
#
__author__ = 'Dave Piché'

site.site_title = 'Cheermin'
site.site_header = 'Cheermin administration'

@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    """Representation of an athlete in the Django admin interface."""

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
        (ugettext('Team Choice'), {
            'fields': (
                'team_choice_1',
                'team_choice_2',
                'team_choice_3',
            )
        }),
        (ugettext('Personal Health Record'), {
            'classes': ('collapse',),
            'fields': (
                'health_insurance_card_photo',
                'health_insurance_number',
                'health_insurance_expiration_date',
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

    def get_list_display(self, request):
        return self.ordering

    def get_list_display_links(self, request, list_display):
        return list_display

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Representation of an athlete in the Django admin interface."""

    pass

class AttendanceInline(admin.TabularInline):
    """Representation of attendance list."""

    model = Attendance

@admin.register(Practice)
class PracticeAdmin(admin.ModelAdmin):
    """Representation of a practice session."""

    inlines = [AttendanceInline]
