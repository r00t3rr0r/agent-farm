import streamlit as st
import yaml
from pathlib import Path
import subprocess
import json
from datetime import datetime

# ─── KONFIGURATIONSMAPPING & SMART DEFAULTS ────────────────────────────────
DEFAULT_CONFIG = {
    "farm_name": "Meine KI-Agenten-Farm",
    "openclaw_endpoint": "http://localhost:8090",
    "max_concurrent_agents": 3,
    "agents_enabled": ["tech_writer_agent"],
    "workflows_enabled": ["tech_writer_v1"],
    "git_repo_url": "",
    "auto_push": True,
    "billing_tag_prefix": "farm",
    "reporting_interval_days": 7
}

AGENT_META = {
    "tech_writer_agent": {
        "emoji": "📝", 
        "label": "Technischer Redakteur", 
        "impact": "Generiert Dokumentation aus Code. Niedrige Hardware-Anforderung."
    },
    "automation_architect_agent": {
        "emoji": "⚙️", 
        "label": "Low-Code Architekt", 
        "impact": "Erstellt n8n/Make-Workflows. Benötigt Python-Tools im PATH."
    },
    "qa_test_architect_agent": {
        "emoji": "🧪", 
        "label": "QA Test Generator", 
        "impact": "Schreibt Playwright/Cypress-Tests. Mittelgroßer RAM-Bedarf."
    }
}

WORKFLOW_META = {
    "tech_writer_v1": {
        "emoji": "📄", 
        "label": "API-Dokumentation", 
        "depends_on": ["tech_writer_agent"]
    },
    "lowcode_gen_v1": {
        "emoji": "🔗", 
        "label": "Workflow-Orchestrierung", 
        "depends_on": ["automation_architect_agent"]
    },
    "qa_automation_v1": {
        "emoji": "✅", 
        "label": "Test-Suite Erzeugung", 
        "depends_on": ["qa_test_architect_agent"]
    }
}

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="KI-Agenten-Farm Setup",
    page_icon="🌿",
    layout="wide"
)

# ─── SESSION STATE INITIALISIERUNG ──────────────────────────────────────────
if "config" not in st.session_state:
    cfg_path = Path("farm_config.yaml")
    if cfg_path.exists():
        with open(cfg_path) as f:
            loaded = yaml.safe_load(f) or {}
            # Merge with defaults to ensure all keys exist
            st.session_state.config = {**DEFAULT_CONFIG, **loaded}
    else:
        st.session_state.config = DEFAULT_CONFIG.copy()

if "step" not in st.session_state:
    st.session_state.step = 1

# ─── UI HELPER FUNKTIONEN ──────────────────────────────────────────────────
def info_box(title, body):
    st.info(f"**{title}**\n\n{body}")

def impact_badge(level):
    colors = {
        "low": "🟢 Niedriger Aufwand",
        "medium": "🔵 Mittel",
        "high": "🔴 Höherer Bedarf"
    }
    return f"`{colors.get(level, level)}`"

# ─── HEADER ────────────────────────────────────────────────────────────────
st.title("🌿 KI-Agenten-Farm – Inbetriebnahme-Assistent")
st.caption("Deine intelligente Infrastruktur, einfach konfiguriert")

# ─── SIDEBAR NAVIGATION & FORTSCHRITT ───────────────────────────────────────
with st.sidebar:
    st.title("🧭 Einrichtungsschritte")
    steps = [
        "Identität & Infrastruktur",
        "Agenten & Workflows",
        "Git & Reporting",
        "Review & Deploy"
    ]

    for i, s in enumerate(steps, 1):
        icon = "✅" if st.session_state.step > i else "⬜" if st.session_state.step == i else "⬜"
        st.markdown(f"{icon} **{i}. {s}**")

    st.divider()
    
    if st.session_state.step > 1:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Zurück", use_container_width=True):
                st.session_state.step -= 1
                st.rerun()
        with col2:
            pass

# ─── SCHRITT 1: IDENTITÄT & INFRASTRUKTUR ──────────────────────────────────
def render_step_1():
    st.header("🏗️ Schritt 1: Basis-Infrastruktur")
    
    info_box(
        "Warum das wichtig ist",
        "Diese Einstellungen definieren, wo deine KI läuft und wie viele Aufgaben "
        "parallel bearbeitet werden. Mehr Parallelität = schnellere Durchläufe, "
        "aber höherer RAM-Verbrauch."
    )

    st.session_state.config["farm_name"] = st.text_input(
        "📛 Farm-Name",
        value=st.session_state.config.get("farm_name", "Meine Farm"),
        help="Ein sprechender Name für deine Instanz. Dient zur Kennzeichnung in Logs & Reports."
    )

    st.session_state.config["openclaw_endpoint"] = st.text_input(
        "📍 Lokaler KI-Endpunkt",
        value=st.session_state.config.get("openclaw_endpoint", "http://localhost:8090"),
        help="Die URL, unter der OpenClaw erreichbar ist. Standard: http://localhost:8090"
    )

    conc = st.slider(
        "⚡ Max. parallele Agenten",
        min_value=1,
        max_value=8,
        value=st.session_state.config.get("max_concurrent_agents", 3),
        help="Wie viele KI-Antworten dürfen gleichzeitig generiert werden? "
             "Empfohlen: 3–4 für lokale GPUs mit 8–12 GB VRAM."
    )
    st.caption(f"👉 **Effekt:** `{conc}` gleichzeitige Jobs. RAM-Bedarf skaliert linear.")
    st.session_state.config["max_concurrent_agents"] = conc

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Weiter →", type="primary", use_container_width=True):
            st.session_state.step += 1
            st.rerun()

# ─── SCHRITT 2: AGENTEN & WORKFLOWS ────────────────────────────────────────
def render_step_2():
    st.header("🤖 Schritt 2: Rollen & Abläufe aktivieren")

    info_box(
        "So funktioniert es",
        "Wähle aus, welche KI-Rollen du brauchst. Workflows werden automatisch "
        "freigeschaltet, wenn ihre benötigten Agenten aktiv sind."
    )

    st.subheader("👥 Verfügbare KI-Rollen")
    cols = st.columns(3)
    enabled_agents = []

    for i, key in enumerate(["tech_writer_agent", "automation_architect_agent", "qa_test_architect_agent"]):
        with cols[i % 3]:
            meta = AGENT_META[key]
            checked = key in st.session_state.config.get("agents_enabled", [])
            if st.toggle(
                f"{meta['emoji']} {meta['label']}",
                value=checked,
                help=meta['impact']
            ):
                enabled_agents.append(key)

    st.session_state.config["agents_enabled"] = enabled_agents

    st.divider()
    st.subheader("🔄 Verfügbare Workflows")

    enabled_workflows = []
    for key, wf in WORKFLOW_META.items():
        deps_ok = all(d in enabled_agents for d in wf["depends_on"])
        disabled = not deps_ok
        checked = key in st.session_state.config.get("workflows_enabled", [])
        
        status_text = "✅ Aktivierbar" if deps_ok else "⛔ Agent(en) fehlen"
        help_text = f"Benötigt: {', '.join([AGENT_META[d]['label'] for d in wf['depends_on']])}. {status_text}"

        if st.checkbox(
            f"{wf['emoji']} {wf['label']}",
            value=checked,
            disabled=disabled,
            help=help_text
        ):
            enabled_workflows.append(key)

    st.session_state.config["workflows_enabled"] = enabled_workflows

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Zurück", use_container_width=True):
            st.session_state.step -= 1
            st.rerun()
    with col2:
        if st.button("Weiter →", type="primary", use_container_width=True):
            st.session_state.step += 1
            st.rerun()

# ─── SCHRITT 3: GIT & REPORTING ────────────────────────────────────────────
def render_step_3():
    st.header("🔗 Schritt 3: Versionierung & Abrechnung")

    info_box(
        "Transparenz vorab",
        "Git sichert jede Konfigurationsänderung. Das Billing-Tag ermöglicht "
        "nachträgliche Zuordnung von Kosten & Arbeitszeit pro Kunde/Projekt."
    )

    st.session_state.config["git_repo_url"] = st.text_input(
        "📦 Git Repository (optional)",
        value=st.session_state.config.get("git_repo_url", ""),
        help="Leer lassen, wenn nur lokal gearbeitet wird. Andernfalls: https://github.com/user/repo.git"
    )

    st.session_state.config["auto_push"] = st.toggle(
        "🚀 Automatisches Push nach Änderungen",
        value=st.session_state.config.get("auto_push", True),
        help="Sichert Konfiguration & generierte YAMLs automatisch im Repository."
    )

    st.session_state.config["billing_tag_prefix"] = st.text_input(
        "💰 Billing-Tag Präfix",
        value=st.session_state.config.get("billing_tag_prefix", "farm"),
        help="Wird zu allen Abrechnungs-IDs vorgesetzt (z.B. farm_client_a)"
    )

    interval = st.number_input(
        "📊 Reporting-Intervall (Tage)",
        value=st.session_state.config.get("reporting_interval_days", 7),
        min_value=1,
        max_value=30,
        step=1,
        help="Wie oft soll ein Zusammenfassungs-Report generiert werden?"
    )
    st.caption(f"👉 **Effekt:** Alle `{interval}` Tage wird `storage/farm.db` exportiert.")
    st.session_state.config["reporting_interval_days"] = interval

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Zurück", use_container_width=True):
            st.session_state.step -= 1
            st.rerun()
    with col2:
        if st.button("Weiter →", type="primary", use_container_width=True):
            st.session_state.step += 1
            st.rerun()

# ─── SCHRITT 4: REVIEW & DEPLOY ────────────────────────────────────────────
def render_step_4():
    st.header("✅ Schritt 4: Zusammenfassung & Aktivierung")

    cfg = st.session_state.config

    # Summary Table
    st.subheader("📋 Konfigurationsübersicht")

    summary_cols = st.columns(2)

    with summary_cols[0]:
        st.metric("Farm-Name", cfg.get("farm_name", "—"))
        st.metric("KI-Endpunkt", cfg.get("openclaw_endpoint", "—"))
        st.metric("Parallelität", f"{cfg.get('max_concurrent_agents', 1)} Agenten")

    with summary_cols[1]:
        active_agents = [AGENT_META[k]["label"] for k in cfg.get("agents_enabled", [])]
        st.metric("Aktive Rollen", len(active_agents))
        st.metric("Workflows", len(cfg.get("workflows_enabled", [])))
        st.metric("Billing-Präfix", cfg.get("billing_tag_prefix", "—"))

    st.divider()

    # Detailed breakdown
    with st.expander("📖 Detaillierte Konfiguration", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Aktivierte Rollen:**")
            if cfg.get("agents_enabled"):
                for agent in cfg.get("agents_enabled", []):
                    meta = AGENT_META.get(agent, {})
                    st.write(f"  • {meta.get('emoji', '❓')} {meta.get('label', agent)}")
            else:
                st.write("  *(keine)*")

        with col2:
            st.write("**Aktivierte Workflows:**")
            if cfg.get("workflows_enabled"):
                for wf in cfg.get("workflows_enabled", []):
                    meta = WORKFLOW_META.get(wf, {})
                    st.write(f"  • {meta.get('emoji', '❓')} {meta.get('label', wf)}")
            else:
                st.write("  *(keine)*")

    # Raw YAML preview (collapsible)
    with st.expander("👁️ Raw YAML-Vorschau (für Nerds)", expanded=False):
        yaml_str = yaml.dump(cfg, sort_keys=False, allow_unicode=True, default_flow_style=False)
        st.code(yaml_str, language="yaml")

    st.divider()

    # Deploy action
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button("← Zurück", use_container_width=True):
            st.session_state.step -= 1
            st.rerun()

    with col2:
        if st.button("🚀 Konfiguration speichern & Pipeline starten", type="primary", use_container_width=True):
            with st.spinner("⏳ YAML schreiben, validieren & deployen..."):
                cfg_path = Path("farm_config.yaml")

                # Write config
                with open(cfg_path, "w", encoding="utf-8") as f:
                    yaml.dump(cfg, f, sort_keys=False, allow_unicode=True, default_flow_style=False)

                st.success(f"✅ Konfiguration gespeichert: `{cfg_path}`")

                # Run pipeline
                with st.expander("📋 Pipeline-Ausgabe", expanded=True):
                    try:
                        result = subprocess.run(
                            ["bash", "run.sh", "deploy"],
                            capture_output=True,
                            text=True,
                            timeout=300
                        )

                        if result.returncode == 0:
                            st.success("✅ **Farm erfolgreich deployed!**")
                            st.code(result.stdout, language="text")
                        else:
                            st.error("❌ **Fehler beim Deploy:**")
                            st.code(result.stderr or result.stdout, language="text")

                    except subprocess.TimeoutExpired:
                        st.error("⏱️ Pipeline-Timeout nach 5 Minuten.")
                    except FileNotFoundError:
                        st.error("⚠️ `run.sh` nicht gefunden. Stelle sicher, dass du im `agent-farm/`-Verzeichnis bist.")

    st.divider()
    st.caption("🌿 KI-Agenten-Farm | Lokal, deterministisch & nutzerzentriert")

# ─── RENDERING ENGINE ──────────────────────────────────────────────────────
if st.session_state.step == 1:
    render_step_1()
elif st.session_state.step == 2:
    render_step_2()
elif st.session_state.step == 3:
    render_step_3()
elif st.session_state.step == 4:
    render_step_4()
