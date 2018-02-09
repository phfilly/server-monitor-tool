import paramiko
import os
import keyring
import env


def connectThePitt():
    keyfile = os.path.expanduser(env.BASTION)
    password = keyring.get_password('SSH', keyfile)
    key = paramiko.RSAKey.from_private_key_file(keyfile, password=password)
    c = paramiko.SSHClient()

    print("connecting to The Pitt...")
    c.connect(hostname=env.THEPITT_IP, username=env.BASTION_USERNAME, pkey=key)
    print("connected!")
    stdin, stdout, stderr = c.exec_command(env.FREE_MEMORY_CHECK)
    data = []
    for line in iter(stdout.readline, ""):
        print(line)
        data.append(line)
    print('finished.')
    c.close()

    return ['The Pitt', data]


def connectBastion():
    keyfile = os.path.expanduser(env.BASTION)
    password = keyring.get_password('SSH', keyfile)
    key = paramiko.RSAKey.from_private_key_file(keyfile, password=password)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print("connecting to The Pitt...")
    c.connect(hostname=env.BASTION_IP, username=env.BASTION_USERNAME, pkey=key)
    print("connected!")
    # stdin, stdout, stderr = c.exec_command(env.FREE_MEMORY_CHECK)

    data = []
    # for line in iter(stdout.readline, ""):
    #     print(line)
    #     data.append(line)
    # print('finished.')

    # stdin, stdout, stderr = c.exec_command('pitt')
    # print("stderr: ", stderr.readlines())
    # for line in iter(stdout.readline, ""):
    #     print(line)
    #     data.append(line)
    # print('finished.1')

    data = []
    stdin, stdout, stderr = c.exec_command(env.FREE_MEMORY_CHECK)
    for line in iter(stdout.readline, ""):
        print(line)
        data.append(line)
    print('finished.2')

    c.close()

    return ['The Bastion', data]
