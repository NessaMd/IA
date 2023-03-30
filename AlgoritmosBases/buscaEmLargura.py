from collections import deque

# Definição do grafo como um dicionário de listas de adjacência
grafo = {
    'A': ['B'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

def bfs(grafo, inicio):
    visitados = []  # Lista para armazenar os nós visitados
    fila = deque([inicio])  # Fila para armazenar os nós a serem visitados

    while fila:
        no = fila.popleft()  # Remove o nó mais antigo da fila
        if no not in visitados:
            visitados.append(no)
            vizinhos = grafo[no]

            # Adiciona os vizinhos não visitados na fila
            for vizinho in vizinhos:
                if vizinho not in visitados:
                    fila.append(vizinho)
    
    return visitados

print(bfs(grafo, 'A'))  
