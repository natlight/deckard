---
category: Projects
date: '2026-01-28 05:23:25'
subcategory: Deckard (Second Brain Assistant)
tags:
- deckard
- roadmap
- features
- obsidian
- para
- backlog
- product
title: 'Deckard Project: Feature Enhancements Backlog'
---

# Deckard Project: Feature Enhancements Backlog

> Backlog of feature enhancements for Deckard, formatted as an Obsidian-ready project note with wikilinks to create individual feature files when ready to work on them.

## Goal
Improve Deckard’s capability as a PARA-based “second brain” by adding UX, automation, quality, and integration enhancements.

## Success criteria
- Faster and more accurate PARA classification
- Better task/project handling and follow-through
- Cleaner, more consistent Obsidian note output
- Easier capture-to-note workflow (including external sources)

## Feature backlog (create files when ready)
> [!INFO] How to use
> Each item links to a placeholder note. Click the wikilink in Obsidian to create the feature file when you start work.

### Triage & organization
- [ ] [[Feature - Interactive Clarifying Questions]] — ask 1–3 targeted questions when classification is ambiguous
- [ ] [[Feature - Confidence Score for PARA Classification]] — output confidence and top alternatives
- [ ] [[Feature - Auto-Detect Projects vs Areas From Tasks + Deadlines]]
- [ ] [[Feature - Subcategory Suggestions From Context]] — propose consistent subcategories (e.g., “Health”, “Finances”)
- [ ] [[Feature - Duplicate Note Detection]] — detect near-duplicate titles/ideas and suggest merges
- [ ] [[Feature - Tag Normalization + Canonical Tag List]] — prevent tag drift (singular/plural, synonyms)

### Output quality (Obsidian-optimized Markdown)
- [ ] [[Feature - Standardized Note Templates per PARA Type]] — Projects/Areas/Resources/Archives
- [ ] [[Feature - Automatic Frontmatter Support (Optional)]] — configurable YAML fields
- [ ] [[Feature - Better Callout Heuristics]] — decide when to use INFO/WARNING/TIP blocks
- [ ] [[Feature - Wikilink Entity Extraction]] — consistently link people/tools/topics (e.g., [[PARA]], [[Obsidian]])
- [ ] [[Feature - Filename Slug Rules + Collision Handling]] — deterministic naming with suffixes

### Tasks & execution workflow
- [ ] [[Feature - Next Actions Extraction]] — generate actionable checklists from notes
- [ ] [[Feature - Project Plans With Milestones]] — create milestone sections + task groups
- [ ] [[Feature - Due Dates + Reminders (Obsidian Tasks/Dataview Compatible)]]
- [ ] [[Feature - Weekly Review Mode]] — summarize open projects/areas and propose next steps
- [ ] [[Feature - Definition of Done Generator]] — per project and per feature

### Capture & ingestion
- [ ] [[Feature - Email/Clipboard Quick Capture Format]] — minimal syntax that converts to notes
- [ ] [[Feature - Web Article Ingestion Summary]] — key points + highlights + source metadata
- [ ] [[Feature - YouTube Transcript Enhancer]] — chapters, key takeaways, action items
- [ ] [[Feature - Meeting Notes Processor]] — decisions, action items, owners, follow-ups
- [ ] [[Feature - Image-to-Note (OCR + Structure)]] — turn screenshots/whiteboards into notes

### Integrations
- [ ] [[Feature - Dataview Index Notes]] — auto-generate index pages per subcategory
- [ ] [[Feature - Obsidian Tasks Plugin Compatibility]] — standardized task syntax
- [ ] [[Feature - Calendar Integration]] — sync deadlines/milestones
- [ ] [[Feature - Readwise/Kindle Highlights Import]]
- [ ] [[Feature - GitHub Issues Sync (Optional)]] — mirror backlog items as issues

### Governance & safety
- [ ] [[Feature - Privacy/Sensitive Data Redaction]] — detect and redact secrets/PII
- [ ] [[Feature - Source Attribution + Citations]] — keep links and references to originals
- [ ] [[Feature - Configurable Output Policies]] — per vault preferences (tags, templates, links)

## Prioritization (suggested)
### Now (highest leverage)
- [[Feature - Interactive Clarifying Questions]]
- [[Feature - Standardized Note Templates per PARA Type]]
- [[Feature - Next Actions Extraction]]
- [[Feature - Wikilink Entity Extraction]]

### Next
- [[Feature - Confidence Score for PARA Classification]]
- [[Feature - Weekly Review Mode]]
- [[Feature - Duplicate Note Detection]]

### Later
- [[Feature - GitHub Issues Sync (Optional)]]
- [[Feature - Calendar Integration]]

## Notes
- Consider keeping feature notes in a dedicated folder like `Projects/Deckard (Second Brain Assistant)/Features/`.
- When creating a feature note, include: problem, user story, acceptance criteria, edge cases, and rollout plan.
