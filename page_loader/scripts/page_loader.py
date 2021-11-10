import argparse
import sys
import os
import logging
import requests
import page_loader


def parse_args():
    parser = argparse.ArgumentParser(description='Download a web page')
    parser.add_argument('url', help='URL of the page to download')
    parser.add_argument('--output', default=os.getcwd(),
                        help='Output directory (default: current directory)')
    parser.add_argument('--loglevel', default='error', choices=['debug', 'info', 'warning', 'error'],
                        help='Logging level (default: error)')
    return parser.parse_args()


def main():
    args = parse_args()
    log_level = getattr(logging, args.loglevel.upper())
    logging.basicConfig(format='%(levelname)s: %(message)s', level=log_level)

    if not os.path.exists(args.output) or not os.path.isdir(args.output):
        logging.error(f'Output directory "{args.output}" doesn\'t exist')
        sys.exit(1)
        # os.mkdir(args.output)

    try:
        print(page_loader.download(args.url, args.output))
    except requests.RequestException as ex:
        logging.error(ex)
        sys.exit(1)


if __name__ == '__main__':
    main()
