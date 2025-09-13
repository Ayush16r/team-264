🏥 HealX – Smart Appointment & Patient Dashboard

HealX is a full-stack hospital appointment & patient management system built with Flask, MongoDB, TailwindCSS, and JavaScript.
It provides a live-updating patient dashboard, appointment booking system, admin panel for staff, and an integrated AI chat assistant.

🚀 Features
👨‍⚕️ Patient Dashboard

Live updates on patient queue.

Booking ID search to see slot, name, and estimated waiting time.

Sidebar with quick access: Hospitals near me, Medicine bar, Visit notes, etc.

📅 Appointment Booking

Patients can book appointments with name, department, and slot.

Stores data in MongoDB Atlas.

Auto-generates a unique Booking ID.

🔑 Admin Dashboard

View all booked appointments.

Track status (pending, completed).

See live queue order with estimated wait times.

🤖 AI Chatbox

Integrated AI assistant to answer medical queries.

Chat UI connected with backend endpoint.

🛠️ Tech Stack

Backend: Flask (Python)

Database: MongoDB Atlas

Frontend: HTML, TailwindCSS, JavaScript

Integration: Flask APIs + Fetch (AJAX)

AI Assistant: Flask endpoint + chat frontend



⚙️ Setup Instructions
1️⃣ Clone Repo
git clone https://github.com/Ayush16r/team-264
cd healx

2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # Mac/Linux

3️⃣ Install Dependencies
pip install flask pymongo

4️⃣ Configure MongoDB

Update user.py with your MongoDB URI:

MONGO_URI = "mongodb+srv://ayush16r:Ayush16r@healxtrail.nlpleiz.mongodb.net/?retryWrites=true&w=majority&appName=HealXtrail"

5️⃣ Run the App
python user.py


Visit 👉 http://127.0.0.1:5000/

🌐 Routes
Route	Description
/	Patient Dashboard
/book	Book an Appointment

from url - https://medifind-dtfh.onrender.com 
   or 
   appointment booking server local host
     
     sugested do from url 

/admin	Admin Dashboard
/chat	AI Chatbox
/get_booking	API to fetch booking info by ID
📊 Usage Flow

Patient books appointment via /book.

Booking goes into MongoDB with unique Booking ID.

Patient checks live updates via /.

Admin monitors queue via /admin.

AI Chatbox (/chat) assists patients with FAQs.


🔥 HealX – Helping People, Saving Lives


step 1 - vist dashboard 
![alt text](image.png)

step 2 - click on live appointment 
                and book appointment 

 step 3-            ( on search location must use 
                      Bhubaneswar OR downtown )

                     
![alt text](image-1.png)
                     
step 3-              copy booking id


 step 4 -           search in dashboard
 ![alt text](image-2.png)



 thank you  
