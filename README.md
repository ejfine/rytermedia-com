[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-black.json)](https://github.com/copier-org/copier)
[![Actions status](https://www.github.com/ejfine/rytermedia-com/actions/workflows/ci.yaml/badge.svg?branch=main)](https://www.github.com/ejfine/rytermedia-com/actions)
[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://www.github.com/ejfine/rytermedia-com)
[![OpenIssues](https://isitmaintained.com/badge/open/ejfine/rytermedia-com.svg)](https://isitmaintained.com/project/ejfine/rytermedia-com)



# Development

## Download files from S3 locally
```bash
aws s3 sync s3://manual-artifacts--rytermedia-com--prod-adf4c0c/rytermedia_app/public/s3 ./rytermedia_app/public/s3 --dryrun
```

## Infrastructure Deployments
Run a Pulumi Preview: `uv --directory=./infrastructure run python -m infrastructure.pulumi_deploy --stack=dev`


## Updating from the template
This repository uses a copier template. To pull in the latest updates from the template, use the command:
`copier update --trust --conflict rej --defaults`
