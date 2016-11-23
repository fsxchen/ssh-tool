#!/usr/bin/env python
#coding:utf-8
import os

import sys
import pwd
import getpass
from paramiko import SSHClient
from paramiko import AutoAddPolicy, SSHException

client = SSHClient()

# client.load_system_host_keys()

LOCAL_USER_NAME = pwd.getpwuid(os.getuid()).pw_name

def sync_public_key(host, port=22, username=None, password=None):
    if LOCAL_USER_NAME == "root":
        rsa_pub_path = "/root/.ssh/id_rsa.pub"
    else:
        rsa_pub_path = "/home/{user}/.ssh/id_rsa.pub".format(user=LOCAL_USER_NAME)
    if os.path.exists(rsa_pub_path):
        PUB_KEY = rsa_pub_path
    else:
        print("本地没有可用的SSH公钥，请使用ssh-ken-gen生成")
        sys.exit(-1)
    try:
        client = SSHClient()
        client.connect(hostname=host, username=username, password=password)
    except SSHException, e:
        print e
        client.close()
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(hostname=host, username=username, password=password)

        sftp_client = client.open_sftp()
        if username == "root":
            remote_home = "/root"
            remote_rsa_pub = "/root/.ssh/%s.pub" % (LOCAL_USER_NAME)
        else:
            remote_home = "/home/{username}".format(username=username)
        remote_ssh_home = "{remote_home}/.ssh".format(remote_home=remote_home)

        remote_rsa_pub = "{remote_ssh_home}/{local_user}.pub".format(
                remote_ssh_home=remote_ssh_home, local_user=LOCAL_USER_NAME)
        try:
            sftp_client.put(PUB_KEY , remote_rsa_pub)
        except Exception, e:
            """
            if the remote host did have .ssh dirctory
            """
            print e
        remote_authorized_keys = os.path.join(os.path.dirname(remote_rsa_pub), "authorized_keys")
        remote_cmd = "cat %s >> %s && echo OK" % (remote_rsa_pub, remote_authorized_keys)
        stdin, stdout, stderr = client.exec_command(remote_cmd)
        # pirnt stdin
    else:
        print("OK!")


def main():
    import sys
    username, ip = None, None
    if len(sys.argv) < 2:
        print("usage: %s <ipaddress>" % sys.argv[0])
        sys.exit(-1)
    if "@" in sys.argv[1]:
        username, ip = sys.argv[1].split("@")
    else:
        ip = sys.argv[1]
    if not username:
        username = raw_input("Input username:")
    pwd = getpass.getpass("password:")
    sync_public_key(ip, 22, username, pwd)


if __name__ == '__main__':
    main()
