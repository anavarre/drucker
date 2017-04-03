# drucker: Drupal + Docker

[![demo](https://asciinema.org/a/cp8rkaa9mcux71hdlpc3sxwkl.png)](https://asciinema.org/a/cp8rkaa9mcux71hdlpc3sxwkl)

* [Introduction](#Introduction)
* [Requirements](#Requirements)
  * [Software](#Software)
  * [Disk Space](#Disk_space)
  * [SSH](#SSH)
* [Technology](#Technology)
* [Installation](#Installation)
* [Usage](#Usage)
  * [Passwords](#Passwords)
* [Tips and tricks](#Tips_and_tricks)
  * [Delete a container](#Delete_a_container)
  * [Delete an image](#Delete_an_image)
* [Troubleshooting](#Troubleshooting)

## <a name="Introduction"></a>Introduction

_drucker_ is an opinionated [Docker](https://www.docker.com)-based [Drupal](https://www.drupal.org) stack managed by [Ansible](https://www.ansible.com) for orchestration. It automates creating [Debian](https://www.debian.org) containers on which it will deploy a common web stack to run Drupal applications.

_drucker_ runs on 4 containers:

* `drucker_reverse_proxy` (`203.0.113.2`): Varnish listens on port 80 and sends traffic to the Apache backend via nginx on port 8080).
* `drucker_web` (`203.0.113.10`): Apache listens on port 80 and receives traffic from nginx.
* `drucker_db` (`203.0.113.12`): MySQL listens on port 3306 and allows the stack to act as a multi-tier environment.
* `drucker_search` (`203.0.113.13`): Apache Solr listens on port 8983.

## <a name="Requirements"></a>Requirements

### <a name="Software"></a>Software

You need to have both [Docker](https://www.docker.com/) and [Ansible](https://www.ansible.com/) installed on your machine. Check with the below commands:

```
$ docker --version
Docker version 1.10.3, build 20f81dd
$ ansible --version
ansible 2.2.0.0
```

**Important**: Ansible 2 or later is required.

### <a name="Disk_space"></a>Disk space

You need to have approximately 4GB available.

### <a name="SSH"></a>SSH

You also need to [generate a SSH key](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/) if you don't have one already.

## <a name="Technology"></a>Technology

_drucker_ ships with the following software stack:

| Software            | Version             | Source            |
| --------------------|---------------------|-------------------|
| Debian              | 8 (Jessie)          | [debian:latest](https://hub.docker.com/_/debian/) (Docker Hub) |
| Varnish             | 4.1.2 or higher     | APT, via [Varnish APT repo](https://varnish-cache.org/releases/install_debian.html)      |
| nginx               | 1.10.1 or higher    | APT, via [nginx APT repo](https://nginx.org/en/linux_packages.html)      |
| Apache              | 2.4.10 or higher    | APT      |
| MySQL               | 5.7.17 or higher    | APT, via [MySQL APT repo](https://dev.mysql.com/downloads/repo/apt/)      |
| memcached           | 3.0.3               | APT, via [ppa:ondrej/php](https://deb.sury.org/)       |
| mcstat              | 1.1.0               | [webbj74/mcstat](https://github.com/webbj74/mcstat) (Github)      |
| phpMyAdmin          | 4.7.0               | [phpMyAdmin](https://www.phpmyadmin.net/) (official site)      |
| adminer             | 4.3.0               | [vrana/adminer](https://github.com/vrana/adminer) (Github)      |
| PHP-FPM             | 7.1.1 or higher     | APT, via [ppa:ondrej/php](https://deb.sury.org/)      |
| APCu                | 5.1.8 or later      | APT, via `php-apcu` ([ppa:ondrej/php](https://deb.sury.org/)) |
| Coder               | 8.2.11              | [drupal/coder](https://packagist.org/packages/drupal/coder) (Packagist)      |
| Code Sniffer        | 2.6.1               | [squizlabs/PHP_CodeSniffer](https://github.com/squizlabs/PHP_CodeSniffer) (Github)      |
| PHP-CS-Fixer        | 1.12.2              | [FriendsOfPHP/PHP-CS-Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer) (Github)      |
| phpmd               | 2.6.0               | [PHPMD](https://phpmd.org/) (official site)      |
| PECL uploadprogress | master              | [ php/pecl-php-uploadprogress](https://github.com/php/pecl-php-uploadprogress)  (Github)     |
| PECL YAML           | 2.0.0               | [php/pecl-file_formats-yaml](https://github.com/php/pecl-file_formats-yaml) (Github)      |
| LibYAML             | 0.1.7               | [PyYAML](http://pyyaml.org/) (official site)     |
| Xdebug              | 2.5.1               | [Xdebug](https://xdebug.org/) (official site)     |
| Tideways Profiler   | 4.1.1               | [tideways/php-profiler-extension](https://github.com/tideways/php-profiler-extension)  (Github)     |
| phantomjs           | 2.1.1               | [ariya/phantomjs](https://bitbucket.org/ariya/phantomjs/) (Bitbucket)     |
| Drupal              | 8.4.x               | [Drupal](https://www.drupal.org/project/drupal) (official site)     |
| Drush               | 9.0-dev             | [Drush](http://docs.drush.org/en/master/install/) (Amazon S3 bucket)      |
| Drupal Console      | 1.0.0-rc16          | [hechoendrupal/drupal-console-launcher](https://github.com/hechoendrupal/drupal-console-launcher) (Github)      |
| Composer            | 1.3.3               | [Composer](https://getcomposer.org) (official site)     |
| Apache Solr         | 6.3.0 or higher     | [solr:latest](https://hub.docker.com/_/solr/) (Docker Hub) |
| OpenJDK             | 1.8.0_111 or higher | [solr:latest](https://hub.docker.com/_/solr/) (Docker Hub) |
| bash-git-prompt     | 2.6.1               | [magicmonty/bash-git-prompt](https://github.com/magicmonty/bash-git-prompt) (Github)      |

## <a name="Installation"></a>Installation

Add the below host entries in your hosts file:

```
203.0.113.2    drucker.local phpmyadmin.local adminer.local
203.0.113.13   search.local
```

This will ensure you can access:

* `drucker.local`: Drupal 8
* `phpmyadmin.local`: phpMyAdmin (MySQL/MariaDB database management tool)
* `adminer.local`: adminer (Database management tool in a single file)
* `search.local:8983/solr/#/`: Apache Solr's dashboard

**Recommended**: add the below bash alias entry in your `.bashrc` or `.bash_aliases` file:

```
alias drucker='path/to/drucker/drucker.sh'
```

Source the file (or log out and log back in) to use the alias immediately. E.g.:

```
$ source ~/.bashrc
```

This will allow you to invoke `drucker` from anywhere on your system.

Add the below in your `config` file (under `$HOME/.ssh`) or create the file if it doesn't exist.

```
Host 203.0.113.99 203.0.113.2 203.0.113.10 203.0.113.12 203.0.113.13
  StrictHostKeyChecking no
  UserKnownHostsFile=/dev/null
  LogLevel=error
```

This will prevent SSH strict host key checking from getting in the way, since _drucker_ is for development purposes only.

## <a name="Usage"></a>Usage

Simply run `drucker` if you have a bash alias, or invoke the `drucker.sh` script directly.

```
$ ./drucker.sh
Enter path to SSH public key [/home/<username>/.ssh/id_rsa.pub]:
Where should we store drucker sites locally? [/var/www/html]:
Where should we store drucker databases locally? [/var/lib/mysql]:
```

On the first run, `drucker` will prompt you with the path to your SSH public key, but will also try to map the `drucker` sites and databases paths to local directories of your choice, so that containers are made disposable by still preserving your data. You can totally override the default paths and this information will be stored in the `config` file going forward.

To prevent Git from prompting you with changes to the `config` file, you can exclude it from the Git tracking entirely with:

```
$ git update-index --assume-unchanged config
```

Should you want to stop doing so, just type:

```
git update-index --no-assume-unchanged config
```

For more advanced `drucker` usage, you can pass several CLI parameters:

```
$ drucker --help
--version                      Returns the current drucker version.
--dev                          Prepare drucker for development work with no caching and helper modules enabled.
                               WARNING: when running automated tests, 'twig_debug' should be set to FALSE.

--prod                         Opinionated setup with all known performance best practices enabled.

--create [sitename] [git_tag]  Creates an arbitrary docroot, vHost and corresponding database.

--import [sitename]            Imports the database, files and codebase from the web container's import directory.

--reinstall                    Deletes the existing drucker codebase and database and reinstalls from the latest dev tarball.

--delete [sitename]            Deletes an arbitrary docroot, vHost and corresponding database.

--tests                        Runs the Ansible test suite.
```

The `--import [sitename]` parameter is a special beast. Please [read more about it in the wiki](https://github.com/anavarre/drucker/wiki/Importing-an-existing-site-to-drucker).

At the beginning of the build process, _drucker_ will prompt you to enter the path to your SSH public key (in order to run [Ansible](https://www.ansible.com/) orchestration on your container). `~/.ssh/id_rsa.pub` is assumed, but you can enter the path to a custom public key then.

When spinning up the web container, drucker will try to map its web directory to a local path (`/var/www/html`) on your computer. Feel free to change this default path to one that is more convenient.

The `--composer [sitename]` parameter allows to install Drupal from an arbitrary `composer.json` file. Simply put your file in the webroot (`/var/www/html`) and `drucker` will pick it up. If it can't find any, it'll copy the default `composer-template.json` file from within the `orchestration/files` directory.

To connect to a container as the privileged _drucker_ user, simply type:

```
$ docker exec -u drucker -it <container_name> bash
```

To connect to a container as _root_, type:

```
$ docker exec -it <container_name> bash
```

As _root_, if you wish to log in as the _drucker_ username again (which is recommended and _is_ a sudoer), simply type:

```
$ su drucker
```

### <a name="Passwords"></a>Passwords:

* _drucker_ user on the container: `drucker`
* MySQL credentials: `root`/`root`
* Drupal credentials: `admin`/`admin`

## <a name="Tips_and_tricks"></a>Tips and tricks

### <a name="Delete_a_container"></a>Delete a container

Run:

```
$ docker rm -f <container_name>
```

### <a name="Delete_an_image"></a>Delete an image

Run:

```
$ docker rmi <drucker:image>
```

If you run `drucker` again it will spin up containers (and optionally will build images). Orchestration will then be run as expected.

## <a name="Troubleshooting"></a>Troubleshooting

See [Troubleshooting drucker](https://github.com/anavarre/drucker/wiki/Troubleshooting-drucker)
