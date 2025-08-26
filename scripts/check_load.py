import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.load import load_cdr, load_ipdr

def main():
    print("--- CDR ---")
    df_cdr = load_cdr("data/cdr.csv")
    print(df_cdr.head())
    print("\n--- IPDR ---")
    df_ipdr = load_ipdr("data/ipdr.csv")
    print(df_ipdr.head())

if __name__ == "__main__":
    main()
