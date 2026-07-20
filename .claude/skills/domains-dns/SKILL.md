---
name: domains-dns
description: Domain and DNS checklist - records for Hostinger hosting, www vs
  apex, SSL issuance, email-related records when relevant. Use at first
  deploy or domain changes. Not for the deploy itself (deploy-hostinger).
  Claude prepares exact records; the human applies them in registrar/hPanel.
metadata: {version: 1.0.0, category: deploy, tier: E}
---
# Domains & DNS

## Purpose
Correct, complete DNS with zero guessing - wrong records mean downtime.

## Inputs
Domain + registrar from client (QUESTIONS.md if unknown), Hostinger
target (their current A/CNAME values - LOOK THEM UP in hPanel/docs at
execution time; do not trust memorized IPs).

## Outputs
A record-by-record checklist the human applies; verification steps.

## Rules
1. Produce a table: type | host | value | TTL | why - for A/ALIAS apex,
   CNAME www, and (only if client email rides the domain) MX/SPF/DKIM/
   DMARC lines as provided by their email provider, never invented.
2. Canonical host decision (www vs apex) is made once, redirected
   permanently at the host level, and matches sitemap/canonical tags
   (seo-technical) - log in DECISIONS.md.
3. SSL: issue via hPanel after DNS resolves; verify https + redirect
   http->https; HSTS only after a week of stable https (rollback safety).
4. Verification commands for the human (or run if network permits):
   dig +short A <domain>, dig +short CNAME www.<domain>, curl -I both
   hosts. Record outputs in BUILD_STATE.md - propagation confirmed by
   evidence, not by waiting vibes.
5. NEVER change records affecting email without listing current records
   first and flagging the risk explicitly.

## Anti-patterns
- Copying A-record IPs from memory/old projects; deleting unknown
  existing records ("cleanup") - unknown records get a question, not
  deletion.

## Changelog
- 1.0.0 initial
