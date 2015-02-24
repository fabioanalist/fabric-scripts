from fabric.api import task, hosts, sudo, cd, execute, runs_once, roles


@task
def change_organisation_slug(old_slug, new_slug):
    """Change an organisation slug and all associated artefacts."""
    execute(whitehall_change_organisation_slug, old_slug, new_slug)
    execute(panopticon_change_organisation_slug, old_slug, new_slug)
    execute(signon_change_organisation_slug, old_slug, new_slug)
    execute(need_api_change_organisation_slug, old_slug, new_slug)
    execute(contacts_change_organisation_slug, old_slug, new_slug)


@task
@runs_once
@roles('class-whitehall_backend')
def whitehall_change_organisation_slug(old_slug, new_slug):
    with cd('/var/apps/whitehall'):
        sudo("govuk_setenv whitehall bundle exec rake change_organisation_slug['%s','%s']" % (old_slug, new_slug), user='deploy')

@task
@runs_once
@roles('class-backend')
def panopticon_change_organisation_slug(old_slug, new_slug):
    with cd('/var/apps/panopticon'):
        sudo("govuk_setenv panopticon bundle exec rake change_organisation_slug['%s','%s']" % (old_slug, new_slug), user='deploy')

@task
@runs_once
@roles('class-backend')
def signon_change_organisation_slug(old_slug, new_slug):
    with cd('/var/apps/signon'):
        sudo("govuk_setenv signon bundle exec rake update_organisation_slug['%s','%s']" % (old_slug, new_slug), user='deploy')

@task
@runs_once
@roles('class-backend')
def need_api_change_organisation_slug(old_slug, new_slug):
    with cd('/var/apps/need-api'):
        sudo("govuk_setenv panopticon bundle exec rake organisations:import", user='deploy')
        sudo("govuk_setenv panopticon bundle exec rake change_organisation_slug['%s','%s']" % (old_slug, new_slug), user='deploy')

@task
@runs_once
@roles('class-backend')
def contacts_change_organisation_slug(old_slug, new_slug):
    with cd('/var/apps/contacts'):
        sudo("govuk_setenv contacts bundle exec rake update_organisation_slug['%s','%s']" % (old_slug, new_slug), user='deploy')

