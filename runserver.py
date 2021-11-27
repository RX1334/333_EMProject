# -----------------------------------------------------------------------
# Runs the flask app in emp.py
# -----------------------------------------------------------------------

import argparse
from sys import exit, stderr
from emp import app

def main():
    DESC_STR = 'The EMP application'
    parser = argparse.ArgumentParser(description=DESC_STR,
                                     allow_abbrev=False)
    HELP_STR = "the port at which the server should listen"
    parser.add_argument('port', type=int, help=HELP_STR)

    args = parser.parse_args()

    try:
        app.run(host='0.0.0.0', port=args.port, debug=True)
    except Exception as ex:
        print(ex, file=stderr)
        exit(1)


if __name__ == '__main__':
    main()