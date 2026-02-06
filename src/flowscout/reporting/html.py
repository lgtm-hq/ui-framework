"""HTML report generation — mission control aesthetic with vis.js graph."""

from __future__ import annotations

import json
from pathlib import Path

from jinja2 import Template

from flowscout.analysis.graph import ExplorationResult

REPORT_TEMPLATE = Template("""\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>flowscout — {{ start_url }}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        :root {
            --bg-deep: #06080c;
            --bg-base: #0a0f18;
            --bg-surface: #0f1620;
            --bg-raised: #141e2b;
            --bg-overlay: #1a2636;
            --border-dim: #1c2940;
            --border-base: #243352;
            --border-bright: #2d4a73;
            --text-primary: #c8d6e5;
            --text-secondary: #7a8fa6;
            --text-muted: #4a5f78;
            --accent-green: #00e59b;
            --accent-green-dim: #00e59b33;
            --accent-green-glow: #00e59b18;
            --accent-amber: #ffbe0b;
            --accent-amber-dim: #ffbe0b33;
            --accent-red: #ff4757;
            --accent-red-dim: #ff475733;
            --accent-blue: #4facfe;
            --accent-blue-dim: #4facfe33;
            --accent-cyan: #00f5d4;
            --accent-cyan-dim: #00f5d420;
            --font-mono: 'JetBrains Mono', 'SF Mono', 'Cascadia Code', monospace;
            --font-body: 'DM Sans', 'SF Pro Display', -apple-system, sans-serif;
        }

        *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: var(--font-body);
            background: var(--bg-deep);
            color: var(--text-primary);
            min-height: 100vh;
            overflow-x: hidden;
            -webkit-font-smoothing: antialiased;
        }

        /* === Atmospheric background === */
        body::before {
            content: '';
            position: fixed;
            inset: 0;
            background:
                radial-gradient(ellipse 80% 50% at 20% 0%, #00e59b06 0%, transparent 60%),
                radial-gradient(ellipse 60% 40% at 80% 100%, #4facfe05 0%, transparent 60%),
                radial-gradient(ellipse 100% 100% at 50% 50%, #0a0f18 0%, #06080c 100%);
            pointer-events: none;
            z-index: -1;
        }

        /* === Scanline texture === */
        body::after {
            content: '';
            position: fixed;
            inset: 0;
            background: repeating-linear-gradient(
                0deg,
                transparent,
                transparent 2px,
                #00000008 2px,
                #00000008 4px
            );
            pointer-events: none;
            z-index: 1000;
            mix-blend-mode: multiply;
        }

        /* === Typography === */
        .font-mono { font-family: var(--font-mono); }
        .font-body { font-family: var(--font-body); }

        /* === Layout === */
        .report-container { max-width: 1440px; margin: 0 auto; padding: 0 clamp(1rem, 3vw, 3rem); }

        /* === Header === */
        .report-header {
            position: sticky;
            top: 0;
            z-index: 50;
            border-bottom: 1px solid var(--border-dim);
            background: linear-gradient(180deg, var(--bg-deep) 0%, var(--bg-deep)ee 100%);
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
        }

        .header-inner {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1rem 0;
            gap: 2rem;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .brand-icon {
            width: 32px;
            height: 32px;
            border-radius: 8px;
            background: linear-gradient(135deg, var(--accent-green) 0%, var(--accent-cyan) 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 20px var(--accent-green-dim), inset 0 1px 0 #ffffff20;
        }

        .brand-icon svg { width: 18px; height: 18px; }

        .brand-text {
            font-family: var(--font-mono);
            font-weight: 600;
            font-size: 1.125rem;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, var(--accent-green) 0%, var(--accent-cyan) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .header-meta {
            display: flex;
            align-items: center;
            gap: 1.5rem;
            font-family: var(--font-mono);
            font-size: 0.75rem;
            color: var(--text-muted);
        }

        .header-meta-item {
            display: flex;
            align-items: center;
            gap: 0.375rem;
        }

        .header-meta-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: var(--accent-green);
            box-shadow: 0 0 8px var(--accent-green-dim);
            animation: pulse-dot 2s ease-in-out infinite;
        }

        @keyframes pulse-dot {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.4; }
        }

        /* === Target URL banner === */
        .target-banner {
            margin-top: 2rem;
            padding: 1.25rem 1.5rem;
            background: var(--bg-surface);
            border: 1px solid var(--border-dim);
            border-radius: 12px;
            display: flex;
            align-items: center;
            gap: 1rem;
            position: relative;
            overflow: hidden;
        }

        .target-banner::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 3px;
            background: linear-gradient(180deg, var(--accent-green) 0%, var(--accent-cyan) 100%);
            border-radius: 3px 0 0 3px;
        }

        .target-label {
            font-family: var(--font-mono);
            font-size: 0.625rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: var(--accent-green);
            opacity: 0.7;
        }

        .target-url {
            font-family: var(--font-mono);
            font-size: 0.9375rem;
            font-weight: 400;
            color: var(--text-primary);
            letter-spacing: -0.01em;
        }

        /* === Stats grid === */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 1px;
            margin-top: 2rem;
            background: var(--border-dim);
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid var(--border-dim);
        }

        .stat-card {
            background: var(--bg-surface);
            padding: 1.25rem 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
            position: relative;
            transition: background 0.2s ease;
        }

        .stat-card:hover { background: var(--bg-raised); }

        .stat-value {
            font-family: var(--font-mono);
            font-size: 2rem;
            font-weight: 700;
            letter-spacing: -0.04em;
            line-height: 1;
        }

        .stat-value.green { color: var(--accent-green); }
        .stat-value.amber { color: var(--accent-amber); }
        .stat-value.red { color: var(--accent-red); }
        .stat-value.blue { color: var(--accent-blue); }
        .stat-value.cyan { color: var(--accent-cyan); }
        .stat-value.muted { color: var(--text-muted); }

        .stat-label {
            font-family: var(--font-mono);
            font-size: 0.6875rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-muted);
        }

        .stat-bar {
            height: 2px;
            background: var(--border-dim);
            border-radius: 1px;
            margin-top: 0.5rem;
            overflow: hidden;
        }

        .stat-bar-fill {
            height: 100%;
            border-radius: 1px;
            transition: width 0.6s ease;
        }

        /* === Section headers === */
        .section {
            margin-top: 3rem;
        }

        .section-header {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1.25rem;
        }

        .section-header h2 {
            font-family: var(--font-body);
            font-size: 1.125rem;
            font-weight: 600;
            color: var(--text-primary);
            letter-spacing: -0.01em;
        }

        .section-count {
            font-family: var(--font-mono);
            font-size: 0.6875rem;
            font-weight: 500;
            color: var(--text-muted);
            background: var(--bg-raised);
            border: 1px solid var(--border-dim);
            padding: 0.125rem 0.5rem;
            border-radius: 100px;
        }

        .section-line {
            flex: 1;
            height: 1px;
            background: linear-gradient(90deg, var(--border-dim) 0%, transparent 100%);
        }

        /* === Graph === */
        #graph-container {
            height: 560px;
            background: var(--bg-surface);
            border: 1px solid var(--border-dim);
            border-radius: 12px;
            position: relative;
            overflow: hidden;
        }

        #graph-container::before {
            content: '';
            position: absolute;
            inset: 0;
            background:
                radial-gradient(circle at 50% 50%, var(--accent-green-glow) 0%, transparent 70%);
            pointer-events: none;
            z-index: 0;
        }

        .graph-legend {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            margin-top: 0.75rem;
            padding: 0 0.25rem;
        }

        .legend-item {
            display: flex;
            align-items: center;
            gap: 0.375rem;
            font-family: var(--font-mono);
            font-size: 0.6875rem;
            color: var(--text-muted);
        }

        .legend-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            box-shadow: 0 0 6px currentColor;
        }

        /* === Flows === */
        .flow-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-dim);
            border-radius: 10px;
            overflow: hidden;
            transition: border-color 0.2s ease;
        }

        .flow-card:hover { border-color: var(--border-base); }

        .flow-summary {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.875rem 1.25rem;
            cursor: pointer;
            user-select: none;
            transition: background 0.15s ease;
        }

        .flow-summary:hover { background: var(--bg-raised); }

        .flow-summary-left {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .flow-badge {
            font-family: var(--font-mono);
            font-size: 0.625rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            padding: 0.1875rem 0.5rem;
            border-radius: 4px;
        }

        .flow-badge.linear {
            color: var(--accent-green);
            background: var(--accent-green-dim);
        }

        .flow-badge.cycle {
            color: var(--accent-amber);
            background: var(--accent-amber-dim);
        }

        .flow-name {
            font-weight: 500;
            font-size: 0.875rem;
            color: var(--text-primary);
        }

        .flow-steps {
            font-family: var(--font-mono);
            font-size: 0.6875rem;
            color: var(--text-muted);
        }

        .flow-chevron {
            width: 16px;
            height: 16px;
            color: var(--text-muted);
            transition: transform 0.2s ease;
            flex-shrink: 0;
        }

        details[open] .flow-chevron { transform: rotate(180deg); }

        .flow-detail {
            padding: 0 1.25rem 1rem;
            border-top: 1px solid var(--border-dim);
        }

        .flow-description {
            font-size: 0.8125rem;
            color: var(--text-secondary);
            margin-top: 0.75rem;
            line-height: 1.5;
            word-break: break-all;
        }

        .flow-chain {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 0.375rem;
            margin-top: 0.75rem;
        }

        .flow-node {
            font-family: var(--font-mono);
            font-size: 0.6875rem;
            font-weight: 500;
            padding: 0.25rem 0.625rem;
            background: var(--bg-overlay);
            border: 1px solid var(--border-base);
            border-radius: 6px;
            color: var(--accent-cyan);
        }

        .flow-arrow-sep {
            color: var(--text-muted);
            font-size: 0.75rem;
        }

        /* === Tables === */
        .data-table-wrap {
            background: var(--bg-surface);
            border: 1px solid var(--border-dim);
            border-radius: 12px;
            overflow: hidden;
        }

        .data-table {
            width: 100%;
            font-size: 0.8125rem;
            border-collapse: collapse;
        }

        .data-table thead th {
            font-family: var(--font-mono);
            font-size: 0.625rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-muted);
            text-align: left;
            padding: 0.75rem 1.25rem;
            border-bottom: 1px solid var(--border-dim);
            background: var(--bg-raised);
            position: sticky;
            top: 0;
        }

        .data-table thead th.right { text-align: right; }

        .data-table tbody td {
            padding: 0.625rem 1.25rem;
            border-bottom: 1px solid #0f1620;
            vertical-align: middle;
        }

        .data-table tbody tr { transition: background 0.1s ease; }
        .data-table tbody tr:hover { background: var(--bg-raised); }
        .data-table tbody tr:last-child td { border-bottom: none; }

        .cell-id {
            font-family: var(--font-mono);
            font-weight: 500;
            font-size: 0.75rem;
            color: var(--accent-cyan);
        }

        .cell-url {
            font-family: var(--font-mono);
            font-size: 0.6875rem;
            color: var(--text-muted);
            max-width: 340px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .cell-dim {
            font-family: var(--font-mono);
            font-size: 0.75rem;
            color: var(--text-muted);
        }

        .cell-right {
            text-align: right;
            font-family: var(--font-mono);
            font-size: 0.75rem;
            color: var(--text-muted);
        }

        .cell-action {
            font-size: 0.75rem;
            color: var(--text-secondary);
            max-width: 420px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .cell-signals {
            font-size: 0.6875rem;
            color: var(--text-muted);
            max-width: 250px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        /* === Outcome badges === */
        .outcome {
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
            font-family: var(--font-mono);
            font-size: 0.625rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            padding: 0.1875rem 0.5rem;
            border-radius: 4px;
            white-space: nowrap;
        }

        .outcome.navigation {
            color: var(--accent-green);
            background: var(--accent-green-dim);
        }
        .outcome.dom_change {
            color: var(--accent-amber);
            background: var(--accent-amber-dim);
        }
        .outcome.no_change {
            color: var(--text-muted);
            background: #4a5f7815;
        }
        .outcome.timeout,
        .outcome.validation_error,
        .outcome.network_error,
        .outcome.console_error,
        .outcome.exception {
            color: var(--accent-red);
            background: var(--accent-red-dim);
        }

        /* === Verdict badges === */
        .verdict {
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
            font-family: var(--font-mono);
            font-size: 0.625rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            padding: 0.1875rem 0.5rem;
            border-radius: 4px;
            white-space: nowrap;
        }
        .verdict.pass {
            color: var(--accent-green);
            background: var(--accent-green-dim);
        }
        .verdict.fail {
            color: var(--accent-red);
            background: var(--accent-red-dim);
        }
        .verdict.warn {
            color: var(--accent-amber);
            background: var(--accent-amber-dim);
        }
        .verdict.inconclusive {
            color: var(--text-muted);
            background: #4a5f7815;
        }

        /* === Narrative steps === */
        .narrative-step {
            padding: 0.75rem 1rem;
            border-left: 2px solid var(--border-dim);
            margin-left: 0.75rem;
            margin-bottom: 0.5rem;
            font-size: 0.8125rem;
        }
        .narrative-step .step-action {
            color: var(--text-primary);
            font-weight: 500;
        }
        .narrative-step .step-expected {
            color: var(--text-muted);
            font-size: 0.75rem;
            margin-top: 0.25rem;
        }
        .narrative-step .step-actual {
            color: var(--text-secondary);
            font-size: 0.75rem;
        }

        .gherkin-toggle {
            font-family: var(--font-mono);
            font-size: 0.6875rem;
            cursor: pointer;
            color: var(--accent-cyan);
            background: none;
            border: 1px solid var(--accent-cyan-dim);
            padding: 0.25rem 0.625rem;
            border-radius: 4px;
            margin-top: 0.5rem;
        }
        .gherkin-toggle:hover { background: var(--accent-cyan-dim); }
        .gherkin-block {
            font-family: var(--font-mono);
            font-size: 0.75rem;
            color: var(--accent-cyan);
            background: var(--bg-raised);
            padding: 0.75rem 1rem;
            border-radius: 6px;
            margin-top: 0.5rem;
            white-space: pre-wrap;
            display: none;
        }
        .gherkin-block.visible { display: block; }

        /* === Errors section === */
        .error-card {
            background: linear-gradient(135deg, #ff475708, #ff475703);
            border: 1px solid #ff475725;
            border-radius: 10px;
            padding: 1rem 1.25rem;
            font-size: 0.8125rem;
        }

        .error-card-header {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.5rem;
        }

        .error-type {
            font-family: var(--font-mono);
            font-weight: 600;
            font-size: 0.75rem;
            color: var(--accent-red);
        }

        .error-action {
            font-family: var(--font-mono);
            font-size: 0.6875rem;
            color: var(--text-muted);
        }

        .error-message {
            font-size: 0.8125rem;
            color: #ff8a99;
            line-height: 1.5;
        }

        .error-detail {
            font-family: var(--font-mono);
            font-size: 0.6875rem;
            color: var(--text-muted);
            margin-top: 0.375rem;
        }

        /* === Footer === */
        .report-footer {
            margin-top: 4rem;
            padding: 1.5rem 0;
            border-top: 1px solid var(--border-dim);
            text-align: center;
            font-family: var(--font-mono);
            font-size: 0.6875rem;
            color: var(--text-muted);
        }

        .report-footer span {
            background: linear-gradient(135deg, var(--accent-green), var(--accent-cyan));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 600;
        }

        /* === Animations === */
        @keyframes fade-up {
            from { opacity: 0; transform: translateY(12px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .animate-in {
            animation: fade-up 0.5s ease forwards;
            opacity: 0;
        }

        .delay-1 { animation-delay: 0.1s; }
        .delay-2 { animation-delay: 0.2s; }
        .delay-3 { animation-delay: 0.3s; }
        .delay-4 { animation-delay: 0.4s; }
        .delay-5 { animation-delay: 0.5s; }
        .delay-6 { animation-delay: 0.6s; }

        /* === Scrollbar === */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: var(--border-base); border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--border-bright); }

        /* === Responsive === */
        @media (max-width: 768px) {
            .header-meta { display: none; }
            .stats-grid { grid-template-columns: repeat(2, 1fr); }
            .stat-value { font-size: 1.5rem; }
        }

        /* === Table scroll container === */
        .table-scroll {
            overflow-x: auto;
            max-height: 480px;
            overflow-y: auto;
        }
    </style>
</head>
<body>

    <!-- Header -->
    <header class="report-header">
        <div class="report-container">
            <div class="header-inner">
                <div class="brand">
                    <div class="brand-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="#06080c" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                            <circle cx="12" cy="12" r="3"/>
                            <path d="M12 2v4m0 12v4M2 12h4m12 0h4"/>
                            <path d="m4.93 4.93 2.83 2.83m8.48 8.48 2.83 2.83M4.93 19.07l2.83-2.83m8.48-8.48 2.83-2.83"/>
                        </svg>
                    </div>
                    <div class="brand-text">flowscout</div>
                </div>
                <div class="header-meta">
                    <div class="header-meta-item">
                        <div class="header-meta-dot"></div>
                        <span>{{ started_at[:19] }} UTC</span>
                    </div>
                    <div class="header-meta-item">
                        <span>{{ "%.1f"|format(duration) }}s</span>
                    </div>
                    <div class="header-meta-item">
                        <span>{{ config_strategy }}</span>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <main class="report-container">

        <!-- Target URL -->
        <div class="target-banner animate-in">
            <div>
                <div class="target-label">target</div>
                <div class="target-url">{{ start_url }}</div>
            </div>
        </div>

        <!-- Stats -->
        <div class="stats-grid animate-in delay-1">
            {% for label, value, color_class, pct in stat_cards %}
            <div class="stat-card">
                <div class="stat-value {{ color_class }}">{{ value }}</div>
                <div class="stat-label">{{ label }}</div>
                {% if pct > 0 %}
                <div class="stat-bar">
                    <div class="stat-bar-fill" style="width: {{ pct }}%; background: {% if color_class == 'green' %}var(--accent-green){% elif color_class == 'amber' %}var(--accent-amber){% elif color_class == 'red' %}var(--accent-red){% elif color_class == 'blue' %}var(--accent-blue){% else %}var(--accent-cyan){% endif %};"></div>
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>

        <!-- Graph -->
        <section class="section animate-in delay-2">
            <div class="section-header">
                <h2>State Graph</h2>
                <div class="section-line"></div>
            </div>
            <div id="graph-container"></div>
            <div class="graph-legend">
                <div class="legend-item"><div class="legend-dot" style="color: var(--accent-green);"></div> navigation</div>
                <div class="legend-item"><div class="legend-dot" style="color: var(--accent-amber);"></div> dom change</div>
                <div class="legend-item"><div class="legend-dot" style="color: var(--accent-red);"></div> error / timeout</div>
                <div class="legend-item"><div class="legend-dot" style="color: var(--text-muted);"></div> no change</div>
            </div>
        </section>

        <!-- Flows -->
        <section class="section animate-in delay-3">
            <div class="section-header">
                <h2>Discovered Flows</h2>
                <div class="section-count">{{ flows|length }}</div>
                <div class="section-line"></div>
            </div>
            <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                {% for flow in flows %}
                <details class="flow-card">
                    <summary class="flow-summary">
                        <div class="flow-summary-left">
                            {% if flow.is_cycle %}
                            <span class="flow-badge cycle">cycle</span>
                            {% else %}
                            <span class="flow-badge linear">linear</span>
                            {% endif %}
                            {% if flow.verdict %}
                            <span class="verdict {{ flow.verdict.verdict.value }}">{{ flow.verdict.verdict.value }}</span>
                            {% endif %}
                            <span class="flow-name">{{ flow.name }}</span>
                            <span class="flow-steps">{{ flow.depth }} step{{ 's' if flow.depth != 1 }}</span>
                        </div>
                        <svg class="flow-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
                    </summary>
                    <div class="flow-detail">
                        <div class="flow-description">{{ flow.description }}</div>
                        <div class="flow-chain">
                            {% for sid in flow.state_ids %}
                            <span class="flow-node">{{ sid[:8] }}</span>
                            {% if not loop.last %}
                            <span class="flow-arrow-sep">&rarr;</span>
                            {% endif %}
                            {% endfor %}
                        </div>
                        {% if flow.narrative and flow.narrative.steps %}
                        <div style="margin-top: 0.75rem;">
                            {% for step in flow.narrative.steps %}
                            <div class="narrative-step">
                                <div class="step-action">
                                    {{ step.step_number }}. {{ step.action_description }}
                                    {% if step.verdict %}<span class="verdict {{ step.verdict.value }}">{{ step.verdict.value }}</span>{% endif %}
                                </div>
                                {% if step.expected %}<div class="step-expected">Expected: {{ step.expected }}</div>{% endif %}
                                {% if step.actual %}<div class="step-actual">Actual: {{ step.actual }}</div>{% endif %}
                            </div>
                            {% endfor %}
                        </div>
                        {% endif %}
                        {% if flow.narrative and flow.narrative.gherkin %}
                        <button class="gherkin-toggle" onclick="this.nextElementSibling.classList.toggle('visible')">Toggle Gherkin</button>
                        <div class="gherkin-block">{{ flow.narrative.gherkin }}</div>
                        {% endif %}
                    </div>
                </details>
                {% endfor %}
            </div>
        </section>

        <!-- States -->
        <section class="section animate-in delay-4">
            <div class="section-header">
                <h2>States</h2>
                <div class="section-count">{{ states|length }}</div>
                <div class="section-line"></div>
            </div>
            <div class="data-table-wrap">
                <div class="table-scroll">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Title</th>
                                <th>URL</th>
                                <th class="right">Depth</th>
                                <th>Signals</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for state in states %}
                            <tr>
                                <td class="cell-id">{{ state.state_id[:8] }}</td>
                                <td>{{ state.title or '—' }}</td>
                                <td class="cell-url">{{ state.url }}</td>
                                <td class="cell-right">{{ state.depth }}</td>
                                <td class="cell-signals">{{ state.signals|join(', ') }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- Action Log -->
        <section class="section animate-in delay-5">
            <div class="section-header">
                <h2>Action Log</h2>
                <div class="section-count">{{ results|length }}</div>
                <div class="section-line"></div>
            </div>
            <div class="data-table-wrap">
                <div class="table-scroll">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>From</th>
                                <th>Action</th>
                                <th>Expected</th>
                                <th>Outcome</th>
                                <th>Verdict</th>
                                <th>To</th>
                                <th class="right">Time</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for r in results %}
                            <tr>
                                <td class="cell-dim">{{ loop.index }}</td>
                                <td class="cell-id">{{ r.source_state_id[:8] }}</td>
                                <td class="cell-action">{{ actions.get(r.action_id, r.action_id) }}</td>
                                <td class="cell-dim" style="max-width: 150px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{{ r.expected or '' }}</td>
                                <td><span class="outcome {{ r.outcome.value }}">{{ r.outcome.value }}</span></td>
                                <td>{% if r.verdict %}<span class="verdict {{ r.verdict }}">{{ r.verdict }}</span>{% endif %}</td>
                                <td class="cell-id">{{ r.target_state_id[:8] }}</td>
                                <td class="cell-right">{{ "%.0f"|format(r.duration_ms) }}ms</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- Errors -->
        {% if error_results %}
        <section class="section animate-in delay-6">
            <div class="section-header">
                <h2 style="color: var(--accent-red);">Errors</h2>
                <div class="section-count" style="color: var(--accent-red); border-color: var(--accent-red-dim);">{{ error_results|length }}</div>
                <div class="section-line"></div>
            </div>
            <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                {% for r in error_results %}
                <div class="error-card">
                    <div class="error-card-header">
                        <span class="error-type">{{ r.outcome.value }}</span>
                        <span class="error-action">{{ actions.get(r.action_id, r.action_id) }}</span>
                    </div>
                    {% if r.error_messages %}
                    <div class="error-message">{{ r.error_messages|join('; ') }}</div>
                    {% endif %}
                    {% if r.console_errors %}
                    <div class="error-detail">{{ r.console_errors|join('; ') }}</div>
                    {% endif %}
                    {% if r.message %}
                    <div class="error-detail">{{ r.message[:120] }}</div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
        </section>
        {% endif %}

    </main>

    <!-- Footer -->
    <footer class="report-container">
        <div class="report-footer">
            generated by <span>flowscout</span> v{{ version }}
        </div>
    </footer>

    <!-- Graph Script -->
    <script>
        const graphData = {{ graph_json }};

        const depthPalette = ['#00e59b', '#4facfe', '#00f5d4', '#ffbe0b', '#ff6b6b', '#c084fc'];
        const outcomeEdgeColors = {
            'navigation': '#00e59b',
            'dom_change': '#ffbe0b',
            'visual_change': '#4facfe',
            'no_change': '#4a5f78',
            'validation_error': '#ff4757',
            'network_error': '#ff4757',
            'console_error': '#ff4757',
            'timeout': '#ff6b6b',
            'exception': '#ff4757',
        };

        const nodes = new vis.DataSet(graphData.nodes.map(n => ({
            id: n.id,
            label: (n.label || n.url || n.id).substring(0, 35),
            title: `<div style="font-family:monospace;font-size:11px;padding:6px 10px;line-height:1.6;max-width:320px;">` +
                   `<strong style="color:${depthPalette[Math.min(n.depth, depthPalette.length-1)]}">${n.id.substring(0,8)}</strong><br>` +
                   `URL: ${n.url}<br>Depth: ${n.depth}<br>` +
                   `Signals: ${(n.signals||[]).join(', ')}</div>`,
            color: {
                background: '#0f1620',
                border: depthPalette[Math.min(n.depth, depthPalette.length - 1)],
                highlight: { background: '#1a2636', border: '#00e59b' },
                hover: { background: '#141e2b', border: depthPalette[Math.min(n.depth, depthPalette.length - 1)] },
            },
            font: {
                color: '#c8d6e5',
                size: 11,
                face: "'JetBrains Mono', monospace",
            },
            shape: 'box',
            borderWidth: 2,
            borderWidthSelected: 3,
            margin: { top: 10, right: 14, bottom: 10, left: 14 },
            shadow: {
                enabled: true,
                color: depthPalette[Math.min(n.depth, depthPalette.length - 1)] + '15',
                size: 20,
                x: 0,
                y: 4,
            },
        })));

        const edges = new vis.DataSet(graphData.edges.map((e, i) => ({
            id: i,
            from: e.source,
            to: e.target,
            label: (e.label || '').replace(/^Click:\\s*/, '').substring(0, 22),
            title: `<div style="font-family:monospace;font-size:11px;padding:6px 10px;">` +
                   `Action: ${e.label}<br>Outcome: <strong>${e.outcome}</strong></div>`,
            color: {
                color: outcomeEdgeColors[e.outcome] || '#4a5f78',
                highlight: '#00e59b',
                hover: outcomeEdgeColors[e.outcome] || '#7a8fa6',
                opacity: 0.7,
            },
            arrows: { to: { enabled: true, scaleFactor: 0.6, type: 'arrow' } },
            font: {
                color: '#7a8fa6',
                size: 9,
                strokeWidth: 0,
                face: "'JetBrains Mono', monospace",
                align: 'top',
            },
            smooth: { type: 'curvedCW', roundness: 0.15 },
            width: 1.5,
            hoverWidth: 0.5,
        })));

        const container = document.getElementById('graph-container');
        const network = new vis.Network(container, { nodes, edges }, {
            physics: {
                solver: 'forceAtlas2Based',
                forceAtlas2Based: {
                    gravitationalConstant: -50,
                    centralGravity: 0.008,
                    springLength: 180,
                    springConstant: 0.04,
                    damping: 0.4,
                    avoidOverlap: 0.5,
                },
                stabilization: { iterations: 200, fit: true },
            },
            interaction: {
                hover: true,
                tooltipDelay: 150,
                zoomView: true,
                dragView: true,
            },
            layout: { improvedLayout: true },
        });

        // Fit after stabilization
        network.once('stabilizationIterationsDone', () => {
            network.fit({ animation: { duration: 400, easingFunction: 'easeInOutQuad' } });
        });
    </script>

</body>
</html>
""")


class HTMLReporter:
    """Generates a standalone HTML report."""

    def generate(self, result: ExplorationResult, output_path: str) -> None:
        """Generate the HTML report file."""
        from flowscout import __version__

        graph_data = _build_graph_data(result)
        stat_cards = _build_stat_cards(result)
        error_results = [
            r
            for r in result.results
            if r.outcome.value
            in (
                "validation_error",
                "network_error",
                "console_error",
                "timeout",
                "exception",
            )
        ]

        # Build action label lookup
        action_labels = {aid: a.label for aid, a in result.actions.items()}

        html = REPORT_TEMPLATE.render(
            start_url=result.config.get("start_url", "unknown"),
            started_at=result.started_at,
            duration=result.duration_seconds,
            config_strategy=result.config.get("strategy", "priority"),
            stat_cards=stat_cards,
            flows=result.flows,
            states=list(result.states.values()),
            results=result.results,
            actions=action_labels,
            error_results=error_results,
            graph_json=json.dumps(graph_data),
            version=__version__,
        )

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html)


def _build_graph_data(result: ExplorationResult) -> dict:
    """Build vis.js-compatible graph data."""
    nodes = []
    for sid, state in result.states.items():
        nodes.append(
            {
                "id": sid,
                "label": state.title or state.url,
                "url": state.url,
                "depth": state.depth,
                "signals": state.signals,
            }
        )

    edges = []
    for r in result.results:
        action = result.actions.get(r.action_id)
        edges.append(
            {
                "source": r.source_state_id,
                "target": r.target_state_id,
                "label": action.label if action else r.action_id,
                "outcome": r.outcome.value,
            }
        )

    return {"nodes": nodes, "edges": edges}


def _build_stat_cards(result: ExplorationResult) -> list[tuple[str, str, str, int]]:
    """Build stat card data: (label, value, color_class, bar_pct)."""
    stats = result.stats
    total_actions = max(stats.get("total_actions_executed", 1), 1)

    nav_count = stats.get("outcome_navigation", 0)
    dom_count = stats.get("outcome_dom_change", 0)
    error_count = sum(
        stats.get(f"outcome_{k}", 0)
        for k in (
            "validation_error",
            "network_error",
            "console_error",
            "timeout",
            "exception",
        )
    )

    pass_count = sum(1 for r in result.results if r.verdict == "pass")
    fail_count = sum(1 for r in result.results if r.verdict == "fail")

    return [
        ("States", str(stats.get("total_states", 0)), "cyan", 0),
        ("Actions", str(total_actions), "blue", 0),
        ("Flows", str(len(result.flows)), "green", 0),
        (
            "Passed",
            str(pass_count),
            "green",
            int(pass_count / total_actions * 100) if pass_count else 0,
        ),
        (
            "Failed",
            str(fail_count),
            "red" if fail_count > 0 else "muted",
            int(fail_count / total_actions * 100) if fail_count else 0,
        ),
        ("Navigations", str(nav_count), "green", int(nav_count / total_actions * 100)),
        ("DOM Changes", str(dom_count), "amber", int(dom_count / total_actions * 100)),
        (
            "Errors",
            str(error_count),
            "red" if error_count > 0 else "muted",
            int(error_count / total_actions * 100),
        ),
    ]
