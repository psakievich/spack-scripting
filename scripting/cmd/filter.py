# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import sys

from ..functions import filter_specs

description = "filter specs based on their properties"
section = "scripting"
level = "long"


def setup_parser(subparser):
    install_status = subparser.add_mutually_exclusive_group()
    install_status.add_argument(
        '--installed', dest='installed', default=None, action='store_true',
        help='select installed specs'
    )
    install_status.add_argument(
        '--not-installed', dest='installed', default=None,
        action='store_false',
        help='select specs that are not yet installed'
    )

    explicit_status = subparser.add_mutually_exclusive_group()
    explicit_status.add_argument(
        '--explicit', dest='explicit', default=None, action='store_true',
        help='select specs that were installed explicitly'
    )
    explicit_status.add_argument(
        '--implicit', dest='explicit', default=None,
        action='store_false',
        help='select specs that are not installed or were installed implicitly'
    )

    subparser.add_argument(
        '--output', default=sys.stdout, type=argparse.FileType('w'),
        help='where to dump the result'
    )

    subparser.add_argument(
        'specs', nargs=argparse.REMAINDER, help='specs to be filtered'
    )


def filter(parser, args):
    specs = filter_specs(args.specs, installed=args.installed, explicit=args.explicit)
    
    if not specs:
        sys.stdout.write("None of the spec matches the request\n")
        sys.exit(1)

    for spec in specs:
        args.output.write(str(spec.abstract) + '\n')
