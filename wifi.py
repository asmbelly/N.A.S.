import subprocess
import re


def get_wifi_signal():
    try:
        out = subprocess.check_output(
            ["netsh", "wlan", "show", "interfaces"],
            text=True
        )

        match = re.search(r"Signal\s*:\s*(\d+)%", out)
        return int(match.group(1)) if match else None

    except Exception:
        return None