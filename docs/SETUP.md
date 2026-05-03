# ARS Setup

Prerequisites and optional setup for Academic Research Skills on Codex.

---

## Minimum Viable Setup

1. Install Codex CLI.
2. Run `codex login`.
3. Install the four ARS skill folders under `~/.codex/skills/`.
4. Start Codex with `codex`.

That is enough for Markdown output and DOCX conversion instructions. Pandoc, LaTeX, corpus adapters, and cross-model verification are optional.

---

## Install And Authenticate Codex

Install Codex CLI using the method appropriate for your environment, then authenticate:

```bash
codex login
```

Useful local checks:

```bash
codex --version
codex --help
```

For a lower-friction long-running session, Codex supports:

```bash
codex --full-auto
```

Use `--dangerously-bypass-approvals-and-sandbox` only in an externally sandboxed environment where you are comfortable disabling both approvals and sandboxing.

## DOCX Output (Optional)

Direct `.docx` generation uses [Pandoc](https://pandoc.org/). If Pandoc is unavailable, the formatter falls back to Markdown plus DOCX conversion instructions.

```bash
# macOS
brew install pandoc

# Linux (Debian/Ubuntu)
sudo apt-get install pandoc

# Windows — download from https://pandoc.org/installing.html
```

## LaTeX / PDF Output (Optional)

PDF output requires [tectonic](https://tectonic-typesetting.github.io/) and specific fonts. **This is optional** — Markdown output and DOCX conversion instructions work without any of this.

```bash
# macOS
brew install tectonic

# Linux (Debian/Ubuntu)
curl --proto '=https' --tlsv1.2 -fsSL https://drop-sh.fullyjustified.net | sh

# Windows — download from https://tectonic-typesetting.github.io/en-US/install.html
```

**Required fonts** for APA 7.0 CJK output:

- **Times New Roman** — usually pre-installed on macOS/Windows; on Linux install `ttf-mscorefonts-installer`
- **Source Han Serif TC VF** — download from [Google Fonts](https://fonts.google.com/specimen/Noto+Serif+TC) or [Adobe GitHub](https://github.com/adobe-fonts/source-han-serif)
- **Courier New** — usually pre-installed

> Direct `.docx` generation requires Pandoc, and PDF generation requires `tectonic`.

---

## Installation Methods

Codex discovers skills under `~/.codex/skills/<skill-name>/SKILL.md` by default. This repo contains four separate skills, each with its own `SKILL.md`:

- `deep-research`
- `academic-paper`
- `academic-paper-reviewer`
- `academic-pipeline`

Do not install the whole repository as one nested skill folder unless your Codex build is known to recurse through nested skill directories. The most portable shape is one folder per skill directly under `~/.codex/skills/`.

### Method 0: Codex Plugin Metadata

This Codex-adapted fork includes `.codex-plugin/plugin.json` for environments that can consume a repository root as a Codex plugin. The manifest points at the same ARS skill suite and keeps repository plugin metadata separate from the standard skill install path.

If your Codex build does not load repository plugin metadata directly, use Method 1 or Method 2.

### Method 1: Symlink Install

Use this when you want updates by pulling the repository. This remains the most portable Codex install shape.

```bash
git clone https://github.com/xrb936/academic-research-skills-codex.git ~/academic-research-skills-codex

mkdir -p ~/.codex/skills
ln -s ~/academic-research-skills-codex/deep-research ~/.codex/skills/deep-research
ln -s ~/academic-research-skills-codex/academic-paper ~/.codex/skills/academic-paper
ln -s ~/academic-research-skills-codex/academic-paper-reviewer ~/.codex/skills/academic-paper-reviewer
ln -s ~/academic-research-skills-codex/academic-pipeline ~/.codex/skills/academic-pipeline
```

Expected path shape:

```text
~/.codex/skills/deep-research/SKILL.md
~/.codex/skills/academic-paper/SKILL.md
~/.codex/skills/academic-paper-reviewer/SKILL.md
~/.codex/skills/academic-pipeline/SKILL.md
```

### Method 2: Copy Install

Use this when symlinks are inconvenient or when syncing across machines.

```bash
git clone https://github.com/xrb936/academic-research-skills-codex.git ~/academic-research-skills-codex

mkdir -p ~/.codex/skills
cp -R ~/academic-research-skills-codex/deep-research ~/.codex/skills/deep-research
cp -R ~/academic-research-skills-codex/academic-paper ~/.codex/skills/academic-paper
cp -R ~/academic-research-skills-codex/academic-paper-reviewer ~/.codex/skills/academic-paper-reviewer
cp -R ~/academic-research-skills-codex/academic-pipeline ~/.codex/skills/academic-pipeline
```

### Method 3: Standalone Repository Work

Use this when developing or testing ARS directly.

```bash
git clone https://github.com/xrb936/academic-research-skills-codex.git
cd academic-research-skills-codex
codex
```

The root `AGENTS.md` contains project-level routing and workflow guidance for Codex when working inside this repository.

---

## Material Passport `literature_corpus[]` Adapters

If you maintain a curated literature corpus (Zotero, Obsidian, a folder of PDFs, etc.), you can pre-load it into a Material Passport so Phase 1 ARS agents read your library before searching external databases. This is opt-in and presence-based — when no corpus is supplied, ARS runs the external-DB-only flow unchanged.

Three reference Python adapters ship at `scripts/adapters/`:

```bash
# 1. Install adapter dependencies
pip install -r requirements-dev.txt

# 2. Run a reference adapter. Both --passport and --rejection-log are required.
python scripts/adapters/folder_scan.py --input /path/to/pdfs         --passport passport.yaml --rejection-log rejection_log.yaml
python scripts/adapters/zotero.py      --input my-zotero-export.json --passport passport.yaml --rejection-log rejection_log.yaml
python scripts/adapters/obsidian.py    --input ~/Obsidian/Lit\ Notes --passport passport.yaml --rejection-log rejection_log.yaml
```

Each adapter emits `passport.yaml` and `rejection_log.yaml`. Users with non-reference corpus sources are expected to write their own adapters following [`academic-pipeline/references/adapters/overview.md`](../academic-pipeline/references/adapters/overview.md). Consumer behavior is documented in [`academic-pipeline/references/literature_corpus_consumers.md`](../academic-pipeline/references/literature_corpus_consumers.md).

## Optional Environment Flags

ARS exposes a few opt-in flags. All default to OFF; setting them changes behaviour for the current session only.

| Flag | Since | What it does | Reference |
|---|---|---|---|
| `ARS_CROSS_MODEL` | v3.0 | Enable cross-model verification | [`shared/cross_model_verification.md`](../shared/cross_model_verification.md) |
| `ARS_SOCRATIC_READING_PROBE=1` | v3.5.1 | Activate the Socratic reading-check probe layer in `socratic_mentor_agent`. Goal-oriented intent only; fires at most once per session when user has cited a specific paper; decline logged without penalty. | `deep-research/agents/socratic_mentor_agent.md` |
| `ARS_PASSPORT_RESET=1` | v3.6.3 | Promote every FULL checkpoint to a context-reset boundary. Required to emit boundary entries; not required to invoke `resume_from_passport=<hash>` in a fresh session. | `academic-pipeline/references/passport_as_reset_boundary.md` |
| `ARS_CROSS_MODEL_SAMPLE_INTERVAL` | v3.5.0 | Sampling interval for cross-model integrity checks (advisory) | [`shared/cross_model_verification.md`](../shared/cross_model_verification.md) |

---

## Cross-Model Verification (Optional)

ARS runs on Codex as the primary agent. For higher confidence, you can optionally enable a second model/provider to independently verify integrity checks and challenge devil's-advocate judgments.

```bash
# Example: choose a verifier available to your environment
export OPENAI_API_KEY="sk-your-key-here"
export GOOGLE_AI_API_KEY="AIza-your-key-here"
export ARS_CROSS_MODEL="gpt-5.4-pro"

codex
```

When `ARS_CROSS_MODEL` is not set, everything runs as a normal single-model Codex workflow. See [`shared/cross_model_verification.md`](../shared/cross_model_verification.md) for supported model IDs and API call patterns.
