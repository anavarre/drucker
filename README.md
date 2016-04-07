# drucker: Drupal + Docker

**This is a WIP (Work In Progress). Use at your own risk.**

_drucker_ is a [Docker](https://www.docker.com/)-based [Drupal](https://www.drupal.org) stack managed by [Ansible](https://www.ansible.com/) for orchestration. It automates creating [Debian]() containers on which it will deploy a common PHP/MySQL web stack to run Drupal applications.

Currently, _drucker_ runs on one container to rule them all. The plan is to make it a truly service-based suite of containers, to isolate MySQL from multiple Apache/PHP web nodes, have a distributed network filesystem, but also reverse proxy (Varnish) and Load-Balancing (nginx) capabilities.

Currently, _drucker_ ships with:

* Apache 2.4
* PHP-FPM 5.6
* MySQL 5.5
* Drupal 8.1.x
* Drush 8.0.5
* Composer (latest)
* phpMyAdmin 4.6.0
* adminer 4.2.4

## Requirements

You need to have both [Docker](https://www.docker.com/) and [Ansible](https://www.ansible.com/) installed on your machine. Check with the below commands:

```
$ docker --version
Docker version 1.10.3, build 20f81dd
$ ansible --version
ansible 1.9.4
```

## Installation

Add the below host entries in your hosts file:

```
203.0.113.2	drucker.local phpmyadmin.local adminer.local
```

This will ensure you can access:

* `drucker.local`: Drupal 8
* `phpmyadmin.local`: phpMyAdmin (MySQL/Maria database management tool)
* `adminer.local`: adminer (Database management tool in a single file)

**Recommended**: add the below bash alias entry in your `.bashrc` or `.bash_aliases` file:

```
alias drucker='path/to/drucker/drucker.sh'
```

This will allow you to invoke `drucker` from anywhere on your system.

## Usage

Simply run `drucker` if you have a bash alias, or invoke the `drucker.sh` script directly.

```
$ ./drucker.sh
```

During the build process, _drucker_ will expect two things from you:

* Enter the path to your SSH public key (in order to run [Ansible](https://www.ansible.com/) orchestration on your container). `~/.ssh/id_rsa.pub` is assumed, but you can enter the path to a custom public key
* Enter the SUDO password to run the [Ansible](https://www.ansible.com/) playbook. Just type `drucker`

To connect to the container, simply type:

```
$ docker exec -it drucker_stack bash
```

It will give you root access to the container.

## Passwords:

* drucker user on the container: `drucker`
* Ansible playbook SUDO password: `drucker`
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

Delete the `drucker` directory under `/var/www/html`

```
$ rm -Rf /var/www/html/drucker
```

Also delete the Drupal dev archive (e.g. `drupal-8.1.x-dev.tar.gz`) under `/tmp`

```
$ rm /tmp/drupal-8.1.x-dev.tar.gz
```

Then run `drucker` again.

### Delete the container

Run:

```
$ docker rm -f drucker_stack
```

### Delete the drucker base image

Run:

```
$ docker rmi drucker:base
```
