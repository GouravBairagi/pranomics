import os
import urllib.request
import time
import hashlib
from pathlib import Path


# =====================================================
# DOWNLOAD WITH PROGRESS BAR
# =====================================================
def download_file(url, dest_path, chunk_size=8192):
    """
    Downloads a file with progress display.
    Works for large bioinformatics files (Conda, FASTQ tools, etc.)
    """

    dest_path = Path(dest_path)
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with urllib.request.urlopen(url) as response:
            total_size = response.getheader("Content-Length")

            if total_size:
                total_size = int(total_size)

            downloaded = 0
            start_time = time.time()

            with open(dest_path, "wb") as f:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break

                    f.write(chunk)
                    downloaded += len(chunk)

                    _print_progress(downloaded, total_size, start_time)

        print(f"\n✔ Download complete: {dest_path}")
        return str(dest_path)

    except Exception as e:
        print(f"\n❌ Download failed: {e}")
        raise


# =====================================================
# PROGRESS DISPLAY
# =====================================================
def _print_progress(downloaded, total, start_time):
    """
    Simple CLI progress indicator (no external libs)
    """

    if not total:
        # unknown size
        print(f"\r⬇ Downloaded: {downloaded/1024/1024:.2f} MB", end="")
        return

    percent = (downloaded / total) * 100
    elapsed = time.time() - start_time
    speed = downloaded / (1024 * elapsed + 1e-9)

    bar_length = 30
    filled = int(bar_length * downloaded // total)
    bar = "█" * filled + "-" * (bar_length - filled)

    print(
        f"\r⬇ [{bar}] {percent:.1f}% "
        f"{downloaded/1024/1024:.1f}/{total/1024/1024:.1f} MB "
        f"({speed:.1f} KB/s)",
        end="",
    )


# =====================================================
# RETRY DOWNLOAD (IMPORTANT FOR CONDA)
# =====================================================
def download_with_retry(url, dest_path, retries=3, delay=3):
    """
    Reliable download wrapper with retry logic
    """

    last_error = None

    for attempt in range(1, retries + 1):
        try:
            return download_file(url, dest_path)

        except Exception as e:
            last_error = e
            print(f"⚠ Retry {attempt}/{retries} failed")

            time.sleep(delay * attempt)

    raise RuntimeError(f"Failed after retries: {last_error}")


# =====================================================
# SHA256 VERIFICATION
# =====================================================
def verify_sha256(file_path, expected_hash):
    """
    Validates file integrity after download
    """

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            sha256.update(data)

    computed = sha256.hexdigest()

    if computed != expected_hash:
        raise ValueError(
            f"Hash mismatch!\nExpected: {expected_hash}\nGot: {computed}"
        )

    return True


# =====================================================
# SAFE DOWNLOAD WRAPPER
# =====================================================
def safe_download(url, dest_path, sha256=None):
    """
    Full safe pipeline:
    - download
    - retry
    - verify
    """

    path = download_with_retry(url, dest_path)

    if sha256:
        print("\n🔐 Verifying file integrity...")
        verify_sha256(path, sha256)
        print("✔ File verified successfully")

    return path
    