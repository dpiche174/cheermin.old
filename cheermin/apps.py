"""Configuration of the Cheermin application."""
# -----------------------------------------------------------------------------
# Import
# ------
#
# - Other libraries and frameworks
from django.apps import AppConfig

# -----------------------------------------------------------------------------
# Module Metadata
# ---------------
#
__author__ = 'Dave Piché'
__version__ = '0.1'

# -----------------------------------------------------------------------------
# CheerminAdminConfig
# ^^^^^^^^^^^^^^^^^^^
#
class CheerminAdminConfig(AppConfig):
    """Cheermin configuration."""

    name = 'cheermin'
    verbose_name = 'Cheermin'
