import argparse
import sys
import os
import logging
from page_loader import *


def parse_args():
    parser = argparse.ArgumentParser(description='Download a web page')
    parser.add_argument('url', help='URL of the page to download')
    parser.add_argument('-o', '--output', default=os.getcwd(),
                        help='Output directory (default: current directory)')
    return parser.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.ERROR)

    try:
        if not os.path.exists(args.output) or not os.path.isdir(args.output):
            os.mkdir(args.output)
        print(download(args.url, args.output))
    except (RequestException, PermissionException) as ex:
        logging.error(str(ex))
        sys.exit(1)


if __name__ == '__main__':
    main()
