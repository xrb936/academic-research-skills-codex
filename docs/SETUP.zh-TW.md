# ARS 安裝設定

Academic Research Skills 在 Codex 上使用時的前置需求與選用設定。

---

## 最小可行設定

1. 安裝 Codex CLI。
2. 執行 `codex login` 完成登入。
3. 將四個 ARS skill 資料夾安裝到 `~/.codex/skills/`。
4. 執行 `codex` 開始使用。

這樣就能取得 Markdown 輸出與 DOCX 轉換說明。Pandoc、LaTeX、文獻語料 adapter 與跨模型驗證都是選用功能。

---

## 安裝與登入 Codex

請依你的環境安裝 Codex CLI，然後登入：

```bash
codex login
```

常用檢查：

```bash
codex --version
codex --help
```

長時間 workflow 可視需要使用：

```bash
codex --full-auto
```

`--dangerously-bypass-approvals-and-sandbox` 會同時關閉 approvals 與 sandbox，只應在外部已隔離的環境中使用。

## DOCX 輸出（選用）

若要直接產出 `.docx`，需要安裝 [Pandoc](https://pandoc.org/)。若系統沒有 Pandoc，formatter 會回退為 Markdown 與 DOCX 轉換說明。

```bash
# macOS
brew install pandoc

# Linux (Debian/Ubuntu)
sudo apt-get install pandoc

# Windows — download from https://pandoc.org/installing.html
```

## LaTeX / PDF 輸出（選用）

PDF 輸出需要 [tectonic](https://tectonic-typesetting.github.io/) 和特定字型。**這是選用的**。Markdown 輸出與 DOCX 轉換說明不需要這些。

```bash
# macOS
brew install tectonic

# Linux (Debian/Ubuntu)
curl --proto '=https' --tlsv1.2 -fsSL https://drop-sh.fullyjustified.net | sh

# Windows — download from https://tectonic-typesetting.github.io/en-US/install.html
```

**所需字型**（APA 7.0 中文輸出）：

- **Times New Roman**：macOS/Windows 通常已內建；Linux 安裝 `ttf-mscorefonts-installer`
- **Source Han Serif TC VF**（思源宋體）：從 [Google Fonts](https://fonts.google.com/specimen/Noto+Serif+TC) 或 [Adobe GitHub](https://github.com/adobe-fonts/source-han-serif) 下載
- **Courier New**：通常已內建

> 直接產出 `.docx` 需要 Pandoc，PDF 需要 `tectonic`。

---

## 安裝方式

Codex 預設從 `~/.codex/skills/<skill-name>/SKILL.md` 發現 skills。此 repo 包含四個獨立 skills，每個都有自己的 `SKILL.md`：

- `deep-research`
- `academic-paper`
- `academic-paper-reviewer`
- `academic-pipeline`

最可攜的安裝形狀是讓四個 skill 資料夾直接位於 `~/.codex/skills/` 下。

### 方法零：Codex Plugin Metadata

本 Codex 適配 fork 包含 `.codex-plugin/plugin.json`，供可直接讀取 repo root 作為 Codex plugin 的環境使用。此 manifest 指向同一套 ARS skills，並將 repository plugin metadata 與標準 skill 安裝路徑分開。

如果你的 Codex build 不會直接載入 repo plugin metadata，請使用方法一或方法二。

### 方法一：Symlink 安裝

如果你希望日後透過 pull repo 更新，這仍是最可攜的 Codex 安裝形狀。

```bash
git clone https://github.com/xrb936/academic-research-skills-codex.git ~/academic-research-skills-codex

mkdir -p ~/.codex/skills
ln -s ~/academic-research-skills-codex/deep-research ~/.codex/skills/deep-research
ln -s ~/academic-research-skills-codex/academic-paper ~/.codex/skills/academic-paper
ln -s ~/academic-research-skills-codex/academic-paper-reviewer ~/.codex/skills/academic-paper-reviewer
ln -s ~/academic-research-skills-codex/academic-pipeline ~/.codex/skills/academic-pipeline
```

預期路徑形狀：

```text
~/.codex/skills/deep-research/SKILL.md
~/.codex/skills/academic-paper/SKILL.md
~/.codex/skills/academic-paper-reviewer/SKILL.md
~/.codex/skills/academic-pipeline/SKILL.md
```

### 方法二：Copy 安裝

如果不方便使用 symlink，或需要跨機器同步，請使用 copy。

```bash
git clone https://github.com/xrb936/academic-research-skills-codex.git ~/academic-research-skills-codex

mkdir -p ~/.codex/skills
cp -R ~/academic-research-skills-codex/deep-research ~/.codex/skills/deep-research
cp -R ~/academic-research-skills-codex/academic-paper ~/.codex/skills/academic-paper
cp -R ~/academic-research-skills-codex/academic-paper-reviewer ~/.codex/skills/academic-paper-reviewer
cp -R ~/academic-research-skills-codex/academic-pipeline ~/.codex/skills/academic-pipeline
```

### 方法三：直接在 Repository 內使用

開發或測試 ARS 本身時可直接進入 repo：

```bash
git clone https://github.com/xrb936/academic-research-skills-codex.git
cd academic-research-skills-codex
codex
```

根目錄的 `AGENTS.md` 是 Codex 在此 repo 內工作時使用的專案層級 routing 與 workflow 指引。

---

## Material Passport `literature_corpus[]` Adapters（選用）

如果你已經維護一個策展過的文獻語料（Zotero、Obsidian、PDF 資料夾等），可以先把它打包進 Material Passport，讓 Phase 1 ARS agent 在去外部資料庫搜尋之前先讀你的文獻庫。此功能採 opt-in 與 presence-based 設計。沒提供語料時，ARS 走 external-DB-only flow，行為不變。

三個 reference Python adapter 位於 `scripts/adapters/`：

```bash
# 1. Install adapter dependencies
pip install -r requirements-dev.txt

# 2. Run a reference adapter. Both --passport and --rejection-log are required.
python scripts/adapters/folder_scan.py --input /path/to/pdfs         --passport passport.yaml --rejection-log rejection_log.yaml
python scripts/adapters/zotero.py      --input my-zotero-export.json --passport passport.yaml --rejection-log rejection_log.yaml
python scripts/adapters/obsidian.py    --input ~/Obsidian/Lit\ Notes --passport passport.yaml --rejection-log rejection_log.yaml
```

每個 adapter 會輸出 `passport.yaml` 與 `rejection_log.yaml`。Reference 之外的語料來源預期由使用者自行撰寫 adapter，遵循 [`academic-pipeline/references/adapters/overview.md`](../academic-pipeline/references/adapters/overview.md)。Consumer 行為見 [`academic-pipeline/references/literature_corpus_consumers.md`](../academic-pipeline/references/literature_corpus_consumers.md)。

## 選用環境變數

ARS 暴露若干 opt-in flag，全部預設 OFF；設定後僅影響當前 session。

| Flag | 起始版本 | 作用 | 參考 |
|---|---|---|---|
| `ARS_CROSS_MODEL` | v3.0 | 啟用跨模型驗證 | [`shared/cross_model_verification.md`](../shared/cross_model_verification.md) |
| `ARS_SOCRATIC_READING_PROBE=1` | v3.5.1 | 啟用 `socratic_mentor_agent` 的讀書檢查 probe layer。僅 goal-oriented intent；使用者引用過具體論文時最多觸發一次；婉拒不留紀錄懲罰。 | `deep-research/agents/socratic_mentor_agent.md` |
| `ARS_PASSPORT_RESET=1` | v3.6.3 | 把每個 FULL checkpoint 提升為 context 重置邊界。Emit boundary entry 必須設此 flag；新 session 用 `resume_from_passport=<hash>` 續跑不需要 flag。 | `academic-pipeline/references/passport_as_reset_boundary.md` |
| `ARS_CROSS_MODEL_SAMPLE_INTERVAL` | v3.5.0 | 跨模型完整性抽查的取樣間隔（advisory） | [`shared/cross_model_verification.md`](../shared/cross_model_verification.md) |

---

## 跨模型驗證（選用）

ARS 在 Codex 上以目前的 Codex 模型作為 primary agent。若需要更高信心，可選擇啟用第二模型或第二供應商來獨立驗證完整性檢查，並挑戰魔鬼代言人的判斷。

```bash
# Example: choose a verifier available to your environment
export OPENAI_API_KEY="sk-your-key-here"
export GOOGLE_AI_API_KEY="AIza-your-key-here"
export ARS_CROSS_MODEL="gpt-5.4-pro"

codex
```

沒有設定 `ARS_CROSS_MODEL` 時，一切會以一般單模型 Codex workflow 運作。支援的 model ID 與 API call pattern 見 [`shared/cross_model_verification.md`](../shared/cross_model_verification.md)。
