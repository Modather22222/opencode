# appycode Branding Map

Complete inventory of OpenCode's branding surface in this codebase, with the
customization action, lane, and merge-impact for each item. Policy statement
guides every decision; phases order the actual work.

## Policy

1. **Brand our surface.** Anything a user sees as *the product* (TUI, desktop,
   web app shell, CLI) gets the appycode name and art.
2. **Keep upstream service names.** "OpenCode Console", "OpenCode Go", the
   `opencode` provider, and their URLs are OpenCode-the-service, like
   "Anthropic" is Anthropic-the-provider. Rebranding those lies about who
   serves the models and breaks integrations.
3. **Keep functional plumbing.** `@opencode/*` package and SDK names,
   `OpenCode.make`/`OpenCodeClient`, `OPENCODE_*` env vars (including the
   `OPENCODE_CLI_NAME` define), `.opencode` config convention, startup paths.
   They are code/API identity, not brand, and live in upstream's hot paths.
4. **Additive over replacing.** Where a brand id is user-visible data (theme
   names for example), add an appycode variant and make it the default instead
   of renaming upstream ids users may reference.

## Inventory

### TUI (`packages/tui/src`)

| Location | Current | Action | Notes |
| --- | --- | --- | --- |
| `app.tsx:644,651` | terminal title `OpenCode` | `appycode` | lane C, safe |
| `app.tsx:1066` | "Update OpenCode" | "Update appycode" | lane C |
| `config/index.tsx:252` | "release highlights once after OpenCode updates" | "...after appycode updates" | lane C |
| `routes/session/permission.tsx:328` | "Tell OpenCode what to do differently" | lane C |
| `util/error-details.ts:11,18` | "OpenCode component"/"OpenCode configuration" (agent-facing debug prompt) | reword to appycode | lane C |
| `routes/session/index.tsx:2533` | "Upgrade to OpenCode Go" | **keep** | upstream's paid tier |
| `util/usage.tsx:121,274` | "Sign in to OpenCode Console…", "…credits in OpenCode Console" | **keep** | service names |
| `util/tool-display.ts:42` | provider label `opencode` → "OpenCode" | **keep** | provider display name |
| `theme/index.ts`, `context/theme.tsx` | theme ids `opencode`, `opencode2`, default active `opencode` | add `appycode` theme (or variants), make default | lane B+C hybrid, keep old ids for compat |
| 33-file total | most "OpenCode" hits are `@opencode/client` imports/types | **keep** | functional |

### CLI (`packages/cli/src`, `packages/core/src`)

| Location | Current | Action | Notes |
| --- | --- | --- | --- |
| `commands/commands.ts:48-49` | root spec name `appycode`, "appycode command line interface" | done (rebrand commit) | — |
| `script/build.ts:197` | `OPENCODE_CLI_NAME: "'appycode'"` | done | drives packaged builds |
| `services/standalone.ts:53`, `services/server-connection.ts:34` | HTTP basic auth username `"opencode"` | keep-candidate | internal wire credential; rename only if in doubt about fingerprinting, otherwise upstream-compat |
| `services/updater.ts` | Homebrew formulas, `opencode.exe` paths, update API `opencode.ai`, install script URL | keep until appycode ships its own release channel | fork updater work is its own project |
| `commands/handlers/stats.ts:120,131` | prints `opencode.ai` in stats table | keep (upstream stats site) or replace later if we host our own |
| `config/schema.ts:4` | `$schema` → `https://opencode.ai/v2/cli.json` | keep | editor validation against upstream schema; fork fields land upstream anyway |
| `commands/handlers/auth/login.ts:22` | `["opencode", 1]` (cwd basename check) | investigate before touching | env-specific tweak |

### Desktop (`packages/desktop`)

| Location | Current | Action | Notes |
| --- | --- | --- | --- |
| `electron-builder.config.ts:164,209,227,246` | `name: "OpenCode"`, productName "OpenCode"/"OpenCode Dev"/"OpenCode Beta" | "appycode" (+ channel suffix) | lane C; app store metadata |
| `electron-builder.config.ts` appIds | `ai.opencode.desktop(.dev/.beta)` | `dev.appycode.desktop(.dev/.beta)` | lane C; changes data dir identity of the app |
| `electron-builder.config.ts:228,247` | protocols scheme `opencode` | `appycode` | lane C; deep links |
| `electron-builder.config.ts:254` | rpm `packageName: "opencode"` | `appycode` | lane C |
| `electron-builder.config.ts` icons | `resources/<appId>.metainfo.xml` paths | appycode copies | fork-only additions + config refs |
| `src/main/windows/appearance.ts:29` | window title "OpenCode" | "appycode" | lane C |
| `resources/linux/opencode-desktop.desktop` | Name/Icon/Exec branding | appycode copy + config ref | fork-only + lane C ref |
| `resources/windows/installer.nsh` | channel install dirs keyed by `appId`/`APP_FILENAME` | mostly follows appIds; verify `APP_FILENAME` origin | lane C, light |
| `resources/icons/{prod,beta,dev}/icon.icns/ico/png` | opencode art | **replace with appycode art, same filenames** | binary lane C (upstream rarely changes them); ledger |
| i18n | no standalone dictionaries found; user-facing text is inline in components | string edits surfaces live with those files | — |

### Web app / desktop renderer (`packages/app/src`)

| Location | Current | Action | Notes |
| --- | --- | --- | --- |
| `app.tsx:60` | `<Title>OpenCode</Title>` | "appycode" | lane C |
| `shell/titlebar/windows-menu.tsx:127` | menu group label "OpenCode" | "appycode" | lane C |
| `servers/connect/screen.tsx:117` | connect screen brand `aria-label="OpenCode"` + `<Wordmark />` | "appycode" + our wordmark | lane C + art swap |
| `new-session/wordmark.tsx`, `wordmark.css` | new-session splash art/animation | appycode art (fork-only restyle or simplified static mark) | lane B preferred; keep component API |
| `settings/about/animated-wordmark.tsx` | about-page animated logo | appycode version or remove animation | lane C |
| `providers/opencode-logo.tsx` | provider icon for the `opencode` provider row | **keep** (service/provider icon) | — |
| `composer/model-label.ts:46` | `OpenCode / <model>` provider-prefixed label | **keep** | provider name |
| `voice/spec.ts:5,16` | "You are OpenCode's voice assistant" (live-voice persona) | "You are appycode's voice assistant" | lane C; only if voice ships |
| `usage/dialog.tsx`, `limits.ts` | OpenCode Console/Go copy | **keep** | service names |

### System prompts & skills (`packages/core/src`)

| Location | Current | Action | Notes |
| --- | --- | --- | --- |
| `plugin/identity.ts` | system prompt exposes only model name/provider — **no brand persona** | nothing to do | verified |
| `plugin/plan.ts`, `plugin/agent.ts` | task-mode prompts, brandless | nothing to do | verified |
| `plugin/skill/opencode.md`, `plugin/skill/report.md` | OpenCode usage/config docs as skill content | reword to appycode paths-or-keep | low value; doc-only |
| `tool/plugin/opencode.ts` | worktree tool prompt text mentions `tools.opencode.*` | **keep** | tool namespace references |

### Assets & non-shipped surfaces

| Item | Current | Action |
| --- | --- | --- |
| `packages/console/app/src/asset/brand/*` | official OpenCode logo/wordmark set (light/dark/simple), icon square, `opencode-brand-assets.zip` | upstream art — add appycode set alongside as fork-only files, then reference ours; do not delete upstream art (merge hygiene) |
| `packages/web/src/assets/lander/*` | marketing site screenshots/logos | www is upstream's site — fork does not ship it; no action |
| `packages/console` | OpenCode's SaaS console | fork uses upstream's hosted console; no rebrand |
| `services/www` | docs + lander | not fork-shipped; no action |

## Keep list (upstream-compat hard rules)

- Package/SDK names: `@opencode/*`, `OpenCode.make`, `OpenCodeClient`, plugin ids like `opencode.prompt.identity`
- Env prefix `OPENCODE_*` and build defines (`OPENCODE_CLI_NAME=appycode` is fine — the *define name* stays)
- `.opencode` project config convention, `opencode.json(c)` file names, `$schema` URL
- `/tmp/opencode`-style internal caches are already appycode-rooted via `packages/util/src/global.ts` `app = "appycode"` (done)
- `Provider.ID.opencode`, `ai.opencode/sessionID` MCP meta key, `console.opencode.ai`, `models.opencode.ai`, `models.dev`
- `opencode-local.db` and storage layer names (renaming touches schema context for zero user value)

## Execution phases

| Phase | Scope | Effort | Conflict risk |
| --- | --- | --- | --- |
| 1. TUI strings | six lane-C files in `packages/tui/src` | ~30 min | low |
| 2. Theme ids | additive `appycode` theme + default switch | ~1 h incl. token design | low |
| 3. Web app shell | title, menu, connect brand, voice persona | ~1 h | low-medium |
| 4. Desktop identity | electron-builder ids/names/protocols, window title, resources | ~2 h, verify by packaging | medium |
| 5. Art assets | appycode logo/wordmark/icon set, splash + about tiles | design-dependent | low (fork-only files) |
| 6. (later) own release channel | updater URLs, brew tap, npm scope | separate project | n/a until then |

## Phase 1 execution log (2026-10-29)

Audit method: exhaustive enumeration of every `OpenCode` occurrence in
`packages/tui/src` (string literals, JSX text, template literals, comments),
classified into functional / service-name / comment / visible-brand. Outcome:
68 functional, ~15 service-namekeepers, ~8 comments, 23 visible-brand edits
across 12 files.

| File | Edits | Note |
| --- | --- | --- |
| `app.tsx` | 4 | terminal title ×2, session-title prefix `OC \|` → `Appy \|`, "Update appycode" |
| `attention.ts` | 1 | `DEFAULT_TITLE` fallback title |
| `mini/runtime.lifecycle.ts` | 1 | fallback terminal title |
| `component/dialog-update.tsx` | 5 | updating/installing/success/copy incl. the literal `opencode` binary name users run |
| `component/terminal-pane.tsx` | 1 | persistent-terminal restart copy |
| `component/error-component.tsx` | 4 | crash screen header, version footer, report body, agent-facing `head` |
| `config/index.tsx` | 1 | release-highlights setting description |
| `mini/footer.permission.tsx` | 2 | permission prompt placeholder + text |
| `routes/session/permission.tsx` | 1 | permission prompt text |
| `mini/footer.prompt.tsx` | 1 | "close appycode" slash description |
| `util/error-details.ts` | 2 | agent-facing debug prompts |
| `feature-plugins/system/storybook/highlights.tsx` | 2 | storybook release-highlight fixtures |

Decisions made:

- `OC | ` prefix → `Appy | ` as the product's session-title abbreviation; revisit
  in Phase 2 theme work if a different mark is preferred.
- Kept "OpenCode includes free models…" (sidebar) — an OpenCode-service claim.
- Kept "Upgrade to OpenCode Go" and all OpenCode Console/Go copy — service names.
- Kept `opencode.ai/v2/docs` link and `openCode.*` command ids — ecosystem ids.
- Kept theme ids (`opencode`, `opencode2`) — Phase 2 adds an appycode theme and
  switches the default instead of renaming.

Verification: `bun typecheck` in `packages/tui` — clean across 1,773 files.

