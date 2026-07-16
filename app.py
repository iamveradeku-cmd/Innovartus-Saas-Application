"""
Innovartus — Fine Dining Restaurant
A lightweight, fully-functional Flask application.
"""

from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# ---------------------------------------------------------------------------
# In-memory "database" — swap for SQLite/Postgres when going to production.
# ---------------------------------------------------------------------------
RESERVATIONS = []

# The tasting menu is genuinely sequential (a chef's progression of courses),
# so numbering it communicates real information rather than decoration.
MENU = [
    {
        "course": "I",
        "name": "Amber Consommé",
        "description": "Slow-clarified beef broth, charred shallot, thyme oil.",
        "price": "$18",
    },
    {
        "course": "II",
        "name": "Hand-Cut Tuna",
        "description": "Yellowfin tartare, yuzu kosho, crisp nori, quail yolk.",
        "price": "$26",
    },
    {
        "course": "III",
        "name": "Roasted Duck Breast",
        "description": "Cherry gastrique, charred endive, duck-fat potato.",
        "price": "$42",
    },
    {
        "course": "IV",
        "name": "Dry-Aged Ribeye",
        "description": "28-day aged, bone marrow butter, red wine jus.",
        "price": "$58",
    },
    {
        "course": "V",
        "name": "Valrhona Dark Chocolate",
        "description": "Salted caramel core, cocoa nib tuile, gold leaf.",
        "price": "$16",
    },
]

TESTIMONIALS = [
    {"quote": "The most refined dining experience in the city.", "author": "The Weekly Table"},
    {"quote": "Every course feels considered, quiet, and intentional.", "author": "Gourmet Review"},
    {"quote": "Innovartus doesn't serve dinner — it stages an evening.", "author": "City & Palate"},
]

RESTAURANT_INFO = {
    "name": "Innovartus",
    "tagline": "Modern Fine Dining, Composed With Intent",
    "address": "12 Marbrook Lane, Downtown District",
    "phone": "+1 (555) 019-2847",
    "hours": [
        {"days": "Tuesday – Thursday", "time": "5:30 PM – 10:00 PM"},
        {"days": "Friday – Saturday", "time": "5:30 PM – 11:00 PM"},
        {"days": "Sunday – Monday", "time": "Closed"},
    ],
}


@app.route("/")
def home():
    """Render the single-page restaurant experience."""
    return render_template(
        "index.html",
        restaurant=RESTAURANT_INFO,
        menu=MENU,
        testimonials=TESTIMONIALS,
        year=datetime.now().year,
    )


@app.route("/api/reserve", methods=["POST"])
def reserve():
    """Accept a table reservation submitted via fetch() from scripts.js."""
    data = request.get_json(silent=True) or {}

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    phone = (data.get("phone") or "").strip()
    date = (data.get("date") or "").strip()
    time_ = (data.get("time") or "").strip()
    guests = (data.get("guests") or "").strip()

    errors = {}
    if len(name) < 2:
        errors["name"] = "Please enter your full name."
    if "@" not in email or "." not in email:
        errors["email"] = "Please enter a valid email address."
    if len(phone) < 7:
        errors["phone"] = "Please enter a valid phone number."
    if not date:
        errors["date"] = "Please choose a date."
    if not time_:
        errors["time"] = "Please choose a time."
    if not guests or not guests.isdigit() or int(guests) < 1:
        errors["guests"] = "Please enter the number of guests."

    if errors:
        return jsonify({"success": False, "errors": errors}), 400

    reservation = {
        "id": len(RESERVATIONS) + 1,
        "name": name,
        "email": email,
        "phone": phone,
        "date": date,
        "time": time_,
        "guests": guests,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    RESERVATIONS.append(reservation)

    return jsonify(
        {
            "success": True,
            "message": (
                f"Thank you, {name.split()[0]}. Your table for {guests} on "
                f"{date} at {time_} is confirmed. A confirmation email is on its way."
            ),
            "confirmation_id": reservation["id"],
        }
    )


@app.route("/api/reservations", methods=["GET"])
def list_reservations():
    """Simple admin-style endpoint to view bookings (for demo purposes)."""
    return jsonify({"count": len(RESERVATIONS), "reservations": RESERVATIONS})


if __name__ == "__main__":
    app.run(debug=True)
