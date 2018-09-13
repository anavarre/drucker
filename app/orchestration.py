# -*- coding: utf-8 -*-
"""Manages orchestration for all containers"""

import os
import subprocess
import colorful
import click
from . import containers


def run_orchestration(drucker, container, shortname):
    """Parent function to manage container orchestration."""
    print(colorful.blue("Running %s orchestration on the container..." % (container)))
    subprocess.getoutput("export ANSIBLE_HOST_KEY_CHECKING=False")
    subprocess.run('''
                   ansible-playbook -i %s/orchestration/hosts --user=%s %s/orchestration/provisioning/%s.yml --extra-vars ansible_sudo_pass=%s
                   ''' % (drucker.vars.APP_DIR, drucker.vars.APP, drucker.vars.APP_DIR, shortname, drucker.vars.APP), shell=True)


def run_base_orchestration(drucker):
    """Runs orchestration on base container"""
    run_orchestration(drucker, drucker.vars.BASE_CONTAINER, "base")


def run_mirror_orchestration(drucker):
    """Runs orchestration on mirror container"""
    run_orchestration(drucker, drucker.vars.MIRROR_CONTAINER, "mirror")


def run_edge_orchestration(drucker):
    """Runs orchestration on edge container"""
    run_orchestration(drucker, drucker.vars.EDGE_CONTAINER, "edge")


def run_db_orchestration(drucker):
    """Runs orchestration on database container"""
    run_orchestration(drucker, drucker.vars.DB_CONTAINER, "db")


def run_search_orchestration(drucker):
    """Runs orchestration on search container"""
    run_orchestration(drucker, drucker.vars.SEARCH_CONTAINER, "search")


def run_ssh_orchestration(drucker):
    """Runs SSH orchestration"""
    run_orchestration(drucker, "SSH", "ssh")


def run_web_orchestration(drucker):
    """Runs orchestration on web container"""
    run_orchestration(drucker, drucker.vars.WEB_CONTAINER, "web")


def run_tests_orchestration(drucker, shortname):
    """Parent function to manage running the test suite"""
    print(colorful.blue("Running the %s test suite..." % (shortname)))
    subprocess.getoutput("export ANSIBLE_HOST_KEY_CHECKING=False")
    subprocess.run('''
                   ansible-playbook -i %s/orchestration/hosts --user=%s %s/orchestration/_tests/%s-tests.yml --extra-vars ansible_sudo_pass=%s
                   ''' % (drucker.vars.APP_DIR,
                          drucker.vars.APP,
                          drucker.vars.APP_DIR,
                          shortname,
                          drucker.vars.APP),
                          shell=True)


def run_tests(drucker):
    """Runs the Ansible test suite"""
    containers.status(drucker)

    php_version_check = subprocess.getoutput('''docker exec -u %s -it %s /bin/cat\
                                                /etc/php/default_php_version
                                             ''' % (drucker.vars.APP,
                                                    drucker.vars.WEB_CONTAINER))
    if drucker.vars.DEFAULT_PHP not in php_version_check:
        print("Tests need to be executed against the current stable PHP version")
        print("Please switch to PHP %s with 'drucker --php%s'"
              % (drucker.vars.DEFAULT_PHP,
                 drucker.vars.DEFAULT_PHP))
        return drucker.vars.EXITCODE_FAIL
    for group in drucker.vars.TEST_GROUPS:
        run_tests_orchestration(drucker, group)
    return drucker.vars.EXITCODE_OK


def app_list(drucker):
    """Returns a list of installed apps."""
    subprocess.run("docker exec -it %s cat %s/.app-registry"
                   % (drucker.vars.WEB_CONTAINER,
                      drucker.vars.CONTAINER_HTML_PATH), shell=True)
    return drucker.vars.EXITCODE_OK


def hosts_file(app):
    """Prompts the user with modifying their /etc/hosts file"""
    print(colorful.green("Remember to add the %s.local entry to your local /etc/hosts file!" % (app)))


def param_check(drucker):
    """Determines whether a second parameter (sitename) was passed"""
    if not drucker.app:
        print(colorful.red("This command needs a sitename to run. Aborting..."))


def app_delete(drucker):
    """Deletes an arbitrary docroot"""
    param_check(drucker)

    # TODO: actually enforce arbitrary docroots through positional arguments

    if os.path.isdir("%s/%s" % (drucker.vars.CONTAINER_HTML_PATH, drucker.app)):
        if click.confirm("Should we overwrite the codebase, files and database?", default=True):
            print(colorful.blue("Deleting %s docroot..." % (drucker.app)))
            subprocess.run('''ansible-playbook -i %s/orchestration/hosts\
                              --user=%s %s/orchestration/commands/app-delete.yml\
                              --extra-vars "ansible_sudo_pass=%s app=delete sitename=%s"
                           ''' % (drucker.vars.APP_DIR,
                                  drucker.vars.APP,
                                  drucker.vars.APP_DIR,
                                  drucker.vars.APP,
                                  drucker.app),
                                  shell=True)
            print(colorful.green("Remember to remove the %s.local entry from your"
                          " local /etc/hosts file!" % (drucker.app)))
        else:
            print(colorful.green("Back to the comfort zone. Aborting..."))
    else:
        print("This app doesn't exist.")


def app_drupal(drucker):
    """Spins up a ready-to-use Drupal install"""
    app_delete(drucker)

    # if [[ -z "${GIT_TAG}" ]]; then
    print(colorful.blue("Installing Drupal into new %s docroot..." % (drucker.app)))
    subprocess.run('''ansible-playbook -i %s/orchestration/hosts\
                      --user=%s %s/orchestration/commands/app-drupal.yml\
                      --extra-vars "ansible_sudo_pass=%s app=Drupal sitename=%s"
                   ''' % (drucker.vars.APP_DIR,
                          drucker.vars.APP,
                          drucker.vars.APP_DIR,
                          drucker.vars.APP,
                          drucker.app),
                          shell=True)
    hosts_file(drucker.app)
    # elif [[ -n "${GIT_TAG}" ]]; then
    #     echo -e "${BLUE}Installing Drupal ${GIT_TAG} into new
    #         ${SITE} docroot...${COLOR_ENDING}"
    #     ${COMMANDS}/app-drupal.yml --extra-vars "ansible_sudo_pass=${USER}
    #         app=Drupal sitename=${SITE} git_tag=${GIT_TAG}"
    #     hosts_file(drucker.app)
    return drucker.vars.EXITCODE_OK


def app_lightning(drucker):
    """Spins up a ready-to-use Lightning install"""
    app_delete(drucker)

    print(colorful.blue("Installing Lightning into new %s docroot..." % (drucker.app)))
    subprocess.run('''ansible-playbook -i %s/orchestration/hosts\
                      --user=%s %s/orchestration/commands/app-lightning.yml\
                      --extra-vars "ansible_sudo_pass=%s app=Lightning sitename=%s"
                   ''' % (drucker.vars.APP_DIR,
                          drucker.vars.APP,
                          drucker.vars.APP_DIR,
                          drucker.vars.APP,
                          drucker.app),
                          shell=True)
    hosts_file(drucker.app)
    return drucker.vars.EXITCODE_OK


def app_blt(drucker):
    """Spins up a ready-to-use BLT build"""
    app_delete(drucker)

    print(colorful.blue("Installing BLT into new %s docroot..." % (drucker.app)))
    subprocess.run('''ansible-playbook -i %s/orchestration/hosts\
                      --user=%s %s/orchestration/commands/app-blt.yml\
                      --extra-vars "ansible_sudo_pass=%s app=BLT sitename=%s"
                   ''' % (drucker.vars.APP_DIR,
                          drucker.vars.APP,
                          drucker.vars.APP_DIR,
                          drucker.vars.APP,
                          drucker.app),
                          shell=True)
    hosts_file(drucker.app)
    return drucker.vars.EXITCODE_OK


def app_dev(drucker):
    """Prepares app for development work with no caching and helper modules enabled."""
    param_check(drucker)

    identify_drupal_type = subprocess.getoutput('''grep "%s" "%s/.app-registry" |\
                                                   awk '{print $NF}' | tr --d '()'
                                                ''' % (drucker.app,
                                                       drucker.vars.CONTAINER_HTML_PATH))

    if "BLT" in identify_drupal_type:
        print(colorful.red("This command is not currently compatible with BLT. Exiting..."))
        return drucker.vars.EXITCODE_FAIL
    if not identify_drupal_type:
        print(colorful.red("Could not identify the application type. Exiting..."))
        return drucker.vars.EXITCODE_FAIL
    print(colorful.blue("Configuring %s docroot for development..." % (drucker.app)))
    subprocess.run('''ansible-playbook -i %s/orchestration/hosts\
                      --user=%s %s/orchestration/commands/app-dev.yml\
                      --extra-vars "ansible_sudo_pass=%s app=dev sitename=%s"
                   ''' % (drucker.vars.APP_DIR,
                          drucker.vars.APP,
                          drucker.vars.APP_DIR,
                          drucker.vars.APP,
                          drucker.app),
                          shell=True)
    return drucker.vars.EXITCODE_OK


def app_prod(drucker):
    """Opinionated setup with all known performance best practices enabled."""
    identify_drupal_type = subprocess.getoutput('''grep "%s" "%s/.app-registry" |\
                                                   awk '{print $NF}' | tr --d '()'
                                                ''' % (drucker.app,
                                                       drucker.vars.CONTAINER_HTML_PATH))

    if "BLT" in identify_drupal_type:
        print(colorful.red("This command is not currently compatible with BLT. Exiting..."))
        return drucker.vars.EXITCODE_FAIL
    if not identify_drupal_type:
        print(colorful.red("Could not identify the application type. Exiting..."))
        return drucker.vars.EXITCODE_FAIL
    print(colorful.blue("Configuring %s docroot for production..." % (drucker.app)))
    subprocess.run('''ansible-playbook -i %s/orchestration/hosts\
                      --user=%s %s/orchestration/commands/app-prod.yml\
                      --extra-vars "ansible_sudo_pass=%s app=prod sitename=%s"
                   ''' % (drucker.vars.APP_DIR,
                          drucker.vars.APP,
                          drucker.vars.APP_DIR,
                          drucker.vars.APP,
                          drucker.app),
                          shell=True)
    return drucker.vars.EXITCODE_OK


def app_import(drucker):
    """Imports an app from the web container's import directory"""
    import_path = drucker.vars.CONTAINER_IMPORT_PATH
    if not os.path.isdir("%s/%s" % (import_path, drucker.app)):
        print(colorful.red("The %s app doesn't exist. Aborting..." % (drucker.app)))
        return drucker.vars.EXITCODE_FAIL
    if os.path.isdir("%s/%s/blt" % (import_path, drucker.app)):
        app_detected = "BLT"
    elif os.path.isdir("%s/%s/vendor/bin/lightning" % (import_path,
                                                       drucker.app)):
        app_detected = "Lightning"
    else:
        app_detected = "Drupal"

    subprocess.run('''ansible-playbook -i %s/orchestration/hosts\
                      --user=%s %s/orchestration/commands/app-import.yml\
                      --extra-vars "ansible_sudo_pass=%s app=%s sitename=%s"
                   ''' % (drucker.vars.APP_DIR,
                          drucker.vars.APP,
                          drucker.vars.APP_DIR,
                          drucker.vars.APP,
                          app_detected,
                          drucker.app),
                          shell=True)
    hosts_file(drucker.app)
    return drucker.vars.EXITCODE_OK
