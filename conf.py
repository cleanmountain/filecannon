from get_ip import get_local_ip

_host = get_local_ip()
_port = 6969
bind = f"{_host}:{_port}"
workers = 2
loglevel = "warning"