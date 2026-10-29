# appycode

appycode is a fork of [OpenCode](https://github.com/anomalyco/opencode), the
open source AI coding agent, maintained independently with its own branding and
customer customizations.

OpenCode under the hood: client–server architecture, build/plan agents,
plugins, MCP, and the full provider ecosystem. This fork tracks upstream's
`dev` branch through regular merges and adds its own user-facing layer.

## Building on top of OpenCode

appycode is **not** built by the OpenCode team and is not affiliated with the
OpenCode project in any way, beyond deriving from and crediting its MIT-licensed
code. The upstream project documents this expectation for forks.

## Local development

```sh
bun install          # from the repository root
bun dev              # dev CLI + TUI
bun src/index.ts serve --port 4096   # dev server only
bun run check        # lint + typecheck
```

app's binary is `appycode`; UX differs from upstream only in branding and
config/state isolation (`~/.config/appycode`, `~/.local/share/appycode`).

## Fork maintenance

- `FORK.md` — divergence ledger and environment quirks. Any change to a
  tracked upstream file must be recorded there.
- `script/fork-sync.sh` — fetch upstream, fast-forward `dev`, merge into
  `our-release` weekly.

## License

MIT (upstream's license, inherited and preserved for our changes). See
[LICENSE](LICENSE).
