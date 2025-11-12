# noinspection PyUnusedImports
from pywizlight import wizlight, PilotBuilder, PilotParser, discovery
# noinspection PyUnusedImports
from colorama import Fore, Back, Style
import winreg as wr
import ipaddress
import asyncio
import netifaces
faces = netifaces.interfaces()
import logging

action_logger = logging.getLogger(__name__)
fh = logging.FileHandler('commands/command_logs/connection.log', encoding='utf-8')
fmt = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
fh.setFormatter(fmt)
action_logger.propagate = False
logging.basicConfig(handlers=[fh], level=logging.DEBUG)


# noinspection PyUnusedLocal
def get_connection_name_from_guid(iface_guids):
    iface_names = ['(unknown)' for i in range(len(iface_guids))]
    reg = wr.ConnectRegistry(None, wr.HKEY_LOCAL_MACHINE)
    reg_key = wr.OpenKey(reg, r'SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}')
    for i in range(len(iface_guids)):
        try:
            reg_subkey = wr.OpenKey(reg_key, iface_guids[i] + r'\Connection')
            iface_names[i] = wr.QueryValueEx(reg_subkey, 'Name')[0]
        except FileNotFoundError:
            print(f"Interface {iface_guids[i]} not found.")
            pass
    return iface_names

lol = get_connection_name_from_guid(faces)
print(lol)

def get_if_ip(iface):
    inf_ips = []
    for inf in iface:
        try:
            inf_ips.append(str(ipaddress.ip_network(netifaces.ifaddresses(inf)[netifaces.AF_INET][0]['addr'] + "/24", strict=False).broadcast_address))
            action_logger.debug(f"interface, {inf}, has IP address, {inf_ips[-1]}")
        except KeyError:
            action_logger.debug(f"Interface {inf} has no IP address to be found")
            pass
    return inf_ips


list_of_ips = get_if_ip(faces)
print(list_of_ips)

async def get_bulb_ip():
    ips = []
    for ip_if in list_of_ips:
        discovery_info = await discovery.discover_lights(broadcast_space=ip_if)
        if discovery_info:
            for bulb in discovery_info:
                print(Fore.GREEN + "Found bulb at IP address: " + str(bulb.ip) + Style.RESET_ALL)
                action_logger.debug(f"Found bulb at IP address: {bulb.ip}")
                ips.append(str(bulb.ip))
            break
        elif not discovery_info:
            print(Fore.RED + "No bulbs found in the network. Please ensure that the bulb is powered on and connected to the same network as this device." + Style.RESET_ALL)
            action_logger.debug("No bulbs found in the network.")


    return ips

def get_ip():
    ipss = asyncio.run(get_bulb_ip())
    return ipss

ip = get_ip()

async def bulb_config():  # Connects to the bulb and puts configuration into a file
    bulb = wizlight(ip[0])
    bulbconf = await bulb.getBulbConfig()
    with open("../bulbconf.txt", "w") as f:
        f.write(str(bulbconf))
    return bulb


async def turn_on(): # Turns on the bulb if it is off
    bulb_on = await bulb_config()
    state_light = await bulb_on.updateState()
    state = state_light.get_state()

    valid = False
    if state:  # Checks if the bulb is already on
        valid = False
    elif not state: # If the bulb is off, it turns on
        await bulb_on.turn_on(PilotBuilder(brightness=255))
        valid = True

    return valid

async def turn_off():
    bulb_off = await bulb_config()
    bulb_state = await bulb_off.updateState()
    is_off = bulb_state.get_state()
    if is_off:
        await bulb_off.turn_off()
    elif not is_off:
        pass
    return is_off

async def get_state():
    bulb = await bulb_config()
    bulb_state = await bulb.updateState()
    state = bulb_state.get_state()
    print(state)

async def green():
    bulb = await bulb_config()
    state = await bulb.updateState()
    is_green = state.get_rgb()
    if is_green == (0, 255, 0):
        valid = False
    else:
        await bulb.turn_on(PilotBuilder(rgb=(0,255,0)))
        valid = True
    return valid


async def red():
    bulb = await bulb_config()
    state = await bulb.updateState()
    is_red = state.get_rgb()
    if is_red == (255, 0, 0):
        valid = False
    else:
        valid = True
        await bulb.turn_on(PilotBuilder(rgb=(255,0,0)))
    return valid


async def blue():
    bulb = await bulb_config()
    state = await bulb.updateState()
    is_blue = state.get_rgb()
    if is_blue == (0, 0, 255):
        valid = False
    else:
        valid = True
        await bulb.turn_on(PilotBuilder(rgb=(0,0,255)))
    return valid

async def custom_color(r, g, b):
    bulb = await bulb_config()
    state = await bulb.updateState()
    is_color = state.get_rgb()
    valid = bool
    if is_color == (r,g,b):
        valid = False
    elif is_color != (r, g, b):
        await bulb.turn_on(PilotBuilder(rgb=(r, g, b)))
        valid = True
    return valid


if __name__ == "__main__":
    lol = asyncio.run(get_bulb_ip())
    print(lol)
