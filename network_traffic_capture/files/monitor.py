from jnpr.junos import Device
from jnpr.junos.utils.start_shell import StartShell
import sys

dev = Device(host=sys.argv[1], user=sys.argv[2], passwd=sys.argv[3])

with StartShell(dev) as ss:
	ss.run('cli -c "{0}"', this=None, timeout=sys.argv[5]).format(sys.argv[4])

#    ss.run('cli -c "monitor traffic interface ge-1/0/0 count 5 extensive write-file /tmp/ge2.pcap no-resolve layer2-headers"', this=None, timeout=600)
#    print(ss.run('cli -c "show version"', this=None, timeout=15))

