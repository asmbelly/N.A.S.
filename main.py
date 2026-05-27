import time
import json
import os

from monitor import check_network
from dns import benchmark_dns
from wifi import get_wifi_signal
from fixer import flush_dns, restart_adapter, set_dns


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def print_ui(latency, loss, signal, status, dns_name):
    print("🌐 Network Optimizer v3")
    print("-" * 45)
    print(f"📶 Ping: {latency:.2f} ms" if latency else "📶 Ping: N/A")
    print(f"📡 Packet Loss: {loss}%")
    print(f"📶 WiFi Signal: {signal if signal else 'Unknown'}%")
    print(f"🧠 Status: {status}")
    print(f"⚙️ DNS: {dns_name}")
    print("-" * 45)


def avg_update(old, new):
    return new if old is None else (old * 0.1 + new * 0.9)


def main():
    with open("config.json", "r") as f:
        cfg = json.load(f)

    targets = cfg["ping_targets"]
    samples = cfg["samples_per_target"]
    interval = cfg["check_interval_seconds"]
    adapter = cfg["wifi_adapter_name"]
    dns_servers = cfg["dns_servers"]
    threshold_mult = cfg["latency_threshold_multiplier"]

    baseline = None
    current_dns = None

    while True:
        clear()

        latency_loss = check_network(targets, samples)
        signal = get_wifi_signal()

        if latency_loss:
            latency, loss = latency_loss
        else:
            latency, loss = None, 100

        best = benchmark_dns(dns_servers, 2)

        if best:
            dns_name, dns_ip, _ = best

            if current_dns != dns_name:
                set_dns(adapter, dns_ip)
                current_dns = dns_name

        if latency:
            baseline = latency if baseline is None else avg_update(baseline, latency)

        threshold = baseline * threshold_mult if baseline else 120

        status = "STABLE"

        if signal and signal < 50:
            status = "WEAK WIFI → RESTART ADAPTER"
            restart_adapter(adapter)

        elif loss > 30:
            status = "PACKET LOSS → FLUSH DNS"
            flush_dns()

        elif latency is None:
            status = "DOWN → FLUSH DNS"
            flush_dns()

        elif latency > threshold:
            status = "HIGH LATENCY → OPTIMIZING"
            flush_dns()

        print_ui(latency, loss, signal, status, current_dns or "unknown")

        time.sleep(interval)


if __name__ == "__main__":
    main()