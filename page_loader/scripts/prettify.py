import bs4
import os.path
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath')
    parser.add_argument('-s', '--save', action='store_true')
    return parser.parse_args()


def main():
    args = parse_args()
    filepath = args.filepath
    if not os.path.exists(filepath) or not os.path.isfile(filepath):
        print(f'File {filepath} doesn\'t exist!')

    with open(filepath) as f:
        soup = bs4.BeautifulSoup(f.read(), 'html.parser')
    pretty_html = soup.prettify()

    if args.save:
        with open(filepath, 'w') as f:
            f.write(pretty_html)
    else:
        print(pretty_html)


if __name__ == '__main__':
    main()
