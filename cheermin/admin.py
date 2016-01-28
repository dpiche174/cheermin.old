"""Configuration of the Django admin application."""
# -----------------------------------------------------------------------------
# Import
# ------
#
# - Other libraries and frameworks
from django.contrib import admin

# - Local Applicaiton
from .models import Attendance, EmailAddress, Team, Athlete, Practice

# -----------------------------------------------------------------------------
# Module Metadata
# ---------------
#
__author__ = 'Dave Piché'
__version__ = '0.1'

class EmailAddressInline(admin.TabularInline):
    """Table linking email addresses to athlete."""

    model = EmailAddress

@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    """Representation of an athlete in the Django admin interface."""

    inlines = [EmailAddressInline]

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
