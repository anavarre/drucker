#!/usr/bin/env python3
"""Manages orchestration for all containers"""

import subprocess as s
import sys
import os
import colorful as c
import click
import variables as v
import containers


def run_orchestration(container, shortname):
    """Parent function to manage container orchestration."""
    print(c.blue("Running %s orchestration on the container..." % (container)))
    s.getoutput("export ANSIBLE_HOST_KEY_CHECKING=False")
    s.run('''
          ansible-playbook -i %s/orchestration/hosts --user=%s %s/orchestration/provisioning/%s.yml --extra-vars ansible_sudo_pass=%s
          ''' % (v.APP_DIR, v.APP, v.APP_DIR, shortname, v.APP), shell=True)


def run_base_orchestration():
    """Runs orchestration on base container"""
    run_orchestration(v.BASE_CONTAINER, "base")


def run_mirror_orchestration():
    """Runs orchestration on mirror container"""
    run_orchestration(v.MIRROR_CONTAINER, "mirror")


def run_edge_orchestration():
    """Runs orchestration on edge container"""
    run_orchestration(v.EDGE_CONTAINER, "edge")


def run_db_orchestration():
    """Runs orchestration on database container"""
    run_orchestration(v.DB_CONTAINER, "db")


def run_search_orchestration():
    """Runs orchestration on search container"""
    run_orchestration(v.SEARCH_CONTAINER, "search")


def run_ssh_orchestration():
    """Runs SSH orchestration"""
    run_orchestration("SSH", "ssh")


def run_web_orchestration():
    """Runs orchestration on web container"""
    run_orchestration(v.WEB_CONTAINER, "web")


def run_tests_orchestration(shortname):
    """Parent function to manage running the test suite"""
    print(c.blue("Running the %s test suite..." % (shortname)))
    s.getoutput("export ANSIBLE_HOST_KEY_CHECKING=False")
    s.run('''
          ansible-playbook -i %s/orchestration/hosts --user=%s %s/orchestration/_tests/%s-tests.yml --extra-vars ansible_sudo_pass=%s
          ''' % (v.APP_DIR, v.APP, v.APP_DIR, shortname, v.APP), shell=True)


def run_tests():
    """Runs the Ansible test suite"""
    containers.status()

    php_version_check = s.getoutput('''docker exec -u %s -it %s /bin/cat\
                                       /etc/php/default_php_version
                                    ''' % (v.APP, v.WEB_CONTAINER))
    if v.DEFAULT_PHP not in php_version_check:
        print("Tests need to be executed against the current stable PHP version")
        print("Please switch to PHP %s with 'drucker --php%s'" % (v.DEFAULT_PHP, v.DEFAULT_PHP))
        sys.exit()

    for group in v.TEST_GROUPS:
        run_tests_orchestration(group)


def app_list():
    """Returns a list of installed apps."""
    s.run('''docker exec -it %s cat %s/.app-registry
          ''' % (v.WEB_CONTAINER, v.CONTAINER_HTML_PATH), shell=True)


      # app:delete)
      # if [[ "${COMMAND}" == "app:delete" ]] && [[ -z ${SITENAME} ]]; then
      #   usage
      # else
      #   check_containers_status
      #   run_app_delete
      # fi
      # ;;

# run_app_delete() {
#   # Comma-separated sitenames are split into single values for drucker to
#   # get a list of sites to delete.
#   for SITE in ${SITENAME//,/ }; do
#     app_delete
#   done
#   exit 0
# }


def hosts_file(app):
    """Prompts the user with modifying their /etc/hosts file"""
    print(c.green("Remember to add the %s.local entry to your local /etc/hosts file!" % (app)))


def param_check(app):
    """Determines whether a second parameter (sitename) was passed"""
    if not app:
        print(c.red("This command needs a sitename to run. Aborting..."))
        sys.exit()

def app_delete(app):
    """Deletes an arbitrary docroot"""
    param_check(app)

    # TODO: actually enforce arbitrary docroots through positional arguments

    if os.path.isdir("%s/%s" % (v.CONTAINER_HTML_PATH, app)):
        if click.confirm("Should we overwrite the codebase, files and database?", default=True):
            print(c.blue("Deleting %s docroot..." % (app)))
            s.run('''ansible-playbook -i %s/orchestration/hosts\
                     --user=%s %s/orchestration/commands/app-delete.yml\
                     --extra-vars "ansible_sudo_pass=%s app=delete sitename=%s"
                  ''' % (v.APP_DIR, v.APP, v.APP_DIR, v.APP, app), shell=True)
            print(c.green("Remember to remove the %s.local entry from your local /etc/hosts file!" % (app)))
        else:
            print(c.green("Back to the comfort zone. Aborting..."))
    else:
        print("This app doesn't exist.")


def app_drupal(app):
    """Spins up a ready-to-use Drupal install"""
    app_delete(app)

  # if [[ -z "${GIT_TAG}" ]]; then
    print(c.blue("Installing Drupal into new %s docroot..." % (app)))
    s.run('''ansible-playbook -i %s/orchestration/hosts\
             --user=%s %s/orchestration/commands/app-drupal.yml\
             --extra-vars "ansible_sudo_pass=%s app=Drupal sitename=%s"
          ''' % (v.APP_DIR, v.APP, v.APP_DIR, v.APP, app), shell=True)
    hosts_file(app)
  # elif [[ -n "${GIT_TAG}" ]]; then
  #   echo -e "${BLUE}Installing Drupal ${GIT_TAG} into new ${SITE} docroot...${COLOR_ENDING}"
  #   ${COMMANDS}/app-drupal.yml --extra-vars "ansible_sudo_pass=${USER} app=Drupal sitename=${SITE} git_tag=${GIT_TAG}"
  #   hosts_file(app)


def app_lightning(app):
    """Spins up a ready-to-use Lightning install"""
    app_delete(app)

    print(c.blue("Installing Lightning into new %s docroot..." % (app)))
    s.run('''ansible-playbook -i %s/orchestration/hosts\
             --user=%s %s/orchestration/commands/app-lightning.yml\
             --extra-vars "ansible_sudo_pass=%s app=Lightning sitename=%s"
          ''' % (v.APP_DIR, v.APP, v.APP_DIR, v.APP, app), shell=True)
    hosts_file(app)


def app_blt(app):
    """Spins up a ready-to-use BLT build"""
    app_delete(app)

    print(c.blue("Installing BLT into new %s docroot..." % (app)))
    s.run('''ansible-playbook -i %s/orchestration/hosts\
             --user=%s %s/orchestration/commands/app-blt.yml\
             --extra-vars "ansible_sudo_pass=%s app=BLT sitename=%s"
          ''' % (v.APP_DIR, v.APP, v.APP_DIR, v.APP, app), shell=True)
    hosts_file(app)


def app_dev(app):
    """Prepares app for development work with no caching and helper modules enabled."""
    param_check(app)

    identify_drupal_type = s.getoutput('''grep "%s" "%s/.app-registry" |\
                                          awk '{print $NF}' | tr --d '()'
                                       ''' % (app, v.CONTAINER_HTML_PATH))

    if "BLT" in identify_drupal_type:
        print(c.red("This command is not currently compatible with BLT. Exiting..."))
        sys.exit()
    elif not identify_drupal_type:
        print(c.red("Could not identify the application type. Exiting..."))
    else:
        print(c.blue("Configuring %s docroot for development..." % (app)))
        s.run('''ansible-playbook -i %s/orchestration/hosts\
                 --user=%s %s/orchestration/commands/app-dev.yml\
                 --extra-vars "ansible_sudo_pass=%s app=dev sitename=%s"
              ''' % (v.APP_DIR, v.APP, v.APP_DIR, v.APP, app), shell=True)


def app_prod(app):
    """Opinionated setup with all known performance best practices enabled."""
    identify_drupal_type = s.getoutput('''grep "%s" "%s/.app-registry" |\
                                          awk '{print $NF}' | tr --d '()'
                                       ''' % (app, v.CONTAINER_HTML_PATH))

    if "BLT" in identify_drupal_type:
        print(c.red("This command is not currently compatible with BLT. Exiting..."))
        sys.exit()
    elif not identify_drupal_type:
        print(c.red("Could not identify the application type. Exiting..."))
    else:
        print(c.blue("Configuring %s docroot for production..." % (app)))
        s.run('''ansible-playbook -i %s/orchestration/hosts\
                 --user=%s %s/orchestration/commands/app-prod.yml\
                 --extra-vars "ansible_sudo_pass=%s app=prod sitename=%s"
              ''' % (v.APP_DIR, v.APP, v.APP_DIR, v.APP, app), shell=True)


def app_import(app):
    """Imports an app from the web container's import directory"""
    if not os.path.isdir("%s/%s" % (v.CONTAINER_IMPORT_PATH, app)):
        print(c.red("The %s app doesn't exist. Aborting..." % (app)))
        sys.exit()
    elif os.path.isdir("%s/%s/blt" % (v.CONTAINER_IMPORT_PATH, app)):
        app_detected = "BLT"
    elif os.path.isdir("%s/%s/vendor/bin/lightning" % (v.CONTAINER_IMPORT_PATH, app)):
        app_detected = "Lightning"
    else:
        app_detected = "Drupal"

    s.run('''ansible-playbook -i %s/orchestration/hosts\
             --user=%s %s/orchestration/commands/app-import.yml\
             --extra-vars "ansible_sudo_pass=%s app=%s sitename=%s"
          ''' % (v.APP_DIR, v.APP, v.APP_DIR, v.APP, app_detected, app), shell=True)
    hosts_file(app)