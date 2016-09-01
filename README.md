# drucker: Drupal + Docker

[![demo](https://asciinema.org/a/82436.png)](https://asciinema.org/a/82436)

**This is a WIP (Work In Progress). Use at your own risk.**

_drucker_ is a [Docker](https://www.docker.com)-based [Drupal](https://www.drupal.org) stack managed by [Ansible](https://www.ansible.com) for orchestration. It automates creating [Debian](https://www.debian.org) containers on which it will deploy a common web stack to run Drupal applications.

Currently, _drucker_ runs on 3 containers:

* `drucker_reverse_proxy` (Varnish/nginx: `203.0.113.2`): Varnish listens on port 80 and sends traffic to the Apache backend via nginx on port 8080).
* `drucker_web` (Apache/PHP: `203.0.113.10`): Apache listens on port 80 and receives traffic from nginx.
* `drucker_db` (MySQL: `203.0.113.12`): MySQL listens on port 3306 and allows the stack to act as a multi-tier environment.

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

You need to have approximately 2.5GB available.

### SSH

You also need to [generate a SSH key](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/) if you don't have one already.

## Technology

_drucker_ ships with the following software stack:

| Software            | Version         |
| --------------------|:---------------:|
| Debian              | 8 (Jessie)      |
| Varnish             | 4.1.2 or later  |
| nginx               | 1.10.1 or later |
| Apache              | 2.4.10 or later |
| PHP-FPM             | 7.0.9 or later  |
| Xdebug              | 2.4.1           |
| PECL uploadprogress | master          |
| Tideways Profiler   | 4.0.5           |
| Code Sniffer        | 2.6.1           |
| phpmd               | 2.4.3           |
| phantomjs           | 2.1.1           |
| MySQL               | 5.5.49 or later |
| Drupal              | 8.3.x           |
| Drush               | 8.1.2           |
| Drupal Console      | 1.0.0-beta5     |
| Composer            | 1.2.0           |
| phpMyAdmin          | 4.6.4           |
| adminer             | 4.2.5           |

## Installation

Add the below host entries in your hosts file:

```
203.0.113.2    drucker.local phpmyadmin.local adminer.local
```

This will ensure you can access:

* `drucker.local`: Drupal 8
* `phpmyadmin.local`: phpMyAdmin (MySQL/MariaDB database management tool)
* `adminer.local`: adminer (Database management tool in a single file)

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
Host 203.0.113.99 203.0.113.2 203.0.113.10 203.0.113.11 203.0.113.12
  StrictHostKeyChecking no
  UserKnownHostsFile=/dev/null
  LogLevel=error
```

This will prevent SSH strict host key checking from getting in the way, since _drucker_ is for development purposes only.

## Usage

Simply run `drucker` if you have a bash alias, or invoke the `drucker.sh` script directly.

```
$ ./drucker.sh
```

For more advanced usage, you can pass the `--dev` or `--prod` CLI parameters. This will configure `drucker` such as the environment becomes dev/prod friendly. The dev mode implies no caching, Twig debugging mode on and helper modules enabled. The prod mode applies all known recommended performance optimizations for near real-life conditions.

```
$ drucker --help
--dev     Prepare drucker for development work with no caching and helper modules enabled.
--prod    Opinionated setup with all known performance best practices enabled.
```

At the beginning of the build process, _drucker_ will prompt you to enter the path to your SSH public key (in order to run [Ansible](https://www.ansible.com/) orchestration on your container). `~/.ssh/id_rsa.pub` is assumed, but you can enter the path to a custom public key then.

When spinning up the web container, drucker will try to map its web directory to a local path (`/var/www/html`) on your computer. Feel free to change this default path to one that is more convenient.

To connect to a container as the privileged _drucker_, simply type:

```
$ docker exec -u drucker -it <container_name> bash
```

To connect to a container as root, type:

```
$ docker exec -it <container_name> bash
```

To log in as the `drucker` username (which is recommended and _is_ a sudoer), simply type:

```
$ su drucker
```

## Passwords:

* drucker user on the container: `drucker`
* MySQL credentials: `root`/`root`
* Drupal credentials: `admin`/`admin`

## Tips and tricks

### Reinstall Drupal from the current dev release

Delete the `drucker` directory under `/var/www/html`

```
$ rm -Rf /var/www/html/drucker
```

Then run `drucker` again.

### Reinstall Drupal from a newer dev release

Delete the `drucker` directory under `/var/www/html`.

```
$ rm -Rf /var/www/html/drucker
```

Also delete the Drupal dev archive (e.g. `drupal-8.1.x-dev.tar.gz`) under `/tmp`

```
$ rm /tmp/drupal-8.1.x-dev.tar.gz
```

Then run `drucker` again.

### Reinstall Drupal from the existing codebase

Delete the `drucker` database. Then run `drucker` again.

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
