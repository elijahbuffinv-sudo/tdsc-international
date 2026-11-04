# Continuation runbook — TDSC hub city pages

State: all 201 jurisdiction pages are live at thieldetectiveagency.com/international/<slug>. Hub city pages remain.
Queue: /home/claude/intl/content/city_batches.json — `redo_weak` (5 cities with <5 sources) and `batches` (lists of "slug|Name|CC", 5 per batch), `done` (batch indexes finished).

Each continuation turn:
1. Launch up to 20 general-purpose agents in ONE message, each taking one unfinished batch (first turn also: one agent for `redo_weak`, told to strengthen the existing files to >=5 sources). Prompt: "Read /home/claude/intl/content/RESEARCH_RULES.md, then /home/claude/intl/content/CITY_BRIEF.md, and follow both exactly (max 2 WebSearch per city; fetch only URLs from your own search results). Cities (slug|name|CC): ... Write /home/claude/intl/content/cities/<slug>.json each. Reply only with files written and key review_flags (brief)."
2. Mark those batch indexes in `done`.
3. Copy content/cities/*.json to /home/claude/tdsc-international/content/cities/, regenerate REVIEW_FLAGS.md, commit + push, rebuild with TDSC_IDX_URL pinned to the new commit SHA (jsDelivr), rebuild /home/claude/upload/gf.html (= /home/claude/build/out/global-footer.html + sq/assets/search.js).
4. First execute /home/claude/intl/gen/sq_loader.js in the tab (javascript_tool) so window.TDSC skips pages not in the upload. Publish in the Squarespace tab (smilodon-tuatara-kttb.squarespace.com/config/pages/code-injection): the page has a hidden file input (aria-label "tdsc loader", recreate if missing — see window.TDSC loader; recreate both if the tab was reloaded) → upload changed fragments + manifest.json + gf.html (≤10 MB per upload), set footer CodeMirror (index 1) to gf.html, click Save, then `TDSC.run(null,'6aeb5f688d0897495b544ea9')`; verify every manifest path returns 200 with its data-tdsc-page key.
5. If batches remain, schedule the next continuation with send_later (10 minutes). When none remain, report to the user.

## Status note (2026-11-04 ~19:25 UTC)
Round 2 (batches 19-38) is built and pushed (commit cd20206c2dfc). Its Squarespace publish was started but the Chrome extension disconnected mid-run, so it is UNVERIFIED. On the next publish, upload every fragment changed since commit 4d679fb277e4 (git diff --name-only 4d679fb277e4 HEAD -- sq/pages), not just the latest round, then verify all manifest paths (throttled ~1/sec).
Held city files (hold: true, search-title-only research) need re-research: tunis, fuzhou, tirana, quito, ningbo, harbin, lahore; plus strasbourg and columbus were never written. These are in city_batches.json `redo_weak` — on re-research, remove the `hold` key.
If the browser is still unreachable, do the research and build/push anyway, then tell the user Chrome must be open for publishing.
