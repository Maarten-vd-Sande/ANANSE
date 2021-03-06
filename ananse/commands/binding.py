#!/usr/bin/env python
# Copyright (c) 2009-2019 Quan Xu <qxuchn@gmail.com>
#
# This module is free software. You can redistribute it and/or modify it under
# the terms of the MIT License, see the file COPYING included with this
# distribution.

from __future__ import print_function
import sys
import os

import ananse.binding


def binding(args):
    if not os.path.exists(args.fin_rpkm):
        print("File %s does not exist!" % args.fin_rpkm)
        sys.exit(1)

    a = ananse.binding.Binding(
        ncore=args.ncore,
        genome=args.genome, 
        # gene_bed=args.annotation, 
        pfmfile=args.pfmfile,
        include_notfs=args.include_notfs,
        rm_curated=args.rm_curated,
        etype=args.etype,
        tffile=args.tffile
    )
    a.run_binding(args.fin_rpkm, args.outfile)
