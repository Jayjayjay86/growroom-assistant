from miio.discovery import Discovery


devices = Discovery.discover_mdns()
print(devices)
