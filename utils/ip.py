#!/usr/bin/env pyenv exec python3
# File: ip.py
import argparse
import socket
import os
import subprocess
import ipaddress


def get_local_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address


def get_router_ip():
    if os.name == "posix":
        if os.uname().sysname == "Darwin":  # macOS
            route = os.popen("netstat -nr | grep default").read()
            router = route.split()[1]
        else:  # Linux
            route = os.popen("ip route").read()
            router = route.split("default via ")[1].split(" ")[0]
    return router


def get_network_cidr():
    """Determine the network CIDR based on local IP and subnet mask."""
    ip = get_local_ip()

    if os.name == "posix":
        if os.uname().sysname == "Darwin":
            # Get netmask from ifconfig (macOS returns hex format)
            mask_hex = (
                os.popen(f"ifconfig | grep {ip} | awk '{{print $4}}'")
                .read()
                .strip()
            )

            try:
                # Convert hex mask (e.g., 0xffff0000) to dotted decimal
                mask_int = int(mask_hex, 16)
                mask = socket.inet_ntoa(mask_int.to_bytes(4, "big"))
            except ValueError:
                raise ValueError(f"Invalid netmask format: {mask_hex}")

        else:  # Linux
            mask = (
                os.popen(f"ip -o -f inet addr show | grep {ip}")
                .read()
                .split()[3]
            )

    else:
        mask = "255.255.255.0"  # Default fallback

    # Convert to CIDR notation
    net = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
    return str(net)


def scan_hosts():
    """Perform a network scan using `ping`."""
    network_cidr = get_network_cidr()
    print(f"\nScanning network: {network_cidr}")

    active_hosts = []
    for ip in ipaddress.IPv4Network(network_cidr, strict=False):
        ip = str(ip)
        if ip == get_local_ip():
            continue  # Skip self

        # Platform-specific ping command
        if os.name == "nt":
            cmd = ["ping", "-n", "1", "-w", "500", ip]
        else:
            cmd = ["ping", "-c", "1", "-W", "1", ip]

        try:
            output = subprocess.run(
                cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            if output.returncode == 0:
                active_hosts.append(ip)
                print(f"Host {ip} is online")
        except Exception as e:
            print(f"Error scanning {ip}: {e}")

    return active_hosts
