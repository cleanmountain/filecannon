from get_ip import get_local_ip

_host = get_local_ip()
_port = 6969
bind = f"{_host}:{_port}"
workers = 2
loglevel="warning"

_green = '\033[92m'
_nc = '\033[0m'
print(_green + f"FILECANNON IS NOW ACCESSIBLE AT http://{bind}" + _nc)
print(_green + f"FILECANNON IS NOW ACCESSIBLE AT http://{bind}" + _nc)
print(_green + f"FILECANNON IS NOW ACCESSIBLE AT http://{bind}" + _nc)