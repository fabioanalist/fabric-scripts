from fabric.api import sudo, task


@task(default=True)
def check(*args):
    """Run rkhunter on the machine"""
    sudo('/usr/local/bin/rkhunter-passive-check')


@task
def propupdate(*args):
    """Update rkhunter file property database on the machine"""
    sudo('/usr/bin/rkhunter --propupdate')


@task
def update(*args):
    """Update rkhunter, check for updates to database files"""
    sudo('/usr/bin/rkhunter --update')
