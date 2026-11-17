# BMad Builder

> [!IMPORTANT]
> **BMad Builder is replaced by Toolsmith in BMad Method v7.** Upgrade to v7 and install Toolsmith to build skills, agents, and modules. This repo is no longer developed.
>
> **[Toolsmith documentation →](https://docs.bmad-method.org/toolsmith/toolsmith/)**

Toolsmith's source, issues, and releases live in the [BMAD-METHOD repo](https://github.com/bmad-code-org/BMAD-METHOD).

## Install Toolsmith

From your project directory, run:

```bash
npx skills add bmad-code-org/BMAD-METHOD/skills/core-tools --skill '*'
npx skills add bmad-code-org/BMAD-METHOD/skills/toolsmith --skill '*'
```

Then open your coding tool in the project and ask the `bmad` skill to run `bmad setup`. [How to Install BMad](https://docs.bmad-method.org/start/install-bmad/) covers the details.

## Upgrade From BMad v6

The v6 installer still installs BMad Builder at its last release, `v2.2.2`. It keeps working but gets no more changes. To upgrade to v7 and Toolsmith:

1. Install BMad v7 and Toolsmith as above, then run `bmad setup`. Setup offers to remove what v6 left behind in `_bmad/`.
2. Delete the old builder skills from your coding tool's skills folder: `bmad-agent-builder`, `bmad-workflow-builder`, `bmad-module-builder`, `bmad-bmb-setup`, and `bmad-eval-runner`.
3. If you built a module with BMad Builder, convert it with [Migrate an Old Module](https://docs.bmad-method.org/toolsmith/migrate-an-old-module/).

## v6 Documentation

The BMad Builder `v2.2.2` docs stay online for v6 users at [bmad-builder-docs.bmad-method.org](https://bmad-builder-docs.bmad-method.org/), with the source at the [`v2.2.2` tag](https://github.com/bmad-code-org/bmad-builder/tree/v2.2.2/docs). They are no longer updated.

## License

MIT. See [LICENSE](LICENSE).
