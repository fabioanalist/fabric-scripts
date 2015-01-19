from fabric.api import *

@task
def bootstrap(utility, config):
    """
    Bootstrap journal files for Heka

    To prevent Heka from reading old log entries and sending duplicate data
    to Elasticsearch, when monitoring new log files. Utility built from:

    https://github.com/dcarley/heka/compare/dcarley:versions/0.8...logstreamer_bootstrap_journals
    """
    put(utility, mirror_local_mode=True)
    put(config)
    sudo('install -d -m0744 /var/cache/hekad/logstreamer')
    sudo('~/%s -config %s -bootstrapJournals' % (utility, config))
    run('rm %s %s' % (utility, config))
