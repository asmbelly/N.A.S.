import subprocess
import platform
import statistics
import re


def ping(host):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    cmd = ["ping", param, "1", host]

    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
        match = re.search(r"time[=<]\s*(\d+)", out)

        if match:
            return float(match.group(1))

        return None

    except subprocess.CalledProcessError:
        return None


def benchmark_dns(dns_servers, samples=3):
    results = {}

    for name, ip in dns_servers.items():
        times = []

        for _ in range(samples):
            r = ping(ip)
            if r is not None:
                times.append(r)

        if times:
            results[name] = statistics.mean(times)

    if not results:
        return None

    best = min(results, key=results.get)
    return best, dns_servers[best], results