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

## Phase 5 execution log — icons + favicons (2026-10-29)

Generated the appycode icon and the full downstream asset pipeline from one
committed 1024px master. Tooling: pure-stdlib Python generator
(`packages/desktop/icons/generate.py`, committed) — analytic-SDF rasterizer +
pyramid/area resampler + ICNS/ICO writers, since Pillow/numpy/ImageMagick were
unavailable in this environment and pip timed out. `bun tauri icon` + Image2Icon
(the upstream process in `icons/README.md`) remain the upstream path; our script
reproduces their invariants (premultiplied ICNS ladder, Big Sur padding/shadow,
`dock.png` sync).

Mark design (first attempt discarded): an amber lowercase "a" (donut bowl +
flush right stem) rendered as only a ring — the stem coincided with the ring's
right band and vanished. Final mark: rounded **frame ring** in `#c8873c`
(outer half-extent 260, thickness 96, corner radius 150) + **badge dot** in
`#f6ece0` (center 708,708, r 90, drawn over the band) on the `#0e3a53`
full-bleed canvas. Legible at 96 px and below; no baked rounding/shadow in the
master (channels/pipeline apply them).

| Output set | Files |
| --- | --- |
| 3 desktop channels × 53 | `icons/{dev,beta,prod}/**` (linux/tauri/ios/android ladder + `icon.icns`/`icon.ico`/`dock.png`) — **byte-identical across channels** |
| Favicon set | `packages/ui/src/assets/favicon/` (8 files: v3 + v1 twins of 96 PNG, SVG, ICO, apple-touch 180²) |

Decisions:

- One master art across dev/beta/prod instead of upstream's per-channel art
  (channel distinction stays in product names/appIds from Phase 4).
- Android adaptive `ic_launcher_background` color `#fff` → `#0E3A53`.
- Every regenerated file matches its committed source pixel size exactly
  (audit: 49 PNGs/channel valid + exact-size parity; `icon.ico` entries
  16–256; `icon.icns` codes icp4/icp5/icp6/ic07/ic08/ic09/ic10).

Code references repointed from the remote `https://opencode.ai/favicon-96x96-v3.png`
to the packaged root path `/favicon-96x96-v3.png` (served by `electron.vite`
`publicDir` for both the desktop renderer and the web app; origin-root
consistent with the app's existing `location.origin` usage):

- `packages/desktop/src/renderer/platform/notifications.ts`
- `packages/app/src/runtime/platform/web.ts`

Verification: 49/49 PNGs per channel parse with exact committed size parity;
ICO ladders 16–256 (prod) and 16/24/32/48/64/96/256 (favicon); ICNS member
codes match upstream's set; android backgrounds `#0E3A53`; visual check of the
master, `dock.png` composite and 96 px favicon; `bun typecheck` clean in
`packages/desktop` (2,937 files) and `packages/app` (1,883 files).

Remaining in Phase 5 (deferred; separate art pass): `<Wordmark />` visual on the
connect screen, about-page animated wordmark, TUI `logo.ts` art, splash/about
tiles.

## Phase 4 execution log (2026-10-29)

Desktop identity rebranded. New application identity: appId
`dev.appycode.desktop` (`.beta` / `.dev` per channel), product names
`appycode` / `appycode Beta` / `appycode Dev`, artifact name
`appycode-desktop-*`.

Edits:

| File | Edit |
| --- | --- |
| `electron-builder.config.ts` | `APP_IDS`, `artifactName`, protocol display names; stale app-id comments refreshed |
| `src/main/constants.ts` | `appIDs` / `appNames` + unpackaged dev fallbacks (`APP_ID`, `APP_NAME`) |
| `src/main/windows/appearance.ts`, `early.ts`, `src/renderer/index.html` | window/document titles → `appycode` |
| `script/copy-metainfo.ts` | appstream id/name/description/developer; bugtracker/vcs URLs → the fork repo; upstream screenshot asset kept (Phase 5) |
| `package.json` | author → `appycode` (upstream email dropped), homepage → fork repo |
| `script/bench-startup.ts` | `appIdFor` brand-family-aware: appycode names → `dev.appycode.desktop.*`, upstream names → `ai.opencode.desktop.*` so A/B benches against upstream builds in `dist/other` still resolve; default exe name; dev-channel proxy check now derives from channel (`.dev` suffix) not a hard-coded app id |
| `README.md` | title, beta channel app id, bench seed/exe paths |
| `electron-builder.config.test.ts` | channel identity table appIds (remaining assertions derive from config) |

Kept / decisions:

- Deep-link scheme `opencode://` unchanged — the redirect URI is registered by
  the OpenCode Console service (kept upstream service); changing schemes would
  break Console sign-in. Only the protocol *display name* rebranded.
- Update feeds remain `https://opencode.ai/update/api/...` (upstream).
  **Do not build distributables before Phase 6 lands own feeds**: the updater
  would otherwise replace appycode installs with upstream-signed builds.
- `resources/linux/opencode-desktop.desktop` legacy shim and its test
  assertions kept verbatim — migration path for users arriving from upstream
  Desktop whose pins still reference `/opt/OpenCode`.
- `install-state.ts` legacy data detection (`opencode.settings`,
  `opencode.global.dat`, `opencode` dir) kept — intentionally recognizes
  upstream-era state so a fresh appycode install can migrate it.

Verification: `bun test electron-builder.config.test.ts` — 7 pass / 193
expects; `bun typecheck` in `packages/desktop` — clean (2,937 files);
metainfo generation smoke — prod generates `dev.appycode.desktop` /
`appycode`.

## Phase 3 execution log (2026-10-29)

Surface: `packages/app` (web app + desktop renderer). ~1,586 user-visible
`OpenCode` occurrences across the i18n layer + shell chrome rebranded.

Method:

1. i18n transform (`packages/app/src/runtime/i18n/*.ts` — language files +
   `desktop-native.ts`): char-masked replace `OpenCode → appycode` (1,586
   occurrences), with English-literal protection spans for service names
   (Console / Go / Free — untranslated in every locale), plus
   `opencode pair → appycode pair` (pairing instructions; our binary name).
2. Translate-phrasing gap fix: protection matches only English literals, so
   translated keep-class strings (trademark line, free-models title,
   "OpenCode connected", "Connect to OpenCode", remote-credentials copy)
   over-rebranded in non-Latin locales; restored verbatim from git HEAD per
   key — `settings.about.trademark`,
   `dialog.model.unpaid.freeModels.title`, `provider.connect.console.connected`,
   `provider.connect.opencode.errorTitle`, `provider.connect.opencode.name`,
   `provider.connect.opencode.freeName`, `provider.connect.remote.description`,
   `command.provider.connect.description`, `command.usage.view.description` —
   124 entries restored.
3. Shell chrome: `app.tsx` `<Title>`, windows-menu group label,
   connect-screen brand aria-label, voice personas (`liveInstructions` +
   delegator `instructions`). The "Adapted from the OpenCode iOS app"
   provenance comment stays (factual attribution).
4. Dev-tooling consistency: 10 storybook `title: "OpenCode/…"` component
   paths → `"Appycode/…"` (provider fixtures inside them untouched).

Kept (audit result — every remaining `OpenCode` classified): OpenCode
Console/Go/Free copy incl. usage sections; trademark line verbatim in all 63
translated locales; provider display suffix ` / OpenCode`
(`providers/catalog/console.ts`), `OpenCode / ${name}`
(`composer/model-label.ts`) and their test fixtures; `OpenCodeLogo` provider
icon; `OpenCode.make/Client/Event`, `X-OpenCode-Capabilities`, `@opencode/*`
imports, `.opencode` config conventions and opencode.ai doc links.

Verification: `bun typecheck` in `packages/app` — clean (1,883 files);
keep-key grep audit — remaining `OpenCode` in i18n maps only to the keep set
above; trademark/free-models lines match HEAD verbatim in sampled locales
with zero stray `appycode` substitutions in the keep class.

## Phase 2 execution log (2026-10-29)

Brand palette provided by the user:

```css
--primary: #0e3a53;  --primary-hover: #0a2c41;  --primary-mid: #1b6284;
--primary-tint: #e6edf1;  --accent: #96591a;  --accent-bright: #c8873c;
--accent-tint: #f6ece0;
```

Method: fork-only theme document at `packages/tui/src/theme/assets/v2/appycode.json`,
generated from upstream's `opencode.json` with hue-only transformation — each
stop's lightness/saturation preserved so legibility equals upstream, hue
reassigned: `blue` ramp → primary navy family (light derived from
`--primary-mid`, dark from `--primary`), `orange` ramp → amber family
(`--accent-bright`). Structural parity with upstream verified (identical token
key set); net diff = 36 ramp stops + 2 mode mappings.

Identity mapping (both modes): `accent → $hue.orange` (amber), `interactive →
$hue.blue` (primary navy). Upstream light already matched this; dark was
reassigned from `{accent: purple, interactive: orange}`.

Registration edits (each logged in `FORK.md`):

| File | Edit |
| --- | --- |
| `theme/index.ts` | `appycode.json` import, `getAppycodeTheme()`, `listThemes()` entry, `system` ultimate-fallback → appycode |
| `context/theme.tsx` | 7 default-flow sites: initial active, config-name fallback, discovery-error fallback, missing-name default, error path (rethrow + fallback load) |
| `mini/theme.ts` | import, mini default name, RUN_THEME_FALLBACK(s), resolve fallback chain — `getOpenCodeTheme()` → `getAppycodeTheme()` |
| `dialog-config.tsx` | `theme.name` setting default → `"appycode"` |

Verification:

1. `bun typecheck` (packages/tui) — clean, 1,773 files.
2. Runtime document resolution: modes `["light","dark"]`; dark bg
   `rgb(10,10,10)` / light bg white — upstream-grade base surfaces preserved.
3. Brand check: dark `syntax.keyword`/`markdown.heading` → `#fac383`
   (accent-bright family); light → `#d68527` (accent family).

Kept: the `opencode` theme remains registered for configs referencing it; gray
neutrals stock (brand-tinted ink is a future iteration); `theme.mode` default
stays `system`. User-level overrides: `<config-dir>/themes/<name>.json`
discovered live with file basename as theme id.


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

