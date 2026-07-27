import ssl
import sys
import os

# =====================================================================
# WINDOWS SSL CERTIFICATE BUG WORKAROUND (MUST RUN BEFORE STREAMLIT IS IMPORTED)
# Protects against: ssl.SSLError: [ASN1: NOT_ENOUGH_DATA] during Tornado import
# Occurs when Windows Certificate Store holds an empty or third-party proxy cert
# =====================================================================
try:
    if hasattr(ssl.SSLContext, '_load_windows_store_certs'):
        orig_win_store = ssl.SSLContext._load_windows_store_certs
        def safe_win_store(self, storename, purpose):
            try:
                orig_win_store(self, storename, purpose)
            except Exception:
                pass
        ssl.SSLContext._load_windows_store_certs = safe_win_store

    orig_load_default = ssl.SSLContext.load_default_certs
    def safe_load_default(self, purpose=ssl.Purpose.SERVER_AUTH):
        try:
            orig_load_default(self, purpose)
        except Exception:
            pass
    ssl.SSLContext.load_default_certs = safe_load_default
except Exception:
    pass

# NOW it is guaranteed 100% safe to import Streamlit and Tornado!
import streamlit.web.cli as stcli

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", "app.py", "--server.port", "8502"]
    sys.exit(stcli.main())
