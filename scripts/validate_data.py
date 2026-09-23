#!/usr/bin/env python3
"""
Data validator script for akademik-feodalizm datasets.
Validates JSON schemas and CSV row integrity.
"""
import os
import json
import csv
import sys

# Ensure UTF-8 output on Windows consoles
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def validate_json_file(file_path):
    print(f"[*] Validating JSON: {file_path}...")
    if not os.path.exists(file_path):
        print(f"[!] Error: File not found: {file_path}")
        return False
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list) or len(data) == 0:
            print(f"[!] Error: JSON root must be a non-empty list.")
            return False
        required_keys = ["id", "ulke", "model", "hukuki_statu", "guc_asimetrisi", "denetim_ve_sikayet", "tahliye_vanalari"]
        for idx, item in enumerate(data):
            for k in required_keys:
                if k not in item:
                    print(f"[!] Error in item {idx}: Missing key '{k}'")
                    return False
        print(f"[+] JSON valid ({len(data)} countries parsed successfully).")
        return True
    except Exception as e:
        print(f"[!] JSON Error: {e}")
        return False

def validate_csv_file(file_path, expected_columns=None):
    print(f"[*] Validating CSV: {file_path}...")
    if not os.path.exists(file_path):
        print(f"[!] Error: File not found: {file_path}")
        return False
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            if expected_columns and len(header) != expected_columns:
                print(f"[!] Header mismatch: expected {expected_columns} columns, got {len(header)}")
                return False
            row_count = 0
            for row in reader:
                if not row or all(c.strip() == "" for c in row):
                    continue
                if len(row) != len(header):
                    print(f"[!] Row length mismatch at row {row_count+1}")
                    return False
                row_count += 1
        print(f"[+] CSV valid ({row_count} data rows).")
        return True
    except Exception as e:
        print(f"[!] CSV Error: {e}")
        return False

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    veriler_dir = os.path.join(base_dir, "veriler")
    
    json_path = os.path.join(veriler_dir, "ulke-akademik-mevzuatlari.json")
    csv1_path = os.path.join(veriler_dir, "sorusturma-sonuclari-ve-ihrac-oranlari.csv")
    csv2_path = os.path.join(veriler_dir, "ogrenci-terk-ve-af-istatistikleri.csv")
    csv3_path = os.path.join(veriler_dir, "universite-akademik-mobbing-ve-intihar-kronolojisi.csv")
    
    success = True
    success &= validate_json_file(json_path)
    success &= validate_csv_file(csv1_path, 9)
    success &= validate_csv_file(csv2_path, 8)
    if os.path.exists(csv3_path):
        success &= validate_csv_file(csv3_path, 7)
    
    if not success:
        print("\n[FAIL] Validation FAILED.")
        sys.exit(1)
    else:
        print("\n[SUCCESS] All datasets validated successfully!")

if __name__ == "__main__":
    main()
