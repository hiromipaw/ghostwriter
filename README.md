GhostWriter lets you edit a website via lektor, a flexible and powerful static
content management system for building complex and beautiful websites out of
flat files — for people who do not want to make a compromise between a CMS and a
static blog engine.
GhostWriter works by starting a lektor project that you have cloned via git. If
the project is a fork, you can keep up with upstream by easily rebasing. The
project can be started locally and be edited as a CMS. Finally it also makes
your website accessible as a Tor onion service, by using either OnionShare or a
nginx webserver on a Docker container. The onion setup is completely transparen
for the end user, that will be able to access it via Tor Browser

If you want to edit a website with the ease of a CMS and share it as static
pages GhostWriter starts a lektor server locally and include some git
functionalities to transparently upload your changes or retrieve updates from an
upstream repository. GhostWriter also allow you to share your work via .onion,
by using OnionShare or a nginx webserver running on a Docker container.
Everything is always hosted on your machine, and disappear when you shutdown
GhostWriter.
The .onion can be accessed via Tor Browser.

GhostWriter is still in alpha. Please don't use it for anything serious. Things
are very likely to break.

## Dependencies

### Install pip

Visit: [https://pip.pypa.io/en/stable/installing/](https://pip.pypa.io/en/stable/installing/)

Or use a [package manager](https://packaging.python.org/guides/installing-using-linux-tools/#installing-pip-setuptools-wheel-with-linux-package-managers)

### Install Lektor

```
curl -sf https://www.getlektor.com/install.sh | sh
```

### Install OnionShare

[https://onionshare.org/#downloads](https://onionshare.org/#downloads)

### Install Docker

#### On OSX you can install [Docker Desktop](https://www.docker.com/products/docker-desktop)

#### On Linux

- [https://docs.docker.com/install/](https://docs.docker.com/install/)

#### Via the convenience script

```
$ curl -fsSL https://get.docker.com -o get-docker.sh
$ sudo sh get-docker.sh

```

### Using a git GUI app to clone repositories

While GhostWriter is experimental and if you do not have a lot of knowledge of
git, you might want to have a desktop git app as backup.
There are a few available:
- [https://desktop.github.com/](https://desktop.github.com/)
- [https://git-scm.com/downloads/guis/](https://git-scm.com/downloads/guis/)
