import sys
import networkx as nx
import matplotlib.pyplot as plt

def ingresar_grafo():
    n = int(input("Ingrese la cantidad de vértices del grafo (entre 2 y 8): "))
    if n < 2 or n > 8:
        print("Cantidad inválida de vértices.")
        return None
    G = nx.Graph()
    # Ingresar vértices
    for i in range(n):
        vertice = input(f"Ingrese el vértice {i+1}: ")
        G.add_node(vertice)
    # Ingresar aristas
    print("Ingrese las aristas en formato 'vertice1 vertice2' o escriba 'fin' para terminar: ")
    while True:
        arista = input()
        if arista == 'fin':
            break
        try:
            v1, v2 = arista.split()
            G.add_edge(v1, v2)
        except:
            print("Formato de arista inválido.")
    return G

def ingresar_vertices():
    v1 = input("Ingrese el vértice de inicio: ")
    v2 = input("Ingrese el vértice de destino: ")
    return v1, v2

def encontrar_caminos(G, v1, v2):
    try:
        camino_optimo = nx.shortest_path(G, v1, v2)
    except:
        print("No hay un camino posible entre los vértices ingresados.")
        return None, None
    
    caminos_adicionales = []
    queue = [(v1, [v1])]
    while queue:
        (node, path) = queue.pop(0)
        for vecino in G[node]:
            if vecino not in path:
                if vecino == v2:
                    camino = path + [vecino]
                    # Revisa si el camino es igual al camino óptimo
                    if all(nodo in camino_optimo for nodo in camino):
                        continue
                    caminos_adicionales.append(camino)
                else:
                    queue.append((vecino, path + [vecino]))
    
    caminos_adicionales = sorted(caminos_adicionales, key=lambda x: len(x))
    
    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 4))

    plt.subplot(1, 3, 1)
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightblue')
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    edges = [(camino_optimo[i], camino_optimo[i+1]) for i in range(len(camino_optimo)-1)]
    nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='green', width=3)
    plt.title("Camino óptimo")

    if caminos_adicionales:
        plt.subplot(1, 3, 2)
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightblue')
        nx.draw_networkx_edges(G, pos)
        nx.draw_networkx_labels(G, pos)
        edges = [(caminos_adicionales[0][i], caminos_adicionales[0][i+1]) for i in range(len(caminos_adicionales[0])-1)]
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='red', width=3)
        plt.title("Primer camino alternativo")

        if len(caminos_adicionales) > 1:
            plt.subplot(1, 3, 3)
            nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightblue')
            nx.draw_networkx_edges(G, pos)
            nx.draw_networkx_labels(G, pos)
            edges = [(caminos_adicionales[1][i], caminos_adicionales[1][i+1]) for i in range(len(caminos_adicionales[1])-1)]
            nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='purple', width=3)
            plt.title("Segundo camino alternativo")

    plt.show()


def main():
    G = ingresar_grafo()
    if not G:
        sys.exit()
    nx.draw(G, with_labels=True)
    plt.show()
    v1, v2 = ingresar_vertices()
    camino_optimo, caminos_adicionales = encontrar_caminos(G, v1, v2)
    if camino_optimo:print(f"El camino óptimo es: {camino_optimo}")
    if caminos_adicionales:
        print("Otros dos caminos posibles son:")
        for i, camino in enumerate(caminos_adicionales):
            print(f"Camino {i+1}: {camino}")

        # Graficar las rutas en tres ventanas diferentes
        plt.plot(list(G.nodes), 'o')
        plt.plot(camino_optimo, marker='o', label='Camino óptimo')
        plt.legend()
        plt.show()

        plt.plot(list(G.nodes), 'o')
        plt.plot(caminos_adicionales[0], marker='o', label='Primer camino posible')
        plt.legend()
        plt.show()

        plt.plot(list(G.nodes), 'o')
        plt.plot(caminos_adicionales[1], marker='o', label='Segundo camino posible')
        plt.legend()
        plt.show()
    input("Presione cualquier tecla para cerrar el programa...")

if __name__ == '__main__':
    main()