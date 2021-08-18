# USCIS Case Status Checker

## Requirements

This script requires Python 3.6+. It depends on the following modules:

  - [Requests](https://docs.python-requests.org/en/master/)
  - [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
  - [Tabulate](https://pypi.org/project/tabulate/)
  
To install the dependencies, run `pip install -r requirements.txt`

## Checking Case Status

This tool can be used to check the case status of one or more receipt numbers.

### Single Case Status

```
$ ./rstat.py -n LIN21902XXXXX
╒══════════════════╤════════╤══════════════════════════════════════════════════════╕
│ Receipt Number   │ Form   │ Summary                                              │
╞══════════════════╪════════╪══════════════════════════════════════════════════════╡
│ LIN21902XXXXX    │ I-485  │ Response To USCIS' Request For Evidence Was Received │
╘══════════════════╧════════╧══════════════════════════════════════════════════════╛

```

### Multiple Case Statuses

```
$ ./rstat.py -n LIN21902XXXXX LIN21902XXXXX LIN21902XXXXX LIN21902XXXXX
╒══════════════════╤════════╤══════════════════════════════════════════════════════╕
│ Receipt Number   │ Form   │ Summary                                              │
╞══════════════════╪════════╪══════════════════════════════════════════════════════╡
│ LIN21902XXXXX    │ I-140  │ Case Was Approved And My Decision Was Emailed        │
├──────────────────┼────────┼──────────────────────────────────────────────────────┤
│ LIN21902XXXXX    │ I-485  │ Response To USCIS' Request For Evidence Was Received │
├──────────────────┼────────┼──────────────────────────────────────────────────────┤
│ LIN21902XXXXX    │ I-131  │ Case Was Received                                    │
├──────────────────┼────────┼──────────────────────────────────────────────────────┤
│ LIN21902XXXXX    │ I-765  │ Case Was Updated To Show Fingerprints Were Taken     │
╘══════════════════╧════════╧══════════════════════════════════════════════════════╛
```
