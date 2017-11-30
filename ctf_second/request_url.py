#coding:utf-8
import socket
from urllib.parse import urlparse

def check_inner_ip(ip):
    ip_list = ip.split('.')

    ip_part = [int(i) for i in ip_list]


    if ip_part[0] == 192 and ip_part[1] == 168:
        return False
    if ip_part[0] == 10 or ip_part[1] == 0:
        return False
    if ip_part[0] == 172 and ip_part[1] >= 16 and ip_part[1] <=31:
        return False
    if ip_part[0] == 127:
        return False

    return True


def check_box(url):
    try:
        url_host = urlparse(url).hostname
        url_ip = socket.getaddrinfo(url_host, 'http')[0][4][0]
    except Exception as e:
        #print(e)
        return False

    if not check_inner_ip(url_ip):
        return False

    return True


