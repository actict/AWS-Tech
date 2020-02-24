유지보수 Security Group 제어 절차서
=======================================

- Last Updated: 2019.7.25
- Created by: scott.hwang@peertec.com
- Updated by: joshua.huh@actwo.com



## 개요

유지보수 작업을 위해 외부 트래픽을 차단하고 유지보수 페이지를 띄우는 작업 절차를 설명하는 문서



## 절차
### 유지보수 작업 시간 수정 & 게시

`SecOps-Documents/AWS/awscli/maintenance/index.html` 파일에서 유지보수 작업 시간을 수정하고 front-maintenance 서버에 업로드한다.


```sh
$ scp index.html front-maintenance:~/
# SSH 로그인 후 /var/www/html 디렉터리에 파일 복사
$ sudo cp ~/index.html /var/www/html/index.html
```



### 유지보수 모드로 전환

```sh
# 유지보수 스크립트 위치 확인(AWS 디렉터리로 이동해야 한다)
$ pwd
/Users/joshua/Playground/SecOps-Documents/AWS
$ ./maintenancectl.sh on
```

`maintenancectl.sh on` 명령은 아래와 같은 순서로 파이썬 스크립트를 호출해 GDAC 서비스 접근을 차단하고, 유지보수 모드 페이지를 띄운다.

- 유지보수 모드를 처음 시작하는 경우,
  1. `awscli/maintenance/set_gdac_maintenance.sh on`: GDAC 프론트로 들어오는 트래픽을 프론트 서버 로드밸런서가 유지보수 알림 페이지로 전달
  2. `boto3/revoke_ingress_to_access_lb.py`: api.gdac.com 로드밸런서에서 접근 차단
  3. `boto3/maintenance_on_alpha_front.py`: alpha.gdac.com으로 SSH 연결만 허용
  4. `boto3/maintenance_on_beta_front.py`: beta.gdac.com으로 SSH 연결만 허용
  5. `boto3/revoke_ingress_to_beta_access_lb.py`: beta-api.gdac.com 로드밸런서에서 접근 차단
  6. `boto3/revoke_ingress_to_beta_access_vpn_lb.py`: beta-api.gdac.com VPN 로드밸런서에서 접근 차단
  7. `boto3/revoke_ingress_to_openapi_lb.py`: openapi.gdac.com 로드밸런서에서 접근 차단
  8. `boto3/revoke_ingress_to_general_vpn_lb.py` openapi.gdac.com VPN 로드밸런서에서 접근 차단
  9. `boto3/revoke_ingress_to_gmartapi_lb.py`: marketapi.gdac.com 로드밸런서에서 접근 차단
  10. `boto3/revoke_ingress_to_partner_lb.py`: partner.gdac.com 로드밸런서에서 접근 차단
- 베타 모드에서 유지보수 모드로 전환하는 경우,
  1. `boto3/maintenance_on_beta_front.py`: beta.gdac.com으로 SSH 연결만 허용
  2. `boto3/revoke_ingress_to_beta_access_lb.py`: beta-api.gdac.com 로드밸런서에서 접근 차단
  3. `boto3/revoke_ingress_to_beta_access_vpn_lb.py`: beta-api.gdac.com VPN 로드밸런서에서 접근 차단
  4. `boto3/revoke_ingress_to_general_vpn_lb.py` openapi.gdac.com VPN 로드밸런서에서 접근 차단

- 유지보수 모드로 전환되면 `/tmp/status` 파일에 `on`으로 값을 기록한다.



### 베타 모드로 전환

유지보수 모드일 때에만 베타 모드로 전환할 수 있다. 베타 모드일 때에는 사내망과 VPN을 이용한 연결만 가능하다. 베타 모드가 아닌 경우, 전환할 수 없음을 알려준다.

```sh
$ pwd
/Users/joshua/Playground/SecOps-Documents/AWS
$ ./maintenancectl.sh beta
```

베타 모드로 전환하면 아래와 같은 순서대로 파이썬 스크립트를 호출하고, `/tmp/status` 파일에 `beta`로 값을 기록한다.

1. `boto3/maintenance_off_beta_front.py`: beta.gdac.com 연결 허용
2. `boto3/authorize_ingress_to_beta_access_lb.py`: beta-api.gdac.com 연결 허용(실제로 이쪽으로 트래픽이 들어오기는 하나?)
3. `boto3/authorize_ingress_to_beta_access_vpn_lb.py`: 사내망/VPN으로부터 beta-api.gdac.com 연결 허용
4. `boto3/authorize_ingress_to_general_vpn_lb.py`: 사내망/VPN으로부터 openapi.gdac.com 연결 허용



### 서비스 모드로 전환

베타 모드에서 기능 시험 결과 문제가 없으면, 서비스 모드로 전환하고 `/tmp/status` 파일을 삭제한다. 베타 모드를 건너뛰고 유지보수 모드에서 서비스 모드로 전환하는 것도 가능하지만 가급적이면 베타 모드에서 테스트하고 전환한다.

```sh
$ pwd
/Users/joshua/Playground/SecOps-Documents/AWS
$ ./maintenancectl.sh off
```

서비스모드로 전환하면 모든 서비스를 허용하고, 마지막으로 유지보수 알림 페이지로 들어오는 트래픽을 프론트 서버로 되돌린다.

1. `boto3/authorize_ingress_to_access_lb.py`: 로드밸런서에서 api.gdac.com 서비스 연결 허용
2. `boto3/maintenance_off_alpha_front.py`: 업무망에서 alpha.gdac.com 서비스 연결 허용
3. `boto3/maintenance_off_beta_front.py`: 업무망에서 beta.gdac.com 서비스 연결 허용
4. `boto3/authorize_ingress_to_beta_access_lb.py`: beta.gdac.com 서비스 연결 허용(beanstakk 로드밸런서)
5. `boto3/authorize_ingress_to_beta_access_vpn_lb.py`: beta.gdac.com 서비스 연결 허용(VPN 로드밸런서)
6. `boto3/authorize_ingress_to_general_vpn_lb.py`: beta-api.gdac.com 서비스 연결 허용
7. `boto3/authorize_ingress_to_openapi_lb.py`: openapi.gdac.com 서비스 연결 허용
8. `boto3/authorize_ingress_to_gmartapi_lb.py`: marketapi.gdac.com 서비스 연결 허용
9. `boto3/authorize_ingress_to_partner_lb.py`: partner.gdac.com 서비스 연결 허용
10. `awscli/maintenance/set_gdac_maintenance.sh off`: 유지보수 알림 페이지로 들어오는 트래픽을 프론트 서버 로드밸런서가 GDAC 프론트로 전달



## ETC

유지보수 모드를 이렇게 스크립트로 정리하기까지 많은 착오가 있었음. 이제 이렇게 심플하게 되었으니 다행. 유지보수 모드로 전환할 때 관건은 로드밸런서에서 서비스 트래픽을 차단하는 건데, **로드밸런서가 사용하는 보안 그룹에 변화가 생기면 즉시 해당 보안 그룹을 제어하는 파이썬 스크립트도 수정해야 하는 것을 잊지 말 것.**
