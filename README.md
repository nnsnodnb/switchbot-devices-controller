# switchbot-devices-controller

## Setup

```shell
$ git clone github.com:nnsnodnb/switchbot-devices-controller.git
$ cd switchbot-devices-controller
$ uv sync
```

## Tools

<details>
<summary>close_curtain</summary>

## Requirements

### Environment variables

- `LATITUDE`
- `LONGITUDE`
- `CFN_STACK_NAME`
- `S3_BUCKET_NAME`
- `SWITCHBOT_API_TOKEN`
- `SWITCHBOT_API_CLIENT_SECRET`
- `IS_CREATE_LOG_GROUP` (Optional) (true or false, default: true)
- `USE_LOCALSTACK` (Optional) (true or false, default: false)

## Run

```shell
$ cd /path/to/switchbot-devices-controller
$ source .venv/bin/activate
$ python close_curtain.py
```

</details>
