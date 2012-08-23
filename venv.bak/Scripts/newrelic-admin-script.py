#!c:\pythondev\Boris-Frontend\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'newrelic==1.4.0.137','console_scripts','newrelic-admin'
__requires__ = 'newrelic==1.4.0.137'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('newrelic==1.4.0.137', 'console_scripts', 'newrelic-admin')()
    )
