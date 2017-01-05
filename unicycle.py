"""
Unicycle Class
"""

#                      STEP 0
#      ######          ######          ######
#       ####################################
#      ######          ######          ######


# Import all the future support libs
from __future__ import absolute_import, division

# Import TF and numpy - basic stuff
import tensorflow as tf
import numpy as np
from tensorflow.python.ops.rnn_cell import RNNCell

# Import Unicycle-specific things
from unicycle_settings import *
from json_import import *
from construct_networkx import *
from node_sizing import *
from initialize_nodes import *
from unroller import *
import imgs

# Import the system-related libs
from random import randint
if VERBOSE:
    from dbgr import dbgr_verbose as dbgr
else:
    from dbgr import dbgr_silent as dbgr


class Unicycle(object):
    def __init__(self):
        print 'Unicycle Initialized'

    def build(self, dbgr=dbgr):
        """
        The main execution routine file for the Universal Neural
        Interpretation and Cyclicity Engine (UNICYCLE)

        The way this works is the following:

        Step 1
        =======
         High-level description of the system is fed in via a JSON object-
         bearing file that is passed in as a command line argument when the
         script is run. Here we get the raw metadata from the JSON file and
         store it in a list of dictionaries, as well as a list of tuples of
         (from,to) links in the graph.

        Step 2
        =======
         Now we create a Network-X graph G for planning purposes. Store the
         nickname only as the pointer to the node to be instantiated, and then
         use this nickname to look up relevant node's metadata in the node
         dictionary list we acquired in step 1.

         Step 3
        =======
         BFS Search - currently unused, might slash this section soon.

        Step 4
        =======
         Using the Network-X graph G we create a parallel graph H and copy the
         main forward links into it.

            if target_node not on any path leading to source node:
                append (source_node, target_node) to forward_list
            NXGRAPH using forward_list -> H

        Step 5
        =======
         Once all the connections are made, we start the size calculation.
         This involves the Harbor of every one of the nodes (here the actual
         Tensors will be scaled or added or concatenated and the resulting
         Tensor will be used as input to the functional "conveyor belt").
         While the Harbor is the place where the actual resizing happens, we
         also have the Harbor-Master policy. This policy can be specified in
         the node metadata in the JSON, or if it isn't specified it can be
         inferred from the default settings (default subject to modification
         too).

         For every NODE:
         - Collect all non-feedback inputs, find their sizes, push list of
         sizes along with Harbor-Master policy into general Harbor-Master
         utility function to find ultimate size.
         - Create a reference dictionary for node metadata that has incoming
         inputs as keys and scaling values as values.
         - Calculate all final sizes for all nodes, use for feedback up and
         down the line.

        Step 6
        =======
         Tensor creation.

        Step 7
        =======
         Perform proper RNN unrolling of nodes within 1 time step. Thi
         cheating, as the RNN is essentially unrolled through a single
         memoized states it's parent and predecessor Cells are queried
         for, creating the illusion of a true RNN unroll. In reality,
         structure is preserved

        Let's kick ass
        """
        imgs.unicycle_logo()

        #                      STEP 1
        #      ######          ######          ######
        #       ####################################
        #      ######          ######          ######

        dbgr('======\nSTEP 1\n JSON Import and Parse\n======================')

        # Import NODES and LINKS from JSON
        nodes, links = json_import(dbgr=dbgr)

        #                      STEP 2
        #      ######          ######          ######
        #       ####################################
        #      ######          ######          ######

        dbgr('======\nSTEP 2\n Network-X Raw Build\n======')

        # Create NetworkX DiGraph G, find root nodes
        G, root_nodes = construct_G(links, dbgr=dbgr)

        #                      STEP 3
        #      ######          ######          ######
        #       ####################################
        #      ######          ######          ######

        dbgr('======\nSTEP 3\n BFS Dependency Parse\n======')
        dbgr('BFS Dependency Parse Temporarily Disabled')

        #                      STEP 4
        #      ######          ######          ######
        #       ####################################
        #      ######          ######          ######

        dbgr('======\nSTEP 4\n Clone Forward-Only Graph Creation\n======')

        # Create the forward-only DiGraph H
        H = construct_H(G, dbgr=dbgr)

        #                      STEP 5
        #      ######          ######          ######
        #       ####################################
        #      ######          ######          ######

        dbgr('======\nSTEP 5\n Input Size Calculation\n======')

        # Calculate the sizes of all of the nodes here
        node_out_size, node_state_size, node_harbors, node_input_touch, \
            node_touch = all_node_sizes(G, H, nodes, dbgr=dbgr)

        #                      STEP 6
        #      ######          ######          ######
        #       ####################################
        #      ######          ######          ######

        dbgr('======\nSTEP 6\n TF Node Creation\n========================')

        # Initialize all the nodes:
        repo = initialize_nodes(nodes,
                                node_out_size,
                                node_state_size,
                                node_input_touch,
                                node_touch)

        # Emotional support
        dbgr(imgs.centaur())

        return G, H, repo

    def __call__(self, input_sequence, G, repo, dbgr=dbgr):
        #                      STEP 7
        #      ######          ######          ######
        #       ####################################
        #      ######          ######          ######

        dbgr('======\nSTEP 7\n TF Unroller\n========================')

        repo, last = unroller_call(input_sequence, G, repo)

        return repo[last]

    def alexnet_demo_out(self, training_input=[], **kwargs):
        G, H, repo = self.build()
        last_ = self(training_input, G, repo)
        return last_

    def unicycle_tfutils(self, training_data, **kwargs):
        m = self.alexnet_demo_out(training_data, **kwargs)
        return m.state, {'input': 'image_input_1',
                         'type': 'lrnorm',
                         'depth_radius': 4,
                         'bias': 1,
                         'alpha': 0.0001111,
                         'beta': 0.00001111}

if __name__ == '__main__':
    print 'THIS\nIS\nA\nTEST\nUNICYCLE\nALEXNET\nINITIALIZATION'
    a = Unicycle()
    b = a.alexnet_demo_out()
