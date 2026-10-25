"""Loads the structured CSVs into Neo4j as a knowledge graph.

Run from the repo root:
    python ingestion/load_structured.py

Safe to re-run: MERGE never creates duplicates.
"""
import csv
import os
from pathlib import Path

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()
DATA = Path(__file__).resolve().parent.parent / "data" / "structured"


def read(name):
    with open(DATA / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


CONSTRAINTS = [
    "CREATE CONSTRAINT hotel_id IF NOT EXISTS FOR (h:Hotel) REQUIRE h.id IS UNIQUE",
    "CREATE CONSTRAINT city_name IF NOT EXISTS FOR (c:City) REQUIRE c.name IS UNIQUE",
    "CREATE CONSTRAINT amenity_name IF NOT EXISTS FOR (a:Amenity) REQUIRE a.name IS UNIQUE",
    "CREATE CONSTRAINT attraction_id IF NOT EXISTS FOR (a:Attraction) REQUIRE a.id IS UNIQUE",
    "CREATE CONSTRAINT room_id IF NOT EXISTS FOR (r:RoomType) REQUIRE r.id IS UNIQUE",
]

LOAD_HOTELS = """
UNWIND $rows AS row
MERGE (c:City {name: row.city})
MERGE (h:Hotel {id: row.hotel_id})
SET h.name = row.name,
    h.area = row.area,
    h.star_rating = toInteger(row.star_rating),
    h.guest_rating = toFloat(row.guest_rating)
MERGE (h)-[:LOCATED_IN]->(c)
"""

LOAD_ROOMS = """
UNWIND $rows AS row
MATCH (h:Hotel {id: row.hotel_id})
MERGE (r:RoomType {id: row.hotel_id + '_' + row.room_type})
SET r.name = row.room_type,
    r.price_inr = toInteger(row.price_inr_per_night),
    r.max_guests = toInteger(row.max_guests)
MERGE (h)-[:OFFERS]->(r)
"""

LOAD_AMENITIES = """
UNWIND $rows AS row
MATCH (h:Hotel {id: row.hotel_id})
MERGE (a:Amenity {name: row.amenity})
MERGE (h)-[:HAS_AMENITY]->(a)
"""

LOAD_ATTRACTIONS = """
UNWIND $rows AS row
MERGE (c:City {name: row.city})
MERGE (a:Attraction {id: row.attraction_id})
SET a.name = row.name, a.category = row.category
MERGE (a)-[:LOCATED_IN]->(c)
"""

LOAD_NEAR = """
UNWIND $rows AS row
MATCH (h:Hotel {id: row.hotel_id})
MATCH (a:Attraction {id: row.attraction_id})
MERGE (h)-[n:NEAR]->(a)
SET n.distance_km = toFloat(row.distance_km)
"""

STEPS = [
    ("hotels + cities", LOAD_HOTELS, "hotels.csv"),
    ("room types", LOAD_ROOMS, "rooms.csv"),
    ("amenities", LOAD_AMENITIES, "amenities.csv"),
    ("attractions", LOAD_ATTRACTIONS, "attractions.csv"),
    ("hotel-attraction distances", LOAD_NEAR, "hotel_attractions.csv"),
]


def main():
    driver = GraphDatabase.driver(
        os.environ["NEO4J_URI"],
        auth=(os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"]),
    )
    db = os.environ.get("NEO4J_DATABASE")

    for c in CONSTRAINTS:
        driver.execute_query(c, database_=db)
    print("Constraints ready")

    for label, query, file in STEPS:
        rows = read(file)
        driver.execute_query(query, rows=rows, database_=db)
        print(f"Loaded {label}: {len(rows)} rows")

    records, _, _ = driver.execute_query(
        "MATCH (n) RETURN labels(n)[0] AS label, count(*) AS count ORDER BY label",
        database_=db,
    )
    print("\nNodes in graph:")
    for r in records:
        print(f"  {r['label']}: {r['count']}")

    records, _, _ = driver.execute_query(
        "MATCH ()-[r]->() RETURN type(r) AS type, count(*) AS count ORDER BY type",
        database_=db,
    )
    print("Relationships in graph:")
    for r in records:
        print(f"  {r['type']}: {r['count']}")

    driver.close()


if __name__ == "__main__":
    main()
