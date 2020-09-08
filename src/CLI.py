import argparse


class CommandLineInterface(object):
    parser = argparse.ArgumentParser(description='Manage your files.')

    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s 0.1'
    )

    parser.add_argument(
        metavar='<file>',
        type=str,
        dest='file',
        nargs='?',
        help='Location of file to manage',
    )

    parser.add_argument(
        metavar='<folder>',
        type=str,
        dest='folder',
        nargs='?',
        help='Name of folder to manage',
    )

    parser.add_argument(
        metavar='<areaname>',
        type=str,
        dest='areaname',
        nargs='?',
        help='Location of area to manage',
    )

    group = parser.add_mutually_exclusive_group(required=False)

    group.add_argument(
        '-m',
        '--move',
        dest='move',
        action='store_true',
        help='Move file to the correct folder within the managed area',
    )

    group.add_argument(
        '-t',
        '--tag',
        metavar='<tags>',
        type=str,
        dest='add_tags',
        nargs='*',
        help='Add new tags',
    )

    group.add_argument(
        '-a',
        '--area',
        metavar='<location>',
        type=str,
        dest='new_area',
        nargs=1,
        help='Add a new area',
    )

    group.add_argument(
        '-f',
        '--folder',
        metavar='<tags>',
        type=str,
        dest='add_folder',
        nargs='*',
        help='Add a new folder',
    )

    def parse(self, manager):
        args = self.parser.parse_args()

        if args.add_folder:
            if not (args.area and args.folder):
                self.parser.error("--folder requires an area and folder to create the folder in with the folder name")
                return
            manager.add_folder(area=args.area, foldername=args.folder)

        if args.move:
            if not (args.file and args.area):
                self.parser.error("--move requires and area and a file to move the file in")
                return
            manager.move(area=args.area, file=args.file)

        if args.add_tags:
            if not (args.area and args.folder):
                self.parser.error("--tag requires the area and folder to find the folder to add tags to")
                return
            manager.add_tag(area=args.area, folder=args.folder, tags=args.new_tags)

        if args.new_area:
            if not args.area:
                self.parser.error("--area requires areaname for the location of the new area")
                return
            manager.new_area(area=args.area)

        # This is useless but its so gross i love it
        # print(all([vars(args)[arg] for arg in vars(args) if arg not in {"area", "file", "folder"}]))
