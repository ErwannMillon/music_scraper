from ppadb.client import Client as AdbClient
# Default is "127.0.0.1" and 5037
client = AdbClient(host="127.0.0.1", port=5037)
device = client.device("19291FDF600G8R")
# device.shell("echo hi")
result = device.screencap()
device.pull("/sdcard/Videoder/Klangkarussell - Alarm (Heldenklang) ( 128kbps ).m4a", "Klangkarussell - Alarm (Heldenklang) ( 128kbps ).m4a")