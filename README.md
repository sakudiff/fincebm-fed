# Wall Street vs. Main Street: The Great Divergence (2007–2026)

This repository contains an automated programmatic analysis of the structural disconnect between financial markets and the real economy over two decades of crisis and recovery.

## Overview

Equity markets frequently rebound while labor markets remain in distress. This analysis utilizes a vectorized methodology to align daily S&P 500 (`^GSPC`) closes with monthly U.S. Civilian Unemployment (`UNRATE`) data from the Federal Reserve Economic Data (FRED).

### Key Findings

- **The Recovery Gap:** S&P 500 rebounds typically begin *within* the crisis window, often gaining 40–50% before labor market conditions even bottom.
- **Divergence Eras:** Shaded regions highlight the Global Financial Crisis (2007–2009) and the COVID-19 Pandemic (2020), showcasing the "K-shaped" nature of modern recoveries.
- **Current State (2026):** Asset prices have reached historical highs (~6,500+) while unemployment has settled into a stabilized floor of ~4.4%.

## Project Structure

- `analysis.py`: The main execution engine. Fetches data via `yfinance`, joins with local FRED history, and generates the visualization.
- `analysis_plot.png`: The final high-fidelity visualization produced using *The Economist* and Quantitative Visualization (QVRS) standards.
- `analysis_data.json`: Aligned dataset and critical markers exported for consumption by analytical LLMs.
- `UNRATE_full.csv`: Local snapshot of historic unemployment data (1948–2026).
- `pyproject.toml`: Dependency and environment configuration for `uv`.

## Execution

This project is managed with `uv` for $O(1)$ environment setup and deterministic builds.

```bash
# Run the complete analysis
uv run python analysis.py
```

### Visualization Specifications

The output plot follows strict design principles:
- **Chicago Blue (`#1F2E7A`)**: Represents the S&P 500 (left axis).
- **Economist Red (`#E3120B`)**: Represents the Unemployment Rate (right axis).
- **Austerity**: Stripped ticks and high-contrast grid lines ensure maximum data-to-ink ratio.

## Sources
- **FRED**: U.S. Civilian Unemployment Rate.
- **Yahoo Finance**: S&P 500 Index History.

---
