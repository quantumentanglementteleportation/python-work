import paramiko
from sshtunnel import SSHTunnelForwarder
from jnpr.junos import Device
from pprint import pprint

with SSHTunnelForwarder(
    # jump host IP and cred
    ('192.168.0.144', 22),
    ssh_username="sumit",
    ssh_password="redhat",
    # System C details
    remote_bind_address=('192.168.4.202', 22),
    local_bind_address=('0.0.0.0', 10022)
) as tunnel:
    client = paramiko.SSHClient()
    #client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # username and password of system C
    client.connect('127.0.0.1', 10022, username='root', password='redhat')
    # do some operations with client session
    with Device(host='127.0.0.1', port='10022', user='root', passwd='redhat') as dev:
        pprint(dev.facts['hostname'])
        pprint(dev.facts)
    stdin, stdout, stderr = client.exec_command('python --version')
    outlines = stdout.readlines()
    resp = ''.join(outlines)
    print(resp)
    print(stderr)
    #print(check)
    #client.invoke_shell
    client.close()

print('FINISH!')

