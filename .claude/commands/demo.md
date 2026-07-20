Set up the hosting branches and push the current local site for a demo.

1. Run `bash scripts/bootstrap-branches.sh` - creates any missing
   `staging` and `deploy` branch as a safe site-only placeholder
   (index.html "coming soon" + noindex robots.txt) so hosting can be
   connected to either branch immediately with zero OS files leaked.
2. Run `bash scripts/stage-split.sh` - snapshots the CURRENT LOCAL
   site/ files (uncommitted + untracked included), forces a noindex
   robots.txt, and force-pushes the site-only result to `staging`.
   The deploy branch's content is only ever written by /deploy.
3. Report: both branches exist site-root-ready; staging carries the
   current local site. The operator connects hosting manually in hPanel
   (staging -> demo subdomain's public folder, deploy -> public_html;
   one-time, per the deploy-hostinger skill) and pulls to view.
   Remind: the demo is PRE-QA - [PLACEHOLDER] text may be visible;
   never connect the client's production domain to staging.
