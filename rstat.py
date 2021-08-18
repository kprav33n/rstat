#!/usr/bin/env python

"""
USCIS Case Status Checker.
"""

from argparse import ArgumentParser
import sys

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
    return div.h1.text, div.p.text


def main():
    """
    Main entrypoint.
    """
    parser = ArgumentParser(description='USCIS Case Status Checker')
    parser.add_argument('--receipt-numbers', '-n', type=str, nargs='*',
                        help='Receipt numbers')
    args = parser.parse_args()

    if not args.receipt_numbers:
        print('At least one receipt number is required')
        sys.exit(1)

    statuses = [
        (receipt_number, ) + get_status(receipt_number)
        for receipt_number in args.receipt_numbers
    ]
    summary = [
        (receipt_number, summary)
        for receipt_number, summary, _ in statuses
    ]
    print(tabulate(summary, ['Receipt Number', 'Summary'],
                   tablefmt='fancy_grid'))


if __name__ == '__main__':
    main()
