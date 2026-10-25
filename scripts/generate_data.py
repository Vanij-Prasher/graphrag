import csv, os, json

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
S = f"{OUT}/structured"
U = f"{OUT}/unstructured"
os.makedirs(S, exist_ok=True)
os.makedirs(U, exist_ok=True)

# ---------------- HOTELS ----------------
# id, name, city, area, stars, guest_rating
hotels = [
    ("H01", "Sea Breeze Residency", "Mumbai", "Colaba", 4, 4.3),
    ("H02", "Marine Crest Hotel", "Mumbai", "Marine Drive", 5, 4.6),
    ("H03", "Andheri Transit Inn", "Mumbai", "Andheri East", 3, 3.9),
    ("H04", "Juhu Palm Suites", "Mumbai", "Juhu", 4, 4.1),
    ("H05", "Calangute Shores Resort", "Goa", "Calangute", 4, 4.4),
    ("H06", "Palolem Bay Huts", "Goa", "Palolem", 2, 4.2),
    ("H07", "Panjim Heritage Stay", "Goa", "Fontainhas, Panaji", 3, 4.5),
    ("H08", "Candolim Grand", "Goa", "Candolim", 5, 4.0),
    ("H09", "Pink City Haveli", "Jaipur", "Old City", 3, 4.6),
    ("H10", "Amber Fort View Hotel", "Jaipur", "Amer", 4, 4.2),
    ("H11", "Rajputana Palace Resort", "Jaipur", "Jagatpura", 5, 4.7),
    ("H12", "Jaipur Budget Stay", "Jaipur", "Sindhi Camp", 2, 3.6),
    ("H13", "Snow Peak Retreat", "Manali", "Old Manali", 3, 4.4),
    ("H14", "Solang Valley Lodge", "Manali", "Solang", 3, 4.0),
    ("H15", "Himalayan Pines Resort", "Manali", "Mall Road", 4, 4.5),
    ("H16", "Beas River Cottages", "Manali", "Vashisht", 2, 4.1),
    ("H17", "Lake Pichola Palace", "Udaipur", "Lal Ghat", 5, 4.8),
    ("H18", "Fateh Sagar Inn", "Udaipur", "Fateh Sagar", 3, 4.3),
    ("H19", "Udaipur Courtyard Stay", "Udaipur", "Hanuman Ghat", 2, 4.0),
    ("H20", "Aravalli Hills Resort", "Udaipur", "Badi", 4, 4.4),
]
H = {h[0]: h for h in hotels}

with open(f"{S}/hotels.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["hotel_id", "name", "city", "area", "star_rating", "guest_rating"])
    w.writerows(hotels)

# ---------------- ROOMS ----------------
# hotel_id -> list of (room_type, price_inr_per_night, max_guests)
rooms = {
    "H01": [("Standard Double", 6500, 2), ("Deluxe Sea View", 9200, 2), ("Family Room", 11800, 4)],
    "H02": [("Deluxe King", 14500, 2), ("Ocean Suite", 26000, 3)],
    "H03": [("Standard Twin", 3800, 2), ("Triple Room", 4900, 3)],
    "H04": [("Studio Suite", 7800, 2), ("Two-Bedroom Suite", 13500, 5)],
    "H05": [("Garden Room", 6200, 2), ("Pool Access Room", 8900, 2), ("Family Villa", 15500, 5)],
    "H06": [("Beach Hut", 2200, 2), ("Family Hut", 3400, 4)],
    "H07": [("Heritage Double", 4200, 2), ("Heritage Suite", 6800, 3)],
    "H08": [("Premier Room", 12500, 2), ("Grand Suite", 22000, 3), ("Pool Villa", 34000, 4)],
    "H09": [("Haveli Room", 3900, 2), ("Royal Chamber", 6200, 3)],
    "H10": [("Fort View Double", 5600, 2), ("Family Room", 8100, 4)],
    "H11": [("Palace Room", 13800, 2), ("Maharaja Suite", 29500, 4)],
    "H12": [("Economy Double", 1600, 2), ("Dormitory Bed", 650, 1)],
    "H13": [("Mountain View Room", 3600, 2), ("Attic Family Room", 5400, 4)],
    "H14": [("Valley Room", 3200, 2), ("Group Room", 5900, 6)],
    "H15": [("Pine Deluxe", 6900, 2), ("Cottage Suite", 10400, 4)],
    "H16": [("Riverside Cottage", 2500, 2), ("Family Cottage", 3900, 4)],
    "H17": [("Lake View Room", 18500, 2), ("Royal Lake Suite", 38000, 3)],
    "H18": [("Lake Facing Double", 4600, 2), ("Triple Room", 5800, 3)],
    "H19": [("Courtyard Double", 2100, 2), ("Shared Dorm Bed", 700, 1)],
    "H20": [("Hill View Room", 7200, 2), ("Family Suite", 11200, 4)],
}
with open(f"{S}/rooms.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["hotel_id", "room_type", "price_inr_per_night", "max_guests"])
    for hid, rs in rooms.items():
        for r in rs:
            w.writerow([hid, *r])

# ---------------- AMENITIES ----------------
amenities = {
    "H01": ["WiFi", "Restaurant", "Room Service", "Gym"],
    "H02": ["WiFi", "Pool", "Spa", "Gym", "Restaurant", "Bar", "Room Service", "Parking"],
    "H03": ["WiFi", "Airport Shuttle", "Restaurant", "Parking"],
    "H04": ["WiFi", "Pool", "Kitchenette", "Parking"],
    "H05": ["WiFi", "Pool", "Restaurant", "Bar", "Kids Play Area", "Parking"],
    "H06": ["WiFi", "Beach Access", "Restaurant"],
    "H07": ["WiFi", "Restaurant"],
    "H08": ["WiFi", "Pool", "Spa", "Gym", "Bar", "Beach Access", "Parking", "Restaurant"],
    "H09": ["WiFi", "Rooftop Restaurant"],
    "H10": ["WiFi", "Pool", "Restaurant", "Parking"],
    "H11": ["WiFi", "Pool", "Spa", "Gym", "Restaurant", "Bar", "Parking", "Kids Play Area"],
    "H12": ["WiFi"],
    "H13": ["WiFi", "Heating", "Bonfire", "Restaurant"],
    "H14": ["Heating", "Parking", "Restaurant"],
    "H15": ["WiFi", "Heating", "Spa", "Restaurant", "Parking", "Kids Play Area"],
    "H16": ["WiFi", "Heating", "Bonfire"],
    "H17": ["WiFi", "Pool", "Spa", "Restaurant", "Bar", "Boat Transfer"],
    "H18": ["WiFi", "Rooftop Restaurant", "Parking"],
    "H19": ["WiFi", "Rooftop Restaurant"],
    "H20": ["WiFi", "Pool", "Spa", "Restaurant", "Parking"],
}
with open(f"{S}/amenities.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["hotel_id", "amenity"])
    for hid, a in amenities.items():
        for x in a:
            w.writerow([hid, x])

# ---------------- ATTRACTIONS ----------------
attractions = [
    ("A01", "Gateway of India", "Mumbai", "Monument"),
    ("A02", "Marine Drive Promenade", "Mumbai", "Viewpoint"),
    ("A03", "Juhu Beach", "Mumbai", "Beach"),
    ("A04", "Mumbai International Airport", "Mumbai", "Transport"),
    ("A05", "Calangute Beach", "Goa", "Beach"),
    ("A06", "Palolem Beach", "Goa", "Beach"),
    ("A07", "Fort Aguada", "Goa", "Fort"),
    ("A08", "Fontainhas Latin Quarter", "Goa", "Heritage District"),
    ("A09", "Basilica of Bom Jesus", "Goa", "Church"),
    ("A10", "Amber Fort", "Jaipur", "Fort"),
    ("A11", "Hawa Mahal", "Jaipur", "Monument"),
    ("A12", "City Palace Jaipur", "Jaipur", "Palace"),
    ("A13", "Nahargarh Fort", "Jaipur", "Fort"),
    ("A14", "Jaipur Railway Station", "Jaipur", "Transport"),
    ("A15", "Hadimba Temple", "Manali", "Temple"),
    ("A16", "Solang Valley", "Manali", "Adventure"),
    ("A17", "Mall Road Manali", "Manali", "Market"),
    ("A18", "Vashisht Hot Springs", "Manali", "Hot Spring"),
    ("A19", "City Palace Udaipur", "Udaipur", "Palace"),
    ("A20", "Lake Pichola", "Udaipur", "Lake"),
    ("A21", "Fateh Sagar Lake", "Udaipur", "Lake"),
    ("A22", "Sajjangarh Monsoon Palace", "Udaipur", "Palace"),
]
A = {a[0]: a for a in attractions}
with open(f"{S}/attractions.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["attraction_id", "name", "city", "category"])
    w.writerows(attractions)

near = {
    "H01": [("A01", 0.6), ("A02", 2.8)],
    "H02": [("A02", 0.2), ("A01", 3.1)],
    "H03": [("A04", 1.2)],
    "H04": [("A03", 0.4), ("A04", 5.5)],
    "H05": [("A05", 0.3), ("A07", 5.2)],
    "H06": [("A06", 0.1)],
    "H07": [("A08", 0.1), ("A09", 9.5)],
    "H08": [("A07", 1.5), ("A05", 3.0)],
    "H09": [("A11", 0.5), ("A12", 0.8), ("A13", 6.0)],
    "H10": [("A10", 0.7), ("A13", 9.0)],
    "H11": [("A12", 14.0)],
    "H12": [("A14", 0.4), ("A11", 3.2)],
    "H13": [("A15", 1.1), ("A17", 2.5)],
    "H14": [("A16", 0.5)],
    "H15": [("A17", 0.3), ("A15", 1.8)],
    "H16": [("A18", 0.3), ("A17", 3.0)],
    "H17": [("A20", 0.1), ("A19", 0.6)],
    "H18": [("A21", 0.2), ("A22", 4.5)],
    "H19": [("A20", 0.3), ("A19", 1.0)],
    "H20": [("A22", 3.8), ("A21", 6.5)],
}
with open(f"{S}/hotel_attractions.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["hotel_id", "attraction_id", "distance_km"])
    for hid, ns in near.items():
        for aid, d in ns:
            w.writerow([hid, aid, d])

# ---------------- UNSTRUCTURED (policies only live here) ----------------
# free_cancel_hours: None = non-refundable
# pets: None = not allowed, else text of the condition
policies = {
    "H01": dict(cancel=48, pets=None, checkin="2 PM", checkout="11 AM", breakfast=True, pay_at_hotel=True, kids="Children under 6 stay free using existing bedding."),
    "H02": dict(cancel=72, pets=None, checkin="3 PM", checkout="12 PM", breakfast=True, pay_at_hotel=False, kids="Children under 12 stay free; extra beds cost ₹2,500 per night."),
    "H03": dict(cancel=24, pets=None, checkin="12 PM", checkout="10 AM", breakfast=False, pay_at_hotel=True, kids="Children are welcome; no extra beds are available."),
    "H04": dict(cancel=None, pets="Small dogs under 10 kg are allowed for a fee of ₹800 per night.", checkin="2 PM", checkout="11 AM", breakfast=False, pay_at_hotel=False, kids="Children of all ages are welcome."),
    "H05": dict(cancel=48, pets=None, checkin="1 PM", checkout="11 AM", breakfast=True, pay_at_hotel=True, kids="Children under 5 stay free, and the resort runs a supervised kids club in the afternoons."),
    "H06": dict(cancel=24, pets="Pets of any size are welcome at no extra cost.", checkin="12 PM", checkout="10 AM", breakfast=False, pay_at_hotel=True, kids="Families are welcome; the Family Hut has bunk beds."),
    "H07": dict(cancel=72, pets=None, checkin="2 PM", checkout="11 AM", breakfast=True, pay_at_hotel=True, kids="Not recommended for children under 8 because of steep heritage staircases."),
    "H08": dict(cancel=None, pets=None, checkin="3 PM", checkout="12 PM", breakfast=True, pay_at_hotel=False, kids="Children under 12 stay free with parents."),
    "H09": dict(cancel=48, pets=None, checkin="12 PM", checkout="11 AM", breakfast=True, pay_at_hotel=True, kids="Children are welcome; an extra mattress costs ₹600."),
    "H10": dict(cancel=24, pets="Dogs are allowed with prior approval and a refundable ₹2,000 deposit.", checkin="1 PM", checkout="11 AM", breakfast=False, pay_at_hotel=True, kids="Children under 6 stay free."),
    "H11": dict(cancel=72, pets=None, checkin="2 PM", checkout="12 PM", breakfast=True, pay_at_hotel=False, kids="Children under 12 stay free; babysitting is available on request."),
    "H12": dict(cancel=None, pets=None, checkin="11 AM", checkout="10 AM", breakfast=False, pay_at_hotel=True, kids="Guests under 18 must be accompanied by an adult."),
    "H13": dict(cancel=48, pets="Pets are welcome; there is a fenced garden for dogs.", checkin="1 PM", checkout="11 AM", breakfast=True, pay_at_hotel=True, kids="Children are welcome; the attic room suits families."),
    "H14": dict(cancel=24, pets=None, checkin="12 PM", checkout="10 AM", breakfast=True, pay_at_hotel=True, kids="Children are welcome; ski gear for kids can be rented on site."),
    "H15": dict(cancel=72, pets="Small pets under 10 kg are allowed for ₹500 per night.", checkin="2 PM", checkout="11 AM", breakfast=True, pay_at_hotel=False, kids="Children under 5 stay free."),
    "H16": dict(cancel=None, pets="Pets of any size are allowed at no extra charge.", checkin="12 PM", checkout="10 AM", breakfast=False, pay_at_hotel=True, kids="Children are welcome."),
    "H17": dict(cancel=96, pets=None, checkin="3 PM", checkout="12 PM", breakfast=True, pay_at_hotel=False, kids="Children under 12 stay free; a heritage walk for families runs every morning."),
    "H18": dict(cancel=48, pets=None, checkin="12 PM", checkout="11 AM", breakfast=False, pay_at_hotel=True, kids="Children under 5 stay free."),
    "H19": dict(cancel=24, pets=None, checkin="12 PM", checkout="10 AM", breakfast=False, pay_at_hotel=True, kids="Dorm beds are for guests aged 18 and over only."),
    "H20": dict(cancel=48, pets="Dogs are welcome; the resort has walking trails nearby.", checkin="2 PM", checkout="11 AM", breakfast=True, pay_at_hotel=True, kids="Children under 6 stay free and there is a small play lawn."),
}

descriptions = {
    "H01": "Sea Breeze Residency is a calm boutique hotel tucked into the lanes of Colaba, a short walk from the Gateway of India. Guests often mention the friendly front desk and the quiet rooms despite the busy neighbourhood.",
    "H02": "Marine Crest Hotel is a luxury property facing the Arabian Sea on Marine Drive. Its rooftop pool and spa are popular with business travellers, and the Ocean Suites have floor-to-ceiling sea views.",
    "H03": "Andheri Transit Inn is a practical choice for travellers with early or late flights. It runs a free 24-hour shuttle to Mumbai International Airport, about 1.2 km away.",
    "H04": "Juhu Palm Suites offers apartment-style suites with kitchenettes, close to Juhu Beach. It is popular with families and long-stay guests who want more space than a normal hotel room.",
    "H05": "Calangute Shores Resort sits just behind Calangute Beach. The resort has a large lagoon-style pool, a beach shack-style bar and plenty of activities for children.",
    "H06": "Palolem Bay Huts is a laid-back set of wooden huts directly on Palolem Beach in South Goa. It is a favourite with backpackers and travellers with pets.",
    "H07": "Panjim Heritage Stay is a restored Portuguese-era home in the colourful Fontainhas Latin Quarter. Rooms have original tiles and wooden balconies, and breakfast is served in the courtyard.",
    "H08": "Candolim Grand is a five-star beachfront resort near Fort Aguada, with private pool villas, a full-service spa and direct beach access.",
    "H09": "Pink City Haveli is an 18th-century haveli converted into a heritage hotel, walking distance from Hawa Mahal and City Palace. The rooftop restaurant has views over the old city.",
    "H10": "Amber Fort View Hotel lies at the foot of Amber Fort in Amer, and many rooms look straight up at the fort walls, which are lit up at night.",
    "H11": "Rajputana Palace Resort is a sprawling luxury resort on the outskirts of Jaipur, built in Rajput palace style with courtyards, fountains and a large spa.",
    "H12": "Jaipur Budget Stay is a no-frills option near Jaipur Railway Station, offering private rooms and dormitory beds for budget travellers.",
    "H13": "Snow Peak Retreat is a wooden mountain lodge in Old Manali with views of snow-capped peaks. Guests gather around the evening bonfire, and the cafe is known for its apple pie.",
    "H14": "Solang Valley Lodge is right next to the Solang Valley ski slopes and paragliding points, making it a base for adventure travellers in winter and summer.",
    "H15": "Himalayan Pines Resort is set among pine trees a few minutes from Mall Road, with heated rooms, a small spa and cottage suites for families.",
    "H16": "Beas River Cottages are simple riverside cottages in Vashisht village, a short walk from the Vashisht hot springs.",
    "H17": "Lake Pichola Palace is a heritage luxury hotel on the banks of Lake Pichola, reached by a private boat transfer. It overlooks the City Palace and is one of Udaipur's most famous stays.",
    "H18": "Fateh Sagar Inn is a mid-range hotel facing Fateh Sagar Lake, with a rooftop restaurant that is busy at sunset.",
    "H19": "Udaipur Courtyard Stay is a friendly budget guesthouse in Hanuman Ghat with a rooftop cafe looking across Lake Pichola.",
    "H20": "Aravalli Hills Resort is a quiet resort in the Aravalli hills near Badi, about 4 km from the Sajjangarh Monsoon Palace, with a pool, spa and nature trails.",
}

def policy_text(p):
    lines = []
    if p["cancel"]:
        lines.append(f"Free cancellation is available up to {p['cancel']} hours before check-in; after that, the first night is charged.")
    else:
        lines.append("All bookings are non-refundable and cannot be cancelled or changed once confirmed.")
    lines.append(p["pets"] if p["pets"] else "Pets are not allowed on the property.")
    lines.append(f"Check-in starts at {p['checkin']} and check-out is by {p['checkout']}.")
    lines.append("Breakfast is included in all room rates." if p["breakfast"] else "Breakfast is not included and is charged separately.")
    lines.append("Guests can pay at the hotel on arrival." if p["pay_at_hotel"] else "Full prepayment is required at the time of booking.")
    lines.append(p["kids"])
    return " ".join(lines)

for hid, h in H.items():
    _, name, city, area, stars, rating = h
    room_lines = "; ".join(f"{r[0]} at ₹{r[1]:,} per night for up to {r[2]} guests" for r in rooms[hid])
    text = (
        f"# {name}\n\n"
        f"## About\n{descriptions[hid]} It is located in {area}, {city}.\n\n"
        f"## Rooms\nAvailable room types: {room_lines}.\n\n"
        f"## Policies\n{policy_text(policies[hid])}\n"
    )
    with open(f"{U}/{hid}_{name.lower().replace(' ', '_')}.md", "w") as f:
        f.write(text)

# ---------------- TEST QUESTIONS (answers computed from the data) ----------------
def names(ids): return ", ".join(H[i][1] for i in ids) or "None"

qa = []

ids = [h for h in H if H[h][2] == "Goa" and "Pool" in amenities[h] and policies[h]["cancel"]]
qa.append(("Which hotels in Goa have a pool and offer free cancellation?", names(ids),
           "Multi-hop: city + amenity (structured) + cancellation policy (only in text)."))

ids = [h for h in H if policies[h]["pets"] and any(A[a][3] == "Fort" and d <= 2 for a, d in near[h])]
qa.append(("Which pet-friendly hotels are within 2 km of a fort?", names(ids),
           "Multi-hop: hotel -> NEAR -> attraction category + distance + pet policy."))

best = min(((r[1], h, r[0]) for h in H if H[h][2] == "Udaipur" for r in rooms[h] if r[2] >= 3))
qa.append(("What is the cheapest room in Udaipur that can sleep 3 or more people?",
           f"{best[2]} at {H[best[1]][1]} (₹{best[0]:,} per night)", "Aggregation over rooms filtered by city and capacity."))

ids = [h for h in H if H[h][4] == 5 and "Spa" in amenities[h] and H[h][5] > 4.5]
qa.append(("Which 5-star hotels with a spa have a guest rating above 4.5, and in which cities?",
           "; ".join(f"{H[i][1]} ({H[i][2]})" for i in ids), "Filters across hotel properties and amenities."))

ids = [h for h in H if H[h][2] == "Manali" and policies[h]["pets"] and "Heating" in amenities[h]]
qa.append(("Which hotels in Manali allow pets and have heating?", names(ids), "Amenity (structured) + pet policy (text)."))

ids = [h for h in H if policies[h]["breakfast"] and any(A[a][3] == "Beach" and d <= 1 for a, d in near[h])]
qa.append(("Which hotels within 1 km of a beach include breakfast?", names(ids), "Attraction category + distance + breakfast policy (text)."))

ids = [h for h in H if not policies[h]["cancel"]]
qa.append(("Which hotels have non-refundable bookings?", names(ids), "Policy extracted from unstructured text only."))

ids = [h for h in H if H[h][2] == "Jaipur" and policies[h]["pay_at_hotel"] and any(A[a][1] in ("Hawa Mahal", "City Palace Jaipur") and d <= 1 for a, d in near[h])]
qa.append(("I want to stay within 1 km of Hawa Mahal or City Palace in Jaipur and pay at the hotel. What are my options?", names(ids), "Named attractions + distance + payment policy."))

with open(f"{OUT}/test_questions.md", "w") as f:
    f.write("# Test questions for the demo\n\n")
    f.write("Answers are computed directly from the dataset, so they are the ground truth for comparing plain vector RAG against graph RAG.\n\n")
    for i, (q, a, why) in enumerate(qa, 1):
        f.write(f"## Q{i}. {q}\n**Expected answer:** {a}\n\n*Why it's a good test:* {why}\n\n")

print(json.dumps(qa, indent=1, ensure_ascii=False))
