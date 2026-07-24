import ssl
import sys

# --- FIX FOR WINDOWS SSL CERTIFICATE CORRUPTION ---
original_load_default_certs = ssl.SSLContext.load_default_certs

def patched_load_default_certs(self, purpose=ssl.Purpose.SERVER_AUTH):
    try:
        original_load_default_certs(self, purpose)
    except ssl.SSLError as e:
        print(f"🔧 Safely bypassed Windows SSL Certificate Error: {e}")
        pass

ssl.SSLContext.load_default_certs = patched_load_default_certs
# --------------------------------------------------

# IMPORTANT: We must import Streamlit AFTER the patch is applied above!
import streamlit.web.cli as stcli

if __name__ == '__main__':
    print("🚀 Launching ClearSight V5 Engine with SSL bypass...")
    sys.argv = ["streamlit", "run", "app.py"]
    sys.exit(stcli.main())
