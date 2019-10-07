from jnpr.junos import Device
from jnpr.junos.utils.scp import SCP

dev = Device(host=sys.argv[1], user=sys.argv[2], passwd=sys.argv[3])
with SCP(dev) as scp:
    scp.get(sys.argv[4], local_path=sys.argv[5])