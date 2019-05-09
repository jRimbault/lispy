# -*- coding: utf-8 -*-
'''
Author : Vincent Genin ESGI-3AL 2018
'''

import uuid
import graphviz


def printTreeGraph(t):
    graph = graphviz.Digraph(format='png')
    graph.attr('node')
    addNode(graph, t)
    graph.render(filename='render') #Pour Sauvegarder
    #graph.view() #Pour afficher


def addNode(graph, t):
    enumerable = lambda x: type(x) == list or type(x) == tuple
    nodeId = str(uuid.uuid4())

    if not enumerable(t):
        graph.node(nodeId, label=str(t))
    else:
        graph.node(nodeId, str(t[0]))
        for node in t[1:]:
            graph.edge(nodeId, str(addNode(graph, node)))

    return nodeId
