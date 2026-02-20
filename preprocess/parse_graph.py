#!/usr/bin/env python3
"""
Parse Graphviz DOT file into structured JSON format.
Extracts nodes, edges, and builds label-to-ID mapping.
"""

import sys
import json
import pydot
import networkx as nx
from pathlib import Path


def parse_dot_file(dot_path):
    """
    Parse a DOT file and extract nodes, edges, and mappings.

    Returns:
        dict with keys: nodes, edges, labelToId, nx_graph
    """
    print(f"Parsing DOT file: {dot_path}")

    # Load DOT file
    graphs = pydot.graph_from_dot_file(dot_path)
    if not graphs:
        raise ValueError(f"Failed to parse DOT file: {dot_path}")

    graph = graphs[0]

    # Create NetworkX graph (preserve direction if digraph)
    is_directed = graph.get_type() == "digraph"
    G = nx.DiGraph() if is_directed else nx.Graph()

    # Parse nodes
    nodes = []
    label_to_id = {}
    valid_node_ids = set()

    for node in graph.get_nodes():
        node_name = node.get_name()

        # Skip special DOT keywords
        if node_name in ("node", "graph", "edge"):
            continue

        # Remove quotes from node name
        node_id = node_name.strip('"')

        # Get attributes
        attrs = node.get_attributes()

        # Extract label (fallback to node_id if not present)
        label = attrs.get("label", node_id).strip('"')

        # Build node object
        node_obj = {
            "id": node_id,
            "label": label,
        }

        # Add all other attributes
        for key, value in attrs.items():
            if key != "label":
                node_obj[key] = value.strip('"') if isinstance(value, str) else value

        nodes.append(node_obj)
        valid_node_ids.add(node_id)

        # Add to NetworkX graph
        G.add_node(node_id, **node_obj)

        # Build label-to-ID mapping
        if label:
            label_to_id[label] = node_id

    print(f"  Parsed {len(nodes)} nodes")

    # Parse edges
    edges = []
    skipped_edges = 0

    for edge in graph.get_edges():
        source = edge.get_source().strip('"')
        target = edge.get_destination().strip('"')

        # Skip edges that reference non-existent nodes
        if source not in valid_node_ids or target not in valid_node_ids:
            skipped_edges += 1
            continue

        # Get attributes
        attrs = edge.get_attributes()

        edge_obj = {
            "source": source,
            "target": target,
        }

        # Add all attributes
        for key, value in attrs.items():
            edge_obj[key] = value.strip('"') if isinstance(value, str) else value

        edges.append(edge_obj)

        # Add to NetworkX graph
        G.add_edge(source, target, **attrs)

    print(f"  Parsed {len(edges)} edges")
    if skipped_edges > 0:
        print(f"  Skipped {skipped_edges} edges referencing non-existent nodes")

    return {
        "nodes": nodes,
        "edges": edges,
        "labelToId": label_to_id,
        "nx_graph": G,
        "is_directed": is_directed
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_graph.py <path_to_dot_file>")
        sys.exit(1)

    dot_path = sys.argv[1]

    if not Path(dot_path).exists():
        print(f"Error: File not found: {dot_path}")
        sys.exit(1)

    result = parse_dot_file(dot_path)

    # Don't include NetworkX graph in JSON output
    output = {
        "nodes": result["nodes"],
        "edges": result["edges"],
        "labelToId": result["labelToId"],
        "is_directed": result["is_directed"]
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
