from fabric.api import *
import util

@task
def mainstream(old_url, new_url):
    """Change a mainstream slug. Usage: fab preview slug_changes.mainstream:old-slug,new_slug"""
    util.use_random_host('class-backend')
    util.rake('panopticon', 'delete_mainstream_slug_from_search', [old_url])
    util.rake('publisher', 'update_mainstream_slug', [old_url, new_url])
