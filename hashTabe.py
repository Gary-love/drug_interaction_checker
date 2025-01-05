from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# HashTable class from the uploaded file
class HashTable:
    def __init__(self, size=3):
        self.data_map = [None] * size

    def custom_hash(self, key):
        if key == "danger":
            return 0
        elif key == "mild":
            return 1
        elif key == "safe":
            return 2
        else:
            raise ValueError(f"Invalid key: {key}. Allowed keys are 'danger', 'mild', and 'safe'.")

    def set_item(self, key, drug1, drug2):
        index = self.custom_hash(key)
        if self.data_map[index] is None:
            self.data_map[index] = []
        self.data_map[index].append([key, drug1, drug2])

    def find_all_drug_interactions(self, drug):
        interactions = {"danger": [], "mild": [], "safe": []}

        for i in range(len(self.data_map)):
            if self.data_map[i] is not None:
                for interaction in self.data_map[i]:
                    if drug in interaction[1:]:
                        interactions[interaction[0]].append(interaction[1:])

        return interactions

    def find_interactions_between_two_drugs(self, drug1, drug2):
        for i in range(len(self.data_map)):
            if self.data_map[i] is not None:
                for interaction in self.data_map[i]:
                    if (interaction[1] == drug1 and interaction[2] == drug2) or \
                       (interaction[1] == drug2 and interaction[2] == drug1):
                        return {"interaction": interaction[0]}

        return {"interaction": "none"}

# Initialize HashTable with data
myhash = HashTable()
myhash.set_item("danger", "Warfarin", "Aspirin")
myhash.set_item("danger", "Cisapride", "Erythromycin")
myhash.set_item("mild", "Ibuprofen", "Losartan")
myhash.set_item("safe", "Paracetamol", "Ibuprofen")

# Flask Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/find_interaction", methods=["GET"])
def find_interaction():
    drug = request.args.get("drug")
    if not drug:
        return jsonify({"error": "No drug specified"}), 400
    interactions = myhash.find_all_drug_interactions(drug)
    return jsonify(interactions)

@app.route("/check_two_drugs", methods=["GET"])
def check_two_drugs():
    drug1 = request.args.get("drug1")
    drug2 = request.args.get("drug2")
    if not drug1 or not drug2:
        return jsonify({"error": "Two drugs must be specified"}), 400
    result = myhash.find_interactions_between_two_drugs(drug1, drug2)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
