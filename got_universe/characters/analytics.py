import networkx as nx
from .models import Character


def build_character_graph():
    G = nx.Graph()

    characters = Character.objects.all()

    # Add nodes
    for char in characters:
        G.add_node(char.id, name=char.name)

    # Add family edges
    for char in characters:
        if char.father:
            G.add_edge(char.id, char.father.id)

        if char.mother:
            G.add_edge(char.id, char.mother.id)

        if char.spouse:
            G.add_edge(char.id, char.spouse.id)

        # Event-based relationships
        for event in char.events.all():
            for other in event.involved_characters.all():
                if other.id != char.id:
                    G.add_edge(char.id, other.id)

    return G


def calculate_influence():
    G = build_character_graph()

    degree = nx.degree_centrality(G)
    betweenness = nx.betweenness_centrality(G)

    scores = {}

    for node in G.nodes():
        scores[node] = (
            degree.get(node, 0) * 0.6 +
            betweenness.get(node, 0) * 0.4
        )

    return scores
