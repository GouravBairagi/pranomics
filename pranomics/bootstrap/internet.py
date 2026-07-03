import urllib.request
import socket
import time


# =====================================================
# BASIC INTERNET CHECK (FAST)
# =====================================================
def _check_url(url, timeout=3):
    """
    Internal helper: tries to open a URL
    """
    try:
        urllib.request.urlopen(url, timeout=timeout)
        return True
    except Exception:
        return False


# =====================================================
# MULTI-ENDPOINT INTERNET CHECK (ROBUST)
# =====================================================
def internet_available(timeout=3):
    """
    Checks internet using multiple reliable endpoints.
    Returns True if ANY endpoint works.
    """

    endpoints = [
        "https://repo.anaconda.com",
        "https://pypi.org",
        "https://www.google.com",
    ]

    for url in endpoints:
        if _check_url(url, timeout):
            return True

    return False


# =====================================================
# DEEP NETWORK CHECK (DNS + SOCKET TEST)
# =====================================================
def deep_network_check():
    """
    More strict check using DNS resolution + socket connection
    Useful for servers where HTTP is blocked but network exists
    """

    try:
        host = "8.8.8.8"
        socket.create_connection((host, 53), timeout=3)
        return True
    except Exception:
        return False


# =====================================================
# WAIT FOR INTERNET (USEFUL IN BOOTSTRAP)
# =====================================================
def wait_for_internet(retries=5, delay=3):
    """
    Waits until internet becomes available
    Useful during Conda installation bootstrap
    """

    for i in range(retries):
        if internet_available():
            return True

        print(f"🌐 No internet... retrying ({i+1}/{retries})")
        time.sleep(delay)

    return False


# =====================================================
# NETWORK STATUS SUMMARY
# =====================================================
def network_status():
    """
    Returns a diagnostic dictionary
    """

    return {
        "internet": internet_available(),
        "dns_socket": deep_network_check(),
    }
    