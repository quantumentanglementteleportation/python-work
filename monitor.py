from jnpr.junos import Device
from jnpr.junos.utils.start_shell import StartShell

dev = Device(host='router1.example.net', user='user', passwd='')

with StartShell(dev) as ss:
    #ss.run('cli -c "monitor traffic interface fxp0"', this=None, timeout=15)
    ss.run('cli -c "hostname"', this=None, timeout=15)
