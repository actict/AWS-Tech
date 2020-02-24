Using awslogs instead of cloudwatch-agent
===========================================

# Summary
- Last Updated: 2019.06.11
- Updated by: scott.hwang@peertec.com

> AWS now recommends using `awslogs` agent instead of
> `amazon-cloudwatch-agent`. The latter used to be open-source,
> but the newer version is closed-source. Also the latter changed
> its configuration format from `.json` to `.toml`. Luckily,
> `amazon-cloudwatch-agent` has the ability to generate `.toml`
> files from `.json`.
>
> On Amazon Linux 1, 2 `awslogs` is available as a package from the
> default OS repository. On non-Amazon Linux distros, however, you
> have to download the install scripts from S3.
>
> Note: On ElasticBeanstalk instances running Amazon Linux 1, awslogs
> is installed by default, although the daemon is not running unless
> you make some add'l settings.


# Installation

## Amazon Linux 1

> Installing the package for awslogs is not necessary on Amazon
> Linux 1, but necessary on Amazon Linux 2

```sh
sudo yum install awslogs
```

> edit `/etc/awslogs/awscli.conf`

```
[plugins]
cwlogs = cwlogs
[default]
region = ap-northeast-2
```

> edit `/etc/awslogs/awslogs.conf`
> By default, this file contains the following directive:

```
[/var/log/messages]
datetime_format = %b %d %H:%M:%S
file = /var/log/messages
buffer_duration = 5000
log_stream_name = {instance_id}
initial_position = start_of_file
log_group_name = /var/log/messages
```

> This will create a new log group called `/var/log/messages`
> but this is not the log group name convention that Actwo uses.
> This file need only contain the following line:

```
[general]
state_file = /var/lib/awslogs/agent-state
```

> you must change `region` from `us-east-1` to `ap-northeast-2`
> Next, create your custom conf file in `/etc/awslogs/config/`

> `config/auth_bank_logs.conf`

```
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

> Note: In the custom log config above the `[header_name]` can
> contain underbars, **BUT HYPHENS ARE NOT SUPPORTED**! If a
> hyphen is placed inside the header, the log settings under that
> header will be ignored.

### Start the awslogs daemon and enable startup at boot

```sh
sudo chkconfig --level 2345 awslogs on
sudo service awslogs start
```

### See list of services enabled at startup

`chkconfig --list`

> make sure that `awslogs` is set to `on` for runlevels
> 2, 3, 4, 5


### Check that awslogsd is running properly

```
tail -f /var/log/awslogs.log
```

### awslogs upstart (init) config file

> When you start the awslogs daemon on AWS Linux 1, you inovke it
> with `service awslogs start`. When you do this, what is actually
> executed is `/etc/init.d/awslogs` an upstart init script.


### awslogs service does not automatically restart if it dies

> workaround: create an Elastic Beanstalk cron job by placing it
> inside `.ebextensions` in your source bundle. You can see an
> example at

https://github.com/awsdocs/elastic-beanstalk-samples/blob/master/configuration-files/aws-provided/instance-configuration/cron-linux.config


### logs do not show up in Cloudwatch Logs despite awslogs running

> This can occur if `awslogs` service has been dead for more than a
> few days. When you restart the daemon, the backlog is too large, so
> nothing gets sent. The workaround for this issue is to delete the
> awslogs counter which keeps track of its place in log files. The
> location of this counter is `/var/lib/awslogs`

```sh
rm agent-state
service awslogs start
sleep 10
service awslogs restart
```



## Ubuntu

> **NOTE: awslogs does not work on Ubuntu**
> it works great on Amazon Linux 1,2 however.


```sh
curl https://s3.amazonaws.com/aws-cloudwatch/downloads/latest/awslogs-agent-setup.py -O
chmod +x awslogs-agent-setup.py
curl https://s3.amazonaws.com/aws-cloudwatch/downloads/latest/AgentDependencies.tar.gz -O
tar xvf AgentDependencies.tar.gz -C /tmp/
./awslogs-agent-setup.py --region ap-northeast-2 --dependency-path /tmp/AgentDependencies/
```

> You will then be prompted to enter some settings interactively:

```
Launching interactive setup of CloudWatch Logs agent ...

Step 1 of 5: Installing pip ...libyaml-dev does not exist in system DONE

Step 2 of 5: Downloading the latest CloudWatch Logs agent bits ... DONE

Step 3 of 5: Configuring AWS CLI ...
AWS Access Key ID [None]:
AWS Secret Access Key [None]:
Default region name [ap-northeast-2]:
Default output format [None]:

Step 4 of 5: Configuring the CloudWatch Logs Agent ...
Path of log file to upload [/var/log/syslog]:
Destination Log Group name [/var/log/syslog]: hdac_{ip_address}_logs

Choose Log Stream name:
  1. Use EC2 instance id.
  2. Use hostname.
  3. Custom.
Enter choice [1]: 2

Choose Log Event timestamp format:
  1. %b %d %H:%M:%S    (Dec 31 23:59:59)
  2. %d/%b/%Y:%H:%M:%S (10/Oct/2000:13:55:36)
  3. %Y-%m-%d %H:%M:%S (2008-09-08 11:52:54)
  4. Custom
Enter choice [1]: 1

Choose initial position of upload:
  1. From start of file.
  2. From end of file.
Enter choice [1]:
More log files to configure? [Y]: n

Step 5 of 5: Setting up agent as a daemon ...DONE


------------------------------------------------------
- Configuration file successfully saved at: /var/awslogs/etc/awslogs.conf
- You can begin accessing new log events after a few moments at https://console.aws.amazon.com/cloudwatch/home?region=ap-northeast-2#logs:
- You can use 'sudo service awslogs start|stop|status|restart' to control the daemon.
- To see diagnostic information for the CloudWatch Logs Agent, see /var/log/awslogs.log
- You can rerun interactive setup using 'sudo python ./awslogs-agent-setup.py --region ap-northeast-2 --only-generate-config'
```

> Note that it is *NOT* necessary to enter an AWS API Key ID
> and Secret if you have already created a custom role containing
> permissions to write to Cloudwatch (`put_metrics`)

# Miscellaneous Notes

> If you have assigned an IAM Role to an EC2 instance and you also
> have populated `~/.aws/{config,credentials}` (API key and secret),
> apps that rely on the IAM Role will fail, although apps using the
> API credentials will work fine.

## {ip_address} parameter in awslogs config files not working

> `awslogs` uses python's `socket` module to find the IP of the
> host machine. But this only works if `/etc/hosts` contains a
> non-localhost IP (i.e. not `127.0.0.1`) mapped to a unique
> hostname. If your `hosts` file only contains the line
> `127.0.0.1  localhost myhostname`, then python will only
> see `127.0.0.1` as your local IP:


```python
>>> import socket
>>> socket.gethostbyname(socket.gethostname())
'127.0.0.1'
```

> But if you manually register your unique VPC IP in `/etc/hosts`
> like `10.0.48.103  hashivault`, then python will return the
> proper internal IP:

```python
>>> import socket
>>> socket.gethostbyname(socket.gethostname())
'10.0.48.103'
```
