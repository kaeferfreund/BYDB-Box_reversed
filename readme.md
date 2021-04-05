# This is a repo about reverse engineering the new Fronius GEN24 Inverters to attach a DIY HV Battery

* Sofware is supplied as .swe file - just a zip file that can be unpacked
* Processor sees to be an imx6sx Arm® Quad-/Dual-Core Cortex A53 CPU up to 1.5 GHz, integrated Cortex M4
* RootFS seems to be located in rootfs.ubifs file - signed unfortunately

# How can I help?
We are currently looking for people that have a BYD battery AND a GEN24 on hand. We are shipping logging devices with premade cables at our own cost to sniff RS485 communication between GEN24 and BYD batteries, so that we can reverse engineer and immitate the protocol.

IF you have both, GEN24 + BYD we would be really happy to generate a logfile.

# How does the logger work?
Its a simple RS485 to USB converter. We are simply loggin the raw serial-data with timestamps added.

# Supporting Links
* https://keith-koep.com/en/products/products-trizeps/trizeps-viii-imx8-features/?gclid=CjwKCAjw-5v7BRAmEiwAJ3DpuPQ6A34wcfwYbqatG6AUj-NO5naHUnLqs9uFIsSlAf9oZhX7sAYQpxoCZ70QAvD_BwE
* https://pjankows.blogspot.com/2012/01/how-to-mount-ubi-image.html
* https://seeklinwin.wordpress.com/2017/05/11/simulate-ubifs-on-pc/

# Fronius Links
* https://www.fronius.com/~/downloads/Solar%20Energy/Datasheets/SE_DS_Fronius_Symo_GEN24_Plus_EN.pdf
* https://www.fronius.com/~/downloads/Solar%20Energy/Quick%20Guides/SE_QG_Fronius_Symo_GEN24_Plus_-_System_configurati_MULTI.pdf
* https://www.fronius.com/~/downloads/Solar%20Energy/Firmware/SE_FW_Fronius_Solar.update_Symo_GEN24_Plus_1.9.7-0_DE_EN.zip

# BYD Stuff
1. BYD LAN IP 192.168.23.244
2. BYD WiFi IP 192.168.16.254

## BYD Accounts
```
Installer:          BYDB-Box
Service Partner:    B-Box2EFT
Inverter Partner:   B-Box2inv
Admin:              BYD#Premium*2020
```
