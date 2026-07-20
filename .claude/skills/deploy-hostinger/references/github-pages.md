# GitHub Pages Deploy (from the client repo)

VERIFY current GitHub UI labels against docs at setup time - panels change.

## Setup
Repo Settings -> Pages -> "Deploy from a branch", pick branch + directory,
save. Pages builds and serves within ~1 minute; the URL appears on the
same screen (`https://<user>.github.io/<repo>/`).

## Serving the site/ subdir - two options
Pages serves a directory, and only offers `/` (root) or `/docs` of the
chosen branch. The deliverable lives in `site/`, so:

1. **The `deploy` branch (RECOMMENDED - already generated):** the same
   site-only branch scripts/deploy-split.sh produces for Hostinger works
   unchanged for Pages - its ROOT contains the CONTENTS of site/ (zero
   OS files, proven on every run). Update flow per deploy: /qa then
   `bash scripts/deploy-split.sh`. Pages setting: branch `deploy`,
   directory `/`. One deploy mechanism for both hosts.

2. **docs/ convention (simpler, noisier):** rename/copy the deliverable
   into `docs/` on the deploy branch and point Pages at `/docs`. One
   branch, but the repo carries a second copy of the site and the "docs"
   name is misleading. Acceptable for quick demos; not preferred.

Log the chosen option in DECISIONS.md at first deploy and never mix.

## Custom domain + HTTPS
Settings -> Pages -> Custom domain: enter the domain; add the DNS records
per domains-dns skill (CNAME for www to <user>.github.io; A/AAAA records
for apex per current GitHub docs). Check "Enforce HTTPS" once the cert
provisions (can take up to a day after DNS propagates).

## Notes
- The QA-gate hook applies: any `git push` is blocked until phase 6 = done.
- Post-deploy checks from the skill body apply (every page 200s, assets
  load, forms/embeds work, https padlock).
- Pages is static-only: fine — this system ships plain HTML/CSS/JS.
