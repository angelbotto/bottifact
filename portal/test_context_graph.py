import unittest
from portal import test_knowledge as fixtures


class ContextGraphTests(unittest.TestCase):
    setUp = fixtures.KnowledgeTests.setUp
    tearDown = fixtures.KnowledgeTests.tearDown
    client = fixtures.KnowledgeTests.client
    publish = fixtures.KnowledgeTests.publish

    def test_links_pin_evidence_and_never_leak_private_target(self):
        source = self.publish(
            self.owner, title="Source", body="Evidence for the decision"
        )
        target = self.publish(self.owner, title="Target")
        body = {
            "source": source["id"],
            "target": target["id"],
            "kind": "cites",
            "quote": "Evidence for the decision",
        }
        r = self.owner.post("/api/context/links", json=body)
        self.assertEqual(r.status_code, 200, r.text)
        self.assertEqual(
            self.owner.post(
                "/api/context/links", json={**body, "quote": "invented"}
            ).status_code,
            422,
        )
        self.owner.put(
            "/api/artifacts/" + source["id"] + "/access",
            json={"visibility": "public", "comments": "readers"},
        )
        self.assertEqual(
            self.other.get("/api/context/links?artifact=" + source["id"]).json()[
                "items"
            ],
            [],
        )
        self.assertNotIn(
            target["id"],
            str(self.other.get("/api/artifacts?view=public&graph=1").json()),
        )
        self.owner.put(
            "/api/artifacts/" + target["id"] + "/access",
            json={"visibility": "public", "comments": "readers"},
        )
        links = self.other.get("/api/context/links?artifact=" + source["id"]).json()[
            "items"
        ]
        self.assertEqual(links[0]["version"], source["version"])
        self.assertIn(
            self.other.post("/api/context/links", json=body).status_code, (403, 404)
        )
        newer = self.owner.post(
            "/api/artifacts/" + source["id"] + "/versions",
            json={
                "title": "Source revised",
                "html": '<meta name="nota-documento" content="test"><main><p>New evidence</p></main>',
            },
        ).json()
        old = self.other.get(
            "/api/artifacts/" + source["id"] + "/render?version=" + source["version"]
        )
        self.assertEqual(old.status_code, 200, old.text[:200])
        bundle = self.other.post(
            "/api/review/bundle",
            json={
                "artifact": source["id"],
                "threads": [],
                "evidence": [r.json()["id"]],
                "version": source["version"],
            },
        )
        self.assertEqual(bundle.status_code, 200, bundle.text)
        self.assertIn("Evidence for the decision", bundle.text)
        self.owner.patch(
            "/api/context/links/" + r.json()["id"], json={"state": "dismissed"}
        )
        self.assertEqual(self.owner.get("/api/context/links").json()["items"], [])
        self.assertEqual(self.other.get("/api/artifacts/"+source["id"]+"/render?version="+source["version"]).status_code,404)

    def test_aliases_are_personal_and_not_automatic_merges(self):
        a = self.publish(self.owner)
        for name in ("Acme", "Acme Inc"):
            r = self.owner.post(
                "/api/context/entities",
                json={
                    "kind": "company",
                    "name": name,
                    "aliases": ["Acme"],
                    "properties": {"region": "LATAM"},
                    "artifacts": [a["id"]],
                },
            )
            self.assertEqual(r.status_code, 200, r.text)
        self.assertEqual(
            len(self.owner.get("/api/context/entities").json()["items"]), 2
        )
        self.assertEqual(self.other.get("/api/context/entities").json()["items"], [])
        network = self.owner.get("/api/artifacts?graph=1").json()["network"]
        self.assertEqual(
            len([n for n in network["nodes"] if n["kind"] == "company"]), 2
        )

    def test_saved_views_recheck_access_and_batch_is_atomic(self):
        mine = self.publish(self.owner, title="Mine")
        other = self.publish(self.other, title="Shared temporarily")
        self.other.put(
            "/api/artifacts/" + other["id"] + "/access",
            json={
                "visibility": "invited",
                "grants": [{"email": "owner@example.com", "role": "viewer"}],
            },
        )
        body = {
            "kind": "board",
            "name": "Private board",
            "body": {
                "items": [
                    {"artifact": mine["id"], "x": 20, "y": 30},
                    {"artifact": other["id"], "x": 50, "y": 60},
                    {"text": "Private thought", "x": 0, "y": 0},
                ]
            },
        }
        r = self.owner.put("/api/context/views/board-test", json=body)
        self.assertEqual(r.status_code, 200, r.text)
        self.assertEqual(self.other.get("/api/context/views").json()["items"], [])
        self.assertEqual(
            self.other.put("/api/context/views/board-test", json=body).status_code, 404
        )
        self.other.put(
            "/api/artifacts/" + other["id"] + "/access", json={"visibility": "private"}
        )
        view = self.owner.get("/api/context/views").json()
        self.assertNotIn("Shared temporarily", str(view))
        self.assertNotIn(other["id"], str(view))
        self.assertIn("Private thought", str(view))
        r = self.owner.post(
            "/api/context/batch",
            json={"artifacts": [mine["id"], other["id"]], "action": "archive"},
        )
        self.assertNotEqual(r.status_code, 200)
        self.assertFalse(
            self.owner.get("/api/artifacts/" + mine["id"]).json()["archived"]
        )
        r = self.owner.post(
            "/api/context/batch",
            json={"artifacts": [mine["id"]], "action": "tag", "value": "Priority"},
        )
        self.assertEqual(r.json()["updated"], 1)

    def test_filters_scope_cursors_and_sessions(self):
        for title, space in [("A", "Acme"), ("B", "Acme"), ("C", "Other")]:
            self.publish(
                self.owner,
                title=title,
                space=space,
                source={
                    "agent": "Codex",
                    "session": "test-session",
                    "device": "MacBook",
                },
            )
        import json

        params = {
            "filters": json.dumps(
                {
                    "join": "and",
                    "rules": [{"column": "space", "operator": "in", "value": ["Acme"]}],
                }
            ),
            "limit": 1,
            "sort": "title",
        }
        first = self.owner.get("/api/artifacts", params=params).json()
        self.assertEqual(first["total"], 2)
        second = self.owner.get(
            "/api/artifacts", params={**params, "cursor": first["next_cursor"]}
        ).json()
        self.assertEqual(second["artifacts"][0]["title"], "B")
        self.assertEqual(
            self.owner.get(
                "/api/artifacts",
                params={**params, "filters": "", "cursor": first["next_cursor"]},
            ).status_code,
            422,
        )
        self.assertEqual(
            len(self.owner.get("/api/context/sessions").json()["items"][0]["outputs"]),
            3,
        )
        self.assertEqual(self.other.get("/api/context/sessions").json()["items"], [])
