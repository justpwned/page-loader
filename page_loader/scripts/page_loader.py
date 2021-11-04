import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser(description='Download a web page')
    parser.add_argument('--output', default=os.getcwd(),
                        help='Output directory (default: current directory)')
    parser.add_argument('url', help='URL of page to download')
    return parser.parse_args()


def main():
    args = parse_args()
    for k, v in args.items():
        print(f'{k}: {v}')


if __name__ == '__main__':
    main()
