import matplotlib.pyplot as plt 
import networkx as nx 

def open_file(fileName):
    with open(fileName) as file : 
        lines = file.readlines()

    matrix= []
    for line in lines[:-3]:
        line = line.strip().split('->')
        src = line[0]
        wieght, dest = line[1].strip('()').split(',')

        matrix.append(list(map(int, (src, wieght, dest))))
    return matrix, lines


def make_adjacency_matrix(matrix, alpha):
    try:
        nodes = set()
        for line in matrix:
            nodes.add(line[0])

        len_nodes = len(nodes)

        adjancy_matrix = []
        for _ in range(len_nodes):
            x = []
            for _ in range(len_nodes):
                x.append(-1)
            adjancy_matrix.append(x)

        for line in matrix: # matrix: [ line: [src, weight, dest] ]
            if adjancy_matrix[line[0]][line[2]] == -1:
                adjancy_matrix[line[0]][line[2]] = line[1]

            elif adjancy_matrix[line[0]][line[2]] in alpha:
                adjancy_matrix[line[0]][line[2]]= [adjancy_matrix[line[0]][line[2]], line[1]]
            else:
                exit(f'Problem in line 48  def make_adjancy_matrix')
    
        return adjancy_matrix
    except:
        exit('File Erorr \nmake_adjacency_matrix()')


def draw_dfa(matrix, start, finals):
    G = nx.MultiDiGraph()

    # Add edges with labels
    for src, weight, dest in matrix:
        G.add_edge(src, dest, label=str(weight))

    # Generate positions for nodes
    pos = nx.spring_layout(G, seed=2)

    # Draw nodes
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color="skyblue", font_size=15, font_weight="bold", arrowsize=20)

    # Create edge labels
    edge_labels = {}
    for src, dest, key, data in G.edges(keys=True, data=True):
        label = data['label']
        if (src, dest) in edge_labels:
            edge_labels[(src, dest)] += f", {label}"
        else:
            edge_labels[(src, dest)] = label

    # Draw edge labels
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

    # Highlight the start node
    nx.draw_networkx_nodes(G, pos, nodelist=[start], node_color='green', node_size=900)

    # Highlight final nodes with double circles
    nx.draw_networkx_nodes(G, pos, nodelist=finals, node_color='skyblue', node_size=1000, edgecolors='blue')
    nx.draw_networkx_nodes(G, pos, nodelist=finals, node_color='skyblue', node_size=800, edgecolors='blue')

    # Handle self-loops separately
    for node in G.nodes():
        if G.has_edge(node, node):
            loop_edge = (node, node)
            nx.draw_networkx_edges(G, pos, edgelist=[loop_edge], connectionstyle='arc3, rad=0.4', arrows=True)
            loop_label = {loop_edge: edge_labels[loop_edge]}
            offset_pos = {k: (v[0], v[1] + 0.1) for k, v in pos.items()}  # Adjust label position slightly
            nx.draw_networkx_edge_labels(G, offset_pos, edge_labels=loop_label, font_color='red')

    plt.show()


def alpha_check(adjacency_matrix, alpha): # all nodes noeed to use all alphas    
    def flatten(row):
        flat_list = []
        for item in row:
            if isinstance(item, list):
                flat_list.extend(item)
            else:
                flat_list.append(item)
        return flat_list

    for row in adjacency_matrix:
        flat_row = flatten(row)
        if not all(item in flat_row for item in alpha):
            exit(f'ERORR on adjacency_matrix row :\n {row}\nalpha_check()')


def remove_unreachable_nodes(matrix, alpha, start):
    nodes_src = set()
    nodes_dest = set()
    for row in matrix:
        if row[1] not in alpha:
            exit(f'ERORR!\n{row[1]} not in alpha= {alpha}')

        nodes_src.add(row[0]) # row[0] is src 
        nodes_dest.add(row[-1]) # row[-1] is dest

    nodes_src.remove(start) # all the src nodes 

    bad_nodes = nodes_src - nodes_dest

    nodes_src -= bad_nodes
    for node in list(nodes_dest - nodes_src):        
        bad_nodes.add(node)
    
    if len(bad_nodes) > 0:
        print(f'{bad_nodes} was removed')

        new_matrix = []
        for row in matrix:
            if not any(item in bad_nodes for item in row):
                new_matrix.append(row)

        return new_matrix
    
    else:
        return matrix


def finals_non_finals(matrix, finals):
    # Classify states into non-final and final states
    states = set()
    for trans in matrix:
        states.add(trans[0])
        states.add(trans[2])

        non_finals = []
        for state in states:
            if state not in finals:
                non_finals.append(state)

    return non_finals, finals


def get_transition_class(state, matrix, equivalence_classes, alpha):
    # Get the destination states for the given state for each alpha symbol
    transition_classes = []
    for symbol in alpha:
        destination = None
        for trans in matrix:
            if trans[0] == state and trans[1] == symbol:
                destination = trans[2]
                break
        
        # Find the equivalence class index of the transition destination
        if destination is None:
            transition_classes.append(-1)  # Use -1 to represent no transition
        else:
            for idx, eq_class in enumerate(equivalence_classes):
                if destination in eq_class:
                    transition_classes.append(idx)
                    break
    
    return transition_classes


def refine_equivalence_classes(matrix, finals, alpha):
    # Initial classification into non-final and final states
    non_finals, finals = finals_non_finals(matrix, finals)
    
    # Start with two equivalence classes: non-finals and finals
    equivalence_classes = [non_finals, finals]

    while True:
        new_classes = []

        for group in equivalence_classes:
            if len(group) <= 1:
                new_classes.append(group)
                continue

            refined_groups = {}
            
            for state in group:
                state_transitions = tuple(get_transition_class(state, matrix, equivalence_classes, alpha))
                
                if state_transitions not in refined_groups:
                    refined_groups[state_transitions] = []
                refined_groups[state_transitions].append(state)

            new_classes.extend(refined_groups.values())

        new_classes = [sorted(group) for group in new_classes]
        new_classes.sort()

        if new_classes == equivalence_classes:
            break

        equivalence_classes = new_classes

    return equivalence_classes


def write_transactions(equivalence_classes, matrix):
    transactions = []

    # Iterate over each equivalence class
    for group in equivalence_classes:
        for state in group:
            transitions = {}

            # Find transitions for the current state in the matrix
            for transition in matrix:
                if transition[0] == state:
                    symbol = transition[1]
                    next_state = transition[2]

                    # Add the next state to transitions dictionary for the current symbol
                    if symbol in transitions:
                        transitions[symbol].append(next_state)
                    else:
                        transitions[symbol] = [next_state]

            transactions.append((state, transitions))

    return transactions


def visualize_dfa_transactions(equivalence_classes, transactions):
    G = nx.DiGraph()

    # Add nodes for each equivalence class
    for group in equivalence_classes:
        G.add_node(tuple(group))

    # Add edges with labels based on transactions
    for state, transitions in transactions:
        current_group = None
        for group in equivalence_classes:
            if state in group:
                current_group = tuple(group)
                break
        if current_group:
            for symbol, next_states in transitions.items():
                for next_state in next_states:
                    next_group = None
                    for group in equivalence_classes:
                        if next_state in group:
                            next_group = tuple(group)
                            break
                    if next_group:
                        G.add_edge(current_group, next_group, label=str(symbol))

    # Plot DFA graph
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)  # Positions nodes using Fruchterman-Reingold algorithm
    nx.draw(G, pos, with_labels=True, node_size=1500, node_color='skyblue', font_size=12, font_weight='bold', edge_color='gray')
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    
    plt.title('Minimized DFA Visualization')
    plt.show()


def main():
    # 1 open file and make a 2D matrix  
    matrix, lines = open_file('file.txt')
    start = int(lines[-3].strip())
    alpha = list(map(int, lines[-1].split(',')))
    finals = list(map(int, lines[-2].split(',')))

    # 2 show the dfa 
    draw_dfa(matrix, start, finals)
    # 3 check if dfa is logicly True.
    adjacency_matrix = make_adjacency_matrix(matrix, alpha)
    alpha_check(adjacency_matrix, alpha)
    shorten_matrix = remove_unreachable_nodes(matrix, alpha, start)
    # 4 remove extra nodes ... 
    equivalence_classes  = refine_equivalence_classes(shorten_matrix, finals, alpha)
    print('lat equivalence class: ', equivalence_classes)
    transactions = write_transactions(equivalence_classes, matrix)
    # 5 Visualize minimized dfa
    visualize_dfa_transactions(equivalence_classes, transactions)

if __name__ == '__main__':
    main()