"""
app.py

Flask backend for the Page Replacement Simulator.

Routes:
    GET  /          -> Renders the main webpage (index.html)
    POST /simulate   -> Receives frames, reference string, and algorithm
                        from the frontend (JSON), runs the selected
                        algorithm from simulator.py, and returns the
                        results as JSON.
"""

import time
from flask import Flask, render_template, request, jsonify

from simulator import fifo, lru, optimal

app = Flask(__name__)

# Map the algorithm name coming from the frontend to the actual function.
ALGORITHMS = {
    "fifo": fifo,
    "lru": lru,
    "optimal": optimal
}


@app.route("/")
def index():
    """Render the homepage."""
    return render_template("index.html")


@app.route("/simulate", methods=["POST"])
def simulate():
    """
    Receives JSON data of the form:
        {
            "frames": 3,
            "reference_string": "7 0 1 2 0 3 0 4 2 3 0 3 2",
            "algorithm": "fifo"
        }

    Validates the input, runs the selected algorithm, and returns the
    simulation result as JSON.
    """
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid or missing JSON data."}), 400

    algorithm = data.get("algorithm", "").strip().lower()
    frames_raw = data.get("frames")
    reference_raw = data.get("reference_string", "")

    # --- Validate algorithm ---
    if algorithm not in ALGORITHMS:
        return jsonify({"error": "Invalid algorithm selected."}), 400

    # --- Validate frames ---
    try:
        frames = int(frames_raw)
    except (TypeError, ValueError):
        return jsonify({"error": "Number of frames must be a valid integer."}), 400

    if frames <= 0:
        return jsonify({"error": "Number of frames must be greater than 0."}), 400

    # --- Validate reference string ---
    if not reference_raw or not str(reference_raw).strip():
        return jsonify({"error": "Reference string cannot be empty."}), 400

    raw_tokens = str(reference_raw).strip().split()

    reference_string = []
    for token in raw_tokens:
        if not token.lstrip("-").isdigit():
            return jsonify({
                "error": f"Invalid character '{token}' found in reference string. "
                         f"Only whole numbers separated by spaces are allowed."
            }), 400
        reference_string.append(int(token))

    if len(reference_string) == 0:
        return jsonify({"error": "Reference string must contain at least one page."}), 400

    # --- Run the selected algorithm and measure execution time ---
    start_time = time.perf_counter()
    result = ALGORITHMS[algorithm](reference_string, frames)
    end_time = time.perf_counter()

    execution_time_ms = round((end_time - start_time) * 1000, 4)

    result["execution_time_ms"] = execution_time_ms
    result["algorithm"] = algorithm
    result["frames"] = frames
    result["reference_string"] = reference_string

    return jsonify(result), 200


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
