from threading import Thread, Event
from argparse import ArgumentParser
from pathlib import Path
from scapy.all import *
from time import sleep
from re import findall
from os import system
from sys import path

# Adding suite utils
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in path:
	path.insert(0, str(ROOT))
from utils import *

# Script wide variables
stop_event = Event()
interface = ""
networks = {}
path = None
save = False
show = False

# Extracting info from a 11Beacon
def extract_info(frame):
	global show
	global networks
	if frame.haslayer(Dot11Beacon):
		bssid = str(frame[Dot11].addr2)
		ssid = str(frame[Dot11Elt].info.decode())
		signal = "N/A"
		try:
			signal = frame.dBm_AntSignal
		except:
			pass
		if ssid == "":
			ssid = "N/A"
		stats = frame[Dot11Beacon].network_stats()
		channel = stats.get("channel")
		crypto = list(stats.get("crypto"))
		network_data = (bssid, signal, channel, crypto)
		if ssid in networks:
			if not network_data in networks[ssid]:
				networks[ssid].append(network_data)
		else:
			if show:
				print(f"Found Network: {ssid} | {network_data}")
			networks[ssid] = [network_data]

# Changing the channel we are listening on
def change_channel(stop_event, interface):
	channel = 1
	while not stop_event.is_set():
		system(f"iwconfig {interface} channel {channel}")
		channel = channel % 13 + 1
		sleep(0.25)

# Scanning for networks
def scan():
	global networks
	channel_thread = None
	try:
		channel_thread = Thread(target=change_channel, args=(stop_event, interface)).start()
		sniff(iface=interface, prn=extract_info)
	except:
		pass
	stop_event.set()
	if channel_thread:
		channel_thread.close()

# Filtering out duplacates within the scanned networks
def filter_scan():
	global networks
	networks = filter_dict(networks)

# Just some text because I like it
def show_welcome():
	print(" ____                                  ")
	print("/ ___|  ___ __ _ _ __  _ __   ___ _ __ ")
	print("\\___ \\ / __/ _` | '_ \\| '_ \\ / _ \\ '__|")
	print(" ___) | (_| (_| | | | | | | |  __/ |   ")
	print("|____/ \\___\\__,_|_| |_|_| |_|\\___|_|   ")
	print("A LoudMouth tool\n")

# Getting the passed arguments
def parse_args():
	global interface
	global path
	global save
	global show
	parser = ArgumentParser(
		prog="Scanner",
		usage="python3 %(prog)s [interface] [arguments]",
		epilog="It\'s in the air!"
	)
	parser.add_argument("interface", type=str, help="Interface to listen to for WiFi networks")
	parser.add_argument("--path", type=str, help="Path to a JSON file that holds data about known networks.")
	parser.add_argument("--save", action="store_true", help="Save the captured networks within a JSON file")
	parser.add_argument("--show", action="store_true", help="Display every new network found")
	arguments = parser.parse_args()
	interface = arguments.interface
	path = arguments.path
	save = arguments.save
	show = arguments.show

if __name__ == "__main__":
	show_welcome()
	parse_args()
	# Handling the passed path to a JSON file
	if path:
		if not check_file(path):
			exit_script(1, "It\'s in the air!")
		print("Loading networks...")
		output = load_json(path)
		if output:
			networks = output
		else:
			exit_script(1, "It\'s in the air!")
		print(f"Loaded {len(networks.keys())} networks!")
	# Handling the interface
	if not check_interface(interface):
		exit_script(1, "It\'s in the air!")
	# Checking if Network Manager is used and the config file disallowing randomized MAC addresses
	print("Checking if Network Manager is installed on device...")
	check_networkmanager()
	# Starting the scan
	print("Starting scan...")
	scan()
	# Saving data
	print("Ending scan...")
	filter_scan()
	if save:
		save_scan()
	exit_script(0, "It\'s in the air!")
