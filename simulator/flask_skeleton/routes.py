from flask import Flask, request, render_template, session
from pyvis.network import Network
from main import app
import graphs



@app.route('/', methods=['POST', 'GET'])
def index():
    net = graphs.fetch_net()
    pik_pop = []
    
    if not net:
        net = graphs.init_net()
        session["node_count"] = 0
        session["turn_number"] = 0
        session["pik_pop"] = ['']
        session["active_pikmin_controller"] = []
        session["red_count"] = 0
        session["colored_count"] = 0
        session["instructions_history"] = []
        session["game_complete"] = False
        node_count = 0
        turn_number = 0
        pik_pop = ['']
        active_pikmin_controller = []
        red_count = 0
        colored_count = 0
        instructions_history = []
        game_complete = False
        turn_validity_error = ""
    else:
        node_count = graphs.fetch_size()
        turn_number = graphs.fetch_turn()
        pik_pop = graphs.fetch_pik_pop()
        instructions_history = graphs.fetch_instructions_history()
        red_count = graphs.fetch_red_count()
        colored_count = graphs.fetch_colored_count()
        game_complete = graphs.check_completion()
        turn_validity_error = ""

        active_pikmin_controller = []
        
        if pik_pop != ['']:
            for pikmin in pik_pop:
                active_pikmin_controller.append([pikmin,"pikmin_move_selector_"+pikmin.replace(" ", "_"),"pikmin_color_selector_"+pikmin.replace(" ", "_")])



    if request.method == "POST":
        # Form Values
        default_size = '1'
        size = request.form.get('input_size', default_size)

        default_pos = '0'
        init_pos = request.form.get('input_pik_pos', default_pos)

        default_graph_family = 'Path'
        init_graph_family = request.form.get('input_graph_family', default_graph_family)

        # Collect Input from the manual instructions
        # Input should be in the form [["Pik n","v","red"]]
        pikmin_total_instructions = []
        for pik_movement_input_form in active_pikmin_controller:
            pikmin_i_instructions = []
            pikmin_i_instructions.append(pik_movement_input_form[0])
            pikmin_i_instructions.append(request.form.get(pik_movement_input_form[1]))
            pikmin_i_instructions.append(request.form.get(pik_movement_input_form[2]))
            pikmin_total_instructions.append(pikmin_i_instructions)
        #print("Pik Instructions: ", pikmin_total_instructions)


        # Submit Buttons
        add_node = request.form.get('add_node', None)
        init_pik = request.form.get('init_pik', None)
        init_graph = request.form.get('init_graph', None)
        run_automatic = request.form.get('run_automatic', None)
        execute_turn = request.form.get('execute_turn', None)

        if run_automatic:
            graphs.run_automatic()
        elif init_pik:
            pik_pop = graphs.init_pik(int(init_pos))
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
            
            graphs.set_pik_pop([''])

            node_count = graphs.fetch_size()   
        elif execute_turn:
            turn_valid = True
            for pikmin_step in pikmin_total_instructions:
                if not graphs.check_step(pikmin_step):
                    turn_valid = False

            # Only execute the turn if the turn was valid
            if turn_valid:
                turn_validity_error = ""
                for pikmin_step in pikmin_total_instructions:
                    graphs.execute_step(pikmin_step)

                instructions_history.append([turn_number,pikmin_total_instructions])
                turn_number = graphs.increment_turn()
                pik_pop = graphs.fetch_pik_pop()
                red_count = graphs.fetch_red_count()
                colored_count = graphs.fetch_colored_count()
            else:
                turn_validity_error = "Error: At least one action selected was invalid. Please correct the instructions and try inputting the turn again"
        game_complete = graphs.check_completion()
        print("Game Complete? ", game_complete)

        # Pikmin Movement
        default_move_pos = ''
        default_pik = ""
        cur_pik = request.form.get("pik_select", default_pik)
        move_loc = request.form.get("input_pik_move", default_move_pos)
        #graphs.move_pik(cur_pik,int(move_loc))

        # Update the options again at the end of an input in the likely case that something changed
        active_pikmin_controller = []
        if pik_pop != ['']:
            for pikmin in pik_pop:
                active_pikmin_controller.append([pikmin,"pikmin_move_selector_"+pikmin.replace(" ", "_"),"pikmin_color_selector_"+pikmin.replace(" ", "_")])
        print(" Active Pikmin Controller ", active_pikmin_controller)
        
        
        

    return render_template('pik_sim.html', graph_size = node_count, pikmin_agents_control = active_pikmin_controller, graph_vertices=range(node_count), turn_number=turn_number, red_count = red_count, colored_count = colored_count, instructions_history=instructions_history, game_complete=game_complete,turn_validity_error=turn_validity_error)