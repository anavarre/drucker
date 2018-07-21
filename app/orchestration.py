#!/usr/bin/env python3
"""Manages orchestration for all containers"""

import subprocess as s
import colorful as c
import variables as v
import orchestration as o
import os
import containers

def run_orchestration(container, shortname):
    """Parent function to manage container orchestration"""
    print(c.blue("Running %s orchestration on the container..." % (container)))
    s.getoutput("export ANSIBLE_HOST_KEY_CHECKING=False")
    s.run('''
          ansible-playbook -i %s/orchestration/hosts --user=%s %s/orchestration/provisioning/%s.yml --extra-vars ansible_sudo_pass=%s
          ''' % (v.APP_DIR, v.APP, v.APP_DIR, shortname, v.APP), shell=True)


def run_base_orchestration():
    """Run orchestration on base container"""
    run_orchestration(v.BASE_CONTAINER, "base")


def run_mirror_orchestration():
    """Run orchestration on mirror container"""
    run_orchestration(v.MIRROR_CONTAINER, "mirror")


def run_edge_orchestration():
    """Run orchestration on edge container"""
    run_orchestration(v.EDGE_CONTAINER, "edge")

def run_db_orchestration():
    """Run orchestration on database container"""
    run_orchestration(v.DB_CONTAINER, "db")

def run_search_orchestration():
    """Run orchestration on search container"""
    run_orchestration(v.SEARCH_CONTAINER, "search")


def run_ssh_orchestration():
    """Run SSH orchestration"""
    run_orchestration("SSH", "ssh")


def run_web_orchestration():
    """Run orchestration on web container"""
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

    php_version_check = s.getoutput('''docker exec -u %s -it %s /bin/cat /etc/php/default_php_version
                                    ''' % (v.APP, v.WEB_CONTAINER))
    if v.DEFAULT_PHP not in php_version_check:
        print("Tests need to be executed against the current stable PHP version")
        print("Please switch to PHP %s with 'drucker php:%s'" % (v.DEFAULT_PHP, v.DEFAULT_PHP))
        sys.exit()

    for group in v.TEST_GROUPS:
        o.run_tests_orchestration(group)

def app_list():
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

def user_confirmation():
    # if "${COMMAND}" == "app:delete":
    input("You're about to delete the %s app. Are you sure? [Y/n] " % (v.APP))
    # else:
    # read -p "The ${SITE} docroot already exists. Should we overwrite the codebase, files and database? [Y/n] "

def cancellation():
    """Cancels a user action"""
    print(c.green("Back to the comfort zone. Aborting..."))
    sys.exit()

def failure():
    """Quits when the user-entered input doesn't meet the requirements"""
    print(c.red("Sorry, the only accepted input characters are [Yy/Nn]. Aborting..."))
    sys.exit

def hosts_file():
    """Prompts the user with modifying their /etc/hosts file"""
    print(c.green("Remember to add the %s.local entry to your local /etc/hosts file!"))


def app_delete():
    """Deletes an arbitrary docroot"""
    """TODO: actually enforce arbitrary docroots through positional arguments"""
    if os.path.isdir("%s/%s" % (v.CONTAINER_HTML_PATH, v.APP)):
        print("OK")
        user_confirmation
    #   if [[ ${REPLY} =~ ^[Nn]$ ]]; then
    #     # cancellation
    #   elif [[ ! ${REPLY} =~ ^[Yy]$ ]]:
    #     # failure
    else:
        print("NOK")
    #     print(c.blue("Deleting % docroot..." % (BLABLA)))
    #     ${COMMANDS}/app-delete.yml --extra-vars "ansible_sudo_pass=${USER} app=delete sitename=${SITE}"
    #     print(c.green("Remember to remove the %s.local entry from your local /etc/hosts file!"))
    # else
    #   print("This app doesn't exist.")

# app_delete() {
#   if [[ -d ${LOCAL_HTML_PATH}/${SITE} ]]; then
#     user_confirmation
#     if [[ ${REPLY} =~ ^[Nn]$ ]]; then
#       cancellation
#     elif [[ ! ${REPLY} =~ ^[Yy]$ ]]; then
#       failure
#     else
#       echo -e "${BLUE}Deleting ${SITE} docroot...${COLOR_ENDING}"
#       ${COMMANDS}/app-delete.yml --extra-vars "ansible_sudo_pass=${USER} app=delete sitename=${SITE}"
#       echo -e "${GREEN}Remember to remove the ${SITE}.local entry from your local /etc/hosts file!${COLOR_ENDING}"
#     fi
#   else
#     echo "This app doesn't exist."
#   fi
# }