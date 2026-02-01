---
category: Resources
date: '2026-01-23 04:23:59'
subcategory: Databases
tags:
- database
- sqlite
- libsql
- edge
- replication
- serverless
- github
- tooling
title: "Turso (libSQL) \u2014 GitHub Repository"
---

# Turso (libSQL) — GitHub Repository

> Reference note for the Turso GitHub repository (tursodatabase/turso), a libSQL/SQLite-based database project focused on edge/serverless use cases and replication.

## Link
- Repo: https://github.com/tursodatabase/turso

## What it is
- [[Turso]] is a database project in the Turso ecosystem, built around [[libSQL]] (a fork/evolution of [[SQLite]]) and oriented toward low-latency/edge deployments.

> [!INFO] Why this matters
> Turso/libSQL commonly comes up when you want SQLite-like simplicity with replication and edge-friendly deployment patterns.

## Notes / angles to explore
- Architecture: libSQL + replication model (primary + replicas / edge copies)
- Hosting options: managed vs self-hosted
- Compatibility: SQLite APIs, drivers, extensions
- Operational concerns: backups, migrations, consistency model, latency

## Possible next actions
- [x] Skim README and extract key commands (install, local dev, deploy)
- [x] Identify supported languages/drivers and add links (e.g., [[TypeScript]], [[Go]], [[Rust]], [[Python]])
- [x] Capture replication/consistency guarantees and limitations
- [ ] Compare with [[SQLite]], [[PostgreSQL]], [[Cloudflare D1]]

## Related notes (create if useful)
- [[SQLite]]
- [[libSQL]]
- [[Edge databases]]
- [[Serverless databases]]
- [[Database replication]]