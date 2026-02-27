## Next Session: Revenue Analysis Follow-ups

**Date:** 2026-02-28
**Pick up from here tomorrow morning.**

---

### 1. Apply the pitch plan to the 50 Tips script

The self-audit now has a full pitch plan for the 50 Tips video (see `self-audit/2026-02-self-audit.md`, bottom section). The script at `scripts/50 Tips for Claude Code.md` needs:

- [ ] Add opening pitch after tip 1 (newsletter-first, masterclass secondary — it's a pillar video)
- [ ] Upgrade mid-video CTAs to reference specific downloadables (tips 1, 30, 31)
- [ ] Add closing pitch with masterclass + price escalation (if price increase is planned)
- [ ] Keep total CTAs to 3-4 max (opening, 1-2 mid-video, closing)

### 2. Project reorganisation ideas

The revenue data currently lives in `socials/youtube/revenue/`. Consider:

**Option A: Keep revenue/ as-is, add cross-references**
- Revenue analysis stays in `revenue/`
- Self-audit stays in `self-audit/`
- Add `@revenue/2026-02-pitch-analysis.md` reference in the self-audit
- Lightweight, no restructuring needed

**Option B: Create a unified `strategy/` folder**
```
socials/youtube/
├── strategy/
│   ├── 2026-02-self-audit.md        (moved from self-audit/)
│   ├── 2026-02-revenue-analysis.md  (moved from revenue/)
│   ├── 2026-02-pitch-analysis.md    (moved from revenue/)
│   ├── hypotheses.md                (extracted from self-audit)
│   └── chart.html                   (moved from revenue/)
├── ab-tests/
├── analysis/
├── scripts/
└── transcripts/
```
Pro: everything actionable is in one place. Con: breaks the existing convention where `self-audit/` = your content, `analysis/` = competitors.

**Option C: Keep structure, add a lightweight `playbook.md` at the youtube root**
- `socials/youtube/playbook.md` — a single file that links to the self-audit, revenue analysis, pitch analysis, and hypotheses
- Acts as an index page / dashboard for "what to do next"
- Doesn't move any files

**Recommendation: Option C** — least disruptive, and Obsidian's backlinks will connect everything. Create the playbook tomorrow once you decide what goes in it.

### 3. Track hypothesis results going forward

After each new video, run the same Stripe query (3-day window) and log:
- Which hypotheses were tested (H1-H7)
- Exact pitch language used
- Revenue result
- Compare to baseline

Could add a `revenue/hypothesis-log.md` file that accumulates results over time.

### 4. Rotate the Stripe API key

The restricted key `rk_live_...` was shared in the chat. Rotate it in the Stripe dashboard.
