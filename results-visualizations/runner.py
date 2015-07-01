import os
import sys
import pyx
import argparse
import layouts
import samplers
import data_loader


def main(arguments):
    parser = argparse.ArgumentParser(description='Generate clustering visualizations.')
    parser.add_argument(
        '--tables_dir', dest='tables_dir', default='input/tables',
        help='contents of the "individual_stages" subdirectory of results (default: "input/tables")'
    )
    parser.add_argument(
        '--clusters_dir', dest='clusters_dir', default='input/clusters',
        help='directory containing the cluster assignment for each stage (default: "input/clusters")'
    )
    parser.add_argument(
        '--output_dir', dest='output_dir', default='output',
        help='output directory to write the results (default: "output")'
    )
    parser.add_argument(
        '--layout', dest='layout', required=True, choices=layouts.available_names(),
        help='layout to use for displaying clusters'
    )
    parser.add_argument(
        '--sampler', dest='sampler', required=True, choices=samplers.available_names(),
        help='algorithm for selecting which items and in what order to show'
    )
    parser.add_argument(
        '-n', dest='total_items', type=int, default=200,
        help='total number of items to show'
    )

    args = parser.parse_args(arguments[1:])

    if os.path.exists(args.output_dir):
        print('ERROR: the directory "{}" already exists, please use another name'.format(
          args.output_dir), file=sys.stderr
        )
        return 1
    else:
        os.makedirs(args.output_dir)

    layout_class = layouts.from_name(args.layout)
    sampler_class = samplers.from_name(args.sampler)
    clusters = data_loader.DataLoader(args.tables_dir, args.clusters_dir).results

    for k, v in clusters.items():
        a_layout = layout_class()
        a_sampler = sampler_class(v, args.total_items)
        figure = pyx.canvas.canvas()
        a_layout.draw(a_sampler, figure)

        canvas = pyx.canvas.canvas()
        transform = pyx.trafo.scale(40, 40)
        canvas.insert(figure, [transform])
        canvas.writePDFfile("{}/{}".format(args.output_dir, k))

    return 0


if __name__ == "__main__":
    status = main(sys.argv)
    sys.exit(status)
