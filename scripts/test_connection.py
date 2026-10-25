"""Checks that Neo4j AuraDB and the Gemini API are reachable. Run from the repo root:
    python scripts/test_connection.py
"""
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from google import genai

load_dotenv()

# 1. Neo4j
print("Checking Neo4j...")
driver = GraphDatabase.driver(
    os.environ["NEO4J_URI"],
    auth=(os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"]),
)
driver.verify_connectivity()
with driver.session(database=os.environ.get("NEO4J_DATABASE")) as session:
    count = session.run("MATCH (n) RETURN count(n) AS c").single()["c"]
print(f"  OK: connected, the database currently has {count} nodes")
driver.close()

# 2. Gemini LLM
print("Checking Gemini LLM...")
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
model = os.environ["GEMINI_MODEL"]
reply = client.models.generate_content(model=model, contents="Reply with just the word: ready")
print(f"  OK: {model} replied '{reply.text.strip()}'")

# 3. Gemini embeddings
print("Checking Gemini embeddings...")
emb = client.models.embed_content(model="gemini-embedding-001", contents="pet-friendly hotel near a fort")
print(f"  OK: embedding has {len(emb.embeddings[0].values)} dimensions")

print("\nAll connections working.")
