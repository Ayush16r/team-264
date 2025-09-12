from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# ---------------- MongoDB Setup ----------------
MONGO_URI = "mongodb+srv://ayush16r:Ayush16r@healxtrail.nlpleiz.mongodb.net/?retryWrites=true&w=majority&appName=HealXtrail"
client = MongoClient(MONGO_URI)
db = client["medifind"]
bookings_col = db["bookings"]

# Expected time per department (minutes per patient)
DEPT_TIME = {
    "General Medicine": 4,
    "Orthopedics": 3,
    "ENT": 5,
    "Dermatology": 4
}

# ---------------- ROUTES ----------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/live-appointments")
def live_appointments():
    return render_template("live_appointments.html")

@app.route("/hospitals-near-me")
def hospitals_near_me():
    return render_template("hospitals_near_me.html")

@app.route("/med_box")
def med_box():
    return render_template("med_box.html")

@app.route("/feedback_reward")
def feedback_reward():
    return render_template("feedback_reward.html")
# ---------------- GET BOOKING WITH ESTIMATED WAIT ----------------
@app.route("/get_booking", methods=["POST"])
def get_booking():
    data = request.get_json()
    booking_id = data.get("bookingId") if data else None
    if not booking_id:
        return jsonify({"error": "No Booking ID provided"}), 400

    booking = bookings_col.find_one({"booking_id": booking_id})
    if not booking:
        return jsonify({"error": "Booking ID not found"}), 404

    department = booking.get("department", "General Medicine")
    per_patient_time = DEPT_TIME.get(department, 5)  # e.g., 5 mins default

    # Use created_at timestamp to count previous uncompleted bookings
    queue_count = bookings_col.count_documents({
        "department": department,
        "status": {"$ne": "completed"},
        "created_at": {"$lt": booking["created_at"]}
    })

    estimated_wait = queue_count * per_patient_time

    return jsonify({
        "slot": booking.get("appointment_time", ""),
        "name": booking.get("patient_name", ""),
        "estimated_wait": estimated_wait
    })


if __name__ == "__main__":
    app.run(debug=True)
