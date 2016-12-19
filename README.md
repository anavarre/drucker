# drucker: Drupal + Docker

[![demo](https://asciinema.org/a/51lh7ymc9q6dselpyw61ii2hv.png)](https://asciinema.org/a/51lh7ymc9q6dselpyw61ii2hv)

_drucker_ is an opinionated [Docker](https://www.docker.com)-based [Drupal](https://www.drupal.org) stack managed by [Ansible](https://www.ansible.com) for orchestration. It automates creating [Debian](https://www.debian.org) containers on which it will deploy a common web stack to run Drupal applications.

Currently, _drucker_ runs on 4 containers:

* `drucker_reverse_proxy` (Varnish/nginx: `203.0.113.2`): Varnish listens on port 80 and sends traffic to the Apache backend via nginx on port 8080).
* `drucker_web` (Apache/PHP: `203.0.113.10`): Apache listens on port 80 and receives traffic from nginx.
* `drucker_db` (MySQL: `203.0.113.12`): MySQL listens on port 3306 and allows the stack to act as a multi-tier environment.
* `drucker_search` (MySQL: `203.0.113.13`): Apache Solr instance.

The plan is to make _drucker_ a true service-based suite of containers, by leveraging GlusterFS for distributed network filesystem across N number of web containers. Load-Balancing and HA capabilities will also be enforced to replicate a production environment locally. When we have this, then a 1.0.0 release will be tagged. But for now, the aim is to incrementally make things more stable and more fully-featured.

## Requirements

### Software

You need to have both [Docker](https://www.docker.com/) and [Ansible](https://www.ansible.com/) installed on your machine. Check with the below commands:

```
$ docker --version
Docker version 1.10.3, build 20f81dd
$ ansible --version
ansible 2.0.2.0
```

**Important**: Ansible 2 or later is required.

### Disk space

You need to have approximately 4GB available.

### SSH

You also need to [generate a SSH key](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/) if you don't have one already.

## Technology

_drucker_ ships with the following software stack:

| Software            | Version         | Source |
| --------------------|:---------------:|:--------:
| Debian              | 8 (Jessie)      | [debian:latest](https://hub.docker.com/_/debian/)    |
| Varnish             | 4.1.2 or later  | Custom build   |
| nginx               | 1.10.1 or later | Custom build   |
| Apache              | 2.4.10 or later | Custom build    |
| Apache Solr         | 6.2.0 or later  | [geerlingguy.solr](https://galaxy.ansible.com/geerlingguy/solr/) (3.2.4) |
| Java                | 8               | [williamyeh.oracle-java](https://galaxy.ansible.com/williamyeh/oracle-java/) (2.10.0)    |
| PHP-FPM             | 7.0.13 or later | Custom build   |
| APCu                | 5.1.7           | APT            |
| Xdebug              | 2.5.0           | Custom build   |
| PECL uploadprogress | master          | Custom build   |
| PECL YAML           | 2.0.0           | Custom build   |
| LibYAML             | 0.1.7           | Custom build   |
| Tideways Profiler   | 4.0.7           | Custom build   |
| Coder               | 8.2.9           | Custom build   |
| Code Sniffer        | 2.6.1           | Custom build   |
| PHP-CS-Fixer        | 1.12.2          | Custom build   |
| phpmd               | 2.5.0           | Custom build   |
| phantomjs           | 2.1.1           | Custom build   |
| MySQL               | 5.7.14 or later | Custom build   |
| Drupal              | 8.3.x           | Custom build   |
| Drush               | 9.0-dev         | Custom build   |
| Drupal Console      | 1.0.0-rc11      | Custom build   |
| Composer            | 1.2.4           | Custom build   |
| phpMyAdmin          | 4.6.5           | Custom build   |
| adminer             | 4.2.5           | Custom build   |
| bash-git-prompt     | 2.6.1           | Custom build   |

## Installation

Add the below host entries in your hosts file:

```
203.0.113.2    drucker.local phpmyadmin.local adminer.local
203.0.113.13   search.local
```

This will ensure you can access:

* `drucker.local`: Drupal 8
* `phpmyadmin.local`: phpMyAdmin (MySQL/MariaDB database management tool)
* `adminer.local`: adminer (Database management tool in a single file)
* `search.local`: Apache Solr's dashboard

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
Host 203.0.113.99 203.0.113.2 203.0.113.10 203.0.113.11 203.0.113.12 203.0.113.13
  StrictHostKeyChecking no
  UserKnownHostsFile=/dev/null
  LogLevel=error
```

This will prevent SSH strict host key checking from getting in the way, since _drucker_ is for development purposes only.

## Usage

Simply run `drucker` if you have a bash alias, or invoke the `drucker.sh` script directly.

```
$ ./drucker.sh
Enter path to SSH public key [/home/<username>/.ssh/id_rsa.pub]:
Where should we store drucker sites locally? [/var/www/html]:
Where should we store drucker databases locally? [/var/lib/mysql]:
```

On the first run, `drucker` will prompt you with the path to your SSH public key, but will also try to map the `drucker` sites and databases paths to local directories of your choice, so that containers are disposable by still preserving your data. You can totally override the default paths and this information will be stored in the `config` file going forward.

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
--dev                 Prepare drucker for development work with no caching and helper modules enabled.
                      WARNING: when running automated tests, 'twig_debug' should be set to FALSE.

--prod                Opinionated setup with all known performance best practices enabled.

--create [sitename]   Creates an arbitrary docroot, vHost and corresponding database.

--import [sitename]   Imports the database, files and codebase from the web container's import directory.

--reinstall           Deletes the existing drucker codebase and database and reinstalls from the latest dev tarball.

--delete [sitename]   Deletes an arbitrary docroot, vHost and corresponding database.

--tests               Runs the Ansible test suite.
```

The `--import [sitename]` parameter is a special beast. Please [read more about it in the wiki](https://github.com/anavarre/drucker/wiki/Importing-an-existing-site-to-drucker).

At the beginning of the build process, _drucker_ will prompt you to enter the path to your SSH public key (in order to run [Ansible](https://www.ansible.com/) orchestration on your container). `~/.ssh/id_rsa.pub` is assumed, but you can enter the path to a custom public key then.

When spinning up the web container, drucker will try to map its web directory to a local path (`/var/www/html`) on your computer. Feel free to change this default path to one that is more convenient.

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

## Passwords:

* _drucker_ user on the container: `drucker`
* MySQL credentials: `root`/`root`
* Drupal credentials: `admin`/`admin`

## Tips and tricks

### Delete a container

Run:

```
$ docker rm -f <container_name>
```

### Delete an image

Run:

```
$ docker rmi <drucker:image>
```

If you run `drucker` again it will spin up containers (and optionally will build images). Orchestration will then be run as expected.

## Troubleshooting

See [Troubleshooting drucker](https://github.com/anavarre/drucker/wiki/Troubleshooting-drucker)
