import ssl
import sys

# Windows SSL Bug Fix for Tornado/Streamlit
# This bypasses the corrupted Windows Certificate Store error: [ASN1: NOT_ENOUGH_DATA]
try:
    def _mock_load_windows_store_certs(self, storename, purpose):
        pass
    ssl.SSLContext._load_windows_store_certs = _mock_load_windows_store_certs
except Exception:
    pass

# Now safely import and run Streamlit
from streamlit.web.cli import main

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", "app.py"]
    sys.exit(main())
