import psutil

COMMON_SUSPICIOUS_PORTS = [21, 23, 445, 3389, 4444]

def scan_ports():
    open_ports = []

    for conn in psutil.net_connections(kind='inet'):
        if conn.status == "LISTEN" and conn.laddr:
            port = conn.laddr.port
            if port in COMMON_SUSPICIOUS_PORTS:
                open_ports.append(port)

    return open_ports