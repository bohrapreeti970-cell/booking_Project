import streamlit as st

# Example placeholders for external functions (replace with your actual implementations)
def create_place(db, name, price):
    return True, f"Added {name} successfully!"  # dummy success message

def list_places(db):
    return [{"name": "Goa", "price": 5000}, {"name": "Manali", "price": 7000}]

def get_all_bookings(db):
    return [{"booking_id": "A123", "username": "preeti", "place_name": "Goa", "price": 5000}]

def create_booking(db, username, place_doc):
    return {"booking_id": "B456", "username": username, "place_name": place_doc["name"], "price": place_doc["price"]}

def get_user_bookings(db, username):
    return [{"booking_id": "B456", "place_name": "Goa", "price": 5000}]

db = None  # dummy db object for testing

# Simulate Streamlit tabs
tab = st.tabs(["Add Place", "Users", "Places", "Bookings"])

# ---------------------- TAB 1: Add Place ----------------------
with tab[0]:
    st.subheader("Add a place with price")
    with st.form("create_place_form"):
        place_name = st.text_input("Place name")
        place_price = st.number_input("Price (INR)", min_value=0.0, format="%.2f")
        submit_place = st.form_submit_button("Add place")

        if submit_place:
            ok, msg = create_place(db, place_name.strip(), place_price)
            if ok:
                st.success(msg)
            else:
                st.error(msg)

# ---------------------- TAB 2: Users ----------------------
with tab[1]:
    st.subheader("Users")
    users = list([{"username": "admin"}, {"username": "user1"}])  # dummy data
    if users:
        for u in users:
            st.write(u)
    else:
        st.info("No users yet.")

# ---------------------- TAB 3: Places ----------------------
with tab[2]:
    st.subheader("Places")
    places = list_places(db)
    if places:
        for p in places:
            st.write(p)
    else:
        st.info("No places yet.")

# ---------------------- TAB 4: All Bookings ----------------------
with tab[3]:
    st.subheader("All Bookings")
    bookings = get_all_bookings(db)
    if bookings:
        for b in bookings:
            st.write(b)
    else:
        st.info("No bookings yet.")

# ---------------------- USER BOOKING PAGE ----------------------
st.header("Book your trip")
st.markdown("Plan a trip in seconds — select a place and confirm booking.")

places = list_places(db)
if not places:
    st.info("No places available yet. Ask admin to add places.")
else:
    for p in places:
        with st.expander(f"{p['name']} — ₹{p['price']:.2f}"):
            st.write(f"**Price:** ₹{p['price']:.2f}")
            if st.button(f"Book {p['name']}", key=f"book_{p['name']}"):
                booking = create_booking(db, "test_user", p)
                st.success(f"Booked {p['name']} — Booking ID: {booking['booking_id']}")

st.markdown("---")
st.subheader("Your booking history")
bookings = get_user_bookings(db, "test_user")
if bookings:
    for b in bookings:
        st.write(b)
else:
    st.info("You have no bookings yet.")
