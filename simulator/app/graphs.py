from pyvis.network import Network

def run_automatic():
    global net

    global turn_count
    global red_count
    global colored_count

    # So. for the moment the easiest upper limit on turns is the size of the graph ^ size of the graph
    # This covers the worst case where it is somehow optimal to route through the entire graph every single time
    # you need to color a vertex
    # But- we can add a termination tracker for red count, and when the game is finished, and we can front load
    # so probably we'll never reach a strategy of size^size

    best_strategy = []
    best_support = float("inf")
    best_strat_red = float("inf")
    best_strat_turn = float("inf")

    for starting_vertex in net.get_nodes():
        current_strategy = []
        turn_count = 0
        red_count = 0
        colored_count = 0
        support = 0

        # But rn this will only evaluate one strategy, we need to find a way to feed it all possible combos still
        while not check_completion() and support < best_support:
            current_strategy.append([])

            support = turn_count + red_count

        
        net.neighbors(starting_vertex)

    optimal_strategy = {
        "support":best_support,
        "turn":best_strat_turn,
        "red":best_strat_red,
        "strategy":best_strategy
    }
    return optimal_strategy

def init_globals():
    global turn_count
    global red_count
    global colored_count
    global instructions_history

    turn_count = 0
    red_count = 0
    colored_count = 0
    instructions_history = []

def color_node(node_idx):
    global net
    net.nodes[node_idx]['color'] = '#0b22b8'
    net.save_graph("app/templates/pik_graph.html")

def check_step(step_instructions):
    global net

    # Assume valid until proven invalid
    step_valid = True

    all_nodes = net.get_nodes()
    for node_idx in all_nodes:
        if step_instructions[0] in net.get_node(node_idx)['label']:
            print("Neighbors ", net.neighbors(node_idx))
            print("Cur node ", node_idx)
            print("Movement ", int(step_instructions[1])-1)
            if (int(step_instructions[1])-1) not in net.neighbors(node_idx) and (int(step_instructions[1])-1) != node_idx: 
                step_valid = False
    
    if step_instructions[2] == "red" or step_instructions[2] == "blue":
        if net.nodes[(int(step_instructions[1])-1)]['color'] != '#f7f7f5':
            step_valid = False

    print(step_valid)
    return step_valid

def execute_step(step_instructions):
    global net
    global red_count
    global colored_count
    global pik_pop

    all_nodes = net.get_nodes()
    for node_idx in all_nodes:
        if step_instructions[0] in net.get_node(node_idx)['label'] :
            net.get_node(node_idx)['label'] = net.get_node(node_idx)['label'].replace(step_instructions[0], '')
            net.get_node(node_idx)['label'] = net.get_node(node_idx)['label'].strip()
        
        if net.nodes[node_idx]['title'] == str(step_instructions[1]):
            new_node_idx = node_idx
            net.get_node(new_node_idx)['label'] += " " + step_instructions[0]
            net.get_node(new_node_idx)['label'] = net.get_node(new_node_idx)['label'].strip()
    
    if step_instructions[2] == "red":
        #print("Ran red")
        net.nodes[new_node_idx]['color'] = '#f61709'
        new_pik_name = "Pik " + str(len(pik_pop)+1)
        net.nodes[new_node_idx]['label'] += " " + new_pik_name
        net.get_node(new_node_idx)['label'] = net.get_node(new_node_idx)['label'].strip()

        pik_pop.append(new_pik_name)

        red_count += 1
        colored_count += 1
    elif step_instructions[2] == "blue":
        #print("Ran blue")
        net.nodes[new_node_idx]['color'] = '#091df6'
        colored_count += 1

    net.save_graph("app/templates/pik_graph.html")

def check_completion():
    all_nodes = net.get_nodes()
    complete = True
    for node_idx in all_nodes:
        # If any node is colored grey, the game is not complete
        if net.nodes[node_idx]['color'] == '#f7f7f5':
            complete = False
    return complete

def glimpse_network(): 
    net.show_buttons(['manipulation'])
    net.show("gameofthrones.html", notebook=False)

def load_n_node(n):
    net = Network()
    net.add_nodes(range(n))
    #for i in range(n):
    #    net.add_nodes([str(i)],color=['#222222'])
    net.save_graph("app/templates/pik_graph.html")    
    return n

def init_pik(init_idx):
    global net
    global turn_count

    turn_count = 0

    if init_idx != 0:
        init_idx = init_idx - 1

    # Clear out the labels of everything in the graph
    for node_idx in range(len(net.get_nodes())):
        net.nodes[node_idx]['label'] = ''

    # Iniatlize the node we want with the label
    net.nodes[init_idx]['label'] = 'Pik 1'
    
    net.save_graph("app/templates/pik_graph.html")   

    print(net.get_node(init_idx)["label"])
    set_pik_pop([net.get_node(init_idx)["label"]])
    return([net.get_node(init_idx)["label"]])
    #net.nodes[node_idx]['color'] = '#0b22b8'

def move_pik(cur_pik, move_loc):
    global net

    # Clear out the labels of everything in the graph
    for node_idx in range(len(net.get_nodes())):
        if net.nodes[node_idx]['label'] == cur_pik:
            net.nodes[node_idx]['label'] = ""

    # Iniatlize the node we want with the label
    net.nodes[move_loc]['label'] = cur_pik
    
    net.save_graph("app/templates/pik_graph.html")   

def load_path(n):
    global net
    net = Network()
    net.add_nodes(range(n))
    for node_idx in range(n):
        net.nodes[node_idx]['color'] = '#f7f7f5'
        net.nodes[node_idx]['title'] = str(node_idx+1)
        if node_idx > 0:
            net.add_edge((node_idx-1),node_idx)
    net.save_graph("app/templates/pik_graph.html")    
    init_globals()
    return n

def load_cycle(n):
    global net
    net = Network()
    net.add_nodes(range(n))
    for node_idx in range(n):
        net.nodes[node_idx]['color'] = '#f7f7f5'
        net.nodes[node_idx]['title'] = str(node_idx+1)
        if n > 1:
            net.add_edge(node_idx%n,(node_idx+1)%n)
    net.save_graph("app/templates/pik_graph.html")    
    init_globals()
    return n

def load_star(n):
    global net
    net = Network()
    net.add_nodes(range(n))
    for node_idx in range(n):
        net.nodes[node_idx]['color'] = '#f7f7f5'
        net.nodes[node_idx]['title'] = str(node_idx+1)
        if node_idx > 0:
            net.add_edge(0,node_idx)
    net.save_graph("app/templates/pik_graph.html")   
    init_globals() 
    return n

def load_wheel(n):
    global net
    net = Network()
    net.add_nodes(range(n))
    for node_idx in range(n):
        net.nodes[node_idx]['color'] = '#f7f7f5'
        net.nodes[node_idx]['title'] = str(node_idx+1)
        if node_idx > 0:
            net.add_edge(0,node_idx)
        if n > 2:
            if ((node_idx+1)%n) == 0:
                net.add_edge(node_idx%n,1)
            else: 
                net.add_edge(node_idx%n,(node_idx+1)%n)
    net.save_graph("app/templates/pik_graph.html")  
    init_globals()  
    return n

def load_complete(n):
    global net
    net = Network()
    net.add_nodes(range(n))
    for node_idx in range(n):
        net.nodes[node_idx]['color'] = '#f7f7f5'
        net.nodes[node_idx]['title'] = str(node_idx+1)
        for node_idx_secondary in net.get_nodes():
            if node_idx_secondary != node_idx:
                net.add_edge(node_idx,node_idx_secondary)
    net.save_graph("app/templates/pik_graph.html")    
    init_globals()
    return n

def set_turn(turn):
    global turn_count
    turn_count += turn
    return turn_count

def increment_turn():
    global turn_count
    turn_count += 1
    return turn_count

def set_pik_pop(new_pik_pop):
    global pik_pop
    pik_pop = new_pik_pop
    return pik_pop

def fetch_pik_pop():
    try:
        return pik_pop
    except:
        return ['']

def fetch_red_count():
    try:
        return red_count
    except:
        return 0
    
def fetch_colored_count():
    try:
        return colored_count
    except:
        return 0
    
def fetch_instructions_history():
    try:
        return instructions_history
    except:
        return []
    
def fetch_size():
    try:
        return len(net.get_nodes())
    except:
        return 0
    
def fetch_turn():
    try:
        return turn_count
    except:
        return 0

def fetch_net():
    try:
        return net
    except:
        return 

def init_net():
    global net 
    net = Network()
    return net