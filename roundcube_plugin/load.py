#!/usr/local/bin/python3.5
"""Load contacts from Cheermin."""
# -----------------------------------------------------------------------------
# Import
# ------
#
# - Python Standard Library
import argparse
import functools
import json
import os
import sys

# - Other Libraries or Frameworks
import django

# todo: Define this env. variable in the Roundcube plugin.
sys.path += ['/opt/spirit07/cheermin', '/opt/spirit07']
os.environ['DJANGO_SETTINGS_MODULE'] = 'spirit07.settings'

# - Local application

# Load Cheermin Django settings.
# settings.configure()
django.setup()

# Now this script or any imported module can use any part of Django it needs.
from cheermin.models import Athlete, Team
from django.contrib.auth.models import User

def main():
    """Program entry-point."""
    args = cli()
    if args.command == 'groups':
        data = groups(search=args.search, search_mode=args.search_mode)
    elif args.command == 'get_record_groups':
        data = get_record_groups(record_id=args.record_id)
    elif args.command == 'records':
        data = records(args.group_id)
    else:
        sys.stderr.write('Error: unknown command %s' % args.command)
        return 1
    print(json.dumps(data))
    return 0

def cli():
    """Command-line interface."""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help', dest='command')

    parser_get_record_groups = subparsers.add_parser('get_record_groups', help=get_record_groups.__doc__.splitlines()[0])
    parser_get_record_groups.add_argument('record_id')

    parser_groups = subparsers.add_parser('groups', help=groups.__doc__.splitlines()[0])
    parser_groups.add_argument('--search')
    parser_groups.add_argument('--search-mode', choices=['strict', 'prefix', 'fuzzy'], default='fuzzy')

    parser_records = subparsers.add_parser('records', help=records.__doc__.splitlines()[0])
    parser_records.add_argument('--group-id', help='ID of the group')

    return parser.parse_args()

def groups(search=None, search_mode='fuzzy'):
    """Return all available groups."""
    data = [{'ID': 'everyone', 'name': 'Tous le monde', 'virtual': False, 'email': []}]
    for team in Team.objects.all().order_by('name'):
        data.append({'ID': 'team_{}'.format(team.pk), 'name': 'Team: {}'.format(team), 'virtual': False, 'email': []})
    team_filter = None
    if search:
        search = search.lower()
        if search_mode == 'fuzzy':
            def team_filter(team):
                return search in team['name'].lower()
        elif search_mode == 'prefix':
            def team_filter(team):
                team_name = team['name']
                if team_name.startswith('Team: '):
                    team_name = team_name[6:]
                return team_name.lower().startswith(search)
        else:
            def team_filter(team):
                team_name = team['name']
                if team_name.startswith('Team: '):
                    team_name = team_name[6:]
                return search == team_name.lower()
    data = list(filter(team_filter, data))
    return data

def records(group_id=None):
    """Returns records."""
    data = []

    group = None
    if group_id and group_id != 'everyone':
        group = group_id.rsplit('_', maxsplit=1)[-1]

    query = User.objects.exclude(email__isnull=True).exclude(email='')
    if group:
        query = query.filter(teams__pk=group)
    for contact in query.order_by('first_name'):
        data.append({
            'ID': 'coach_{}'.format(contact.pk),
            'name': 'Coach: {} {}'.format(contact.first_name, contact.last_name),
            'firstname': contact.first_name,
            'surname': contact.last_name,
            'email': contact.email,
        })

    query = Athlete.objects.exclude(active=False).exclude(email__isnull=True).exclude(email='')
    if group:
        query = query.filter(teams__pk=group)
    for contact in query.order_by('first_name'):
        data.append({
            'ID': 'athlete_{}'.format(contact.pk),
            'name': str(contact),
            'firstname': contact.first_name,
            'surname': contact.last_name,
            'email': contact.email,
        })

    return data

def get_record_groups(record_id):
    """Get groups for a contact."""
    group_id = sys.argv[2].rsplit('_', maxsplit=1)[-1]
    groups = [{'ID': 'everyone', 'name': 'Tous le monde'}]
    groups += ({'ID': 'team_{}'.format(team.pk), 'name': 'Team: {}'.format(team)} for team in Athlete.objects.get(pk=record_id.rsplit('_', maxsplit=1)[-1]).teams.all())
    return groups

if __name__ == '__main__':
    sys.exit(main())
