# Fork of OpenCode

- Upstream: https://github.com/anomalyco/opencode (default branch `dev`)
- Upstream base commit: `1341387981` — "feat(app): align searchable dialogs (#60162)"
- Remote layout: `upstream` = anomalyco/opencode, `origin` = Modather22222/opencode
- Working branch: `our-release` (merges `dev` regularly). `dev` here tracks upstream `dev`.

This file documents everything that is not upstream. If a sync conflict ever
touches a file listed in the divergence ledger, each entry explains why the
file was changed and what must be preserved.

## Customization rules

1. Prefer customization **as data**: configuration files, themes, agent
   definitions, instructions. These live outside the tracked tree or in
   clearly-named directories and merge cleanly, forever.
2. Code edits to tracked upstream files go in the ledger below. If a file is
   not in the ledger, the file must be identical to upstream.

## Divergence ledger

| Change | Files | Reason | Upstream merge behavior |
| --- | --- | --- | --- |
| Fork bookkeeping | `FORK.md`, `script/fork-sync.sh` | fork maintenance | none (fork-only additions) |

## Environment quirks

### Bun cache truncation bug (worked around once)

During the first corrupted install, bun's global cache stored a truncated
extraction of `@babel/types@7.29.8` (missing `lib/constants/generated/index.js`),
which later installs trusted and propagated. Verified the npm registry tarball
was intact, then repaired by extracting it over the store copy:

```sh
curl -sL https://registry.npmjs.org/@babel/types/-/types-7.29.8.tgz -o /tmp/t.tgz
mkdir /tmp/fresh && tar -xzf /tmp/t.tgz -C /tmp/fresh
cp -a /tmp/fresh/package/. node_modules/.bun/@babel+types@7.29.8/node_modules/@babel/types/
```

If a "Cannot find module ./constants/generated/index.js" style error reappears
after a future `bun install`, re-verify the tarball and re-apply this repair
against the version bun resolved.

### pkg.pr.new egress blocked (workspace only)

The catalog pins `@solidjs/start` from `https://pkg.pr.new/@solidjs/start@dfb2020`
and this workspace's egress does not allow pkg.pr.new, so `bun install` ends
with "Failed to install 1 package". Impact is limited to the web app and
desktop packages (`bun dev:web`, `bun dev:desktop`, `bun dev:console`), not the
CLI/server/TUI. Do not repoint the pin: it is an upstream choice. Development
must happen where pkg.pr.new is reachable, or the affected packages need an
environment-specific resolution we document here.

## Development recipes

```sh
bun install                          # full workspace install
bun dev [directory]                  # dev CLI + TUI (from repo root)
bun src/index.ts serve --port 4096   # dev server only (from packages/cli)
curl localhost:4096/api/info         # expect {"_tag":"UnauthorizedError"} when healthy
```

## Sync runbook

```sh
script/fork-sync.sh
```

Fetches upstream, fast-forwards `dev` to `upstream/dev` (no merge commits on
the tracking branch), then merges `dev` into `our-release`. Resolve conflicts
with the divergence ledger open; push with `git push -u origin our-release`.
Run it weekly — upstream averages dozens of commits per day and drift
compounds.
