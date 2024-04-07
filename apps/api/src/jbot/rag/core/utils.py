from pyvis.network import Network


def draw_dag(p):
    net = Network(notebook=True, cdn_resources="in_line", directed=True)
    net.from_nx(p.dag)
    net.show("rag_dag.html")
