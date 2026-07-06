"""
Script to extract data from JAZIRA3001-JUN2026.csv and populate 5_Al-Jazira Bank_Import File.csv
- Clears existing data in the destination file
- Maps columns by header names
- Formats debits as negative numbers and credits as positive
"""

import csv
from pathlib import Path

def process_amount(credit, debit):
    """
    Convert Credit/Debit to signed amount:
    - Credit = positive
    - Debit = negative
    """
    try:
        credit_val = float(str(credit).strip().replace(',', '')) if credit and str(credit).strip() else 0
        debit_val = float(str(debit).strip().replace(',', '')) if debit and str(debit).strip() else 0
        
        if credit_val > 0:
            return credit_val
        elif debit_val > 0:
            return -debit_val
        else:
            return 0
    except ValueError:
        return 0

def main():
    try:
        source_file = '5_Al-Jazira Bank_Import File.csv'
        dest_file = 'JAZIRA3001-JUN2026.csv'
        output_file = '5_Al-Jazira Bank_Import File.csv'
        
        print("Reading source file: JAZIRA3001-JUN2026.csv")
        
        # Read source file
        source_rows = []
        with open(dest_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            source_rows = list(reader)
        
        print(f"Source data rows: {len(source_rows)}")
        print(f"Source headers: {source_rows[0].keys() if source_rows else 'None'}")
        
        # Destination headers
        dest_headers = ['Date', 'Description', 'Balance (SAR)']
        
        print(f"\nDestination headers: {dest_headers}")
        
        # Process and transform data
        output_rows = []
        for row in source_rows:
            if row.get('Date') and row.get('Date').strip():
                date = row.get('Date', '').strip()
                description = row.get('Description', '').strip()
                credit = row.get('Credit', '0')
                debit = row.get('Debit', '0')
                
                # Calculate signed amount (credit positive, debit negative)
                amount = process_amount(credit, debit)
                
                output_rows.append({
                    'Date': date,
                    'Description': description,
                    'Balance (SAR)': amount
                })
        
        print(f"\nProcessed data rows: {len(output_rows)}")
        print("\nFirst 5 rows of processed data:")
        for row in output_rows[:5]:
            print(f"  {row}")
        
        # Write to output file
        print(f"\nWriting to output file: {output_file}")
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=dest_headers)
            writer.writeheader()
            writer.writerows(output_rows)
        
        print(f"✓ Successfully updated: {output_file}")
        print(f"✓ Total rows written: {len(output_rows)}")
        print(f"✓ Headers: {dest_headers}")
        
    except FileNotFoundError as e:
        print(f"✗ Error: File not found - {e}")
        print("Please ensure both files are in the same directory as this script")
    except Exception as e:
        print(f"✗ Error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
