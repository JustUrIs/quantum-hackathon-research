# QCP-only Vercel deployment

## Target

Repository: https://github.com/JustUrIs/quantum-hackathon-research
Production branch: main.
Root Directory: `qcp-qollab`.
Framework: Other. Build command: empty. Output directory: `.`.
Environment variables: none. Budget: zero.

Vercel must serve only that folder. Do not deploy the repository root, `docs/`
or the other experiments. Keep `.vercel` project metadata out of Git and public
handoff archives. No authentication credentials belong in source or the bundle.

## Status: deployed and Git connected

Production: https://qcp-arena.vercel.app
Vercel project: `qcp-arena`.
Owner scope: `justurisbussines-2489s-projects` (Hobby).
Project ID: `prj_IqE0MOMxzh6yV7mzUZi28sUR7nNu`.
First verified deployment: `dpl_2hheRJUJukK4haPDt2j4uAVk3AhC`.
GitHub connection succeeded for the repository above; root is `qcp-qollab`.

On October 11, an unauthenticated browser reached HTTP 200, submitted A's
reference and obtained AC / 124 of 124 cases. Removing target preparation gave
WA. The legacy `/ambulancias-qollab/` path returned 404. The public domain does
not require login; generated preview/deployment domains may have Vercel auth.

The root `.vercelignore` allowlists QCP for CLI uploads. A dry run confirmed
15 QCP files totaling 147,775 bytes, excluding other projects and local env files.

Future Git pushes can produce new deployments. The deployment ID above records
the verified initial release, not necessarily the latest release.

Existing public fallback:
https://justuris.github.io/quantum-hackathon-research/qcp/

## Validation after deploy

1. Open the production URL in a clean browser without signing in.
2. Check that the title is QCP Arena and only three QCP problems appear.
3. Submit A's reference: expect AC, 124/124, browser execution source.
4. Remove target preparation: expect WA with a counterexample.
5. Confirm worker assets, Python runtime and solver.py load over HTTPS.
6. Confirm Git connection uses main and rootDirectory `qcp-qollab`.
7. Record the project identity, production URL and deployment ID here.

The Qollab ZIP is a separate deliverable. Vercel hosts browser practice; it does
not run the Qiskit backend or create a trusted server-side contest judge.

## Future deployment commands

In the original repository, the root is linked to the Vercel project:

```sh
npx vercel deploy --dry --json
npx vercel deploy --prod --yes --scope justurisbussines-2489s-projects
```

Run CLI deployment from the repository root, since the Vercel project's root
setting already points to `qcp-qollab`. An extracted handoff does not include
the local link: use `vercel link --project qcp-arena --scope
justurisbussines-2489s-projects` there before deploying. Retain a root
`.vercelignore` allowlist or deploy through the connected Git repository.
