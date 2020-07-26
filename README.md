# Docker-files

Docker-files is a website to index Dockerfile and docker-compose files from open source projects.

## Web-Infra

Setting up infrastructure for running Flask website

### Setting up venv

```bash
make venv requirements
```

### Running on DigitalOcean

*Pre-requisite*

- [ ] Set `DIGITALOCEAN_ACCESS_TOKEN` environment variable to token from [Digital Ocean API Key](https://cloud.digitalocean.com/account/api/tokens).
- [ ] Set `DIGITAL_OCEAN_SSH_FINGERPRINT` environment variable to SSH fingerprint from [Digital Ocean SSH Key](https://cloud.digitalocean.com/account/security).
- [ ] Set `DIGITAL_OCEAN_SSH_KEY` environment variable to the file path of private SSH key. For eg. ~/.ssh/py-flask-digitalocean as this will be used when setting up the Digital Ocean droplet.
- [ ] Set `FLASK_SECRET_KEY` environment variable as a secure random string which is used by Flask framework.

These can be setup by

```bash
export DIGITAL_OCEAN_TOKEN=
export DIGITAL_OCEAN_SSH_FINGERPRINT=
export DIGITAL_OCEAN_SSH_KEY=
export FLASK_SECRET_KEY=
```

*Setting up application*

- Start up DigitalOcean droplet

```bash
make doplaybook
```

- Setup user for management and deployment

```bash
make bootstrap
```

- Deploy Flask application

```bash
make deployapp
```

- Setup Supervisor, Nginx etc

```bash
make setupplaybook
```

*Updating application*

To re-deploy changes and restart supervisor daemon after deployment

```bash
make deployapp updateapp
```

*Rollback application*

```bash
make updateapp
```

*Cleanup*

Make sure you have [doctl](https://github.com/digitalocean/doctl) installed

It can be initialised with the token in the environment variable

```bash
doctl auth init --access-token $DIGITAL_OCEAN_TOKEN
```

Then run the following to delete the droplet.

> Please note that the following action is destructive and remove any unsaved changes/data on the droplet.

```
make deleteinfra
```
