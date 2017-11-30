## L_PLAYGROUND STARTED

### 1.环境介绍

服务器外网只开启22、80端口，防火墙内开了6379、8000端口。22端口是服务器的ssh端口，80端口是nginx,为了提高服务可用性和日志记录。内网8000端口是我们模拟的未上线的开发环境(或5000端口)，6379端口是没有密码的redis服务。

### 2.源码介绍

源码在ctf_django和ctf_second两个文件夹，这里使用gunicorn是为了使web服务更加健壮。

#### 1.nginx配置

nginx相关配置文件(目录相关配置需要改动)如下：
```
        upstream app_server {
                server unix:/home/grt1st/ctf_django/ctf_django.sock fail_timeout=0;
        }

        server {
                listen 80;
                server_name localhost;
                keepalive_timeout 5;
                location ~* \.(py|sqlite3|service)$ {
                        deny all;
                }
                location /static  {
                        alias /home/grt1st/ctf_django/static/;
                }
                location / {
                        add_header Server Django/1.11.5;
                        add_header Server CPython/3.4.1;                        
                        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                        proxy_set_header Host $host;
                        proxy_set_header X-Real-IP $remote_addr;
                        proxy_set_header X-Scheme $scheme;
                        proxy_redirect off;
                        proxy_pass http://app_server;
                }
        }

```

（已经提供了nginx配置文件的示例

#### redis配置

redis需要做一些安全的限制，修改`/etc/redis/redis.conf`，找到rename-command处，对命令进行重命名：
```
rename-command CONFIG XDSEC_FLAG
rename-command FLUSHALL XDSEC_FLUSHALL
rename-command FLUSHDB  XDSEC_FLUSHDB
rename-command EVAL XDSEC_EVAL
rename-command SAVE XDSEC_SAVE
rename-command BGSAVE XDSEC_BGSAVE
rename-command SHUTDOWN XDSEC_SHUTDOWN
rename-command DEBUG XDSEC_dEBUG
rename-command CLUSTER XDSEC_CLUSTER
rename-command EVALSHA XDSEC_EVALSHA
rename-command SCRIPT XDSEC_SCRIPT
rename-command BGREWRITEAOF XDSEC_BGREWRITEAOF
rename-command CLIENT XDSEC_CLIENT
rename-command EXEC XDSEC_EXEC
rename-command SLAVEOF XDSEC_SLAVEOF
```

#### 3.web服务配置

##### 1.第一个web服务

将以下内容(目录相关配置需要改动)保存为gunicorn.service文件名，放在ctf_django目录下。
```
[unit]
Description=gunicorn daemon
After=network.target

[Service]
User=nobody
Group=nogroup
WorkingDirectory=/home/grt1st/ctf_first
ExecStart=/usr/local/bin/gunicorn --workers 3 --bind unix:/home/grt1st/ctf_django/ctf_django.sock ctf_django.wsgi

[Install]
WantedBy=multi-user.target
```

然后进入目录(目录相关配置需要改动)，启动服务。

```
cd /home/grt1st/ctf_django/
sudo /home/grt1st/.conda/envs/ctf/bin/gunicorn --workers 3 --bind unix:/home/grt1st/ctf_django/ctf_django.sock ctf_django.wsgi
```

##### 2.第二个web服务

之后需要python3.4.1的虚拟环境，因为要模拟漏洞环境。这里虚拟环境我使用的是anaconda。启动虚拟环境`source activate ctf`，然后启动ctf_second：`python ～/ctf_second/ctf_second.py`，此时监听端口为5000。在比赛时，为了使web服务更加健壮，服务器上启用的是gunicorn：`pip install gunicorn`（虚拟环境安装gunicorn）、`cd ～/ctf_Second`、`gunicorn ctf_second:app`，监听的端口改动到了8000。