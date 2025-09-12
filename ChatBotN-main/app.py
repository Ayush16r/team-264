from flask import Flask, render_template, request, jsonify
import pandas as pd
import aiml, os, re
from difflib import get_close_matches

app = Flask(__name__, template_folder="templates")

DATA_FILE = "data.csv"
AIML_FILE = "symptoms.aiml"

# --- Load + Clean CSV ---
df = pd.read_csv(DATA_FILE)

# Ensure clean strings
df["symptom"] = (
    df["symptom"]
    .astype(str)
    .str.strip()
    .str.strip('"')
    .str.strip("'")
    .str.lower()
)
df["conditions"] = (
    df["conditions"]
    .astype(str)
    .str.strip()
    .str.strip('"')
    .str.strip("'")
    .str.title()
)
df["department"] = (
    df["department"]
    .astype(str)
    .str.strip()
    .str.strip('"')
    .str.strip("'")
    .str.title()
)

# Group duplicate symptoms → merge conditions + department
df = (
    df.groupby("symptom")
    .agg({
        "conditions": lambda x: ", ".join(sorted(set(", ".join(x).split(", ")))),
        "department": lambda x: ", ".join(sorted(set(", ".join(x).split(", "))))
    })
    .reset_index()
)

# Dictionary for fast lookup
symptom_data = {
    row["symptom"]: {
        "conditions": row["conditions"].split(", "),
        "department": row["department"].split(", ")
    }
    for _, row in df.iterrows()
}

print("✅ Symptoms loaded:", len(symptom_data))
print("🔍 Example symptoms:", list(symptom_data.keys())[:20])

# --- AIML Kernel ---
kernel = aiml.Kernel()
if os.path.exists(AIML_FILE):
    kernel.learn(AIML_FILE)
    print("✅ AIML loaded")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").lower().strip()
    user_input = user_input.strip('"').strip("'")  # clean user input
    reply = []

    # 1️⃣ Word-based exact match
    words = re.findall(r"\b\w+\b", user_input)
    for word in words:
        word = word.strip().lower()
        if word in symptom_data:
            conditions = ", ".join(symptom_data[word]["conditions"])
            departments = ", ".join(symptom_data[word]["department"])
            reply.append(
                f"🤖 Based on your symptom '{word}':\n   Possible Condition(s): {conditions}\n   Department to Consult: {departments}"
            )

    # 2️⃣ Fuzzy match
    if not reply:
        matches = get_close_matches(user_input, symptom_data.keys(), n=1, cutoff=0.8)
        if matches:
            match = matches[0]
            conditions = ", ".join(symptom_data[match]["conditions"])
            departments = ", ".join(symptom_data[match]["department"])
            reply.append(
                f"🤖 Based on your symptom '{match}':\n   Possible Condition(s): {conditions}\n   Department to Consult: {departments}"
            )

    # 3️⃣ AIML fallback
    if not reply:
        response = kernel.respond(user_input.upper())
        reply.append(response if response else "🤖 I’m not sure. Please consult a doctor.")

    return jsonify({"reply": " | ".join(dict.fromkeys(reply))})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
