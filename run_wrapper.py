import sys
import ssl

# --- WINDOWS SSL CERTIFICATE STORE BUG FIX ---
# Traps and neutralizes "ssl.SSLError: [ASN1: NOT_ENOUGH_DATA]" caused by corrupted third-party root certs in Windows
if hasattr(ssl.SSLContext, '_load_windows_store_certs'):
    _old_load_win_certs = ssl.SSLContext._load_windows_store_certs
    def safe_load_win_certs(self, storename, purpose):
        try:
            _old_load_win_certs(self, storename, purpose)
        except Exception:
            pass
    ssl.SSLContext._load_windows_store_certs = safe_load_win_certs

_old_load_default_certs = ssl.SSLContext.load_default_certs
def safe_load_default_certs(self, purpose=ssl.Purpose.SERVER_AUTH):
    try:
        _old_load_default_certs(self, purpose)
    except Exception:
        pass
ssl.SSLContext.load_default_certs = safe_load_default_certs

_old_create_default_context = ssl.create_default_context
def safe_create_default_context(purpose=ssl.Purpose.SERVER_AUTH, *, cafile=None, capath=None, cadata=None):
    try:
        return _old_create_default_context(purpose=purpose, cafile=cafile, capath=capath, cadata=cadata)
    except Exception:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT if purpose == ssl.Purpose.SERVER_AUTH else ssl.PROTOCOL_TLS_SERVER)
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx

ssl.create_default_context = safe_create_default_context
try:
    ssl._create_default_https_context = safe_create_default_context
except AttributeError:
    pass
# ---------------------------------------------

from streamlit.web.cli import main

if __name__ == '__main__':
    # Launch Streamlit securely with SSL patch active on port 8502
    sys.argv = ["streamlit", "run", "app.py", "--server.port", "8502", "--server.headless", "false"]
    sys.exit(main())
