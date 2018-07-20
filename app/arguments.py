#!/usr/bin/env python3
"""Allows to pass arguments to the drucker command"""

import subprocess as s
import colorful as c
import argparse
import variables as v
import sys as q
import orchestration as o

p = argparse.ArgumentParser()

p.add_argument('--health',
    dest='health',
    action="store_true",
    help='Runs a service healthcheck')

p.add_argument('--start',
    dest='start',
    action="store_true",
    help='Starts all drucker containers')

p.add_argument('--list',
    dest='list',
    action="store_true",
    help='Lists all deployed apps')

p.add_argument('--tests',
    dest='tests',
    action="store_true",
    help='Runs the Ansible test suite')

p.add_argument('--version',
    dest='version',
    action="store_true",
    help='Returns the drucker version')

args = p.parse_args()

def containers_health():
    print("health")

def containers_start():
    print("start")

def app_list():
    s.run('''docker exec -it %s cat %s/.app-registry
          ''' % (v.WEB_CONTAINER, v.CONTAINER_HTML_PATH), shell=True)

def run_tests():
    """Runs the Ansible test suite"""
    php_version_check = s.getoutput('''docker exec -u %s -it %s /bin/cat /etc/php/default_php_version
                                    ''' % (v.APP, v.WEB_CONTAINER))
    if v.DEFAULT_PHP not in php_version_check:
        print("Tests need to be executed against the current stable PHP version")
        print("Please switch to PHP %s with 'drucker php:%s'" % (v.DEFAULT_PHP, v.DEFAULT_PHP))
        q.exit()

    for group in v.TEST_GROUPS:
        o.run_tests_orchestration(group)

def return_version():
    """Returns either the latest commit hash or tagged release"""
    latest_commit= s.getoutput("cd %s && git rev-parse --short HEAD" % (v.APP_ROOT))

    if 'dev' in v.APP_VERSION:
        print("You are running the dev version at commit " + c.orange(latest_commit))
    else:
        print("You are running tagged release " + c.orange(v.APP_VERSION))

if args.health:
    containers_health()
elif args.start:
    containers_start()
elif args.list:
    app_list()
elif args.tests:
    run_tests()
elif args.version:
    return_version()

# drucker_argument() {
#   if [[ -n "${COMMAND}" ]] && \
#        [[ "${COMMAND}" != "containers:health" ]] && \
#        [[ "${COMMAND}" != "containers:start" ]] && \
#        [[ "${COMMAND}" != "containers:stop" ]] && \
#        [[ "${COMMAND}" != "containers:restart" ]] && \
#        [[ "${COMMAND}" != "app:drupal" ]] && \
#        [[ "${COMMAND}" != "app:lightning" ]] && \
#        [[ "${COMMAND}" != "app:reservoir" ]] && \
#        [[ "${COMMAND}" != "app:blt" ]] && \
#        [[ "${COMMAND}" != "app:delete" ]] && \
#        [[ "${COMMAND}" != "app:import" ]] && \
#        [[ "${COMMAND}" != "app:dev" ]] && \
#        [[ "${COMMAND}" != "app:prod" ]] && \
#        [[ "${COMMAND}" != "php:7.1" ]] && \
#        [[ "${COMMAND}" != "php:7.2" ]] && \
#        [[ "${COMMAND}" != "tests" ]] && \
#        [[ "${COMMAND}" != "help" ]]; then
#     usage
#   else
#     case "$COMMAND" in
#       containers:health)
#         run_healthcheck
#       ;;
#       containers:start)
#       if [[ "${COMMAND}" == "containers:start" ]]; then
#         start_containers
#       fi
#       ;;
#       containers:stop)
#       if [[ "${COMMAND}" == "containers:stop" ]]; then
#         stop_containers
#         exit 0
#       fi
#       ;;
#       containers:restart)
#       if [[ "${COMMAND}" == "containers:restart" ]]; then
#         restart_containers
#       fi
#       ;;
#       app:drupal)
#       if [[ "${COMMAND}" == "app:drupal" ]] && [[ -z ${SITENAME} ]] || [[ ! ${SITENAME} =~ [^[:digit:]] ]]; then
#         validation
#         usage
#       else
#         check_containers_status
#         run_app_drupal
#       fi
#       ;;
#       app:lightning)
#       # See validation() for details.
#       if [[ "${COMMAND}" == "app:lightning" ]] && [[ -z ${SITENAME} ]] || [[ ! ${SITENAME} =~ [^[:digit:]] ]]; then
#         validation
#         usage
#       else
#         check_containers_status
#         run_app_lightning
#       fi
#       ;;
#       app:reservoir)
#       # See validation() for details.
#       if [[ "${COMMAND}" == "app:reservoir" ]] && [[ -z ${SITENAME} ]] || [[ ! ${SITENAME} =~ [^[:digit:]] ]]; then
#         validation
#         usage
#       else
#         check_containers_status
#         run_app_reservoir
#       fi
#       ;;
#       app:blt)
#       if [[ "${COMMAND}" == "app:blt" ]] && [[ -z ${SITENAME} ]] || [[ ! ${SITENAME} =~ [^[:digit:]] ]]; then
#         validation
#         usage
#       else
#         check_containers_status
#         run_app_blt
#       fi
#       ;;
#       app:delete)
#       if [[ "${COMMAND}" == "app:delete" ]] && [[ -z ${SITENAME} ]]; then
#         usage
#       else
#         check_containers_status
#         run_app_delete
#       fi
#       ;;
#       app:import)
#       if [[ "${COMMAND}" == "app:import" ]] && [[ -z ${SITENAME} ]] || [[ ! ${SITENAME} =~ [^[:digit:]] ]]; then
#         validation
#         usage
#       else
#         check_containers_status
#         run_app_import
#       fi
#       ;;
#       app:dev)
#       if [[ "${COMMAND}" == "app:dev" ]] && [[ -z ${SITENAME} ]] || [[ ! ${SITENAME} =~ [^[:digit:]] ]]; then
#         usage
#       else
#         check_containers_status
#         run_app_dev
#       fi
#       ;;
#       app:prod)
#       if [[ "${COMMAND}" == "app:prod" ]] && [[ -z ${SITENAME} ]] || [[ ! ${SITENAME} =~ [^[:digit:]] ]]; then
#         usage
#       else
#         check_containers_status
#         run_app_prod
#       fi
#       ;;
#       php:7.1)
#       if [[ "${COMMAND}" == "php:7.1" ]]; then
#         check_containers_status
#         set_previous_php_version
#         exit 0
#       fi
#       ;;
#       php:7.2)
#       if [[ "${COMMAND}" == "php:7.2" ]]; then
#         check_containers_status
#         set_default_php_version
#         exit 0
#       fi
#       ;;
#       tests)
#       if [[ "${COMMAND}" == "tests" ]] && [[ ! -z ${SITENAME} ]]; then
#         usage
#         exit 0
#       else
#         check_containers_status
#         run_tests
#         exit 0
#       fi
#       ;;
#       help)
#       usage
#       exit 0
#       ;;
#     esac
#   fi
# }
