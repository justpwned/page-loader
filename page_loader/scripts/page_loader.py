import argparse
import os
from page_loader import download


def parse_args():
    parser = argparse.ArgumentParser(description='Download a web page')
    parser.add_argument('--output', default=os.getcwd(),
                        help='Output directory (default: current directory)')
    parser.add_argument('url', help='URL of page to download')
    return parser.parse_args()


def main():
    args = parse_args()
    if not os.path.exists(args.output):
        os.mkdir(args.output)

    out_filepath = download(args.url, args.output)
    print(out_filepath)


if __name__ == '__main__':
    main()
