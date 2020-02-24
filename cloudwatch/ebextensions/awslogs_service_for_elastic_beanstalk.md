Cloudwatch Logs (awslogs service) for Elastic Beanstalk
========================================================

# Summary
- Last Updated: 2018.12.20
- Updated by: jun.go@actwo.com

> Cloudwatch Logs agent는 기본적으로 모든 Elastic Beanstalk 이미지
> 속에 담아져 있습니다.


## Logging

```
tail -f /var/log/awslogs.log
```

## Custom Log File을 cloudwatch logs으로

```
/etc/awslogs/config/mycustom.config
```

> 예제

```

```

# References

https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/AWSHowTo.cloudwatchlogs.html
