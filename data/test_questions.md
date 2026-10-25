# Test questions for the demo

Answers are computed directly from the dataset, so they are the ground truth for comparing plain vector RAG against graph RAG.

## Q1. Which hotels in Goa have a pool and offer free cancellation?
**Expected answer:** Calangute Shores Resort

*Why it's a good test:* Multi-hop: city + amenity (structured) + cancellation policy (only in text).

## Q2. Which pet-friendly hotels are within 2 km of a fort?
**Expected answer:** Amber Fort View Hotel

*Why it's a good test:* Multi-hop: hotel -> NEAR -> attraction category + distance + pet policy.

## Q3. What is the cheapest room in Udaipur that can sleep 3 or more people?
**Expected answer:** Triple Room at Fateh Sagar Inn (₹5,800 per night)

*Why it's a good test:* Aggregation over rooms filtered by city and capacity.

## Q4. Which 5-star hotels with a spa have a guest rating above 4.5, and in which cities?
**Expected answer:** Marine Crest Hotel (Mumbai); Rajputana Palace Resort (Jaipur); Lake Pichola Palace (Udaipur)

*Why it's a good test:* Filters across hotel properties and amenities.

## Q5. Which hotels in Manali allow pets and have heating?
**Expected answer:** Snow Peak Retreat, Himalayan Pines Resort, Beas River Cottages

*Why it's a good test:* Amenity (structured) + pet policy (text).

## Q6. Which hotels within 1 km of a beach include breakfast?
**Expected answer:** Calangute Shores Resort

*Why it's a good test:* Attraction category + distance + breakfast policy (text).

## Q7. Which hotels have non-refundable bookings?
**Expected answer:** Juhu Palm Suites, Candolim Grand, Jaipur Budget Stay, Beas River Cottages

*Why it's a good test:* Policy extracted from unstructured text only.

## Q8. I want to stay within 1 km of Hawa Mahal or City Palace in Jaipur and pay at the hotel. What are my options?
**Expected answer:** Pink City Haveli

*Why it's a good test:* Named attractions + distance + payment policy.

