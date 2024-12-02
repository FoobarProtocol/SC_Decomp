#!/usr/bin/env python3

import argparse
import csv
import os
from pathlib import Path

def split_csv(input_file_path, row_limit, output_dir=None):
    input_path = Path(input_file_path)
    if not input_path.is_file() or not input_path.suffix == '.csv':
        print("Error: Invalid input file.")
        return False

    output_path = Path(output_dir) if output_dir else None
    if output_path and not output_path.is_dir():
        print("Error: Invalid output directory.")
        return

    output_file_count = 0
    rows_written = 0
    current_output = None
    csv_writer = None

    with input_path.open() as input_file:
        csv_reader = csv.reader(input_file)
        headers = next(csv_reader, None)

        if headers is None:
            print("Error: Input file is empty.")
            return

        total_rows = sum(1 for row in csv_reader)
        input_file.seek(0)
        next(csv_reader)

        is_percentage = row_limit.endswith('%')
        if is_percentage:
            percentage = int(row_limit.rstrip('%'))
            if percentage > 100:
                print("Error: Percentage cannot exceed 100%")
                return
            row_limit = int((percentage / 100) * total_rows)
        else:
            row_limit = int(row_limit)

        if row_limit > total_rows:
            print(f"Error: Number of rows specified ({row_limit}) exceeds total number of rows ({total_rows})")
            return

        for row in csv_reader:
            if rows_written % row_limit == 0:
                if current_output:
                    current_output.close()
                output_file_count += 1
                output_filename = f"{input_path.stem}_part{output_file_count}.csv"
                output_path = output_dir / output_filename if output_dir else input_path.with_name(f"{input_path.stem}_part{output_file_count}.csv")
                current_output = open(output_path, 'w', newline='')
                csv_writer = csv.writer(current_output)
                csv_writer.writerow(headers)

            csv_writer.writerow(row)
            rows_written += 1

        if current_output:
            current_output.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Split a large CSV file into smaller CSV files.')

    parser.add_argument('-i', '--input', type=str, required=True, help='Path to the large CSV file that needs to be split.')
    parser.add_argument('-r', '--rows', type=str, required=True, help='Number or percentage of rows in each smaller CSV file.')
    parser.add_argument('-o', '--output', type=str, help='Output directory for smaller CSV files.')

    args = parser.parse_args()

    split_csv(args.input, args.rows, args.output)