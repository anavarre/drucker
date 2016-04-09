# drucker: Drupal + Docker

**This is a WIP (Work In Progress). Use at your own risk.**

_drucker_ is a [Docker](https://www.docker.com/)-based [Drupal](https://www.drupal.org) stack managed by [Ansible](https://www.ansible.com/) for orchestration. It automates creating [Debian]() containers on which it will deploy a common web stack to run Drupal applications.

**Currently, _drucker_ runs on one container to rule them all**. The plan is to make it a truly service-based suite of containers, to isolate MySQL from multiple Apache/PHP web nodes, have a distributed network filesystem, but also reverse proxy (Varnish) and Load-Balancing (nginx) capabilities.

## Requirements

You need to have both [Docker](https://www.docker.com/) and [Ansible](https://www.ansible.com/) installed on your machine. Check with the below commands:

```
$ docker --version
Docker version 1.10.3, build 20f81dd
$ ansible --version
ansible 1.9.4
```

You also need to [generate a SSH key](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/) if you don't have one already.

## Technology

_drucker_ ships with the following software stack:

| Software       | Version         |
| -------------  |:---------------:|
| Debian         | 8 (Jessie)      |
| Varnish        | 4.0.2.1         |
| Apache         | 2.4.10 or later |
| PHP-FPM        | 5.6.19 or later |
| MySQL          | 5.5.47 or later |
| Drupal         | 8.1.x           |
| Drush          | 8.0.5           |
| Drupal Console | 0.11.2 or later |
| Composer       | 1.0.0 or later  |
| phpMyAdmin     | 4.6.0           |
| adminer        | 4.2.4           |

## Installation

Add the below host entries in your hosts file:

```
203.0.113.2	drucker.local phpmyadmin.local adminer.local
```

This will ensure you can access:

* `drucker.local`: Drupal 8
* `phpmyadmin.local`: phpMyAdmin (MySQL/MariaDB database management tool)
* `adminer.local`: adminer (Database management tool in a single file)

**Recommended**: add the below bash alias entry in your `.bashrc` or `.bash_aliases` file:

```
alias drucker='path/to/drucker/drucker.sh'
```

And source the file (or log out and log back in) to use the alias immediately. E.g.:

```
$ source ~/.bashrc
```

This will allow you to invoke `drucker` from anywhere on your system.

## Usage

Simply run `drucker` if you have a bash alias, or invoke the `drucker.sh` script directly.

```
$ ./drucker.sh
```

During the build process, _drucker_ will prompt you twice to:

* Enter the path to your SSH public key (in order to run [Ansible](https://www.ansible.com/) orchestration on your container). `~/.ssh/id_rsa.pub` is assumed, but you can enter the path to a custom public key
* Enter the SUDO password to run the [Ansible](https://www.ansible.com/) playbook. Just type `drucker`

To connect to the container, simply type:

```
$ docker exec -it drucker_stack bash
```

It will give you root access to the container.

To log in as the `drucker` username (which is recommended and _is_ a sudoer), simply type:

```
$ su drucker
```


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
