import streamlit as st
import uuid
from datetime import datetime

# Assume MongoDB collection is already connected:
# from pymongo import MongoClient
# client = MongoClient(st.secrets["mongo"]["url"])
# db = client["travel_app"]
# bookings_col = db["bookings"]

# Dummy session user (for testing)
if "user" not in st.session_state:
    st.session_state.user = {"user_id": "u123", "name": "Preeti"}

st.title("✈️ Wanderly Travel Booking")

# Fetch bookings (if user is logged in)
bookings = list(bookings_col.find()) if "bookings_col" in locals() else []

if bookings:
    for b in bookings:
        with st.expander(f"Booking {b.get('booking_id')} — {b.get('destination')} for {b.get('name')}"):
            st.write(b)
else:
    st.write("No bookings yet.")

# Booking form
st.header("Book your trip")
st.markdown(
    "<div class='card' style='padding:10px;background-color:#f0f2f6;border-radius:10px;'>"
    "Plan a trip in seconds — enter details and get an instant booking ID."
    "</div>",
    unsafe_allow_html=True,
)

with st.form("booking_form"):
    name = st.text_input("Full name", value=st.session_state.user.get("name"))
    email = st.text_input("Email")
    destination = st.selectbox(
        "Destination",
        ["Paris, France", "New York, USA", "Tokyo, Japan", "Bali, Indonesia", "Goa, India"]
    )
    depart = st.date_input("Depart date")
    ret = st.date_input("Return date")
    travelers = st.number_input("Number of travelers", min_value=1, max_value=10, value=1)
    travel_class = st.selectbox("Class", ["Economy", "Premium Economy", "Business", "First"])
    extras = st.multiselect("Extras", ["Hotel", "Airport Pickup", "Sightseeing", "Travel Insurance"])
    submit_book = st.form_submit_button("Book now")

if submit_book:
    # Basic validation
    if not email or depart > ret:
        st.error("Please provide a valid email and ensure return date is after depart date.")
    else:
        booking_id = str(uuid.uuid4())[:8]
        record = {
            "booking_id": booking_id,
            "user_id": st.session_state.user["user_id"],
            "name": name,
            "email": email,
            "destination": destination,
            "depart": depart.isoformat(),
            "return": ret.isoformat(),
            "travelers": int(travelers),
            "class": travel_class,
            "extras": extras,
            "created_at": datetime.utcnow(),
        }

        # Save to DB (only if Mongo collection exists)
        if "bookings_col" in locals():
            res = bookings_col.insert_one(record)

        st.success("Booking created — see confirmation below")

        # Output field
        st.markdown("### Booking confirmation")
        st.write(f"**Booking ID:** {booking_id}")
        st.write(f"**Destination:** {destination}")
        st.write(f"**Dates:** {depart} → {ret}")
        st.write(f"**Travelers:** {travelers}")
        st.write(f"**Class:** {travel_class}")
        if extras:
            st.write(f"**Extras:** {', '.join(extras)}")
        st.write(f"A confirmation email would normally be sent to {email} — (demo uses DB only)")

# Show user's bookings
st.markdown("---")
st.subheader("Your recent bookings")

if "bookings_col" in locals():
    my_bookings = list(
        bookings_col.find({"user_id": st.session_state.user["user_id"]}).sort("created_at", -1)
    )
else:
    my_bookings = []  # fallback for testing

if my_bookings:
    for b in my_bookings:
        st.markdown(f"**{b['booking_id']}** — {b['destination']} ({b['depart']} → {b['return']})")
else:
    st.info("You have no bookings yet.")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and MongoDB — Wanderly")
