Cloudwatch Logs HOWTO
==============================

# Summary
- Last Updated: 2019.05.17
- Updated by: scott.hwang@peertec.com

> Note: As of Jan 2019, AWS recommends installing the `awslogs`
> package from the default Amazon Linux 2 default repositories.
> `awslogs` is also now available by default in all Elastic
> Beanstalk AMI's. After installation, `awslogs` creates the
> systemd service `awslogsd.service`. If installed from a
> package, `awslogs` config files are located in `/etc/awslogs/`
> and `/etc/awslogs/config/`.
>
> In late 2018, awslabs' `amazon-cloudwatch-agent` went closed-source
> and changed its development language to Golang. With this change,
> `amazon-cloudwatch-agent.json` has been replaced with
> `amazon-cloudwatch-agent.toml` and the syntax has changed, too.
> The config path `/opt/aws/amazon-cloudwatch-agent/etc/` is still
> the same, however. Unfortunately, as of Jan. 2019, however, AWS
> has still not documented the `toml` config syntax for cloudwatch
> agent.
>
> Fortunately, you can use `awslogs` as a drop-in replacement for
> the old `amazon-cloudwatch-agent` although the config is a bit
> different.


# Cloudwatch Agent (awslogs) install

## Create IAM Role for Cloudwatch Log Agent and SSM

- Create Role (or use existing role)
- Attach Policy
    + `CloudWatchAgentServerPolicy`
    + `AmazonEC2RoleforSSM`

## Amazon Linux 2

### `awslogs` Package Install

> `awslogs` replaces the old open-source `amazon-cloudwatch-agent`

```bash
yum update -y
yum install awslogs
```


#### /etc/awslogs/awscli.conf

> By default, all logs are sent to AWS region `us-east-1`, but
> GDAC runs all its servers in `ap-northeast-2`. Therefore you
> must edit `/etc/awslogs/awscli.conf` as follows:

```
[plugins]
cwlogs = cwlogs
[default]
region = ap-northeast-2
```


#### /etc/awslogs/awslogs.conf

> This file contains just the basic settings for the `awslogsd`
> daemon. To specify what logs to send to Cloudwatch Logs, you
> must place a yaml-style `.conf` file in `/etc/awslogs/config/`

```
[general]
# Path to the CloudWatch Logs agent's state file. The agent uses this file to maintain
# client side state across its executions.
state_file = /var/lib/awslogs/agent-state
```

#### /etc/awslogs/config/mylogs.conf

> Here's an example from EC2 server `auth-bank-new`:

```yaml
[auth_bank_new_app_logs]
log_group_name = auth-bank_logs
log_stream_name = auth-bank_{ip_address}_app.log
file = /var/log/nodejs/app/bank.log*
[auth_bank_nginx_access]
log_group_name = auth-bank_logs
log_stream_name = auth-bank_{ip_address}_nginx_access.log
file = /var/log/nginx/access.log
[auth_bank_nginx_error]
log_group_name = auth-bank_logs
log_stream_name = auth-bank_{ip_address}_nginx_error.log
file = /var/log/nginx/error.log
```

> This is the exact same format as the awslogs log config file in
> Elastic Beanstalk template `.ebextensions` folder!


### Package Install
```bash
wget https://s3.amazonaws.com/amazoncloudwatch-agent/linux/amd64/latest/AmazonCloudWatchAgent.zip
unzip AmazonCloudWatchAgent.zip
sudo ./install.sh
#rpm -q amazon-cloudwatch-agent
#dpkg -l amazon-cloudwatch-agent
sudo systemctl enable amazon-cloudwatch-agent
sudo systemctl start amazon-cloudwatch-agent
```

### Cloudwatch Agent 설정파일 수정

#### amazon-cloudwatch-agent.json
> Default 경로: `/opt/aws/amazon-cloudwatch-agent/etc/`
> config 파일은 `amazon-cloudwatch-agent.json`
>  이 파일은 큰 항콕 3개가 있다: `agent`, `metrics`, 그리고 `logs`
> 현재 system metrics은 collectd로 수집하고 있기 때문에 여기서
> `metrics` 따로 설정 하지 않을 거다.

> `logs` section에 `logs_collected` 항목 밑에 어떤 로그 파일을 수집할지
> 정해야 함.

```
{
  "agent": {
    "metrics_collection_interval": 60,
    "region": "ap-northeast-2",
    "logfile": "",
    "debug": false
  },

  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          {
            "file_path": "/var/log/messages",
            "log_group_name": "cosmos_var_log_messages",
            "log_stream_name": "sentry0_{ip_address}_var_log_messages.log",
            "timezone": "UTC",
            "encoding": "utf-8"
          }
        ]
      }
    },
    "log_stream_name":"sentry0_log_default"
  }
}
```


# amazon-cloudwatch-agent 시작

## 최신 리눅스 배포판

- `sudo systemctl start amazon-cloudwatch-agent`
- `sudo systemctl status amazon-cloudwatch-agent`


# Amazon Linux 1을 사용하는 EB instance에서 CW agent 설치하기

## ansible playbook 실행 (DEPRECATED)
- `ansible-playbook install_amzn_cloudwatch_agent.yaml`

## 각각 EB 인스턴스에 붙어서 `...-cloudwatch-agent.json` 설정하기
- 설정 파일 경로: `/opt/aws/amazon-cloudwatch-agent/etc/`

> 각 각 EB 인스턴스의 app log 경로가 달라서 우리 repo에서 현 폴더 내에
> 장비 별 `.json` 파일 참조하세요

## `amazon-cloudwatch-agent-ctl`로 agent 프로세스 실행

- `amazon-cloudwatch-agent-ctl -a start` (root으로)

> 경로는 `/opt/aws/amazon-cloudwatch-agent/etc/bin/`


# Setting up Cloudwatch for on-premises server (not EC2)

> specify credentials to use in `/opt/aws/amazon-cloudwatch-agent/etc`
> file `common-config.toml` and make sure that you have populated
> `~/.aws/{credentials,config}` with IAM ID and Key info.


# Troubleshooting

> If no logs are sent by `amazon-cloudwatch-agent`, try deleting
> all the files in `/var/log/amazon/amazon-cloudwatch-agent/state`;
> These files keep track of the place in the file so that duplicates
> aren't set to Cloudwatch. After removing the files, restart the
> agent.


# References
https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Install-CloudWatch-Agent.html
https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/create-iam-roles-for-cloudwatch-agent.html
