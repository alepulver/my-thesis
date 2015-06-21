import os
import sys
import csv
import argparse


def main(arguments):
    parser = argparse.ArgumentParser(description='Generate clustering visualizations.')
    parser.add_argument(
        '--tables_dir', dest='tables_dir',
        help='contents of the "individual_stages" subdirectory, of the results-analysis output'
    )
    parser.add_argument(
        '--clusters_dir', dest='clusters_dir',
        help='directory containing the cluster assignment for each stage'
    )
    parser.add_argument(
        '--output_dir', dest='output_dir', default='output',
        help='output directory to write the results (default: "output")'
    )

    args = parser.parse_args(arguments[1:])

    if os.path.exists(args.output_dir):
        print('ERROR: the directory "{}" already exists, please use another name'.format(
          args.output_dir), file=sys.stderr
        )
        return 1
    else:
        os.makedirs(args.output_dir)

    # ...

    return 0


if __name__ == "__main__":
    status = main(sys.argv)
    sys.exit(status)
