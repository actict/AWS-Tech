Setting Up Collectd Cloudwatch Plugin
======================================

# Summary
- Last Updated: 2019.05.17
- Updated by: scott.hwang@peertec.com

> `collectd` 리눅스 데몬 사용하면 백 개 이상 지표를 Cloudwatch에 추가
> 가능 https://collectd.org/wiki/index.php/Table_of_Plugins
> 최대 metric 수집 빈도를 1초로 설정 가능
> *High-Resolution Metric* 옵션 활성화 필요 (Cloudwatch에서)

# Setup Cloudwatch to use collectd

## CloudWatch 통계 write 권한이 있는 IAM Role 설정

### Role 만들기
Prod 환경에서 `whalex_prod_cloudwatch` role 만들었습니다

- AWS CLI로 방법
    ```
    aws iam create-role --role-name cw_collectd --description \
        "collectd writes CloudWatch metrics" --assume-role-policy-document\
        "file:///path/to/mypolicy.json"
    ```
- AWS Console 방법
    + 웹 GUI에서 *IAM* 선택
    + IAM 왼쪽 메뉴에서 *Role* 선택
    + *Create Role* 선택
    + *AWS Service* 선택
    + *EC2* 선택
    + *Next: Permissions* 버튼 누르기
    + *Permission Policy* 붙이기 (다음 섹션 참조)

### 새로운 IAM Policy 만들기 (doesn't work?)
- AWS CLI 방법 (새로운 policy 만들기)
    ```
    aws create-policy --policy-name collectd_PutMetricData --description
        "allow writing Cloudwatch metrics" \
        --cli-input-json \
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": [
                            "cloudwatch:PutMetricData"
                        ],
                        "Resource": [
                            "*"
                        ]
                    }
                ]
            }
    ```

- AWS Console 방법
    + IAM 왼쪽 메뉴에서 *Policies* 선택
    + *Create policy* 버튼 누르기
    + *Visual Editor* 버튼 눌러서 policy 권한 설정하거나
    + *{}JSON* 버튼 눌러서 JSON schema를 브라우저 창에 붙여넣기
    + 예제 JSON schema for Cloudwatch

        ```
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "cloudwatch:PutMetricData"
                    ],
                    "Resource": "*"
                }
            ]
        }
        ```

### 권한 정책을 Role에 연결하기 (Attach Permissions Policies)
 - AWS CLI 방법

    ```
    aws attach-role-policy --role-name cw_collectd \
        --policy-arn <Amazon Resource Number>
    ```

- AWS Console 방법
    + 새로운 Role 만들 때 Policy Attach 창이 나온다
    + 메뉴에서 방금 만든 *policy* 선택하면 된다


### IAM Role을 monitoring 할 서버에 적용하기
- AWS GUI Console에서 *EC2* -> *Instances*
- *Instance* 선택
- *Actions* 버튼 클릭하기
- *Instance Settings* -> *Attach/Replace IAM Role*
- *IAM role* -> 아까 만든 role 선택
    + 저인 경우 `whalex_prod_cloudwatch`
- 파란색 *Apply* 버튼 누름

# Setup collectd on EC2 instance

## Install collectd from OS repositories
- Amazon Linux
    + `sudo yum install -y collectd collectd-python`
- Ubuntu
    + `sudo apt install collectd-core`
    + `sudo apt install --no-install-recommends collectd`
        + 보급형 `apt install collectd` 하지말 것!
        + 그렇게 하면 X11 GUI 의존 pkg 400MB+ 설치가 됩니다
        + EC2 instance에 X11 GUI 필요 없음

## Install collectd plugin for Cloudwatch
- Download cloudwatch python install script from github
    + `wget https://raw.githubusercontent.com/awslabs/collectd-cloudwatch/master/src/setup.py`
- Make script executable
    + `chmod +x setup.py`
- Run the plugin install script
    + `sudo ./setup.py`
        + `/usr/bin/env python`은 python2.7 되어야
        + 그렇지 않은 경우 `setup.py` 수정하기
            + 예 `/usr/bin/env python2.7`
            + When you run this script, the existing `collectd.conf`
            + will be backed up as `collectd.conf.YYYY-MM-DD_HH_MM`
- 아래 질문에 답하기
- Choose AWS region for published metrics:
    + 1. Automatic [ap-northeast-2] **선택**
    + 2. Custom
- Choose hostname for published metrics:
    + 1. EC2 instance id [i-0123456789 ...] **선택**
    + 2. Custom
- Choose authentication method:
    + 1. IAM Role [`whalex_prod_cloudwatch`] **선택**
    + 2. IAM User
- Enter proxy server name:
    + 1. None **선택**
    + 2. Custom
- Enter proxy server port:
    + 1. None **선택**
    + 2. Custom
- Include the Auto-Scaling Group name as a metric dimension:
    + 1. No **선택**
    + 2. Yes
- Include the FixedDimension as a metric dimension:
    + 1. No
    + 2. Yes
- Enable high resolution:
    + 1. Yes **선택** (1초 간격 측정)
    + 2. No
- Enter flush internal
    + 1. Default 60s **선택**
    + 2. Custom
- Choose how to install CloudWatch plugin in collectd:
    + 1. Do not modify existing collectd configuration
    + 2. Add plugin to the existing configuration
    + 3. Use CloudWatch recommended configuration (4 metrics) **선택**

## collectd plugin 설정하기
- blacklist된 지표 확인 하기
    + `vim /opt/collectd-plugins/cloudwatch/config/blocked_metrics`
    + 사용하고 싶은 *metric* blacklist에 있다면 통계 이름 복사해서
        + `df-var-log-match-percent_bytes-used` custom mountpoints
        + these need to be manually enabled (non-root devices)
    + `/opt/collectd-plugins/cloudwatch/config/whitelist.conf`에 덧 붙이삼
        + `processes.*`

## collectd.conf 설정하기
- enable native collectd plugins
- edit `/etc/collectd/collectd.conf` (Ubuntu)
- edit `/etc/collectd.conf` (Amazon Linux)

> example: enable `processes` collectd plugin on `redis-match0`

```
<Plugin processes>
        ProcessMatch "match_no_th" "match_no_th.py"
        ProcessMatch "trade_receiver2" "trade_receiver2.py"
        ProcessMatch "wxmon" "wxmon"
</Plugin>
```

> If you place the `processes` snippet at the bottom of the file,
> you must make sure that there is at least one blank line at the
> bottom in order for all the match rules to work!

> NOTE: the path to `collectd.conf` is different on Debian/Ubuntu,
> RHEL/Amazon Linux distros. Ubuntu stores this file under
> `/etc/collectd/` whereas RHEL stores this file directly under
> `/etc/`

> example of monitoring cloudwatch process itself in collectd

```
<Plugin processes>
        ProcessMatch "geth" "/usr/bin/geth"
        ProcessMatch "cloudwatch" "/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent"
</Plugin>
```


## 설정 적용하기
- Amazon Linux (v2 이전)
    + `sudo service collectd restart`
    + `chkconfig --list`
        + `collectd`는 runlevel 2,3,4,5에 `on` 상태 확인
        + `off`이면 `on`으로 전환:
        + `sudo chkconfig --level 2345 collectd on`
- Ubuntu 16.04+ or Amazon Linux v2 이상
    + `sudo systemctl restart collectd`

# Cloudwatch Console에서 collectd 통계 보기
- EC2 -> Instances
- Select instance -> Click *Monitoring* tab below
- Click *View all CloudWatch metrics*
- click *collectd*


# References 참조 링크
- 커스텀 Cloudwatch 지표 만들기
    + https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/publishingMetrics.html
- Cloudwatch collectd plugin
    + https://aws.amazon.com/blogs/aws/new-cloudwatch-plugin-for-collectd/
    + https://github.com/awslabs/collectd-cloudwatch
