# drucker: Drupal + Docker

**This is a WIP (Work In Progress). Use at your own risk.**

_drucker_ is a [Docker](https://www.docker.com)-based [Drupal](https://www.drupal.org) stack managed by [Ansible](https://www.ansible.com) for orchestration. It automates creating [Debian](https://www.debian.org) containers on which it will deploy a common web stack to run Drupal applications.

Currently, _drucker_ runs on 3 minimalistic containers:

* `drucker_reverse_proxy` (Varnish/nginx): Varnish listens on port 80 and sends traffic to the nginx backend on port 8080
* `drucker_web` (Apache/PHP/MySQL): Apache listens on port 8080 and receives traffic from nginx
* `drucker_gluster` (GlusterFS): Distributed network filesystem (WIP - not currently integrated with the web container)

The plan is to make _drucker_ a truly service-based suite of containers, to isolate MySQL from multiple Apache/PHP web nodes but also Load-Balancing and HA capabilities. When we have this, then a [0.1](https://github.com/anavarre/drucker/milestones/0.1) release will be tagged.

## Requirements

You need to have both [Docker](https://www.docker.com/) and [Ansible](https://www.ansible.com/) installed on your machine. Check with the below commands:

```
$ docker --version
Docker version 1.10.3, build 20f81dd
$ ansible --version
ansible 2.0.2.0
```

Note: Ansible 2 or later is assumed in Ansible playbooks. 

You also need to [generate a SSH key](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/) if you don't have one already.

## Technology

_drucker_ ships with the following software stack:

| Software       | Version         |
| -------------  |:---------------:|
| Debian         | 8 (Jessie)      |
| Varnish        | 4.0.2.1         |
| nginx          | 1.6.2           |
| Apache         | 2.4.10 or later |
| PHP-FPM        | 5.6.19 or later |
| GlusterFS      | 3.7.10 or later |
| MySQL          | 5.5.47 or later |
| Drupal         | 8.1.x           |
| Drush          | 8.1.1           |
| Drupal Console | 0.11.3          |
| Composer       | 1.1.0           |
| phpMyAdmin     | 4.6.1           |
| adminer        | 4.2.4           |

## Installation

Add the below host entries in your hosts file:

```
203.0.113.20    drucker.local phpmyadmin.local adminer.local
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

At the beginning of the build process, _drucker_ will prompt you to enter the path to your SSH public key (in order to run [Ansible](https://www.ansible.com/) orchestration on your container). `~/.ssh/id_rsa.pub` is assumed, but you can enter the path to a custom public key

To connect to a container, simply type:

```
$ docker exec -it <container_name> bash
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

### Delete a container

Run:

```
$ docker rm -f <container_name>
```

### Delete the drucker base image

Run:

```
$ docker rmi drucker:base
```
