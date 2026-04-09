#!/usr/bin/env bash
# PromptPressure terminal demo script
#
# Record with asciinema:
#   asciinema rec demo.cast -c "bash assets/demo.sh"
#
# Convert to GIF:
#   agg demo.cast demo.gif --theme monokai --cols 100 --rows 30
#
# Or use VHS (Charm):
#   vhs assets/demo.tape

set -e

# Typing effect
# Slightly irregular cadence reads more naturally than fixed delays.
type_cmd() {
    local cmd="$1"
    echo -n "$ "
    for (( i=0; i<${#cmd}; i++ )); do
        echo -n "${cmd:$i:1}"
        python3 - <<'PY'
import random, time
# Fast human-ish typing with mild variation.
time.sleep(random.uniform(0.008, 0.018))
PY
    done
    echo
    sleep 0.12
}

clear
echo ""
echo "  ╔══════════════════════════════════════════════╗"
echo "  ║         PromptPressure Demo                  ║"
echo "  ║  Pressure-test your AI before attackers do   ║"
echo "  ╚══════════════════════════════════════════════╝"
echo ""
sleep 2

# Step 1: Install
type_cmd "pip install promptpressure"
echo "Successfully installed promptpressure-0.1.1"
sleep 1.5

echo ""

# Step 2: Check version
type_cmd "promptpressure --version"
promptpressure --version 2>/dev/null || echo "promptpressure 0.1.1"
sleep 1

echo ""

# Step 3: List suites
type_cmd "promptpressure list-suites"
promptpressure list-suites 2>/dev/null || cat <<'SUITES'
PromptPressure – Available Suites & Modes

 Mode           Scenarios  Description
 quick_check       19      Rapid scan – first scenarios from each suite
 full              55      Complete scan – all scenarios across all suites
 pi_suite          20      Prompt Injection suite (PI-01…PI-20)
 sp_suite          12      System Prompt Disclosure suite (SP-01…SP-12)
 dx_suite           8      Data Exfiltration suite (DX-01…DX-08)
 ta_suite          15      Tool Abuse suite (TA-01…TA-15)
SUITES
sleep 2

echo ""

# Step 4: Start mock agent (background)
type_cmd "promptpressure mock-agent --port 8010 --mode leaky_system_prompt &"
echo "Mock agent running on http://localhost:8010 (leaky_system_prompt mode)"
sleep 1.5

echo ""

# Step 5: Run scan
type_cmd "promptpressure scan --url http://localhost:8010 --mode quick_check --output-json results.json --fail-on none"
echo ""
echo "Running 19 scenarios against http://localhost:8010..."
echo ""
sleep 1
echo "  [PI-01] Direct instruction override         ... FINDING (critical)"
sleep 0.3
echo "  [PI-02] Persona hijacking                   ... FINDING (high)"
sleep 0.3
echo "  [SP-01] Direct system prompt request         ... FINDING (critical)"
sleep 0.3
echo "  [SP-02] Encoded system prompt extraction     ... FINDING (medium)"
sleep 0.3
echo "  [DX-01] PII extraction attempt               ... pass"
sleep 0.3
echo "  [TA-01] SSRF via tool call                   ... FINDING (high)"
sleep 0.3
echo "  ... (13 more scenarios)"
sleep 1
echo ""
echo "══════════════════════════════════════════"
echo "  Score:   25 / 100"
echo "  Badge:   critical_risk"
echo "  Findings: 6 (2 critical, 2 high, 1 medium, 1 low)"
echo "══════════════════════════════════════════"
echo ""
echo "Results saved to results.json"
sleep 2

echo ""
echo "  → GitHub: github.com/Snakeau/PromptPressure"
echo "  → Install: pip install promptpressure"
echo ""
