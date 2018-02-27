![drucker Logo](drucker-logo.png)

# drucker: Drupal + Docker

[![drucker demo](https://asciinema.org/a/156876.png)](https://asciinema.org/a/156876)

* [Introduction](#introduction)
* [Requirements](#Requirements)
  * [Software](#software)
  * [Disk Space](#disk_space)
  * [SSH](#ssh)
* [Technology](#technology)
* [Installation](#installation)
  * [Configuring the hosts file](#hosts_file)
  * [Creating or configuring the config file](#config_file)
* [Usage](#usage)
  * [Passwords](#passwords)
* [Working with containers](#containers)
  * [Get into a container](#connect_container)
  * [Delete a container](#delete_container)
  * [Delete an image](#delete_image)
* [Troubleshooting](#troubleshooting)

## <a name="introduction"></a>Introduction

_drucker_ is an opinionated [Docker](https://www.docker.com)-based [Drupal](https://www.drupal.org) stack managed by [Ansible](https://www.ansible.com) for orchestration. It automates creating [Debian](https://www.debian.org) containers on which it will deploy a common web stack to run Drupal applications.

_drucker_ runs on 5 containers:

* `drucker_mirror` (`203.0.113.50`): APT mirror. Listens on port 3142. Allows for speedy reinstallation.
* `drucker_reverse_proxy` (`203.0.113.2`): Varnish listens on port 80 and sends traffic to the Apache backend via nginx on port 8080).
* `drucker_web` (`203.0.113.10`): Apache listens on port 80 and receives traffic from nginx.
* `drucker_db` (`203.0.113.12`): MySQL listens on port 3306 and allows the stack to act as a multi-tier environment.
* `drucker_search` (`203.0.113.13`): Apache Solr listens on port 8983.

## <a name="requirements"></a>Requirements

### <a name="software"></a>Software

You need to have both [Docker](https://www.docker.com/) and [Ansible](https://www.ansible.com/) installed on your machine. Check with the below commands:

```
$ docker version
Docker version 17.09.0-ce, build afdb6d4
$ ansible --version
ansible 2.4.1.0
```

**Important**: Ansible 2.4 or later is required.

### <a name="disk_space"></a>Disk space

You need to have approximately 6GB available.

### <a name="ssh"></a>SSH

You also need to [generate a SSH key](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/) if you don't have one already.

## <a name="technology"></a>Technology

_drucker_ ships with the following software stack:

| Software            | Version               | Source            |
| --------------------|-----------------------|-------------------|
| Debian              | 9 (Stretch)           | [debian:stretch](https://hub.docker.com/_/debian/) (Docker Hub) |
| Varnish             | 5.0.0 or higher       | APT               |
| nginx               | 1.10.3 or higher      | APT               |
| Apache              | 2.4.25 or higher      | APT               |
| MariaDB             | 10.1.26 or higher     | APT               |
| memcached           | 3.0.4                 | APT, via [ppa:ondrej/php](https://deb.sury.org/)       |
| mcstat              | 1.1.0                 | [webbj74/mcstat](https://github.com/webbj74/mcstat) (Github)      |
| phpMyAdmin          | 4.7.8                 | [phpMyAdmin](https://www.phpmyadmin.net/) (official site)      |
| adminer             | 4.6.2                 | [vrana/adminer](https://github.com/vrana/adminer) (Github)      |
| PHP-FPM             | 7.1 or 7.2            | APT, via [ppa:ondrej/php](https://deb.sury.org/)      |
| APCu                | 5.1.8 or higher       | APT, via `php-apcu` ([ppa:ondrej/php](https://deb.sury.org/)) |
| Coder               | 8.2.11                | [drupal/coder](https://packagist.org/packages/drupal/coder) (Packagist)      |
| Code Sniffer        | 2.6.1                 | [squizlabs/PHP_CodeSniffer](https://github.com/squizlabs/PHP_CodeSniffer) (Github)      |
| PHP-CS-Fixer        | 2.10.3                | [FriendsOfPHP/PHP-CS-Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer) (Github)      |
| phpmd               | 2.6.0                 | [PHPMD](https://phpmd.org/) (official site)      |
| PECL uploadprogress | master                | [ php/pecl-php-uploadprogress](https://github.com/php/pecl-php-uploadprogress)  (Github)     |
| PECL YAML           | 2.0.0                 | [php/pecl-file_formats-yaml](https://github.com/php/pecl-file_formats-yaml) (Github)      |
| LibYAML             | 0.1.7                 | [PyYAML](http://pyyaml.org/) (official site)     |
| Xdebug              | 2.6.0                 | [Xdebug](https://xdebug.org/) (official site)     |
| Tideways Profiler   | 4.1.5                 | [tideways/php-profiler-extension](https://github.com/tideways/php-profiler-extension)  (Github)     |
| phantomjs           | 2.1.1                 | [ariya/phantomjs](https://bitbucket.org/ariya/phantomjs/) (Bitbucket)     |
| Drupal              | 8.6.x                 | [Drupal](https://www.drupal.org/project/drupal) (official site)     |
| Drush               | ^9.0                  | [Drush](https://packagist.org/packages/drush/drush) (Packagist)      |
| Drush Launcher      | 0.4.2                 | [Drush Launcher](https://github.com/drush-ops/drush-launcher) (Github)      
| Drupal Console      | ~1.0                  | [hechoendrupal/drupal-console-launcher](https://github.com/hechoendrupal/drupal-console-launcher) (Github)      |
| Composer            | 1.6.2                 | [Composer](https://getcomposer.org) (official site)     |
| Apache Solr         | 7.0.1                 | [Solr](https://lucene.apache.org/solr/) (official site) |
| OpenJDK             | 1.8.0_121 or higher   | APT, via debian-backports |
| bash-git-prompt     | 2.7.1                 | [magicmonty/bash-git-prompt](https://github.com/magicmonty/bash-git-prompt) (Github)      |

## <a name="installation"></a>Installation

### <a name="hosts_file"></a>Configuring the hosts file

Add the below entries in your `/etc/hosts` file:

```
203.0.113.2    drucker.local phpmyadmin.local adminer.local lightning.local reservoir.local blt.local
203.0.113.13   search.local
203.0.113.50   mirror.local
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

### <a name="config_file"></a>Creating or configuring the config file

Add the below in your `config` file (under `$HOME/.ssh`) or create the file if it doesn't exist.

```
Host 203.0.113.99 203.0.113.2 203.0.113.10 203.0.113.12 203.0.113.13 203.0.113.50
  StrictHostKeyChecking no
  UserKnownHostsFile=/dev/null
  LogLevel=error
```

This will prevent SSH strict host key checking from getting in the way, since _drucker_ is for development purposes only.

## <a name="usage"></a>Usage

Simply run `drucker` if you have a bash alias, or invoke the `drucker.sh` script directly.

```
$ ./path/to/drucker.sh
Enter path to SSH public key [/home/<username>/.ssh/id_rsa.pub]:
Where should we store drucker sites locally? [/var/www/html]:
Where should we store drucker databases locally? [/var/lib/mysql]:
```

On the first run, `drucker` will prompt you with the path to your SSH public key, but will also try to map the `drucker` sites and databases paths to local directories of your choice, so that containers are made disposable by still preserving your data. You can override the default paths and this information will be stored in the `config` file going forward.

To prevent Git from prompting you with changes to the `config` file, you can exclude it from the Git tracking entirely with:

```
$ git update-index --assume-unchanged config
```

Should you want to stop doing so, just type:

```
$ git update-index --no-assume-unchanged config
```

### <a name="passwords"></a>Passwords:

* _drucker_ user password in containers: `drucker`
* MySQL credentials: `root`/`root`
* Drupal credentials: `admin`/`admin`

For more advanced `drucker` usage, you can pass several CLI parameters:

```
$ drucker help
drucker version dev:ba964ca

Usage:
  drucker [command] [site,...] [git_tag]

  The [site,...] argument is only valid for the following commands:
    app:[drupal,lightning,reservoir,blt]
    app:[delete,import,dev,prod]

  The [git_tag] argument is only valid for the app:drupal command.

 containers
  containers:health   Runs a service healthcheck
  containers:start    Starts all drucker containers
  containers:stop     Stops all drucker containers
  containers:restart  Restarts all drucker containers

 app
  app:drupal          Spins up a ready-to-use Drupal install
  app:lightning       Spins up a ready-to-use Lightning install
  app:reservoir       Spins up a ready-to-use Reservoir install
  app:blt             Spins up a ready-to-use BLT build
  app:delete          Deletes an arbitrary docroot
  app:import          Imports an app from the web container's import directory
  app:dev             Prepare app for development work with no caching and helper modules enabled.
  app:prod            Opinionated setup with all known performance best practices enabled.

 util
  php:[version]       Sets the PHP version to 7.1 or 7.2
  version             Returns the drucker version
  tests               Runs the Ansible test suite
  help                Displays valid drucker commands and their use
```

Notes:

* Warning: when running automated tests, `'twig_debug'` should be set to FALSE.
* The `app:import` parameter is a special beast. Please [read more about it in the wiki](https://github.com/anavarre/drucker/wiki/Importing-an-existing-site-to-drucker).

## <a name="containers"></a>Working with containers

### <a name="connect_container"></a>Get into a container

The below command will get you in as the privileged user _drucker_

```
$ docker exec -u drucker -it <container_name> bash
```

To get in as _root_ instead, type:

```
$ docker exec -it <container_name> bash
```

As _root_, if you wish to log in as the _drucker_ username again (which is recommended and _is_ a sudoer), simply type:

```
$ su drucker
```

### <a name="delete_container"></a>Delete a container

```
$ docker rm -f <container_name>
```

When you run `drucker`, missing containers will be spun up from existing images.

### <a name="delete_image"></a>Delete an image

```
$ docker rmi <drucker:image>
```

When you run `drucker`, missing images will be built.

## <a name="troubleshooting"></a>Troubleshooting

If for any reason an image would fail to be built or a container would be giving you troubles, go ahead and delete the offender! Running _drucker_ will always have your back and rebuild missing images and containers.

For more assistance, see [Troubleshooting drucker](https://github.com/anavarre/drucker/wiki/Troubleshooting-drucker) or file an issue.
