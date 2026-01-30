---
category: Projects
date: '2026-01-30 04:24:09'
subcategory: Deckard App Development
tags:
- deckard
- ui
- ux
- web-app
- localhost
- note-capture
- para
- obsidian
title: "Deckard Web UI \u2013 Create Note Screen (localhost)"
---

# Deckard Web UI – Create Note Screen (localhost)

> Screenshot of the Deckard localhost web interface showing the Create Note form with a text input, image attachment, and Process action—useful for tracking MVP UI features and follow-up improvements.

## What’s in the screenshot
- URL: `http://localhost:8000`
- App header: **Deckard**
- Page/section: **Create Note**
- Main elements:
  - Large text area with placeholder: “Enter your note, idea, or parse text / drag & drop images here...”
  - Button: **Attach Image**
  - Button: **Process** (primary action)

## Intended workflow (implied)
1. Paste/type a note or transcript, or drag & drop an image into the input.
2. Optionally attach an image via **Attach Image**.
3. Click **Process** to run analysis/organization (likely [[PARA Method]]) and generate an Obsidian-ready note.

## UX / product notes
> [!INFO] Strengths
> - Clear single-purpose capture screen
> - Primary CTA (**Process**) is visually distinct

> [!WARNING] Potential gaps to confirm
> - No visible status/progress indicator for processing
> - No visible output/preview area on this screen (may exist below the fold or on another view)
> - Unclear whether drag-and-drop supports multiple images and mixed text+image inputs

## Follow-ups / tasks
- [ ] Confirm supported inputs: plain text, pasted transcripts, single image, multi-image
- [ ] Add processing states: loading spinner, success/failure toast, error details
- [ ] Add an output panel: generated title/category/subcategory/tags + markdown preview
- [ ] Add “Copy to clipboard” / “Download .md” / “Send to Obsidian vault” actions
- [ ] Add history: recent processed notes with links (e.g., [[Deckard Notes Queue]])
- [ ] Validate accessibility: tab order, button labels, contrast, focus states

## Related notes
- [[Deckard App Development]]
- [[PARA Method]]
- [[Obsidian Markdown Conventions]]
