"""Extracts hotel policies from the unstructured text files with Gemini
and adds them to the knowledge graph.

Run from the repo root:
    python ingestion/extract_policies.py            # extracts only hotels not cached yet
    python ingestion/extract_policies.py --refresh  # calls Gemini again for every hotel

What it builds:
    (:Document)-[:DESCRIBES]->(:Hotel)                   source text, for provenance
    (:Hotel)-[:HAS_POLICY {details}]->(:Policy {name})   e.g. "Pets Allowed", "Free Cancellation"
    Hotel properties: check_in, check_out, children_policy
"""
import json
import os
import sys
import time
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types
from neo4j import GraphDatabase
from pydantic import BaseModel, Field

load_dotenv()
ROOT = Path(__file__).resolve().parent.parent
TEXT_DIR = ROOT / "data" / "unstructured"
CACHE = ROOT / "data" / "extracted" / "policies.json"


class HotelPolicies(BaseModel):
    free_cancellation: bool = Field(description="True if bookings can be cancelled for free at some point")
    free_cancellation_hours: Optional[int] = Field(description="Hours before check-in until which cancellation is free; null if non-refundable")
    pets_allowed: bool
    pet_conditions: Optional[str] = Field(description="Any pet restrictions, e.g. size limits or approval needed; null if none or pets not allowed")
    pet_fee_inr_per_night: Optional[int] = Field(description="Pet fee per night in INR; 0 if free; null if pets not allowed or a deposit instead")
    check_in_time: str
    check_out_time: str
    breakfast_included: bool
    pay_at_hotel: bool = Field(description="True if guests can pay on arrival; false if prepayment is required")
    children_policy: str = Field(description="One-sentence summary of the children policy")


class ExtractedHotel(HotelPolicies):
    hotel_id: str = Field(description="The ID given in the HOTEL header, e.g. H01")


class Batch(BaseModel):
    hotels: list[ExtractedHotel]


PROMPT = """Extract the policies of each hotel below. Return one entry per hotel, using its ID.
Use only what each hotel's text states. Do not guess. If something is not mentioned, use false or null.

{docs}"""

BATCH_SIZE = 5          # hotels per Gemini call: 20 hotels = 4 requests instead of 20
SECONDS_BETWEEN_CALLS = 15  # stays under free-tier requests-per-minute limits


class DailyQuotaExceeded(Exception):
    pass


def extract_batch(client, model, items):
    """items: list of (hotel_id, text). Returns {hotel_id: policies}."""
    docs = "\n\n".join(f"=== HOTEL {hid} ===\n{text}" for hid, text in items)
    for attempt in range(4):
        try:
            resp = client.models.generate_content(
                model=model,
                contents=PROMPT.format(docs=docs),
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=Batch,
                    temperature=0,
                ),
            )
            out = {}
            for h in resp.parsed.hotels:
                d = h.model_dump()
                out[d.pop("hotel_id")] = d
            return out
        except Exception as e:
            msg = str(e)
            if "404" in msg:
                raise DailyQuotaExceeded(f"Model {model} is not available for this API key. Set EXTRACTION_MODEL in .env to a model that is.")
            if "429" in msg and "PerDay" in msg:
                raise DailyQuotaExceeded(
                    f"Daily free-tier limit reached for {model}. "
                    "Set EXTRACTION_MODEL in .env to another model, or wait for the daily reset."
                )
            wait = 60 if "429" in msg else 10 * (attempt + 1)
            print(f"    retrying in {wait}s ({e.__class__.__name__}: {msg[:120]})")
            time.sleep(wait)
    raise RuntimeError("Extraction failed after retries")


def to_policy_edges(p):
    """Turns the extracted fields into shared Policy nodes, with details on the relationship."""
    edges = []
    if p["free_cancellation"]:
        edges.append({"name": "Free Cancellation", "props": {"hours_before_checkin": p["free_cancellation_hours"]}})
    else:
        edges.append({"name": "Non-refundable", "props": {}})
    if p["pets_allowed"]:
        edges.append({"name": "Pets Allowed", "props": {
            "conditions": p["pet_conditions"], "fee_inr_per_night": p["pet_fee_inr_per_night"]}})
    if p["breakfast_included"]:
        edges.append({"name": "Breakfast Included", "props": {}})
    edges.append({"name": "Pay at Hotel" if p["pay_at_hotel"] else "Prepayment Required", "props": {}})
    return edges


WRITE = """
MATCH (h:Hotel {id: $hotel_id})
SET h.check_in = $p.check_in_time,
    h.check_out = $p.check_out_time,
    h.children_policy = $p.children_policy
MERGE (d:Document {id: $hotel_id})
SET d.file = $file, d.text = $text
MERGE (d)-[:DESCRIBES]->(h)
WITH h
OPTIONAL MATCH (h)-[old:HAS_POLICY]->()
DELETE old
WITH DISTINCT h
UNWIND $edges AS e
MERGE (pol:Policy {name: e.name})
MERGE (h)-[r:HAS_POLICY]->(pol)
SET r += e.props
"""


def main():
    refresh = "--refresh" in sys.argv
    cache = json.loads(CACHE.read_text()) if CACHE.exists() and not refresh else {}

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    model = os.environ.get("EXTRACTION_MODEL") or os.environ["GEMINI_MODEL"]
    driver = GraphDatabase.driver(
        os.environ["NEO4J_URI"],
        auth=(os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"]),
    )
    db = os.environ.get("NEO4J_DATABASE")
    driver.execute_query("CREATE CONSTRAINT policy_name IF NOT EXISTS FOR (p:Policy) REQUIRE p.name IS UNIQUE", database_=db)
    driver.execute_query("CREATE CONSTRAINT document_id IF NOT EXISTS FOR (d:Document) REQUIRE d.id IS UNIQUE", database_=db)

    docs = {p.name.split("_")[0]: p for p in sorted(TEXT_DIR.glob("*.md"))}
    todo = [hid for hid in docs if hid not in cache]
    print(f"{len(docs) - len(todo)} hotels cached, {len(todo)} to extract with {model}")

    for i in range(0, len(todo), BATCH_SIZE):
        batch = [(hid, docs[hid].read_text(encoding="utf-8")) for hid in todo[i:i + BATCH_SIZE]]
        print(f"  extracting {', '.join(h for h, _ in batch)}...")
        try:
            result = extract_batch(client, model, batch)
        except DailyQuotaExceeded as e:
            print(f"\nStopped: {e}\nProgress is saved; rerun later to continue.")
            break
        missing = [h for h, _ in batch if h not in result]
        if missing:
            print(f"    not returned, will retry on next run: {', '.join(missing)}")
        cache.update({h: p for h, p in result.items() if h in docs})
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        CACHE.write_text(json.dumps(cache, indent=2, ensure_ascii=False))
        if i + BATCH_SIZE < len(todo):
            time.sleep(SECONDS_BETWEEN_CALLS)

    for hid, path in docs.items():
        if hid not in cache:
            continue
        p = cache[hid]
        edges = to_policy_edges(p)
        driver.execute_query(WRITE, hotel_id=hid, p=p, file=path.name,
                             text=path.read_text(encoding="utf-8"), edges=edges, database_=db)
        print(f"{hid}: " + ", ".join(e["name"] for e in edges))

    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(cache, indent=2, ensure_ascii=False))
    print(f"\nSaved extractions to {CACHE.relative_to(ROOT)}")

    records, _, _ = driver.execute_query(
        "MATCH (h:Hotel)-[:HAS_POLICY]->(p:Policy) RETURN p.name AS policy, count(h) AS hotels ORDER BY policy",
        database_=db,
    )
    print("\nHotels per policy:")
    for r in records:
        print(f"  {r['policy']}: {r['hotels']}")
    driver.close()


if __name__ == "__main__":
    main()
