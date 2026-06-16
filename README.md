# 🌿 KI-Agenten-Farm

**Version:** `1.1.0` | **Lizenz:** MIT | **Inference:** OpenClaw (lokal, 0 Token-Kosten)

Eine **insel-stabile, vollautomatisierte KI-Agenten-Farm** zur Übernahme von Remote-Jobs durch lokale LLMs. Entwicklung, Validierung, Testing und Git-Deployment laufen als **One-Command-Pipeline**.

---

## 📋 Inhaltsverzeichnis

1. [Projektübersicht](#1-projektübersicht)
2. [Systemarchitektur](#2-systemarchitektur)
3. [Voraussetzungen & Installation](#3-voraussetzungen--installation)
4. [Master-Konfiguration](#4-master-konfiguration)
5. [Skripte & Pipeline](#5-skripte--pipeline)
6. [Workflow-Templates](#6-workflow-templates)
7. [Agenten-Definitionen](#7-agenten-definitionen)
8. [Insel-Stabilität & Zero-Token-Optimierung](#8-insel-stabilität--zero-token-optimierung)
9. [Ausführung & Testing-Protokoll](#9-ausführung--testing-protokoll)
10. [Git-Automatisierung](#10-git-automatisierung)
11. [Skalierung & Gehalts-Pooling](#11-skalierung--gehalts-pooling)
12. [Web-Panel (UI) – Mehrsprachigkeit, Export, Theme](#12-web-panel-ui--mehrsprachigkeit-export-theme)
13. [Datei-Manifest](#13-datei-manifest)

---

## 1. Projektübersicht

### Ziel
Automatisierung einfacher Remote-Jobs (Technical Writing, Low-Code-Entwicklung, QA-Testing) durch eine lokale LLM-Agenten-Farm. Durch **Parallelisierung** und **Bündelung von Einnahmen** (Gehalts-Pooling) wird ein skalierbares, kostenfreies Einkommensmodell aufgebaut.

### Kernprinzipien
| Prinzip | Umsetzung |
|---------|-----------|
| **Zero Token-Kosten** | Lokale Inference über OpenClaw (kein API-Limit, keine Abrechnung) |
| **Insel-Stabilität** | Alle Tools lokal, State in SQLite, keine externen Abhängigkeiten |
| **Determinismus** | `temperature=0`, fixed seeds, Hash-basiertes Caching |
| **Versionierung** | Git-basierte Prompt- und Workflow-Versionen mit automatischen Tags |
| **Skalierbarkeit** | Workflows parallelisierbar; 1 System = 50+ gleichzeitige Jobs |

### Abgedeckte Remote-Job-Typen
| Job | KI-Automatisierbarkeit | Ø Gehalt DE (Remote) |
|-----|------------------------|----------------------|
| Technical Writer | 🟢 Sehr hoch (>90%) | 50.000–65.000 €/Jahr |
| Low-Code Developer | 🟢 Sehr hoch (>85%) | 48.000–62.000 €/Jahr |
| QA Automation Engineer | 🟢 Hoch (>80%) | 52.000–68.000 €/Jahr |

---

## 2. Systemarchitektur

```
agent-farm/
├── farm_config.yaml          # 🔧 Master-Konfiguration (Agenten + Workflows)
├── run.sh                    # ⚡ One-Command Pipeline
├── requirements.txt          # 📦 Python-Abhängigkeiten
│
├── scripts/                  # 🐍 Automation Scripts
│   ├── generate.py           #   Config → YAML-Dateien (Jinja2)
│   ├── validate.py           #   Syntax + Schema + Tool-Check
│   ├── test.py               #   Mock-Inferenz + Workflow-Tests
│   └── git_push.py           #   Atomic Commit, Tag & Push
│
├── templates/j2/             # 📄 Jinja2-Templates
│   ├── agent.yaml.j2         #   Agent-Definition Template
│   └── workflow.yaml.j2      #   Workflow-Definition Template
│
├── schemas/                  # ✅ JSON Schemas (Validierung)
│   ├── agent_schema.json
│   └── workflow_schema.json
│
├── prompts/                  # 🧠 Versionierte System-Prompts
│   ├── tech_writer_system.md
│   ├── lowcode_design_system.md
│   └── qa_test_gen_system.md
│
├── agents/                   # 🤖 Generierte Agent-YAMLs (auto)
├── workflows/                # ⚙️  Workflow-Definitionen
│   ├── tech_writer_workflow.yaml
│   ├── lowcode_automation_workflow.yaml
│   └── qa_test_gen_workflow.yaml
│
├── storage/                  # 💾 SQLite State & Billing-Pool
│   └── farm.db               #   (wird zur Laufzeit erstellt)
└── tools/                    # 🔌 Lokale CLI-Tools
    └── README.md
```

**Datenfluss:**
```
farm_config.yaml
    │
    ▼
generate.py ──► agents/*.yaml + workflows/*.yaml
    │
    ▼
validate.py ──► Schema + YAML-Syntax OK?
    │
    ▼
test.py ──────► Mock-Inferenz + Step-Tests OK?
    │
    ▼
git_push.py ──► Commit + Tag + Push → GitHub
```

---

## 3. Voraussetzungen & Installation

### Systemanforderungen
- **Python** 3.10 oder neuer
- **Git** 2.30+
- **SQLite** 3 (üblicherweise vorinstalliert)
- **OpenClaw** lokal laufend (Inference-Server, Port 8090)

### Optionale Tools (für volle Funktionalität)
- `npx` + Playwright (QA-Workflow)
- `n8n-cli` (Low-Code-Workflow Validation)
- `markdownlint-cli` (Tech-Writer-Workflow)

### Installation

```bash
# 1. Repository klonen
git clone https://github.com/r00t3rr0r/agent-farm.git
cd agent-farm

# 2. Python-Abhängigkeiten installieren
pip install -r requirements.txt

# 3. Run-Skript ausführbar machen
chmod +x run.sh
```

### Erste Inbetriebnahme (empfohlen)

```bash
# 1) Basistest ohne Git-Push
./run.sh test-only

# 2) Web-Panel starten
streamlit run app.py
```

Danach im Browser:
1. Infrastruktur setzen (Farm-Name, OpenClaw-Endpunkt, Parallelität)
2. Agenten und passende Workflows aktivieren
3. Git/Billing konfigurieren
4. Review durchführen und Deploy starten

### Optional: Automatischer Start beim ersten Aufruf

Wenn du das Panel ohne manuelle Startbefehle nutzen möchtest, kannst du einen kleinen Wrapper verwenden.

**Beispiel (macOS/Linux):**
```bash
# Datei: start_panel.sh
#!/usr/bin/env bash
cd "$(dirname "$0")"
if ! pgrep -f "streamlit run app.py" >/dev/null; then
  nohup streamlit run app.py >/tmp/agent-farm-panel.log 2>&1 &
fi
echo "Web-Panel läuft auf: http://localhost:8501"
```

```bash
chmod +x start_panel.sh
./start_panel.sh
```

Nutzen:
- Startet das Panel nur dann, wenn es noch nicht läuft
- Unterstützt einen schnellen, wiederholbaren Einstieg für Teams
- Geeignet als Basis für Autostart via Login-Items, `launchd` oder `systemd --user`

---

## 4. Master-Konfiguration

Die Datei `farm_config.yaml` ist der zentrale Einstiegspunkt. Sie definiert alle **Agenten** und **Workflows**.

```yaml
agents:
  - id: tech_writer_agent
    name: Technical Writer Agent
    system_prompt_ref: prompts/tech_writer_system.md
    tools: []
    model_route: openclaw/local-llm-v1
    inference_params:
      temperature: 0.0     # Deterministic
      max_tokens: 1500
      seed: 42

workflows:
  - id: tech_writer_v1
    name: API-Dokumentation generieren
    trigger_type: file_watch
    input_schema:
      code_file: string
      endpoint_desc: string
    agent_ref: tech_writer_agent
    billing_tag: techwriting_pool  # Gehalts-Pooling Tag
```

### Konfigurationsfelder

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `agents[].id` | string | Eindeutiger Agent-Identifier |
| `agents[].system_prompt_ref` | path | Relativer Pfad zur `.md` System-Prompt-Datei |
| `agents[].model_route` | string | OpenClaw-Modell-Pfad |
| `agents[].inference_params.temperature` | float 0–2 | 0.0 = deterministisch |
| `workflows[].trigger_type` | string | `file_watch`, `webhook`, `git_pr`, `schedule` |
| `workflows[].billing_tag` | string | Pool-Tag für Einnahmen-Aggregation |

---

## 5. Skripte & Pipeline

### `scripts/generate.py`
**Zweck:** Liest `farm_config.yaml`, rendert Jinja2-Templates, schreibt YAML-Dateien nach `agents/` und `workflows/`.

```bash
python3 scripts/generate.py
# Output: agents/tech_writer_agent.yaml, workflows/tech_writer_v1.yaml, ...
```

### `scripts/validate.py`
**Zweck:** Prüft alle generierten YAMLs gegen JSON-Schemas und verifiziert CLI-Tool-Verfügbarkeit.

```bash
python3 scripts/validate.py
# ✅ Schema valid: tech_writer_agent.yaml
# ⚠️  Tool not found: n8n-cli (optional)
```

### `scripts/test.py`
**Zweck:** Führt deterministische Mock-Inferenz durch; simuliert alle Workflow-Steps ohne echte GPU-Last.

```bash
python3 scripts/test.py
# 🧪 Testing tech_writer_v1.yaml...
#   ✅ Step 0: tech_writer_agent → deterministic inference OK
```

### `scripts/git_push.py`
**Zweck:** Atomarer Git-Commit mit Conventional-Commit-Message, automatischem Versions-Tag und Push.

```bash
python3 scripts/git_push.py
# ✅ Pushed & tagged: farm-v202406151430
```

### `run.sh` – Die vollständige Pipeline

```bash
./run.sh deploy      # Vollständige Pipeline: Generate → Validate → Test → Git Push
./run.sh test-only   # Nur Generate → Validate → Test (kein Git Push)
```

---

## 6. Workflow-Templates

Jeder Workflow definiert eine vollständige Automatisierungs-Pipeline.

### Template-Struktur

```yaml
id: <unique_workflow_id>
name: <Beschreibung>
trigger_type: file_watch | webhook | git_pr | schedule | csv_upload | api_event
input_schema:
  <field_name>: <type>
steps:
  - agent_role: <agent_id>
    prompt_template: prompts/<agent_prompt>.md
    inference_params:
      temperature: 0.0
      max_tokens: 1500
    tool_calls: []
  - validation:
      type: json_schema | tsc_check | markdownlint
      schema_file: schemas/<schema>.json   # optional
  - post_process:
      output_dir: <output_path>
fallback: queue_for_human_review
stability_flags:
  deterministic: true
  cache_key: hash(input)
  max_retries: 2
```

### Verfügbare Workflows

#### `tech_writer_workflow.yaml` – API-Dokumentation
- **Input:** Code-Datei + Endpoint-Beschreibung
- **Output:** Markdown-Dokumentation in `docs/generated/`
- **Validierung:** `markdownlint`
- **KI-Temperatur:** 0.0 (rein deterministisch)

#### `lowcode_automation_workflow.yaml` – n8n/Make-Flow-Generator
- **Input:** CSV-Datensample + Business-Regel
- **Output:** n8n-kompatibler JSON-Flow
- **Validierung:** JSON-Schema + n8n-cli dry-run
- **KI-Temperatur:** 0.1 (minimale Kreativität für Workflow-Design)

#### `qa_test_gen_workflow.yaml` – Playwright-Test-Generator
- **Input:** Komponenten-Code + User Stories
- **Output:** TypeScript Playwright-Testdatei
- **Validierung:** TypeScript-Compiler + Playwright-Ausführung
- **KI-Temperatur:** 0.0 (deterministische Tests)

---

## 7. Agenten-Definitionen

### Agenten-Rollen

| Agent | Spezialisierung | Temp | Max Tokens |
|-------|----------------|------|------------|
| `tech_writer_agent` | API-Docs, Markdown, Docusaurus | 0.0 | 1500 |
| `automation_architect_agent` | n8n/Make, Zapier JSON-Flows | 0.1 | 2500 |
| `qa_test_architect_agent` | Playwright TS, POM-Pattern | 0.0 | 3000 |

### System-Prompts

Alle System-Prompts sind in `prompts/` als versionierte `.md`-Dateien gespeichert. Jeder Prompt definiert:
- **Rolle** des Agenten
- **Verantwortlichkeiten** und Aufgaben
- **Output-Format** (Markdown, JSON, TypeScript)
- **Constraints** (Temperatur, Max Tokens, Qualitätsregeln)

---

## 8. Insel-Stabilität & Zero-Token-Optimierung

### Stabilitätsmaßnahmen

| Maßnahme | Umsetzung | Effekt |
|----------|-----------|--------|
| **Deterministische Inference** | `temperature=0`, `seed=42` | Reproduzierbare, nicht-schwankende Outputs |
| **Lokale Tool-Registry** | Alle Tools in `tools/` oder System-PATH | Offline-fähig, keine Cloud-Abhängigkeit |
| **Prompt-Versioning** | Git-Commits + Hash in YAML-Metadaten | Jeder Lauf auditierbar, rollback-fähig |
| **Circuit Breaker** | Orchestrator pausiert nach 3 Fehlern | Verhindert Kaskadenfehler |
| **Batch-Inference** | OpenClaw-Requests gebündelt (8–32) | Maximale GPU-Auslastung |

### OpenClaw-Integration

```bash
# OpenClaw lokaler API-Endpoint
curl -s http://localhost:8090/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openclaw/local-llm-v1",
    "messages": [{"role": "user", "content": "Test"}],
    "temperature": 0.0,
    "seed": 42
  }'
```

### Zero-Token-Kostenprinzip
Da OpenClaw lokal betrieben wird, entstehen **keine API-Token-Kosten**. Skalierungskosten beschränken sich auf:
- Strom/Hardware (GPU)
- Speicher (SQLite, lokal)
- Entwicklungszeit (einmalig)

---

## 9. Ausführung & Testing-Protokoll

### Schnellstart

```bash
# 1. Abhängigkeiten installieren
pip install -r requirements.txt

# 2. Pipeline testen (ohne Git-Push)
./run.sh test-only

# 3. Vollständige Deployment-Pipeline
./run.sh deploy
```

### Häufige Betriebsmodi (mit Beispielen)

| Modus | Befehl | Wann nutzen? | Beispiel |
|------|--------|--------------|----------|
| **Validierung vor Änderungen** | `./run.sh test-only` | Vor jeder größeren Konfigurationsänderung | „Ich habe nur Agenten/Workflows angepasst und möchte sicher prüfen.“ |
| **Produktiver Lauf mit Git-Update** | `./run.sh deploy` | Wenn Änderungen stabil sind und versioniert werden sollen | „Neue Prompt-Version ist fertig und soll ins Repo.“ |
| **UI-gestützte Bedienung** | `streamlit run app.py` | Für schnelle Konfiguration ohne manuelle YAML-Edits | „Fachabteilung passt nur Rollen & Export an.“ |

### Konkreter Ablauf für einen neuen Kunden (Beispiel)

```bash
# 1) Lokalen Test ausführen
./run.sh test-only

# 2) Panel öffnen
streamlit run app.py

# 3) Nach Freigabe deployen
./run.sh deploy
```

Empfohlene Konfiguration im Panel:
- Rollen: `tech_writer_agent`, `qa_test_architect_agent`
- Workflows: `tech_writer_v1`, `qa_automation_v1`
- Export: `YAML` für technische Doku + `CSV` für Abstimmung mit Nicht-Technikteams

### Erwartete Ausgabe (Erfolg)

```
🚀 Agent Farm Pipeline | Mode: deploy
================================================

📝 Step 1/4: Generating agents & workflows...
  📝 Agent generated: agents/tech_writer_agent.yaml
  📝 Agent generated: agents/automation_architect_agent.yaml
  📝 Agent generated: agents/qa_test_architect_agent.yaml
  📝 Workflow generated: workflows/tech_writer_v1.yaml
  ...
✅ Generated 3 agents & 3 workflows.

🔍 Step 2/4: Validating...
  ✅ Schema valid: tech_writer_agent.yaml
  ✅ Schema valid: tech_writer_v1.yaml
  ...
✅ All validations passed.

🧪 Step 3/4: Running tests...
  ✅ Step 0: tech_writer_agent → mock inference OK
  ...
🏁 All tests passed ✅

📤 Step 4/4: Pushing to Git...
✅ Pushed & tagged: farm-v202406151430

================================================
✅ Pipeline complete.
```

### Gehalts-Pooling überwachen

```sql
-- Tägliche Aktivitätszusammenfassung (nach Inbetriebnahme des Orchestrators)
SELECT billing_tag, COUNT(*) as tasks, SUM(execution_time_sec) as total_sec
FROM completed_tasks
GROUP BY billing_tag;
```

---

## 10. Git-Automatisierung

### Commit-Konvention
Automatische Commits folgen dem **Conventional Commits** Standard:

```
chore(farm): auto-generate & validate [farm-v202406151430]
```

### Versions-Tags
Jeder erfolgreiche Deploy-Lauf erstellt einen Tag:
```
farm-v{YYYYMMDDHHMI}
```

### CI/CD-Integration (optional)

```yaml
# .github/workflows/farm-deploy.yml
name: Farm Deploy
on:
  push:
    paths: ['farm_config.yaml', 'prompts/**', 'templates/**']
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r requirements.txt
      - run: ./run.sh test-only
```

---

## 11. Skalierung & Gehalts-Pooling

### Skalierungs-Pfad

| Phase | Zeitraum | Projekte | KI-Anteil | Einnahmen (Schätzung) |
|-------|----------|----------|-----------|----------------------|
| Setup | Monat 1–2 | 3–5 | 60% | ~1.500 €/Monat |
| Growth | Monat 3–6 | 15–20 | 80% | ~8.000 €/Monat |
| Scale | Monat 6+ | 50+ | >90% | ~25.000+ €/Monat |

### Pool-Strategie

```
KI-System
    ├── Tech-Writing-Pool   → 10 Projekte × 800 €  = 8.000 €/Monat
    ├── Low-Code-Pool       →  8 Projekte × 1.200 € = 9.600 €/Monat
    └── QA-Automation-Pool  →  6 Projekte × 1.000 € = 6.000 €/Monat
                                                    ─────────────────
                                         Gesamt:     23.600 €/Monat
    Kosten: Hardware + Zeit                           -500 €/Monat
                                         Netto:      23.100 €/Monat
```

---

## 12. Web-Panel (UI) – Mehrsprachigkeit, Export, Theme

Das Projekt enthält ein Streamlit-Web-Panel (`app.py`), das die Einrichtung ohne manuelle YAML-Bearbeitung ermöglicht.  
Für Teams und Einzelanwender ist dies der schnellste Weg zur sicheren Inbetriebnahme.

### Schnellstart Web-Panel

```bash
# 1) Abhängigkeiten installieren
pip install -r requirements.txt

# 2) Web-Panel starten
streamlit run app.py

# 3) Browser öffnen
# http://localhost:8501
```

### Funktionsumfang

| Funktion | Beschreibung | Nutzen |
|----------|--------------|--------|
| **4-Schritt-Wizard** | Infrastruktur → Rollen/Workflows → Git/Billing → Review/Deploy | Strukturierte, fehlerarme Einrichtung |
| **Mehrsprachigkeit (DE/EN)** | Sprachumschaltung direkt im Panel | Bessere Nutzbarkeit für gemischte Teams |
| **Konfig-Export** | Export der aktuellen Konfiguration als `JSON`, `YAML` oder `CSV` | Dokumentation, Freigabe, Audit |
| **Theme-Unterstützung** | Vorkonfiguration über `.streamlit/config.toml` | Professionelles, konsistentes UI |
| **Dark-Mode-Nutzung** | Umschaltbar über Streamlit-Menü (`⋮` → Settings → Theme) | Angenehme Nutzung in dunkler Umgebung |
| **One-Click Deploy** | Startet `run.sh` aus dem Panel inkl. Ausgabe | Schneller Übergang von Setup zu Betrieb |

### So nutzt du die neuen Möglichkeiten

1. **Sprache wechseln:** Im Panel rechts oben `Deutsch` oder `English` auswählen.  
2. **Konfiguration exportieren:** In der Sidebar Format (`JSON`/`YAML`/`CSV`) wählen und herunterladen.  
3. **Theme anpassen:** Farben/Schrift zentral in `.streamlit/config.toml` pflegen.  
4. **Deployment ausführen:** In Schritt 4 auf „Konfiguration speichern & Pipeline starten“ klicken.

### Hinweise für den produktiven Einsatz

- Exportdateien eignen sich als **Change- und Freigabe-Artefakte** in Projekten.
- Für konsistente Team-Ergebnisse empfiehlt sich die Versionierung von:
  - `farm_config.yaml`
  - `.streamlit/config.toml`
  - `prompts/` und `templates/`
- Die Detail-Dokumentation zum UI findest du in `docs/WEB_PANEL.md`.

### Praxisbeispiele für typische Nutzung

1. **Technische Dokumentation automatisieren**
   - Aktivierte Rolle: `tech_writer_agent`
   - Workflow: `tech_writer_v1`
   - Ergebnis: konsistente API-Dokumentation, exportierbar als JSON/YAML für Archivierung

2. **Low-Code-Flow vorbereiten und abstimmen**
   - Aktivierte Rolle: `automation_architect_agent`
   - Workflow: `lowcode_gen_v1`
   - Ergebnis: strukturierte Workflow-Definition, als CSV exportiert für Review durch Operations/PM

3. **QA-Regression vorbereiten**
   - Aktivierte Rolle: `qa_test_architect_agent`
   - Workflow: `qa_automation_v1`
   - Ergebnis: reproduzierbare Testartefakte mit klaren Deploy-Ständen über Git-Tags

### Verständnisleitfaden: Welche Einstellung beeinflusst was?

| Einstellung | Wirkung | Empfehlung |
|------------|---------|------------|
| `max_concurrent_agents` | Höhere Parallelität, höhere RAM/VRAM-Last | Mit `2-4` starten, dann schrittweise erhöhen |
| `openclaw_endpoint` | Zielsystem für Inferenz | Lokal stabil halten (z. B. `http://localhost:8090`) |
| `agents_enabled` | Schaltet Fähigkeiten frei | Nur Rollen aktivieren, die wirklich benötigt werden |
| `workflows_enabled` | Steuert automatisierte Abläufe | Erst nach erfolgreichem `test-only` produktiv deployen |
| `billing_tag_prefix` | Strukturierte Zuordnung von Kosten/Erträgen | Pro Kunde/Projekt ein eindeutiges Präfix nutzen |

---

## 13. Datei-Manifest

| Datei | Typ | Status | Beschreibung |
|-------|-----|--------|--------------|
| `farm_config.yaml` | YAML | ✅ Vorhanden | Master-Konfiguration |
| `run.sh` | Bash | ✅ Vorhanden | One-Command Pipeline |
| `app.py` | Python (Streamlit) | ✅ Vorhanden | Web-Panel für Setup, Review und Deploy |
| `.streamlit/config.toml` | TOML | ✅ Vorhanden | Theme- und UI-Grundeinstellungen |
| `requirements.txt` | Text | ✅ Vorhanden | Python-Abhängigkeiten |
| `scripts/generate.py` | Python | ✅ Vorhanden | Config → YAML-Generator |
| `scripts/validate.py` | Python | ✅ Vorhanden | Schema + YAML-Validator |
| `scripts/test.py` | Python | ✅ Vorhanden | Mock-Inferenz-Tests |
| `scripts/git_push.py` | Python | ✅ Vorhanden | Git-Automatisierung |
| `templates/j2/agent.yaml.j2` | Jinja2 | ✅ Vorhanden | Agent-Template |
| `templates/j2/workflow.yaml.j2` | Jinja2 | ✅ Vorhanden | Workflow-Template |
| `schemas/agent_schema.json` | JSON | ✅ Vorhanden | Agent-Validierungsschema |
| `schemas/workflow_schema.json` | JSON | ✅ Vorhanden | Workflow-Validierungsschema |
| `prompts/tech_writer_system.md` | Markdown | ✅ Vorhanden | Tech-Writer-Prompt |
| `prompts/lowcode_design_system.md` | Markdown | ✅ Vorhanden | Low-Code-Prompt |
| `prompts/qa_test_gen_system.md` | Markdown | ✅ Vorhanden | QA-Test-Prompt |
| `workflows/tech_writer_workflow.yaml` | YAML | ✅ Vorhanden | Tech-Writer-Workflow |
| `workflows/lowcode_automation_workflow.yaml` | YAML | ✅ Vorhanden | Low-Code-Workflow |
| `workflows/qa_test_gen_workflow.yaml` | YAML | ✅ Vorhanden | QA-Test-Workflow |
| `agents/` | Ordner | 🔄 Generiert | Agent-YAMLs (via generate.py) |
| `storage/farm.db` | SQLite | 🔄 Laufzeit | State & Billing-DB |
| `tools/` | Ordner | 📦 Optional | Lokale CLI-Tools |
| `docs/WEB_PANEL.md` | Markdown | ✅ Vorhanden | Detaillierte UI-Dokumentation |

---

## Lizenz

MIT License – Frei verwendbar, modifizierbar und verteilbar.

---

*Erstellt mit KI-Agenten-Farm v1.1.0 | OpenClaw lokal | 0 Token-Kosten*
