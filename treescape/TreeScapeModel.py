# Copyright 2025 Lawrence Livermore National Security, LLC and other
# Thicket Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: MIT

from .ThicketReader import ThicketReader
from .CaliReader import CaliReader
from .Reader import Reader
import json


class Run:
    def __init__(self, metadata, perftree, reader):
        self.metadata = metadata
        self.perftree = perftree
        self.read_from = reader

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        return {"metadata": self.metadata, "perftree": self.perftree}

    def getMetaData(self, key):
        return self.metadata[key]

    def getPerfTree(self, node, metric):
        return self.perftree[node][metric]

    def getChildrenForNode(self, node):
        return  # list of the node's children

    def getParentForNode(self, node):
        # main has not parent so return None.
        return  # parent


# this should hold the data
# it IS the data, if the user modifies it
# no graph concept, no viz concept.
# this is what should be user iteratable and they iterate over the runs.
class TreeScapeModel(list):

    def __init__(self, reader: Reader, updated_list=None):
        """

        :param th_ens: this comes from the get_th_ens function the user should define.
        Alternatively, you can use the one that comes with the Th_ens class.
        :param profiles:
        :param xaxis_name:  now required for performance optimization.
        """

        if updated_list is not None:
            self.init_with_reader(reader)
            self.update(updated_list)
        else:
            self.init_with_reader(reader)

    def init_with_reader(self, reader):

        self.reader = reader

        #  problem_size, launchdate, iterations
        #  default xaxis_name
        etc = self.reader.get_entire()
        et = etc["nodes"]

        self.childrenMap = etc["childrenMap"]
        self.meta_globals = etc["meta_globals"]

        # Initialize the transformed data list
        tsm_data = []

        # Iterate over each top-level key in the original data
        for key, value in et.items():
            # Iterate over each item in xaxis
            for i, metadata in enumerate(value["xaxis"]):
                # Find or create the entry for the current index
                if len(tsm_data) <= i:
                    tsm_data.append({"metadata": {}, "perftree": {}})

                # Add or update the metadata and perftree
                tsm_data[i]["metadata"] = metadata

                # Ensure the current key is in perftree
                tsm_data[i]["perftree"][key] = (
                    value["ydata"][i] if i < len(value["ydata"]) else None
                )

                # hack for now to get it working initially
                # TODO: FIX!
                if "perftree" in tsm_data[i] and "n" in tsm_data[i]["perftree"]:
                    tsm_data[i]["perftree"]["main"] = tsm_data[i]["perftree"]["n"]

        tsm_runs = []
        for index, td_obj in enumerate(tsm_data):
            r0 = Run(td_obj["metadata"], td_obj["perftree"], reader)
            tsm_runs.append(r0)

        tsm_data = tsm_runs

        self.runs = tsm_data
        super().__init__(tsm_data)

    def get_meta_globals(self):
        return self.meta_globals

    def get_children_map(self):
        return self.childrenMap

    def update(self, new_tsm_list):
        self.runs = new_tsm_list
        super().__init__(new_tsm_list)

    def getMetrics(self):
        return set["min time/rank", "max time/rank", "avg time/rank"]

    #  metadata_key could be "jobsize", "problem_size"
    #  for complex stuff, they will call sorted themselves on our tsm object
    def sort(self, metadata_key: str):
        sorted(self.runs, key=lambda run: run.metadata[metadata_key])

    #  return a new TreeScapeModel
    #  only the runs that have a certain run.metadata value
    #  for example problem_size = 8.
    # this is a simple version that just does Equal only
    def filter(self, type, value):
        return 1

    def get_entire_tsm(self):

        rns = [run.to_dict() for run in self.runs]

        return {
            "nodes": rns,
            "childrenMap": self.childrenMap,
            "meta_globals": self.meta_globals,
        }
