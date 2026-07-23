import os
import sys
import ssl
import certifi

# Fix for Windows SSL "ASN1: NOT_ENOUGH_DATA" crash
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

# Monkeypatch SSL to prevent Windows Store from crashing Tornado/Streamlit
_original_load_default_certs = ssl.SSLContext.load_default_certs
def safe_load_default_certs(self, purpose=ssl.Purpose.SERVER_AUTH):
    try:
        self.load_verify_locations(cafile=certifi.where())
    except Exception:
        pass
ssl.SSLContext.load_default_certs = safe_load_default_certs

from streamlit.web.cli import main

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", "app.py"]
    sys.exit(main())
