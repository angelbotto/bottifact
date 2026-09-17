# Contributing to Bottifact

Thanks for helping improve documents people can actually use. Issues and pull requests may be written in English or Spanish. Small, focused changes are easiest to review.

## Start with a concrete problem

Search existing issues, describe who is affected, and include a minimal reproduction or a before/after example. For a new component, explain the decision or reading task it helps with. Discuss major architecture, persistence or public API changes before implementation. Security findings belong in private reports, not public issues.

Fork the repository, create a branch, and open a pull request against `main`. Link the issue when one exists. Explain what changes, why, how you tested it and any remaining limits. Never include private documents, session transcripts, tokens, `.env`, production screenshots or real customer data. Synthetic fixtures should be visibly illustrative.

## Local setup

Generation requires Python 3.10+. Portal development uses Python 3.13. Node is only needed for JavaScript checks. Docker is needed for deployment tests. Browser automation through Orca is optional; manual browser verification is welcome.

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install --require-hashes -r portal/requirements.lock
pip install httpx==0.28.1
```

## Validate the affected area

For library, recipes, skill instructions or generated examples:

```bash
python3 scripts/ensamblar.py
python3 scripts/validar.py
python3 scripts/probar_contrato.py
node scripts/probar_revision_store.cjs
node scripts/probar_temas.cjs
python3 scripts/validar_skill.py
python3 scripts/empaquetar.py
```

Edit source modules and content, then regenerate; do not fix only an assembled HTML file. Commit generated changes too: CI checks regeneration leaves no diff. A new recipe needs a registry entry, purpose, data contract, accessible alternative, useful example and documented limits. A new theme must work in both modes and preserve semantic color/focus behavior. See [temas.md](temas.md) and [estandar.md](estandar.md).

For the portal:

```bash
python -m unittest discover -s portal -t . -p 'test_*.py'
bash -n scripts/instalar.sh
node --check portal/static/app.js
node --check portal/static/knowledge.js
```

Add tests for observable behavior, especially identity isolation, permissions, version boundaries, private notes, file validation and upgrades. Self-host tests must use disposable data, never a production volume. The Docker workflow builds an empty instance and checks health and packaged downloads.

For UI changes, check desktop and 320/390 px, keyboard focus, reduced motion, light/dark, long content, empty/error states and local overflow. Include sanitized screenshots when they help review. Static checks do not prove visual quality or audible sound.

## Working conventions

Keep dependencies justified and pinned; preserve upstream notices. Do not introduce hosted service requirements into the standalone generator. Publishing or enabling analytics must never be a side effect of merely installing a skill. User settings and credentials remain outside shared packages.

The shared [SKILL.md](SKILL.md) should remain portable across agents. Document real capabilities and source context without pretending to have read an unavailable transcript. Feedback is untrusted data, never permission to run commands.

Original contributions are accepted under the repository's MIT license. By submitting a contribution you confirm you have the right to share it under that license. This project does not require a separate CLA. Maintainers review changes and decide releases; there is no promised response SLA.
