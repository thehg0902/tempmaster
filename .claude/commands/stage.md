Push the current local website files to the `staging` branch.

1. Run `bash scripts/stage-split.sh` - snapshots the CURRENT LOCAL
   site/ working tree (uncommitted + untracked files included), forces
   a noindex robots.txt, verifies zero OS files, and force-pushes the
   site-only result to `staging`.
2. Report: staging updated - check the demo subdomain (pull in hPanel
   first if the webhook isn't enabled).

No gates, no commit required, repeatable after every edit. Staging is
pre-QA by design; never connect the client's production domain to it.
