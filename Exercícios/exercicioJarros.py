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

BUSCA DE CUSTO UNIFORME
Estratégia: Expandir um nó mais barato primeiro
Implementação: Fringe é uma fila prioritária (prioridade:custo cumulativo)
Expande os nós na ordem do custo de caminho ótimo
O primeiro nó objetivo selecionado será a solução ótima
Não se preocupa com a quantidade de passos, mas com o custo total
Se o custo de todos os passos são iguais, então ela é igual a BFS
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
    queue = deque()  # fila de nós a serem explorados
    explored_states = []  # lista de estados já explorados

    if node.is_objective_node(): # se o nó é o nó objetivo
        return node.print_path()  # solução encontrada -> imprime caminho 

    queue.append(node) # adiciona raíz na fila

    while (True):
        if not queue:  # fila vazia
            return "FAILED"

        node = queue.popleft()  # retira elemento da fila -> FIFO
        explored_states.append(node.state) # coloca na lista de estados explorados

        for child in node.children(): # percorre os nós 
            if child.state not in explored_states and child not in queue: # se não está na lista de nós explorados e não está na fila
                if child.is_objective_node(): # se o nó é o nó objetivo
                    return child.print_path()  # solução encontrada no filho -> imprime caminho

                queue.append(child) # adciona nó na fila


# Busca em profundidade.

def depth_first():
    node = Node(initial_state, None)  # estado inicial
    stack = deque()   # pilha de nós a serem explorados
    explored_states = []  # lista de estados explorados
   
    if node.is_objective_node(): # se o nó é o nó objetivo
        return node.print_path()  # solução encontrada -> imprime caminho 

    stack.append(node) # adiciona raíz na pilha

    while (True):
        if not stack:  # pilha vazia
            return "FAILED"
            
        node = stack.pop()  # remoção LIFO
        explored_states.append(node.state) # coloca na lista de estados explorados

        for child in node.children(): # percorre os nós 
            if child.state not in explored_states and child not in stack: # se não está na lista de nós explorados e não está na pilha
                if child.is_objective_node(): # se o nó é o nó objetivo
                    return child.print_path()  # solução encontrada no filho -> imprime caminho

                stack.append(child) # adciona nó na pilha

# Busca de Custo Uniforme

def uniform_cost():
	node = Node(initial_state, None) # estado inicial
	cost_value = 0
	
	priority_queue = {} # fila de nós e suas prioridades
	priority_queue[node] = 0 # nó raiz assume propriedade 0
	explored_states = [] # lista de estados já explorados
	
	while(True):
		if not priority_queue: # fila de prioridade vazia
			return "FAILED"
		
		# busca na fila o nó com prioridade menor
		min_priority = float('inf')
		min_node = None
		
		for n in priority_queue: # percorre a fila de prioridades
			if priority_queue[n] < min_priority: # se o nó visitado tem prioridade menor que a menor prioridade
				min_priority = priority_queue[n] # menor prioridade é igual a prioridade do nó visitado
				min_node = n # nó de menor prioridade é igual ao nó visitado
		
		node = min_node # nó recebe o nó de menor prioridade
		del priority_queue[min_node] # remove o nó de menor prioridade da fila de prioridades
		
		if node.is_objective_node(): # se o nó é o nó objetivo
			return node.print_path() # solução encontrada -> imprime caminho
		  
		explored_states.append(node.state) # coloca na lista de estados explorados
		
		for child in node.children(): # percorre os nós
			cost_value += 1 # aumenta o valor de custo a cada nó 
			
			if child.state not in explored_states and child not in priority_queue: # se não está na lista de nós explorados e não está na fila de prioridade
				priority_queue[child] = cost_value # recebe o valor de custo
			
			elif child in priority_queue and priority_queue[child] > cost_value: # se está na fila de prioridade e o valor de custo do nó é maior que o valor de custo
				priority_queue[child] = cost_value # recebe o valor de custo
 
print("\nBusca em largura:")
print("\n")
print("Caminho:")
breadth_first()


print("\n#########################################################################################################")


print("\nBusca em profundidade:")
print("\n")
print("Caminho:")
depth_first()


print("\n#########################################################################################################")


print("\nBusca de custo uniforme:")
print("\n")
print("Caminho:")
uniform_cost()

print("\n")
