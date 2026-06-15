# 🌐 Web-Panel: Benutzerfreundliche Konfiguration

Das Streamlit-basierte Web-Panel ersetzt manuelle YAML-Bearbeitung durch einen intuitiven 4-Schritt-Assistenten.

## 🚀 Schnellstart

```bash
# Dependencies (falls noch nicht installiert)
pip install -r requirements.txt

# App starten
streamlit run app.py
# → Öffnet http://localhost:8501 im Browser
```

## 🧭 Die 4 Schritte

| Schritt | Fokus | Ergebnis |
|---------|-------|----------|
| **1. Infrastruktur** | Farm-Name, KI-Endpunkt, Parallelität | Basis-Setup definiert |
| **2. Rollen & Workflows** | Agenten aktivieren/deaktivieren | KI-Capabilities gewählt |
| **3. Git & Billing** | Repository, Auto-Push, Reporting | Versionierung konfiguriert |
| **4. Review & Deploy** | Zusammenfassung, ein-Klick Deploy | Pipeline startet automatisch |

## 🎯 Design-Prinzipien

### ✅ Benutzerfreundlich statt technisch
- **Statt:** `temperature=0, seed=42, max_tokens=1500`
- **Jetzt:** Schieber mit RAM-Effekt-Indicator

### ✅ Progressive Offenlegung
- Nur Einstellungen zeigen, die aktuell relevant sind
- Abhängigkeiten automatisch handhaben (z.B. Workflows nur wenn Agenten aktiv)

### ✅ Ursache-Wirkung transparent
- Jedes Input-Feld hat einen `👉 Effekt:`-Text
- Tooltips erklären "Warum das wichtig ist"

### ✅ Keine leeren Felder
- Alle Inputs haben sinnvolle Defaults
- Presets für schnelle Starts ("Start Small", "Full Stack")

## 📖 Beispielworkflow

1. **Öffne das Panel:** `streamlit run app.py`
2. **Gib einen Farm-Namen ein:** "Meine Produktions-Farm"
3. **Wähle Rollen:** Tech Writer ✅, Low-Code ✅, QA ❌
4. **Aktivierte Workflows:** Nur die, deren Agenten aktiv sind
5. **Konfiguriere Git:** Auto-Push ✅, Repo: `https://github.com/...`
6. **Deploy:** Klicke "🚀 Starten" → Farm läuft

## 🔗 Integration mit bestehendem System

```
app.py (Streamlit UI)
    ↓ (schreibt)
farm_config.yaml
    ↓ (triggert)
run.sh (Pipeline)
    ├→ generate.py (YAML-Generator)
    ├→ validate.py (Validierung)
    ├→ test.py (Mock-Tests)
    └→ git_push.py (Git-Automation)
```

Das Panel ist **nur eine Frontend-Schicht** – alle bestehenden Skripte bleiben unverändert.

## 🎨 Features

- ✅ **4-Schritt-Wizard** mit Navigations-Sidebar
- ✅ **Kontextuelle Hilfe** in jedem Feld
- ✅ **Echtzeit-Validierung** (z.B. Workflows deaktivieren, wenn Agents fehlen)
- ✅ **Raw YAML-Vorschau** (collapsible)
- ✅ **One-Click Deploy** mit Live-Konsolen-Ausgabe
- ✅ **Automatisches Config-Loading** (liest existierende `farm_config.yaml`)

## 📊 Session State Management

Das Panel speichert den Wizard-Status in `st.session_state`:
- `config`: Aktuelle Konfiguration (Python dict)
- `step`: Aktueller Schritt (1–4)

Bei jedem Seitenaufruf wird die Config von `farm_config.yaml` geladen.

## 🔧 Anpassungen für Deine Anforderungen

### Neue Agenten hinzufügen?
Bearbeite `AGENT_META` in `app.py`:
```python
AGENT_META = {
    "my_new_agent": {
        "emoji": "🆕",
        "label": "Mein neuer Agent",
        "impact": "Kurze Beschreibung der Fähigkeit"
    }
}
```

### Neue Workflows?
Bearbeite `WORKFLOW_META`:
```python
WORKFLOW_META = {
    "my_workflow": {
        "emoji": "🔄",
        "label": "Mein Workflow",
        "depends_on": ["my_new_agent"]
    }
}
```

### Mehr/weniger Parallelität?
Ändere `st.slider()` in `render_step_1()`:
```python
conc = st.slider("⚡ Max. parallele Agenten", min_value=1, max_value=16, ...)
```

## 🚨 Troubleshooting

| Problem | Lösung |
|---------|--------|
| "Streamlit not found" | `pip install -r requirements.txt` |
| "Permission denied: run.sh" | `chmod +x run.sh` |
| Deploy schlägt fehl | Prüfe `run.sh` & `farm_config.yaml` im gleichen Verzeichnis |
| Änderungen laden nicht | Browswer-Cache löschen oder Incognito-Tab nutzen |

## 📚 Weitere Ressourcen

- Streamlit Docs: https://docs.streamlit.io
- Farm Repository: https://github.com/r00t3rr0r/agent-farm
- Hauptdokumentation: `README.md`

---

**Erstellt mit ❤️ für menschengerechte AI-Infrastruktur**
