#!/usr/bin/env python

"""
USCIS Case Status Checker.
"""

from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
import sys
import re

import requests
from bs4 import BeautifulSoup
from tabulate import tabulate


def parse_args():
    """
    Parse command line arguments and return them.
    """
    parser = ArgumentParser(description='USCIS Case Status Checker')
    parser.add_argument('--receipt-numbers', '-n', type=str, nargs='*',
                        help='Receipt numbers')
    parser.add_argument('--num-threads', '-t', type=int, default=16,
                        help='Maximum number of threads')
    parser.add_argument('--before-cases', '-B', type=int, default=0,
                        help='Number of cases before the given receipt number')
    parser.add_argument('--after-cases', '-A', type=int, default=0,
                        help='Number of cases after the given receipt number')
    args = parser.parse_args()

    if not args.receipt_numbers:
        print('At least one receipt number is required')
        sys.exit(1)

    if (((args.before_cases > 0 or args.after_cases > 0) and
         len(args.receipt_numbers) > 1)):
        print('Use only one receipt number for bulk case queries')
        sys.exit(1)

    return args


def get_receipt_numbers(args):
    """
    Return receipt numbers to query from args.
    """
    base_center = args.receipt_numbers[0][:3]
    base_receipt_number = int(args.receipt_numbers[0][3:])
    before_numbers = []
    after_numbers = []
    if args.before_cases > 0:
        for number in range(base_receipt_number - 1,
                            base_receipt_number - args.before_cases - 1, -1):
            before_numbers.append(f'{base_center}{number}')
    if args.after_cases > 0:
        for number in range(base_receipt_number + 1,
                            base_receipt_number + args.before_cases + 1):
            after_numbers.append(f'{base_center}{number}')
    return before_numbers + args.receipt_numbers + after_numbers


def get_status(receipt_number):
    """
    Get the case status of a given receipt number.

    Returns form number, last updated date, summary and description.
    """
    data = {
        'appReceiptNum': receipt_number,
        'initCaseSearch': 'CHECK STATUS'
    }
    resp = requests.post('https://egov.uscis.gov/casestatus/mycasestatus.do',
                         data)
    soup = BeautifulSoup(resp.text, 'html.parser')
    div = soup.find('div', **{'class': 'rows text-center'})

    summary = div.h1.text
    description = div.p.text

    form = 'NA'
    match = re.search(r'Form ([^,]+),', description)
    if match:
        form = match.group(1)

    last_update = 'NA'
    match = re.search(r'(As of|On) (\w+ \d+, \d+),', description)
    if match:
        last_update = match.group(2)

    return form, last_update, summary, description


def main():
    """
    Main entrypoint.
    """
    args = parse_args()
    receipt_numbers = get_receipt_numbers(args)
    with ThreadPoolExecutor(max_workers=args.num_threads) as executor:
        statuses = executor.map(get_status, receipt_numbers)

    summaries = [
        (number, form, summary, last_update)
        for number, (form, last_update, summary, _) in zip(receipt_numbers,
                                                           statuses)
    ]
    print(tabulate(summaries,
                   ['Receipt Number', 'Form', 'Summary', 'Last Update'],
                   tablefmt='fancy_grid'))


if __name__ == '__main__':
    main()
