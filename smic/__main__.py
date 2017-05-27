import argparse

from .app import Application


def parse_args():
    parser = argparse.ArgumentParser(
        description='Simple Manual Image Categorizer')
    parser.add_argument(
        'src_path', help='Location of images to be categorized')
    parser.add_argument(
        'dest_root_path', help='Destination for images')
    return parser.parse_args()


def main():
    args = parse_args()
    app = Application(args)
    app.master.title('SMIC')
    app.mainloop()


if __name__ == '__main__':
    main()
