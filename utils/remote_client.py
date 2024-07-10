#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/3 11:21
# @Author  : LYF
# @File    : remote_client.py
# @Description : ssh\sftp 远程连接工具
import os
import stat
from paramiko import SSHClient, SFTPClient, Transport, AutoAddPolicy, WarningPolicy, RejectPolicy


class SSH(object):
    def __init__(self, host, port=22, user=None, passwd=None, **kwargs):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.config = kwargs
        self.client = SSHClient()

        self.login()

    def login(self, known_host_path=None):
        # 加载本地公钥校验 默认地址 ~/.ssh/known_host
        self.client.load_system_host_keys(filename=known_host_path)
        # 设置:远程主机没有本地密钥时的处理策略
        # AutoAddPolicy 自动添加密钥不询问
        # WarningPolicy 提示为新连接但连接
        # RejectPolicy 自动拒绝未知连接 只依赖load_system_host_keys的配置 【默认】
        self.client.set_missing_host_key_policy(WarningPolicy)
        self.client.connect(self.host, self.port, self.user, self.passwd)
        print("ssh {} success".format(self.host))

    def close(self):
        self.client.close()
        print("{} closed".format(self.host))

    def exec_command(self, command, real_output=False):
        stdin, stdout, stderr = self.client.exec_command('dir')

        # True 实时输出命令执行结果 / False 命令执行完毕再输出
        if real_output:
            for line in stdout.read().splitlines():
                print(line)
        else:
            print(stdout.read())

        print("command [{}] execution completed".format(command))


class SFTP(object):
    def __init__(self, host, port=22, user=None, passwd=None, **kwargs):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.config = kwargs
        self.transport = Transport((host, port))
        self.client = None
        self.login()

    def login(self):
        if self.passwd is not None:
            self.transport.connect(username=self.user, password=self.passwd)
        else:
            raise Exception("Password or private key must be provided!")
        self.client = SFTPClient.from_transport(self.transport)

    def close(self):
        self.client.close()
        print("{} closed".format(self.host))

    def go_remote_dir(self, remote_dir, auto_create=True):
        try:
            self.client.chdir(remote_dir)
            print('切换远程路径[{}]成功'.format(remote_dir))
        except Exception as e:
            print('切换远程路径[{}]失败:{}'.format(remote_dir, e.args))
            if auto_create:
                try:
                    self.client.mkdir(remote_dir)
                    self.client.chdir(remote_dir)
                    # self.client.chmod(remote_dir, 0o777)
                    print('远程路径不存在,自动创建并切换成功')
                except Exception as e:
                    raise Exception(e.args)
            else:
                raise Exception(e.args)

    def __put(self, local_file, remote_file):
        try:
            self.client.put(local_file, remote_file)
            # self.client.chmod(remote_file, 0o777)  # 777权限 windows不支持权限设置
        except Exception as e:
            print("[PUT] {} ==> {} failed".format(local_file, remote_file))
            raise Exception(e.args)
        else:
            print("[PUT] {} ==> {} ok".format(local_file, remote_file))

    # 上传文件
    def put(self, local_dir, files=None, remote_dir=None, flag_file='put_ok'):
        if not files:
            print('未指定上传文件列表,将上传路径[{}]下所有文件(不含子文件夹)'.format(local_dir))
            files = [f for f in os.listdir(local_dir) if os.path.isfile(os.path.join(local_dir, f))]
            print("上传文件清单:{}".format(files))
        if not remote_dir:
            remote_dir = './'

        # 拼接文件路径 路径需以 / 结尾
        if local_dir:
            local_dir = local_dir if local_dir.endswith('/') else local_dir + '/'
            local_files = [os.path.join(local_dir, f) for f in files]
        if remote_dir:
            remote_dir = remote_dir if remote_dir.endswith('/') else remote_dir + '/'
            remote_files = [os.path.join(remote_dir, f) for f in files]

        # 本地文件路径校验
        if not all([os.path.isfile(f) for f in local_files]):
            raise Exception("local file {0} not exist".format(local_files))

        # 切换路径
        self.go_remote_dir(remote_dir)
        for index, f in enumerate(files):
            self.__put(local_files[index], remote_files[index])

        # put完成后生成标志文件
        flag_dir = os.path.join(remote_dir, flag_file)
        with self.client.open(flag_dir, 'w') as f:
            print('create put complete flag: {0}'.format(flag_dir))

    def __get(self, remote_file, local_file):
        try:
            self.client.get(remote_file, local_file)
            # self.client.chmod(local_file, 0o777)  # 777权限 windows不支持权限设置
        except Exception as e:
            print("[GET] {} ==> {} failed".format(remote_file, local_file))
            raise Exception(e.args)
        else:
            print("[GET] {} ==> {} ok".format(remote_file, local_file))

    # 下载文件 FIXME
    def get(self, remote_dir, files=None, local_dir=None, flag_file='get_ok'):
        if not files:
            print('未指定下载文件列表,将下载路径[{}]下所有文件(不含子文件夹)'.format(remote_dir))
            files = [f for f in self.client.listdir(remote_dir) if not stat.S_ISDIR(self.client.stat(os.path.join(remote_dir, f)).st_mode)]
            print("下载文件清单:{}".format(files))
            # raise Exception('get files must be specified')
        if not local_dir:
            local_dir = './'

        # 拼接文件路径 路径需以 / 结尾
        if local_dir:
            local_dir = local_dir if local_dir.endswith('/') else local_dir + '/'
            local_files = [os.path.join(local_dir, f) for f in files]
        if remote_dir:
            remote_dir = remote_dir if remote_dir.endswith('/') else remote_dir + '/'
            remote_files = [os.path.join(remote_dir, f) for f in files]

        # 远程文件路径校验
        err_files = []
        for f in remote_files:
            try:
                self.client.stat(f)
            except IOError:
                err_files.append(f)
        if err_files:
            raise Exception("remote file {0} not exist".format(err_files))

        for index, f in enumerate(files):
            self.__get(remote_files[index], local_files[index])

        # get完成后本地端生成标志文件
        flag_dir = os.path.join(local_dir, flag_file)
        with open(flag_dir, 'w') as f:
            print('create get complete flag: {0}'.format(flag_dir))


if __name__ == '__main__':
    # ssh = SSH('192.168.2.136', user='ewan', passwd='123456')
    # ssh.exec_command('pwd')
    # ssh.close()

    # sftp = SFTP('192.168.2.136', user='ewan', passwd='123456')
    # sftp.put("e:/pywork/tmp/")
    # sftp.get('/home/ewan/', ['std_data_model_tpl.xls'])
    # sftp.get('/home/ewan/', local_dir='G:/tmp/')
    # sftp.close()
    pass
