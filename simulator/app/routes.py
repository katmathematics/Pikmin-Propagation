from flask import Flask, request, render_template, session
from pyvis.network import Network
from app import app
from app import graphs



@app.route('/', methods=['POST', 'GET'])
def index():
    net = graphs.fetch_net()
    pik_pop = []

    
    if not net:
        graphs.init_net()
        node_count = 0
    else:
        node_count = graphs.fetch_size()


    if request.method == "POST":
        # Form Values
        default_size = '1'
        size = request.form.get('input_size', default_size)

        default_pos = '0'
        init_pos = request.form.get('input_pik_pos', default_pos)

        default_graph_family = 'Path'
        init_graph_family = request.form.get('input_graph_family', default_graph_family)

        # Submit Buttons
        add_node = request.form.get('add_node', None)
        init_pik = request.form.get('init_pik', None)
        init_graph = request.form.get('init_graph', None)
        run_automatic = request.form.get('run_automatic', None)

        if run_automatic:
            graphs.run_automatic()
        elif init_pik:
            pik_pop = graphs.init_pik(int(init_pos))
            print(pik_pop)
        elif init_graph:
            if init_graph_family == "path": 
                graphs.load_path(int(size))
            elif init_graph_family == "cycle":    
                graphs.load_cycle(int(size))
            elif init_graph_family == "star":    
                graphs.load_star(int(size))
            elif init_graph_family == "wheel":    
                graphs.load_wheel(int(size))
            elif init_graph_family == "complete":    
                graphs.load_complete(int(size))

            node_count = graphs.fetch_size()   

        # Pikmin Movement
   
        default_move_pos = ''
        default_pik = ""
        cur_pik = request.form.get("pik_select", default_pik)
        move_loc = request.form.get("input_pik_move", default_move_pos)
        #graphs.move_pik(cur_pik,int(move_loc))

    return render_template('pik_sim.html', graph_size = node_count, pikmin_agents = pik_pop)