#!/usr/bin/env python3
#
# Copyright 2025 Lawrence Livermore National Security, LLC and other
# Thicket Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: MIT

import sys

import pandas as pd

sys.path.append(
    "/usr/gapps/spot/live/hatchet-venv/x86_64/lib/python3.9/site-packages/"
)  # <-- Python packages
sys.path.append("/usr/gapps/spot/live/hatchet/x86_64/")  # <-- Hatchet
sys.path.append("/usr/gapps/spot/live/thicket-playground-dev/")  # <-- Thicket

import hatchet as ht  # noqa: E402
import thicket as th  # noqa: E402

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

ht.__init__
th.__init__

#
