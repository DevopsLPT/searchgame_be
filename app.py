from flask import Flask, request, jsonify, send_file
import time
import tracemalloc
from flask_cors import CORS
from utils.file_handler import read_file, write_file
from search_algorithm.a_star import a_star
from search_algorithm.ucs import ucs

def run_algo(input_file, output_file, algorithm_name):
    init_node, grid = read_file(input_file)
    algorithm_name = algorithm_name.upper()
    write_mode = "w"

    if algorithm_name == "ALL":
        algorithms = ["UCS", "A*"]
    else:
        algorithms = [algorithm_name]

    for algo in algorithms:
        init_time = time.time_ns()
        tracemalloc.start()

        if algo == "UCS":
            node_count, goal_node = ucs(init_node, grid)
        elif algo == "A*":
            node_count, goal_node = a_star(init_node, grid)

        elapsed_time = time.time_ns() - init_time
        _, memory_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        write_file(
            file_name=output_file,
            search_algo=algo,
            node_count=node_count, 
            goal_node=goal_node, 
            memory_used=memory_peak / 1000000, 
            elapsed_time=elapsed_time / 1000000,
            write_mode=write_mode
        )

        write_mode = "a"

app = Flask(__name__)
CORS(app)

@app.route('/api/run', methods=['POST'])
def execute_algorithm():
    algorithm = request.json.get('algorithm', 'BFS')  # Mặc định là BFS nếu không có
    input_file = request.json.get('input_file', 'input-01.txt')
    output_file = request.json.get('output_file', 'output-01.txt')

    input_path = './template/' + input_file
    output_path = './output/' + output_file

    try:
        run_algo(input_path, output_path, algorithm)
        with open(output_path, "r") as f:
           output_data = f.read()
        return jsonify({"output": output_data})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/download', methods=['POST'])
def download():
    algorithm = request.json.get('algorithm', 'BFS')  # Mặc định là BFS nếu không có
    input_file = request.json.get('input_file', 'input-01.txt')
    output_file = request.json.get('output_file', 'output-01.txt')

    input_path = './template/' + input_file
    output_path = './output/' + output_file

    run_algo(input_path, output_path, algorithm)
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  #
