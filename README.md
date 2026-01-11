# mc2sf

mc2sf is a backup tool for Minecraft servers. It is meant to backup servers and then upload those backups to
[Seafile](https://www.seafile.com/en/home/), a self hosted file sync and share software. I developed this tool
because on my homelab I use Seafile for storage and thought it would be neat to make this for the server some friends
and I started. At the current moment the implementation is pretty basic and the deployment of it is very Kubernetes focused
due to my homelab using that as well. Even if you are not using this to backup your server, you can always point it to your
worlds and easily back those up to Seafile as well.

## How to Use

There are a couple of ways to run the program at the moment. There are no CLI arguments when you run it at the moment because this
project takes a Container approach for deployments right now. (Perfect first thing to add if I do not end up doing it)

### Run Locally

The first and probably most straightforward way to run the program is to run it locally. This project utilizes [uv](https://docs.astral.sh/uv/) as the projects package manager. The real only reason this is written in Python is because I heard about it and wanted to give it a try lol. So there are two
ways to run it locally. Using uv and then installing with the wheel that has been released.

#### Method A: uv

If you have uv installed running the program is as simple as running the following commands.

```bash
uv sync
uv pip install -e .
uv run mc2sf
```

#### Method B: Installing the wheel

If you do not want to install uv you can install the whell from the releases like so.

```bash
pip install <path to the wheel>
python -m mc2sf
```

For both methods make sure to set the environment variables as seen below.

### Run as a Container

The project has a container image at the following image reference.

```bash
ghcr.io/cjcocokrisp/mc2sf:latest
```

When using it as a container make sure to mount your Minecraft server's storage location and set the environment variables as
seen below.

### Deploy to Kubernetes

The project also provides a helm chart to be able to deploy the tool as a CronJob in Kubernetes. You most likely will need to create your own values
file to match your server's information. Below is the values file marked with what should be changed when you go to install it. You can download the
zip of the helm chart from the release page because I did not release the helm chart on a registry. If you use Argo CD you can also always point the
application to look this repo to install the chart.

```yaml
# Default values for mc2sf.
# This is a YAML-formatted file.
# Declare variables to be passed into your templates.

# General Options
namespace: default
appname: mc2sf
image: ghcr.io/cjcocokrisp/mc2sf:latest
imagepullpolicy: Always
cron: "0 0 * * 0" # Every Sunday at midnight
mode: stream # Default mode, other option is single

# Job Mount Related Options
mountPath: /app/data
mountType: pvc
pvc:
  claimname: mc-server-pvc # Required
nfs:
  server: 127.0.0.1 # Required, if using nfs
  path: / # Required, if using nfs

# Configmap & Secret Related Options
env:
  server:
    path: "" # Required
    name: "Minecraft Server"
  seafile:
    url: "127.0.0.1" # Required
    username: "your-username" # Required
    password: "your-super-secret-password" # Required
    dir: ""
    repoid: "your-repo-id" # Required
  webhook:
    discord: ""
```

## Backup Modes

The `BACKUP_MODE` environment variable controls the mode in which backups are made. There are two modes `stream` or `single` and both vary in the output and how the backup is created.

`stream` is the default and recommended option that you use. It takes up less amount of memory which is ideal for larger servers. It uses the library [zipfly](https://github.com/sandes/zipfly) which creates a stream to write too instead of just writing it to memory. The downside to this method is the filepaths are directory as they appear when you export it so if the server you are trying to backup is deeply nested then that will be preserved in the backup.

`single` is the other mode available. It takes up more memory due to the entire file being saved in memory. The downside is more memory but the filepath is more neat unlike in the stream version. This is only advised if the server file size is small.

## Environment Variables

Below is the list of environment variables that should be set when running the program.

```
BACKUP_MODE - Mode to do the backup in. stream or single (See Backup Modes section for information)
SERVER_PATH - The path to the directory you are trying to back up (REQUIRED)
SERVER_NAME - The name for your server, if not provided defaults to Minecraft Server
SEAFILE_URL - The url or ip of your Seafile instance (REQUIRED)
SEAFILE_USERNAME - The username for the Seafile account that you will be backing up to (REQUIRED)
SEAFILE_PASSWORD - The password for the Seafile account that you will be backing up to (REQUIRED)
SEAFILE_REPO_ID - The ID of the Seafile library you are backing up to, can be obtained by looking at the URL while using Seafile (REQUIRED)
SEAFILE_UPLOAD_DIR - Which directory inside fo the library you are backing up to, it does not need to exist before
DISCORD_WEBHOOK_URL - A Discord Webhook URL to send notifications to when a backup is finished
```

## Contributing

If you would like to contribute to the project in anyway please open an issue or reach out to me to brainstorm some ideas.
You also can just send a pull request just make sure that it is relatively detailed and explains what you are trying to
accomplish.

## Future Features

Top of my head list of things that I would want to add in the future to expand this project.

- More options when backing up

- Ability to back up multiple servers in one run of the program

- More detailed logging