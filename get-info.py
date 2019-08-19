import platform
from jnpr.junos import Device
from pprint import pprint

#with open('result.txt', 'a') as outfile:
#    outfile.write(str(platform.uname()))

print(platform.uname())


with Device(host='router1.example.net') as dev:
    pprint(dev.facts['hostname'])
    pprint(dev.facts)

