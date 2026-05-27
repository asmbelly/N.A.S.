import os
import platform


def flush_dns():
    if platform.system().lower() == "windows":
        os.system("ipconfig /flushdns")


def restart_adapter(adapter):
    if platform.system().lower() == "windows":
        os.system(f'netsh interface set interface "{adapter}" disable')
        os.system(f'netsh interface set interface "{adapter}" enable')


def set_dns(adapter, dns):
    if platform.system().lower() == "windows":
        os.system(f'netsh interface ip set dns "{adapter}" static {dns}')