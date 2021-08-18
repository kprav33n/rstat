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


def get_status(receipt_number):
    """
    Get the case status of a given receipt number.
    """
    data = {
        'appReceiptNum': receipt_number,
        'initCaseSearch': 'CHECK STATUS'
    }
    resp = requests.post('https://egov.uscis.gov/casestatus/mycasestatus.do',
                         data)
    soup = BeautifulSoup(resp.text, 'html.parser')
    div = soup.find('div', **{'class': 'rows text-center'})
    match = re.search(r'Form (I-\d+),', div.p.text)
    return match.group(1), div.h1.text, div.p.text


def main():
    """
    Main entrypoint.
    """
    parser = ArgumentParser(description='USCIS Case Status Checker')
    parser.add_argument('--receipt-numbers', '-n', type=str, nargs='*',
                        help='Receipt numbers')
    parser.add_argument('--num-threads', '-t', type=int, default=16,
                        help='Maximum number of threads')
    args = parser.parse_args()

    if not args.receipt_numbers:
        print('At least one receipt number is required')
        sys.exit(1)

    with ThreadPoolExecutor(max_workers=args.num_threads) as executor:
        statuses = executor.map(get_status, args.receipt_numbers)

    summaries = [
        (receipt_number, form, summary)
        for receipt_number, (form, summary, _) in zip(args.receipt_numbers,
                                                      statuses)
    ]
    print(tabulate(summaries, ['Receipt Number', 'Form', 'Summary'],
                   tablefmt='fancy_grid'))


if __name__ == '__main__':
    main()
