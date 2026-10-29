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
| Rebrand app name (XDG roots) | `packages/util/src/global.ts` | isolate `~/.config/appycode` et al. from upstream opencode | likely conflict — keep the one-line change |
| Rebrand CLI name | `packages/cli/src/commands/commands.ts`, `packages/cli/script/build.ts` | help/usage show `appycode` | likely conflict — keep literal swap |
| Fork README | `README.md` | appycode intro, attribution | none — content divergence is intentional |
| Branding inventory | `BRANDING.md` | fork-only brand map and phase plan | none (fork-only addition) |
| Branding phase 1 | 12 files in `packages/tui/src` (see `BRANDING.md` execution log) | visible strings say appycode, `OC \|` → `Appy \|` titles | medium — string-level only; on conflicts keep our copy |
| Branding phase 2 theme | `packages/tui/src/theme/assets/v2/appycode.json` (fork-only); edits in `theme/index.ts`, `context/theme.tsx`, `mini/theme.ts`, `component/dialog-config.tsx` | appycode is the registered default theme (navy/amber brand) | medium — small literal swaps; keep ours on conflict; re-base `appycode.json` if upstream updates `opencode.json` |
| Branding phase 3 app shell | `packages/app/src/runtime/i18n/*.ts` (1,586 occurrences rebranded, keep-key restore from HEAD); `app.tsx` Title, `shell/titlebar/windows-menu.tsx`, `servers/connect/screen.tsx` aria-label, `voice/spec.ts` personas, 10 storybook `title:` paths | visible app surface says appycode; Console/Go/Free + trademark + provider labels verbatim | medium — locale files churn heavily upstream; on conflicts re-run the key-level restore (keep-keys listed in `BRANDING.md` phase 3 log) |
| Branding phase 4 desktop identity | `electron-builder.config.ts`, `src/main/constants.ts`, window titles (`windows/appearance.ts`, `windows/early.ts`, `renderer/index.html`), `script/copy-metainfo.ts`, `script/bench-startup.ts`, `package.json` author+homepage, `README.md`, builder config test channel table | appIds `dev.appycode.desktop.*`, product names appycode; `opencode://` scheme + update feeds + legacy shims kept | high — upstream reworks packaging often; keep it, and re-run `bun test electron-builder.config.test.ts` after every sync |
| Branding phase 5 app icons | `packages/desktop/icons/**` (147 binaries + 2 android XMLs, byte-identical across the 3 channels), fork-only `icons/generate.py` + `icons/app-icon.png`, `icons/README.md`, `packages/ui/src/assets/favicon/**` (8), icon refs in `desktop/src/renderer/platform/notifications.ts` + `app/src/runtime/platform/web.ts` | appycode mark (amber frame ring `#c8873c` + cream badge dot `#f6ece0` on navy `#0e3a53`) across all icon ladders and favicons; notifications point at the packaged `/favicon-96x96-v3.png` instead of `opencode.ai` | medium — upstream rarely churns icons; on conflict keep ours and re-run `python3 generate.py` from the committed master (recipe in `icons/README.md`) |

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

### husky pre-push requires `bun run check`

Upstream's pre-push hook runs `bun run check` (lint + typecheck). In this
workspace it fails because `packages/app` cannot typecheck without the
pkg.pr.new dependency. Until the dependency is reachable here, push fork-only
branches with `git push --no-verify`, and run `bun run check` manually for the
packages you actually touched from their package directories. Restore normal
pre-push behavior once egress allows pkg.pr.new or the checks pass again.

## Development recipes

```sh
bun install                          # full workspace install
bun dev [directory]                  # dev CLI + TUI (from repo root)
bun src/index.ts serve --port 4096   # dev server only (from packages/cli)
curl localhost:4096/api/info         # expect {"_tag":"UnauthorizedError"} when healthy
```

## Daily feature development workflow

```sh
git checkout -b short-hyphen-name our-release   # work branch from integration
git commit -m "feat(tui): describe the change"  # conventional, fork commits too
# verify what you touched, from the package you touched:
#   cd packages/<pkg> && bun typecheck && bun run test
git checkout our-release && git merge short-hyphen-name
git push --no-verify
```

Branches off `our-release` are short-lived; never commit on `dev` (it may only
fast-forward). For review before merging, open a PR on the fork branch instead.

Choose the lane shaping the change:

| Feature type | Lane | Where it lives |
| --- | --- | --- |
| Agent, command, skill, theme, instructions | A — data | config/markdown, fork-only paths |
| New tool/plugin, MCP server, package | B — additive | new fork-only directories |
| Changing existing behavior | C — surgical | 1–3 tracked files, ledgered at commit time |

Lane C rules:

1. Attempt an upstream contribution first when the change would serve everyone;
   contributing costs design review but removes divergence permanently.
2. Otherwise keep the diff minimal and add the ledger row in the same commit.
3. Prefer the smallest reuse of upstream extension points (build defines like
   `OPENCODE_CLI_NAME`, plugin APIs) to hand-written harnesses.

## Sync runbook

```sh
script/fork-sync.sh
```

Fetches upstream, fast-forwards `dev` to `upstream/dev` (no merge commits on
the tracking branch), then merges `dev` into `our-release`. Resolve conflicts
with the divergence ledger open; push with `git push -u origin our-release`.
Run it weekly — upstream averages dozens of commits per day and drift
compounds.
