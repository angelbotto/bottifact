import unittest
from portal import test_knowledge as fixtures


class ContextBundleTests(unittest.TestCase):
    setUp = fixtures.KnowledgeTests.setUp
    tearDown = fixtures.KnowledgeTests.tearDown
    client = fixtures.KnowledgeTests.client
    publish = fixtures.KnowledgeTests.publish

    def test_selected_bundle_keeps_notes_explicit_and_private(self):
        a = self.publish(
            self.owner,
            source={
                "agent": "Codex",
                "session": "original-session",
                "device": "Example device",
            },
        )
        for kind in ["comment", "note"]:
            r = self.owner.post(
                "/api/artifacts/" + a["id"] + "/review",
                json={
                    "id": kind,
                    "kind": "create",
                    "entry_type": kind,
                    "version": a["version"],
                    "text": "Text " + kind,
                    "anchor": {
                        "reference": "test",
                        "tag": "P",
                        "text": "Evidence",
                        "quote": "Evidence",
                        "page": "Review",
                        "x": 0.5,
                        "y": 0.5,
                    },
                },
            )
            self.assertEqual(r.status_code, 200, r.text)
        items = self.owner.get("/api/review/export").json()["items"]
        ids = {i["thread"]["entry_type"]: i["thread"]["thread"] for i in items}
        r = self.owner.post(
            "/api/review/bundle",
            json={"artifact": a["id"], "threads": [ids["comment"]]},
        )
        self.assertEqual(r.status_code, 200, r.text)
        self.assertNotIn("Text note", r.text)
        self.assertIn("original-session", r.text)
        r = self.owner.post(
            "/api/review/bundle", json={"artifact": a["id"], "threads": [ids["note"]]}
        )
        self.assertEqual(r.status_code, 404)
        r = self.owner.post(
            "/api/review/bundle",
            json={"artifact": a["id"], "threads": [ids["note"]], "include_notes": True},
        )
        self.assertEqual(r.status_code, 200)
        self.assertIn("Text note", r.text)
        self.owner.put(
            "/api/artifacts/" + a["id"] + "/access",
            json={
                "visibility": "invited",
                "grants": [{"email": "other@example.com", "role": "viewer"}],
            },
        )
        r = self.other.post(
            "/api/review/bundle",
            json={"artifact": a["id"], "threads": [ids["note"]], "include_notes": True},
        )
        self.assertEqual(r.status_code, 404)
        self.assertNotIn("Text note", r.text)

    def test_empty_bundle_still_identifies_artifact_and_bad_selection_is_rejected(self):
        a = self.publish(self.owner)
        r = self.owner.post(
            "/api/review/bundle", json={"artifact": a["id"], "threads": []}
        )
        self.assertEqual(r.status_code, 200)
        self.assertIn(a["id"], r.json()["text"])
        self.assertEqual(
            self.owner.post(
                "/api/review/bundle", json={"threads": "not-a-list"}
            ).status_code,
            422,
        )
