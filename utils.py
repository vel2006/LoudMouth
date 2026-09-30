from os import path as filesystem, geteuid
from platform import system as platform
from scapy.all import get_if_list
from json import load, dump
from typing import Optional

# Checking to see if an interface is a valid one
def check_interface(interface: str) -> bool:
	if interface == "lo":
		print(f"Really? The lo interface?")
		return False
	print(f"Checking for interface \'{interface}\'...")
	interfaces = get_if_list()
	interfaces.remove("lo")
	if not (interface in interfaces):
		print(f"Interface \'{interface}\' is not an activated interface.")
		return False
	if not filesystem.isdir(f"/sys/class/net/{interface}/wireless"):
		print(f"Interface \'{interface}\' is not wireless.")
		return False
	return True

# Checking the NetworkManager config
def check_networkmanager() -> bool:
	if filesystem.isfile("/etc/NetworkManager/NetworkManager.conf"):
		rand_mac = True
		print("Network Manager detected, checking config file for random MAC addresses...")
		with open("/etc/NetworkManager/NetworkManager.conf", "r") as file_handle:
			for line in file_handle.readlines():
				if line.strip("\n") == "wifi.scan-rand-mac-address=no":
					rand_mac = False
			file_handle.close()
		if rand_mac:
			return False
	return True

# Checking if a path is a valid file
def check_file(path: str) -> bool:
	if not filesystem.isfile(path):
		print(f"Path \'{path}\' is not a valid file path.")
		return False
	return True

# Loading a JSON file
def load_json(file_path: str) -> Optional[dict]:
	file_data = {}
	if not check_file(file_path):
		return None
	try:
		with open(file_path, "r") as file_handle:
			file_data = load(file_handle)
			file_handle.close()
	except Exception as error:
		print(f"Encountered error when reading file \'{file_path}\': {error}")
		return None

# Writing a JSON file
def write_json(file_path: str, json_data: dict) -> bool:
	try:
		with open(file_path, "w") as file_handle:
			dump(file_handle, json_data)
			file_handle.close()
	except Exception as error:
		print(f"Encountered error when writing JSON file \'{file_path}\': {error}")
		return False
	return True

# Checking the current user's permissions
def check_perms() -> bool:
	if geteuid() == 0:
		return True
	return False

# Checking platform
def check_platform() -> bool:
	if platform.lower() == "windows":
		print("This suite of tools is designed to work with UNIX and UNIX based systems, not Windows.")
		return False
	return True

# Exiting the script
def exit_script(exit_code: int, message: str):
	print(f"\n{message}")
	exit(exit_code)

# Filtering the networks / dict to return with no copys
def filter_dict(data: dict) -> dict:
	output = {}
	for key in data:
		info_type = type(data[key])
		info = info_type()
		if info_type == list():
			for entry in data[key]:
				if entry not in info:
					info.append(entry)
		elif info_type == dict():
			info = filter_dict(data[key])
		output[key] = info
	return output
