import streamlit as st
import yaml
from pathlib import Path
import subprocess
import json
import csv
import io
from datetime import datetime

# ─── INTERNATIONALIZATION (i18n) ───────────────────────────────────────────
STRINGS = {
    "de": {
        "title": "🌿 KI-Agenten-Farm – Inbetriebnahme-Assistent",
        "subtitle": "Deine intelligente Infrastruktur, einfach konfiguriert",
        "step_nav": "🧭 Einrichtungsschritte",
        "back": "← Zurück",
        "next": "Weiter →",
        "why_important": "Warum das wichtig ist",
        "infra_desc": "Diese Einstellungen definieren, wo deine KI läuft und wie viele Aufgaben parallel bearbeitet werden. Mehr Parallelität = schnellere Durchläufe, aber höherer RAM-Verbrauch.",
        "step1": "🏗️ Schritt 1: Basis-Infrastruktur",
        "farm_name": "📛 Farm-Name",
        "farm_name_help": "Ein sprechender Name für deine Instanz. Dient zur Kennzeichnung in Logs & Reports.",
        "openclaw_endpoint": "📍 Lokaler KI-Endpunkt",
        "endpoint_help": "Die URL, unter der OpenClaw erreichbar ist. Standard: http://localhost:8090",
        "parallel_agents": "⚡ Max. parallele Agenten",
        "parallel_help": "Wie viele KI-Antworten dürfen gleichzeitig generiert werden? Empfohlen: 3–4 für lokale GPUs mit 8–12 GB VRAM.",
        "effect": "👉 **Effekt:**",
        "concurrent_jobs": "gleichzeitige Jobs. RAM-Bedarf skaliert linear.",
        "step2": "🤖 Schritt 2: Rollen & Abläufe aktivieren",
        "roles_desc": "Wähle aus, welche KI-Rollen du brauchst. Workflows werden automatisch freigeschaltet, wenn ihre benötigten Agenten aktiv sind.",
        "available_roles": "👥 Verfügbare KI-Rollen",
        "available_workflows": "🔄 Verfügbare Workflows",
        "requires": "Benötigt:",
        "available": "✅ Aktivierbar",
        "agents_missing": "⛔ Agent(en) fehlen",
        "step3": "🔗 Schritt 3: Versionierung & Abrechnung",
        "git_billing": "Transparenz vorab",
        "git_desc": "Git sichert jede Konfigurationsänderung. Das Billing-Tag ermöglicht nachträgliche Zuordnung von Kosten & Arbeitszeit pro Kunde/Projekt.",
        "git_repo": "📦 Git Repository (optional)",
        "git_help": "Leer lassen, wenn nur lokal gearbeitet wird. Andernfalls: https://github.com/user/repo.git",
        "auto_push": "🚀 Automatisches Push nach Änderungen",
        "auto_push_help": "Sichert Konfiguration & generierte YAMLs automatisch im Repository.",
        "billing_prefix": "💰 Billing-Tag Präfix",
        "billing_help": "Wird zu allen Abrechnungs-IDs vorgesetzt (z.B. farm_client_a)",
        "reporting_interval": "📊 Reporting-Intervall (Tage)",
        "reporting_help": "Wie oft soll ein Zusammenfassungs-Report generiert werden?",
        "export": "alle",
        "export_db": "wird exportiert.",
        "step4": "✅ Schritt 4: Zusammenfassung & Aktivierung",
        "summary": "📋 Konfigurationsübersicht",
        "active_roles": "Aktive Rollen",
        "workflows": "Workflows",
        "detailed": "📖 Detaillierte Konfiguration",
        "enabled_roles": "**Aktivierte Rollen:**",
        "none": "*(keine)*",
        "enabled_workflows": "**Aktivierte Workflows:**",
        "yaml_preview": "👁️ Raw YAML-Vorschau (für Nerds)",
        "deploy_btn": "🚀 Konfiguration speichern & Pipeline starten",
        "saving": "⏳ YAML schreiben, validieren & deployen...",
        "saved": "✅ Konfiguration gespeichert:",
        "deploy_output": "📋 Pipeline-Ausgabe",
        "success": "✅ **Farm erfolgreich deployed!**",
        "error": "❌ **Fehler beim Deploy:**",
        "timeout": "⏱️ Pipeline-Timeout nach 5 Minuten.",
        "not_found": "⚠️ `run.sh` nicht gefunden. Stelle sicher, dass du im `agent-farm/`-Verzeichnis bist.",
        "footer": "🌿 KI-Agenten-Farm | Lokal, deterministisch & nutzerzentriert",
        "export_config": "📥 Konfiguration exportieren",
        "export_json": "JSON",
        "export_yaml": "YAML",
        "export_csv": "CSV",
        "language": "🌐 Sprache",
        "dark_mode": "🌙 Dunkler Modus",
    },
    "en": {
        "title": "🌿 AI Agent Farm – Setup Wizard",
        "subtitle": "Your intelligent infrastructure, simply configured",
        "step_nav": "🧭 Setup Steps",
        "back": "← Back",
        "next": "Next →",
        "why_important": "Why this matters",
        "infra_desc": "These settings define where your AI runs and how many tasks run in parallel. More parallelism = faster runs, but higher RAM usage.",
        "step1": "🏗️ Step 1: Infrastructure Basics",
        "farm_name": "📛 Farm Name",
        "farm_name_help": "A descriptive name for your instance. Used for identification in logs & reports.",
        "openclaw_endpoint": "📍 Local AI Endpoint",
        "endpoint_help": "The URL where OpenClaw is accessible. Default: http://localhost:8090",
        "parallel_agents": "⚡ Max Parallel Agents",
        "parallel_help": "How many AI responses can be generated simultaneously? Recommended: 3–4 for local GPUs with 8–12 GB VRAM.",
        "effect": "👉 **Effect:**",
        "concurrent_jobs": "concurrent jobs. RAM usage scales linearly.",
        "step2": "🤖 Step 2: Enable Roles & Workflows",
        "roles_desc": "Choose which AI roles you need. Workflows are automatically enabled when their required agents are active.",
        "available_roles": "👥 Available AI Roles",
        "available_workflows": "🔄 Available Workflows",
        "requires": "Requires:",
        "available": "✅ Available",
        "agents_missing": "⛔ Agents missing",
        "step3": "🔗 Step 3: Versioning & Billing",
        "git_billing": "Transparency upfront",
        "git_desc": "Git secures every config change. The billing tag allows retroactive assignment of costs & work hours per client/project.",
        "git_repo": "📦 Git Repository (optional)",
        "git_help": "Leave blank if working locally only. Otherwise: https://github.com/user/repo.git",
        "auto_push": "🚀 Auto-Push on Changes",
        "auto_push_help": "Automatically secures config & generated YAMLs in the repository.",
        "billing_prefix": "💰 Billing Tag Prefix",
        "billing_help": "Prepended to all billing IDs (e.g. farm_client_a)",
        "reporting_interval": "📊 Reporting Interval (Days)",
        "reporting_help": "How often should a summary report be generated?",
        "export": "every",
        "export_db": "will be exported.",
        "step4": "✅ Step 4: Summary & Activation",
        "summary": "📋 Configuration Summary",
        "active_roles": "Active Roles",
        "workflows": "Workflows",
        "detailed": "📖 Detailed Configuration",
        "enabled_roles": "**Enabled Roles:**",
        "none": "*(none)*",
        "enabled_workflows": "**Enabled Workflows:**",
        "yaml_preview": "👁️ Raw YAML Preview (for nerds)",
        "deploy_btn": "🚀 Save Config & Start Pipeline",
        "saving": "⏳ Writing YAML, validating & deploying...",
        "saved": "✅ Configuration saved:",
        "deploy_output": "📋 Pipeline Output",
        "success": "✅ **Farm deployed successfully!**",
        "error": "❌ **Deployment failed:**",
        "timeout": "⏱️ Pipeline timeout after 5 minutes.",
        "not_found": "⚠️ `run.sh` not found. Make sure you're in the `agent-farm/` directory.",
        "footer": "🌿 AI Agent Farm | Local, deterministic & human-centric",
        "export_config": "📥 Export Configuration",
        "export_json": "JSON",
        "export_yaml": "YAML",
        "export_csv": "CSV",
        "language": "�� Language",
        "dark_mode": "🌙 Dark Mode",
    }
}

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
        "label_de": "Technischer Redakteur", 
        "label_en": "Technical Writer",
        "impact": "Generiert Dokumentation aus Code. Niedrige Hardware-Anforderung."
    },
    "automation_architect_agent": {
        "emoji": "⚙️", 
        "label_de": "Low-Code Architekt", 
        "label_en": "Low-Code Architect",
        "impact": "Erstellt n8n/Make-Workflows. Benötigt Python-Tools im PATH."
    },
    "qa_test_architect_agent": {
        "emoji": "🧪", 
        "label_de": "QA Test Generator", 
        "label_en": "QA Test Generator",
        "impact": "Schreibt Playwright/Cypress-Tests. Mittelgroßer RAM-Bedarf."
    }
}

WORKFLOW_META = {
    "tech_writer_v1": {
        "emoji": "📄", 
        "label_de": "API-Dokumentation", 
        "label_en": "API Documentation",
        "depends_on": ["tech_writer_agent"]
    },
    "lowcode_gen_v1": {
        "emoji": "🔗", 
        "label_de": "Workflow-Orchestrierung", 
        "label_en": "Workflow Orchestration",
        "depends_on": ["automation_architect_agent"]
    },
    "qa_automation_v1": {
        "emoji": "✅", 
        "label_de": "Test-Suite Erzeugung", 
        "label_en": "Test Suite Generation",
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
            st.session_state.config = {**DEFAULT_CONFIG, **loaded}
    else:
        st.session_state.config = DEFAULT_CONFIG.copy()

if "step" not in st.session_state:
    st.session_state.step = 1

if "language" not in st.session_state:
    st.session_state.language = "de"

# ─── HELPER: Get i18n string ────────────────────────────────────────────────
def t(key):
    """Get translated string"""
    lang = st.session_state.language
    return STRINGS.get(lang, STRINGS["en"]).get(key, f"[{key}]")

def t_agent_label(agent_id):
    """Get agent label in current language"""
    lang = st.session_state.language
    key = f"label_{lang}"
    return AGENT_META.get(agent_id, {}).get(key, agent_id)

def t_workflow_label(workflow_id):
    """Get workflow label in current language"""
    lang = st.session_state.language
    key = f"label_{lang}"
    return WORKFLOW_META.get(workflow_id, {}).get(key, workflow_id)

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

# ─── EXPORT FUNCTIONS ──────────────────────────────────────────────────────
def export_config_json():
    """Export current config as JSON"""
    return json.dumps(st.session_state.config, indent=2, ensure_ascii=False)

def export_config_yaml():
    """Export current config as YAML"""
    return yaml.dump(st.session_state.config, allow_unicode=True, default_flow_style=False)

def export_config_csv():
    """Export current config as CSV"""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=st.session_state.config.keys())
    writer.writeheader()
    writer.writerow(st.session_state.config)
    return output.getvalue()

# ─── HEADER ────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 4, 1])
with col3:
    lang_option = st.selectbox(t("language"), ["Deutsch", "English"], 
                               index=0 if st.session_state.language == "de" else 1,
                               key="lang_select")
    if lang_option == "English":
        st.session_state.language = "en"
    else:
        st.session_state.language = "de"
    st.rerun()

st.title(t("title"))
st.caption(t("subtitle"))

# ─── SIDEBAR NAVIGATION & FORTSCHRITT ───────────────────────────────────────
with st.sidebar:
    st.title(t("step_nav"))
    steps = [
        t("step1"),
        t("step2"),
        t("step3"),
        t("step4")
    ]

    for i, s in enumerate(steps, 1):
        icon = "✅" if st.session_state.step > i else "⬜" if st.session_state.step == i else "⬜"
        st.markdown(f"{icon} **{i}. {s.split(' ')[1:] if ' ' in s else s}**")

    st.divider()
    
    if st.session_state.step > 1:
        col1, col2 = st.columns(2)
        with col1:
            if st.button(t("back"), use_container_width=True):
                st.session_state.step -= 1
                st.rerun()

    st.divider()
    st.subheader(t("export_config"))
    
    export_format = st.radio("Format:", ["JSON", "YAML", "CSV"], key="export_fmt")
    
    if export_format == "JSON":
        content = export_config_json()
        filename = f"farm_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    elif export_format == "YAML":
        content = export_config_yaml()
        filename = f"farm_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml"
    else:
        content = export_config_csv()
        filename = f"farm_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    st.download_button(
        label=f"📥 {t('export_' + export_format.lower())}",
        data=content,
        file_name=filename,
        mime="application/json" if export_format == "JSON" else "text/plain",
        use_container_width=True
    )

# ─── SCHRITT 1: IDENTITÄT & INFRASTRUKTUR ──────────────────────────────────
def render_step_1():
    st.header(t("step1"))
    
    info_box(t("why_important"), t("infra_desc"))

    st.session_state.config["farm_name"] = st.text_input(
        t("farm_name"),
        value=st.session_state.config.get("farm_name", "Meine Farm"),
        help=t("farm_name_help")
    )

    st.session_state.config["openclaw_endpoint"] = st.text_input(
        t("openclaw_endpoint"),
        value=st.session_state.config.get("openclaw_endpoint", "http://localhost:8090"),
        help=t("endpoint_help")
    )

    conc = st.slider(
        t("parallel_agents"),
        min_value=1,
        max_value=8,
        value=st.session_state.config.get("max_concurrent_agents", 3),
        help=t("parallel_help")
    )
    st.caption(f"{t('effect')} `{conc}` {t('concurrent_jobs')}")
    st.session_state.config["max_concurrent_agents"] = conc

    col1, col2 = st.columns(2)
    with col1:
        if st.button(t("next"), type="primary", use_container_width=True):
            st.session_state.step += 1
            st.rerun()

# ─── SCHRITT 2: AGENTEN & WORKFLOWS ────────────────────────────────────────
def render_step_2():
    st.header(t("step2"))

    info_box(t("why_important"), t("roles_desc"))

    st.subheader(t("available_roles"))
    cols = st.columns(3)
    enabled_agents = []
    
    for i, (agent_id, agent) in enumerate(AGENT_META.items()):
        with cols[i % 3]:
            checkbox = st.checkbox(
                f"{agent['emoji']} {t_agent_label(agent_id)}",
                value=agent_id in st.session_state.config.get("agents_enabled", []),
                key=f"agent_{agent_id}"
            )
            if checkbox:
                enabled_agents.append(agent_id)
    
    st.session_state.config["agents_enabled"] = enabled_agents

    st.divider()
    st.subheader(t("available_workflows"))
    
    enabled_workflows = []
    for wf_id, wf in WORKFLOW_META.items():
        deps_ok = all(d in enabled_agents for d in wf["depends_on"])
        
        if deps_ok:
            checkbox = st.checkbox(
                f"{wf['emoji']} {t_workflow_label(wf_id)}",
                value=wf_id in st.session_state.config.get("workflows_enabled", []),
                key=f"workflow_{wf_id}"
            )
            if checkbox:
                enabled_workflows.append(wf_id)
        else:
            deps_str = ", ".join([f"`{d}`" for d in wf["depends_on"]])
            st.caption(f"⛔ {wf['emoji']} {t_workflow_label(wf_id)} – {t('requires')} {deps_str}")
    
    st.session_state.config["workflows_enabled"] = enabled_workflows

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(t("back"), use_container_width=True):
            st.session_state.step -= 1
            st.rerun()
    with col3:
        if st.button(t("next"), type="primary", use_container_width=True):
            st.session_state.step += 1
            st.rerun()

# ─── SCHRITT 3: GIT & ABRECHNUNG ────────────────────────────────────────────
def render_step_3():
    st.header(t("step3"))

    info_box(t("git_billing"), t("git_desc"))

    st.session_state.config["git_repo_url"] = st.text_input(
        t("git_repo"),
        value=st.session_state.config.get("git_repo_url", ""),
        help=t("git_help")
    )

    st.session_state.config["auto_push"] = st.checkbox(
        t("auto_push"),
        value=st.session_state.config.get("auto_push", True),
        help=t("auto_push_help")
    )

    st.session_state.config["billing_tag_prefix"] = st.text_input(
        t("billing_prefix"),
        value=st.session_state.config.get("billing_tag_prefix", "farm"),
        help=t("billing_help")
    )

    st.session_state.config["reporting_interval_days"] = st.slider(
        t("reporting_interval"),
        min_value=1,
        max_value=30,
        value=st.session_state.config.get("reporting_interval_days", 7),
        help=t("reporting_help")
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(t("back"), use_container_width=True):
            st.session_state.step -= 1
            st.rerun()
    with col3:
        if st.button(t("next"), type="primary", use_container_width=True):
            st.session_state.step += 1
            st.rerun()

# ─── SCHRITT 4: REVIEW & DEPLOY ────────────────────────────────────────────
def render_step_4():
    st.header(t("step4"))

    tab1, tab2 = st.tabs([t("summary"), t("detailed")])
    
    with tab1:
        cfg = st.session_state.config
        st.markdown(f"**📛 {t('farm_name')}:** `{cfg.get('farm_name')}`")
        st.markdown(f"**📍 {t('openclaw_endpoint')}:** `{cfg.get('openclaw_endpoint')}`")
        st.markdown(f"**⚡ {t('parallel_agents')}:** `{cfg.get('max_concurrent_agents')}`")
        
        st.markdown(f"\n{t('enabled_roles')}")
        if cfg.get('agents_enabled'):
            for agent_id in cfg['agents_enabled']:
                emoji = AGENT_META[agent_id]['emoji']
                label = t_agent_label(agent_id)
                st.markdown(f"  • {emoji} {label}")
        else:
            st.markdown(f"  {t('none')}")
        
        st.markdown(f"\n{t('enabled_workflows')}")
        if cfg.get('workflows_enabled'):
            for wf_id in cfg['workflows_enabled']:
                emoji = WORKFLOW_META[wf_id]['emoji']
                label = t_workflow_label(wf_id)
                st.markdown(f"  • {emoji} {label}")
        else:
            st.markdown(f"  {t('none')}")

    with tab2:
        st.subheader(t("yaml_preview"))
        st.code(yaml.dump(st.session_state.config, allow_unicode=True, default_flow_style=False), language="yaml")

    st.divider()
    
    if st.button(t("deploy_btn"), type="primary", use_container_width=True):
        with st.status(t("saving"), expanded=True) as status:
            try:
                # Write farm_config.yaml
                with open("farm_config.yaml", "w") as f:
                    yaml.dump(st.session_state.config, f, allow_unicode=True, default_flow_style=False)
                st.write("✅ farm_config.yaml written")

                # Run pipeline
                result = subprocess.run(
                    ["bash", "run.sh"],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                st.write(result.stdout if result.stdout else result.stderr)
                
                if result.returncode == 0:
                    status.update(label=t("success"), state="complete")
                    st.success(t("saved"))
                    st.code(result.stdout, language="log")
                else:
                    status.update(label=t("error"), state="error")
                    st.error(result.stderr or "Unknown error")
            
            except subprocess.TimeoutExpired:
                status.update(label=t("timeout"), state="error")
                st.error(t("timeout"))
            except FileNotFoundError:
                status.update(label=t("not_found"), state="error")
                st.error(t("not_found"))

    col1, col2 = st.columns(2)
    with col1:
        if st.button(t("back"), use_container_width=True):
            st.session_state.step -= 1
            st.rerun()

# ─── SCHRITT RENDERER ───────────────────────────────────────────────────────
if st.session_state.step == 1:
    render_step_1()
elif st.session_state.step == 2:
    render_step_2()
elif st.session_state.step == 3:
    render_step_3()
elif st.session_state.step == 4:
    render_step_4()

st.divider()
st.caption(t("footer"))
