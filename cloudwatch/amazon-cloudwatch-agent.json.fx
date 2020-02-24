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
            "file_path": "/home/ubuntu/apps/er-cycle/logs/*log",
            "log_group_name": "fx_logs",
            "log_stream_name": "fx_{ip_address}_er-cycle_logs",
            "timezone": "UTC",
            "encoding": "utf-8"
          },
          {
            "file_path": "/home/ubuntu/apps/er-api/logs/*log",
            "log_group_name": "fx_logs",
            "log_stream_name": "fx_{ip_address}_er-api_logs",
            "timezone": "UTC",
            "encoding": "utf-8"
          },
          {
            "file_path": "/var/log/auth.log",
            "log_group_name": "all_ssh_logs",
            "log_stream_name": "fx_{ip_address}_ssh.log",
            "timezone": "UTC",
            "encoding": "utf-8"
          },
          {
            "file_path": "/var/log/dpkg.log",
            "log_group_name": "all_ssh_logs",
            "log_stream_name": "fx_{ip_address}_dpkg.log",
            "timezone": "UTC",
            "encoding": "utf-8"
          },
          {
            "file_path": "/home/ubuntu/.bash_history",
            "log_group_name": "all_shell_history",
            "log_stream_name": "fx_{ip_address}_ubuntu_bash_history",
            "timezone": "UTC",
            "encoding": "utf-8"
          },
          {
            "file_path": "/root/.bash_history",
            "log_group_name": "all_shell_history",
            "log_stream_name": "fx_{ip_address}_root_bash_history",
            "timezone": "UTC",
            "encoding": "utf-8"
          },
          {
            "file_path": "/var/log/aide/aide.log",
            "log_group_name": "all_aide_logs",
            "log_stream_name": "fx_{ip_address}_aide.log",
            "timezone": "UTC",
            "encoding": "utf-8"
          }
        ]
      }
    },
    "log_stream_name":"fx_log_default"
  }
}
