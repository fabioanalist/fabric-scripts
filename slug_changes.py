from fabric.api import *
import util

@task
def mainstream(old_url, new_url):
    """Change a mainstream slug. Usage: fab preview slug_changes.mainstream:old-slug,new_slug"""
    util.use_random_host('class-backend')
    util.rake('panopticon', 'delete_mainstream_slug_from_search', [old_url])
    util.rake('publisher', 'update_mainstream_slug', [old_url, new_url])
# TODO: UPDATE DOCS @  https://github.com/alphagov/wiki/wiki/Changing-GOV.UK-URLs#making-the-change
# AFTER RENAME OF ABOVE slug_changes.mainstream TASK - IT IS NO LONGER mainstream_slugs.update!!!

@task
def organisation(old_slug, new_slug, dry_run=True):
    """Change an organisation slug. Usage: fab preview slug_changes.organisation:old-slug,new-slug,dry_run=True"""
    if dry_run:
        print_long_instructions_and_warning()
    else
        do_organisation_slug_change(old_slug, new_slug)

def do_organisation_slug_change(old_slug, new_slug):
    util.use_random_host('class-backend')

    ### CHECK ORDER HERE!!!!!!!! ####
    util.rake('signonotron2',   'update_organisation_slug', [old_slug, new_slug])
    util.rake('whitehall',      'change_organisation_slug', [old_slug, new_slug])
    util.rake('panopticon',     'change_organisation_slug', [old_slug, new_slug])
    util.rake('hmrc-contacts',  'update_organisation_slug', [old_slug, new_slug])
    # Transition
    # Need API
    clear_maslow_cache()

def clear_maslow_cache:
    sudo('service maslow reload')

def print_long_instructions_and_warning:
    """
1. change signon (other slug change cascades down to other apps)
2. change whitehall
3. change panopticon
4. change need api
5. change contacts
6. change redirector
7. add redirector
8. tell search and browse team
"""

# Bear in mind
# - side effect on govukdelivery (topic mapping change)

# Transition steps:
# - make a pull request against transition-config to amend the sites (check extra_organisation_slugs too)
# - make sure it's been reviewed and ready to merge
# - disable https://deploy.production.alphagov.co.uk/job/Transition_load_site_config/configure
# - run fabric script
#   -
#   -
#   -
#   - run transition rake task
#   -
#   -
#   -
# - merge PR
# - delpoy transition-config
# - re-enable https://deploy.production.alphagov.co.uk/job/Transition_load_site_config/configure
