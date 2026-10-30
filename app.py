from flask import Flask, request, jsonify
from flask_cors import CORS
from smartcrop import predict

app = Flask(__name__)
CORS(app)

# Land size mapping
LAND_SIZE_MAP = {
    "10–30 cent (Very small farms)": 1,
    "30–50 cent (small farms)": 2,
    "50–80 cent (medium farms)": 3,
    "80+ cent (large farms)": 4
}

@app.route("/predict", methods=["POST"])
def get_prediction():
    try:
        data = request.json or {}

        required = ["soil_type", "location", "previous_crop", "land_size"]
        for field in required:
            if field not in data or not str(data[field]).strip():
                return jsonify({"error": f"Missing field: {field}"}), 400

        # Convert land size category to number
        land_display = str(data["land_size"]).strip()
        if land_display in LAND_SIZE_MAP:
            data["land_size"] = LAND_SIZE_MAP[land_display]
        else:
            try:
                data["land_size"] = float(land_display)
            except ValueError:
                data["land_size"] = 3  # default medium

        result = predict(data)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)