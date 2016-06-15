# This source file is part of the Phogo project
# https://github.com/CRM-UAM/Phogo
# Released under the GNU General Public License Version 3
# Club de Robotica-Mecatronica, Universidad Autonoma de Madrid, Spain

import bluetooth

print("Scanning for nearby bluetooth devices...")
nearby_devices = bluetooth.discover_devices(duration=3)

if len(nearby_devices) > 0:
    print("Done! Mac addresses of nearby devices:")
    print(nearby_devices)
else:
    print("Oops! No devices were found :-(")
