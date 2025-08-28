import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.load import load_ipdr
from src.heuristics import add_voip_flags

def main():
    df_ipdr = load_ipdr("data/ipdr.csv")
    df_flagged = add_voip_flags(df_ipdr)
    print(df_flagged)

if __name__ == "__main__":
    main()
