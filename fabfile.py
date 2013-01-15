from __future__ import print_function

from collections import defaultdict
import json
import sys
import subprocess
import textwrap
import urllib
import urllib2

from fabric import state
from fabric.colors import *
from fabric.api import *
from fabric.task_utils import crawl

# Our command submodules
import cache
import licensify
import mongo
import puppet
import search
import vm

env.hosts = []
env.roledefs = defaultdict(list)

def facter(*args):
    facter_args = ['facter', '--json']
    facter_args.extend(args)
    proc = subprocess.Popen(facter_args, stdout=subprocess.PIPE)
    out, err = proc.communicate()

    if proc.returncode != 0:
        raise RuntimeError("facter returned non-zero exit code! (args={0})".format(args))

    return json.loads(out)

if facter('govuk_class')['govuk_class'] != 'jumpbox':
    print("ERROR: govuk_fab is designed to run from a jumpbox (govuk_class != jumpbox)", file=sys.stderr)
    sys.exit(1)

with hide('running'):
    qs = urllib.urlencode({'query': '["=", ["node", "active"], true]'})
    res = urllib2.urlopen('http://puppetdb.cluster/nodes?{0}'.format(qs))
    hosts = json.load(res)

for host in hosts:
    try:
        name, vdc, org = host.rsplit('.', 3)
    except ValueError:
        print("WARNING: discarding badly formatted hostname '{0}'".format(host), file=sys.stderr)
        continue

    env.roledefs['all'].append(host)
    env.roledefs['org-%s' % org].append(host)
    env.roledefs['vdc-%s' % vdc].append(host)
    env.roledefs['class-%s' % name.rstrip('-1234567890')].append(host)

@task
def help(name):
    """Show extended help for a task (e.g. 'fab help:search.reindex')"""
    task = crawl(name, state.commands)

    if task is None:
        abort("%r is not a valid task name" % task)

    puts(textwrap.dedent(task.__doc__).strip())

@task
def list(role='all'):
    """List known hosts"""
    puts('\n'.join(sorted(env.roledefs[role])))

@task
def list_roles():
    """List available roles"""
    for role in sorted(env.roledefs.keys()):
        print("%-30.30s : %s" % (role, len(env.roledefs[role])))

@task
def do(command):
    """Execute arbitrary commands"""
    run(command)

@task
def sdo(command):
    """Execute arbitrary commands with sudo"""
    sudo(command)
