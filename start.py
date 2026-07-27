import ssl
import sys
import os
import streamlit.web.cli as stcli

# =====================================================================
# WINDOWS SSL CERTIFICATE BUG WORKAROUND
# Protects against: ssl.SSLError: [ASN1: NOT_ENOUGH_DATA] during Tornado import
# Occurs when Windows Certificate Store holds an empty or third-party proxy cert
# =====================================================================
if hasattr(ssl.SSLContext, '_load_windows_store_certs'):
    orig_load_certs = ssl.SSLContext._load_windows_store_certs
    def safe_load_windows_store_certs(self, storename, purpose):
        try:
            orig_load_certs(self, storename, purpose)
        except Exception as e:
            # Skip malformed/empty ASN.1 certificates in Windows memory without crashing Tornado
            pass
    ssl.SSLContext._load_windows_store_certs = safe_load_windows_store_certs

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", "app.py", "--server.port", "8502"]
    sys.exit(stcli.main())
