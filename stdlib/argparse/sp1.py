import argparse as ap

def main():
    ps = ap.ArgumentParser(
        prog='prog',
        description='ETo da'
    )
    ps.add_argument('file')
    ps.add_argument('-c', '--count')
    ps.add_argument('-v', '--verbose', action='store_true')
    args = ps.parse_args()
    ps.print_help()
    pass

if __name__ == '__main__':
    main()
