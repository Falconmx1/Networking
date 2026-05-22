import random
import time
import sys
import os

def random_delay(base=0.1, jitter=0.3):
    """Modo sigiloso: retraso aleatorio para evitar detección"""
    time.sleep(base + random.uniform(0, jitter))

def stealth_mode_enabled():
    """Verifica si estamos en modo sigiloso por variable de entorno"""
    return os.getenv('STEALTH_MODE', 'false').lower() == 'true'

def print_banner():
    banner = """
    ╔═══════════════════════════════════════╗
    ║     🌐 NETWORKING TOOL v2.0          ║
    ║     Pentesting & Security Suite      ║
    ╚═══════════════════════════════════════╝
    """
    print(banner)

def get_platform():
    import platform
    return platform.system()
