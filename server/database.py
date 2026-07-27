"""
SQLite-backed document store exposing a MongoDB-compatible API.
Replaces pymongo so no external DB server is required for deployment.

Collections are stored as JSON blobs in a single SQLite table:
    documents(id INTEGER PK AUTOINCREMENT, col TEXT, data TEXT)

Each document's _id is the auto-increment integer serialised as a string,
matching the string-ID convention used throughout the route layer.
"""

import json
import os
import re
import sqlite3
from datetime import datetime
from threading import Lock

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ayurdiet.db")
_lock = Lock()


# ─── Connection helpers ──────────────────────────────────────────────────────

def _open() -> sqlite3.Connection:
    """Open a fresh SQLite connection and ensure schema exists."""
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            col  TEXT NOT NULL,
            data TEXT NOT NULL
        )
        """
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_col ON documents(col)")
    conn.commit()
    return conn


def _row_to_doc(row) -> dict:
    """Convert a (id, col, data) row to a dict with _id injected."""
    doc = json.loads(row[2])
    doc["_id"] = str(row[0])
    return doc


# ─── Filter matching ─────────────────────────────────────────────────────────

def _matches(doc: dict, filt: dict) -> bool:
    """Return True if *doc* satisfies the MongoDB-style *filt* dict."""
    for key, value in filt.items():
        doc_val = doc.get(key)
        if isinstance(value, dict) and any(k.startswith("$") for k in value):
            # Operator query (e.g. {"age": {"$gte": 18}})
            for op, op_val in value.items():
                if op == "$options":
                    continue  # modifier for $regex, handled there
                if op == "$regex":
                    flags = re.IGNORECASE if value.get("$options", "") == "i" else 0
                    if not re.search(op_val, str(doc_val or ""), flags):
                        return False
                elif op == "$lte":
                    if doc_val is None or not (doc_val <= op_val):
                        return False
                elif op == "$lt":
                    if doc_val is None or not (doc_val < op_val):
                        return False
                elif op == "$gte":
                    if not _gte(doc_val, op_val):
                        return False
                elif op == "$gt":
                    if doc_val is None or not (doc_val > op_val):
                        return False
                elif op == "$ne":
                    if doc_val == op_val:
                        return False
                elif op == "$in":
                    if doc_val not in op_val:
                        return False
        else:
            # Exact match — always compare _id as strings
            if key == "_id":
                if str(doc_val or "") != str(value):
                    return False
            elif doc_val != value:
                return False
    return True


def _gte(doc_val, op_val) -> bool:
    if doc_val is None:
        return False
    if isinstance(op_val, datetime):
        if isinstance(doc_val, str):
            try:
                return datetime.fromisoformat(doc_val) >= op_val
            except ValueError:
                return False
        return doc_val >= op_val
    return doc_val >= op_val


def _apply_projection(doc: dict, projection: dict) -> dict:
    result = dict(doc)
    for field, include in projection.items():
        if include == 0:
            result.pop(field, None)
    return result


# ─── Cursor ──────────────────────────────────────────────────────────────────

class Cursor:
    """Chainable result set mirroring pymongo Cursor behaviour."""

    def __init__(self, docs: list):
        self._docs = docs

    def sort(self, field: str, direction: int = 1) -> "Cursor":
        reverse = direction == -1

        def _key(d):
            v = d.get(field)
            if field == "_id":
                try:
                    return (0, int(v))
                except (TypeError, ValueError):
                    return (0, 0)
            if v is None:
                return (1, "")
            return (0, v)

        self._docs.sort(key=_key, reverse=reverse)
        return self

    def limit(self, n: int) -> "Cursor":
        self._docs = self._docs[:n]
        return self

    def __iter__(self):
        return iter(self._docs)

    def __len__(self):
        return len(self._docs)

    def __getitem__(self, item):
        return self._docs[item]


# ─── Result stubs ────────────────────────────────────────────────────────────

class InsertOneResult:
    def __init__(self, inserted_id: str):
        self.inserted_id = inserted_id


class InsertManyResult:
    def __init__(self, inserted_ids: list):
        self.inserted_ids = inserted_ids


class UpdateResult:
    def __init__(self, matched_count: int = 0, modified_count: int = 0):
        self.matched_count = matched_count
        self.modified_count = modified_count


class DeleteResult:
    def __init__(self, deleted_count: int = 0):
        self.deleted_count = deleted_count


# ─── Collection ──────────────────────────────────────────────────────────────

class Collection:
    """Represents one logical collection (table) inside the SQLite DB."""

    def __init__(self, name: str):
        self.name = name

    # ── Internal ──────────────────────────────────────────────────────────

    def _all(self) -> list:
        with _lock:
            conn = _open()
            rows = conn.execute(
                "SELECT id, col, data FROM documents WHERE col=?", (self.name,)
            ).fetchall()
            conn.close()
        return [_row_to_doc(r) for r in rows]

    # ── Read API ──────────────────────────────────────────────────────────

    def find(self, filt: dict = None, projection: dict = None) -> Cursor:
        docs = self._all()
        if filt:
            docs = [d for d in docs if _matches(d, filt)]
        if projection:
            docs = [_apply_projection(d, projection) for d in docs]
        return Cursor(docs)

    def find_one(self, filt: dict = None, projection: dict = None):
        for doc in self._all():
            if not filt or _matches(doc, filt):
                return _apply_projection(doc, projection) if projection else doc
        return None

    def count_documents(self, filt: dict = None) -> int:
        docs = self._all()
        if not filt:
            return len(docs)
        return sum(1 for d in docs if _matches(d, filt))

    def distinct(self, field: str, filt: dict = None) -> list:
        docs = self._all()
        if filt:
            docs = [d for d in docs if _matches(d, filt)]
        seen: set = set()
        result = []
        for doc in docs:
            val = doc.get(field)
            if val is not None and val not in seen:
                seen.add(str(val))
                result.append(val)
        return result

    def aggregate(self, pipeline: list) -> list:
        """Supports $match, $group (with $sum:1/$sum:0), $sort, $limit."""
        docs = self._all()
        for stage in pipeline:
            if "$match" in stage:
                docs = [d for d in docs if _matches(d, stage["$match"])]
            elif "$group" in stage:
                spec = stage["$group"]
                expr = spec.get("_id")
                group_field = expr[1:] if isinstance(expr, str) and expr.startswith("$") else None
                groups: dict = {}
                for doc in docs:
                    key = doc.get(group_field) if group_field else None
                    if key not in groups:
                        groups[key] = {"_id": key, "count": 0}
                    groups[key]["count"] += 1
                docs = list(groups.values())
            elif "$sort" in stage:
                for field, direction in stage["$sort"].items():
                    docs.sort(
                        key=lambda d: (d.get(field) is None, d.get(field) or ""),
                        reverse=direction == -1,
                    )
            elif "$limit" in stage:
                docs = docs[: stage["$limit"]]
        return docs

    # ── Write API ─────────────────────────────────────────────────────────

    def insert_one(self, doc: dict) -> InsertOneResult:
        doc_copy = {k: v for k, v in doc.items() if k != "_id"}
        data = json.dumps(doc_copy, default=str)
        with _lock:
            conn = _open()
            cur = conn.execute(
                "INSERT INTO documents (col, data) VALUES (?, ?)", (self.name, data)
            )
            conn.commit()
            inserted_id = str(cur.lastrowid)
            conn.close()
        doc["_id"] = inserted_id
        return InsertOneResult(inserted_id)

    def insert_many(self, docs: list) -> InsertManyResult:
        ids = [self.insert_one(doc).inserted_id for doc in docs]
        return InsertManyResult(ids)

    def update_one(self, filt: dict, update: dict, upsert: bool = False) -> UpdateResult:
        doc = self.find_one(filt)
        if doc is None:
            if upsert:
                # Build new document from filter + $set fields
                new_doc = {}
                for k, v in filt.items():
                    if not isinstance(v, dict):
                        new_doc[k] = v
                if "$set" in update:
                    new_doc.update(update["$set"])
                self.insert_one(new_doc)
                return UpdateResult(matched_count=0, modified_count=1)
            return UpdateResult(matched_count=0)

        row_id = int(doc["_id"])
        if "$set" in update:
            doc.update(update["$set"])

        doc_copy = {k: v for k, v in doc.items() if k != "_id"}
        data = json.dumps(doc_copy, default=str)
        with _lock:
            conn = _open()
            conn.execute(
                "UPDATE documents SET data=? WHERE id=? AND col=?",
                (data, row_id, self.name),
            )
            conn.commit()
            conn.close()
        return UpdateResult(matched_count=1, modified_count=1)

    def delete_one(self, filt: dict) -> DeleteResult:
        doc = self.find_one(filt)
        if doc is None:
            return DeleteResult(0)
        row_id = int(doc["_id"])
        with _lock:
            conn = _open()
            conn.execute(
                "DELETE FROM documents WHERE id=? AND col=?", (row_id, self.name)
            )
            conn.commit()
            conn.close()
        return DeleteResult(1)

    def delete_many(self, filt: dict) -> DeleteResult:
        docs = list(self.find(filt))
        if not docs:
            return DeleteResult(0)
        ids = [int(d["_id"]) for d in docs]
        placeholders = ",".join("?" * len(ids))
        with _lock:
            conn = _open()
            conn.execute(
                f"DELETE FROM documents WHERE id IN ({placeholders}) AND col=?",
                (*ids, self.name),
            )
            conn.commit()
            conn.close()
        return DeleteResult(len(ids))


# ─── Database ────────────────────────────────────────────────────────────────

class SQLiteDB:
    """Top-level DB object — attribute access yields named Collections."""

    def __getattr__(self, name: str) -> Collection:
        return Collection(name)


db = SQLiteDB()


def get_db():
    yield db
