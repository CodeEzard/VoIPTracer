"""Small script to verify `src.schemas` can be imported and models instantiated.

Run with (Git Bash on Windows):

py -3 -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
python scripts/check_schemas.py
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import datetime, timedelta


def main():
    try:
        from src.schemas import CDR, IPDR
    except Exception as e:
        print('Failed to import src.schemas:', type(e).__name__, e)
        raise

    now = datetime.utcnow()
    c = CDR(subscriber='A', called='B', call_type='VOICE',
            start_time=now.isoformat(), end_time=(now+timedelta(seconds=30)).isoformat())
    print('CDR OK:', c.dict())

    ip = IPDR(subscriber='A', destination_ip='203.0.113.5', protocol='udp', dst_port=5060,
              start_time=now.isoformat(), end_time=(now+timedelta(seconds=25)).isoformat())
    print('IPDR OK:', ip.dict())


if __name__ == '__main__':
    main()
