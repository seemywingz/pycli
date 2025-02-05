import socket
import os


# get ip address
def get_local_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address


def get_router_ip_address():
    if os.name == "posix":
        if os.uname().sysname == "Darwin":  # macOS
            route = os.popen("netstat -nr | grep default").read()
            router = route.split()[1]
        else:  # Linux
            route = os.popen("ip route").read()
            router = route.split("default via ")[1].split(" ")[0]
    return router
