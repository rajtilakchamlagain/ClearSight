import sys
import ssl

# Monkey patch the SSL module to bypass the Windows Certificate Store bug
# that causes "ssl.SSLError: [ASN1: NOT_ENOUGH_DATA] not enough data"
if hasattr(ssl.SSLContext, '_load_windows_store_certs'):
    original_load = ssl.SSLContext._load_windows_store_certs
    def safe_load(self, storename, purpose):
        try:
            original_load(self, storename, purpose)
        except ssl.SSLError:
            pass
    ssl.SSLContext._load_windows_store_certs = safe_load

# Now start Streamlit normally
from streamlit.web.cli import main

if __name__ == '__main__':
    # streamlit expects 'streamlit run app.py' in sys.argv
    # If run as 'python run_wrapper.py app.py', sys.argv is ['run_wrapper.py', 'app.py']
    # We change it to ['streamlit', 'run', 'app.py']
    sys.argv = ["streamlit", "run", "app.py"]
    sys.exit(main())
