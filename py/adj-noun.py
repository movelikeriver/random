"""Generates dot graph for common adjective and noun adjacencies.

The data is from the novel "David Copperfield" by Charles Dickens, as
described by M. Newman.

Prerequisites:
Install graphviz (from http://www.graphviz.org) for dot command line.
Probably the easist way is:
  brew install graphviz

Install NetworkX for reading gml file. Probably the easist way is:
  sudo pip install NetworkX

Run the code:
  python adj-noun.py | dot -Tpdf > /tmp/a.pdf ; open /tmp/a.pdf

"""

import collections
import networkx as nx


def Gml2AdjList(G):
    """Convers gml to adj-list.

    G.edge dict is like:
    {0: {1: {}, 2: {}, 3: {}},
     1: {0: {}, 19: {}, 2: {},
     ...}

    G.node dict is like:
    {0: {'id': 0, 'value': 0, 'label': u'agreeable'},
     1: {'id': 1, 'value': 1, 'label': u'man'},
     ...}

    Returns
        OrderedDict([(u'agreeable', [u'man', u'old', u'person']),
                     (u'man', [u'agreeable', u'best', ...]),
                     ...])
    """

    words = collections.OrderedDict()
    for k, vs in G.edge.items():
        kn = G.node[k]['label']
        if kn not in words:
            words[kn] = []
        for v in vs.keys():
            vn = G.node[v]['label']
            words[kn].append(vn)
    return words


def GenerateDot(adj):
    """Generates dot from adj-list."""

    dots = ['digraph g {',
            '  rankdir=LR;']
    for k, arr in adj.items():
        for v in arr:
            dots.append('  %s -> %s;' % (k, v))

    dots.append('}')
    return '\n'.join(dots)


# main
dg = nx.read_gml('adjnoun/adjnoun.gml')
list = Gml2AdjList(dg)
print GenerateDot(list)



