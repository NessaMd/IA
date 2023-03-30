"""
Autoria: Vanessa Machado Araújo

Exercício: Existem dois jarros inicialmente vazios. Um possui capacidade igual a 3 litros
e o outro igual a 4 litros. Ambos podem ser enchidos completamente
utilizando uma torneira e podem também ser esvaziados, despejando a água
em um ralo. Além disso, a água presente em um jarro pode ser passada para
o outro. Os jarros não possuem marcações e não é permitido o uso de
qualquer instrumento de medida. Deseja-se colocar exatamente dois litros
de água no jarro maior. Pode-se representar as quantidades de água
presentes nos dois jarros pelo par ordenado (x,y), em que x é a quantidade
de água no jarro menor e y a quantidade no jarro maior. O estado inicial
(ambos vazios) é o par (0,0) e o objetivo é encontrar um par do tipo (x,2), isto
é, dois litros no jarro maior e qualquer quantidade no jarro menor.

Solucione este problema utilizando os algoritmos de busca em profundidade
e em largura.

Formulação:
j1 = jarro 1 (jarro menor = 3 litros)
j2 = jarro 2 (jarro maior = 4 litros)

estado:  (j1, j2) de tal forma que 0 <= j1 <= 3 e 0 <= j2 <= 4
objetivo: j2 == 2 -> (j1, 2)
estado inicial: (0, 0) raíz da árvore
ações: 
A1: Se j1 não estiver cheio -> encher j1
A2: Se j2 não estiver cheio -> encher j2

A3: Se j1 não estiver vazio e j2 não estiver cheio -> transferir conteúdo de j1 para j2
A4: Se j2 não estiver vazio e j1 não estiver cheio -> transferir conteúdo de j2 para j1

A5: Se j1 não estiver vazio -> esvaziar j1
A6: Se j2 não estiver vazio -> esvaziar j2

BUSCA EM LARGURA:
Estratégia: Expandir um nó mais raso primeiro
Implementação: Fringe é uma fila FIFO

BUSCA EM PROFUNDIDADE:
Estratégia: Expandir um nó mais profundo primeiro
Implementação: Fringe é uma pilha LIFO
"""


from collections import deque


initial_state = (0, 0)  # começa com as duas jarros vazios

"""
Classe usada para representar um nó da árvore de busca.
Contém: um estado (state) e seu estado pai(state_parent).
"""

class Node:
    def __init__(self, state, state_parent):
        self.state = state
        self.state_parent = state_parent

    
    # Função de verificação: Verifica se obteve sucesso na busca, ou seja, se o nó é um nó objetivo.
    
    def is_objective_node(self):
        return (self.state[1] == 2)

    
	# Função de impressão: Quando um nó é o objetivo, imprime o caminho da solução do estado inicial até o estado objetivo.

    def print_path(self):
        if (self.state_parent is not None):
            self.state_parent.print_path()

        print(self.state)


	# Função que retorna os possíveis nós filhos de um nó, ou seja, os nós dos estados seguintes dependendo das ações que podem ser executadas no estado atual.

    def children(self):
        children = []

        j1 = self.state[0]  # j1 = jarro menor
        j2 = self.state[1]  # j2 = jarro maior

    # Ações:

        if (j1 == 0):  # se j1 vazia
            children.append(Node((3, j2), self))  # encher j1

        if (j2 == 0):  # se j2 vazia
            children.append(Node((j1, 4), self))  # encher j2

        if (j1 != 0 and j2 != 4):  # j1 não está vazio e j2 não está cheia 
            amount_transferred = 4 - j2 # quantidade máxima que j2 pode receber
            if (amount_transferred > j1): # se a quantidade máxima é igual ao conteúdo de j1
                amount_transferred = j1 # transfere todo j1
            children.append(
                Node((j1-amount_transferred, j2+amount_transferred), self)) # transferir o conteúdo de j1 para j2 

        if (j1 != 3 and j2 != 0):  # se j1 não está cheia e j2 não está vazia
            # amount_transferredir o conteúdo de j2 para j1 até encher
            amount_transferred = 3 - j1 # quantidade máxima que j1 pode receber
            if (amount_transferred > j2): # se a quantidade máxima é igual ao conteúdo de j2
                amount_transferred = j2 # transfere todo j2
            children.append(
                Node((j1+amount_transferred, j2-amount_transferred), self)) # transferir o conteúdo de j2 para j1

        if (j1 != 0):  # se j1 não está vazia
            children.append(Node((0, j2), self))  # esvaziar j1

        if (j2 != 0):  # se j2 não está vazia
            children.append(Node((j1, 0), self))  # esvaziar j2

        return children


# Busca em Largura 

def breadth_first():
    node = Node(initial_state, None)  # estado inicial 
    row = deque()  # fila de nós a serem explorados
    explored_states = []  # lista de estados já explorados

    if node.is_objective_node(): # se o nó é o nó objetivo
        return node.print_path()  # solução encontrada -> imprime caminho 

    row.append(node) # adiciona raíz na fila

    while (True):
        if not row:  # fila vazia
            return "FAILED"

        node = row.popleft()  # retira elemento da fila -> FIFO
        explored_states.append(node.state) # coloca na fila de estados explorados

        for child in node.children(): # percorre os nós 
            if child.state not in explored_states and child not in row: # se não está na lista de nós explorados e não está na fila
                if child.is_objective_node(): # se o nó é o nó objetivo
                    return child.print_path()  # solução encontrada no filho -> imprime caminho

                row.append(child) # adciona nó na fila


# Busca em profundidade.

def depth_first():
    node = Node(initial_state, None)  # estado inicial
    stack = deque()   # pilha de nós a serem explorados
    explored_states = []  # lista de estados explorados
   
    if node.is_objective_node(): # se o nó é o nó objetivo
        return node.print_path()  # solução encontrada -> imprime caminho 

    stack.append(node) # adiciona raíz na pilha

    while (True):
        if not stack:  # fronteira vazia
            return "FAILED"
            
        node = stack.pop()  # remoção LIFO
        explored_states.append(node.state)

        for child in node.children():
            if child.state not in explored_states and child not in stack:
                if child.is_objective_node():
                    return child.print_path()  # solução encontrada no filho

                stack.append(child)

 
print("\nBusca em largura:")
breadth_first()


print("\n#########################################################################################################")


print("\nBusca em profundidade:")
depth_first()
