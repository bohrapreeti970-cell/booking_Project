import streamlit as st
place_price = st.number_input("Price (INR)", min_value=0.0, format="%.2f")
submit_place = st.form_submit_button("Add place")
if submit_place:
ok, msg = create_place(db, place_name.strip(), place_price)
if ok:
st.success(msg)
else:
st.error(msg)


with tab[2]:
st.subheader("Users")
users = list(db.users.find({}, {"password":0}).sort("created_at", -1))
if users:
for u in users:
st.write(u)
else:
st.info("No users yet.")


with tab[3]:
st.subheader("Places")
places = list_places(db)
if places:
for p in places:
st.write(p)
else:
st.info("No places yet.")


with tab[4]:
st.subheader("All Bookings")
bookings = get_all_bookings(db)
if bookings:
for b in bookings:
st.write(b)
else:
st.info("No bookings yet.")


else:
st.header("Book your trip")
st.markdown("Plan a trip in seconds — select a place and confirm booking.")


places = list_places(db)
if not places:
st.info("No places available yet. Ask admin to add places.")
else:
for p in places:
with st.expander(f"{p['name']} — ₹{p['price']:.2f}"):
st.write(f"**Price:** ₹{p['price']:.2f}")
if st.button(f"Book {p['name']}", key=f"book_{p['_id']}"):
booking = create_booking(db, st.session_state.username, p)
st.success(f"Booked {p['name']} — Booking ID: {booking['booking_id']}")


st.markdown("---")
st.subheader("Your booking history")
bookings = get_user_bookings(db, st.session_state.username)
if bookings:
for b in bookings:
st.write(b)
else:
st.info("You have no bookings yet.")
