import subprocess
import platform
import re
import statistics


def ping_raw(host):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    cmd = ["ping", param, "1", host]

    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)

        time_match = re.search(r"time[=<]\s*(\d+)", out)
        loss_match = re.search(r"Lost = \d+ \((\d+)% loss\)", out)

        latency = float(time_match.group(1)) if time_match else None
        loss = int(loss_match.group(1)) if loss_match else 0

        return latency, loss

    except subprocess.CalledProcessError:
        return None, 100


def multi_ping(host, samples=5):
    latencies = []
    losses = []

    for _ in range(samples):
        lat, loss = ping_raw(host)
        if lat is not None:
            latencies.append(lat)
        losses.append(loss)

    if not latencies:
        return None, 100

    return statistics.median(latencies), max(losses)


def check_network(targets, samples=5):
    all_lat = []
    all_loss = []

    for t in targets:
        lat, loss = multi_ping(t, samples)

        if lat is not None:
            all_lat.append(lat)
        all_loss.append(loss)

    if not all_lat:
        return None, 100

    return statistics.median(all_lat), max(all_loss)