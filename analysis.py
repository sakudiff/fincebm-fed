import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import os

def fetch_and_analyze():
    # S&P 500 (Wall Street proxy)
    sp500 = yf.download("^GSPC", start="2000-01-01", end="2026-04-01")
    # Flatten columns if multi-index
    sp500.columns = [col[0] if isinstance(col, tuple) else col for col in sp500.columns]
    sp500 = sp500[['Close']].rename(columns={'Close': 'SP500'})
    sp500.index = pd.to_datetime(sp500.index)

    # Unemployment Rate (Main Street proxy)
    unrate_path = "/Users/hoshi/Local Code/fincebm-fed/UNRATE_full.csv"
    if os.path.exists(unrate_path):
        unrate = pd.read_csv(unrate_path, index_col=0, parse_dates=True)
        if 'observation_date' in unrate.columns:
            unrate['observation_date'] = pd.to_datetime(unrate['observation_date'])
            unrate.set_index('observation_date', inplace=True)
    else:
        print("UNRATE_full.csv missing")
        return

    # Filter for the relevant window: 2007-2026
    start_viz = "2007-01-01"
    end_viz = "2026-04-01"
    sp500_viz = sp500.loc[start_viz:end_viz]
    unrate_viz = unrate.loc[start_viz:end_viz]
    
    # Align data for export
    combined = sp500_viz.join(unrate_viz, how='inner').dropna()

    # Plotting: Economist + QVRS Style
    # ... (same colors ...)
    ECONOMIST_RED = "#E3120B"
    CHICAGO_30 = "#1F2E7A"
    LONDON_95 = "#F2F2F2"
    LONDON_20 = "#333333"
    LOS_ANGELES_95 = "#F5F4EF"

    fig, ax1 = plt.subplots(figsize=(10, 6), dpi=300)
    fig.patch.set_facecolor(LOS_ANGELES_95)
    ax1.set_facecolor(LOS_ANGELES_95)

    # Wall Street (S&P 500)
    ax1.plot(sp500_viz.index, sp500_viz['SP500'], color=CHICAGO_30, linewidth=1.8, label='S&P 500 (left)')
    ax1.set_ylabel('S&P 500 index', color=CHICAGO_30, fontweight='bold', fontsize=10)
    ax1.tick_params(axis='y', labelcolor=CHICAGO_30, labelsize=9)

    # Main Street (Unemployment)
    ax2 = ax1.twinx()
    ax2.plot(unrate_viz.index, unrate_viz['UNRATE'], color=ECONOMIST_RED, linewidth=1.5, linestyle='--', label='Unemployment rate (right)')
    ax2.set_ylabel('Unemployment rate, %', color=ECONOMIST_RED, fontweight='bold', fontsize=10)
    ax2.tick_params(axis='y', labelcolor=ECONOMIST_RED, labelsize=9)

    # Grid and Spines
    ax1.grid(True, axis='y', color=LONDON_95, linewidth=0.5)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    ax1.spines['bottom'].set_color(LONDON_20)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.spines['bottom'].set_color(LONDON_20)
    
    # Remove ticks
    ax1.tick_params(size=0)
    ax2.tick_params(size=0)

    # Shaded Epochs
    # GFC Epoch
    ax1.axvspan(pd.to_datetime('2007-10-01'), pd.to_datetime('2009-10-01'), 
                color="#D6DBF5", alpha=0.3, label='Global Financial Crisis')
    ax1.text(pd.to_datetime('2008-10-01'), ax1.get_ylim()[1]*0.95, 'GFC', 
             ha='center', fontsize=9, fontweight='bold', color=CHICAGO_30)

    # COVID Epoch
    ax1.axvspan(pd.to_datetime('2020-02-01'), pd.to_datetime('2020-12-01'), 
                color="#F9D2DB", alpha=0.3, label='COVID-19 Pandemic')
    ax1.text(pd.to_datetime('2020-07-01'), ax1.get_ylim()[1]*0.95, 'COVID-19', 
             ha='center', fontsize=9, fontweight='bold', color=ECONOMIST_RED)

    # Annotations for Divergence Points
    # GFC Divergence (Oct 2009)
    ax1.annotate('Markets rebound', xy=(pd.to_datetime('2009-10-01'), 1030), 
                 xytext=(pd.to_datetime('2011-01-01'), 2000),
                 arrowprops=dict(arrowstyle='->', color=CHICAGO_30),
                 fontsize=9, color=CHICAGO_30)
    
    # COVID Divergence (Dec 2020)
    ax1.annotate('New highs', xy=(pd.to_datetime('2020-12-01'), 3662), 
                 xytext=(pd.to_datetime('2018-01-01'), 5000),
                 arrowprops=dict(arrowstyle='->', color=CHICAGO_30),
                 fontsize=9, color=CHICAGO_30)

    # Current Market State (2026)
    ax1.annotate('Current market stability', xy=(pd.to_datetime('2026-03-31'), 6528), 
                 xytext=(pd.to_datetime('2022-01-01'), 6500),
                 arrowprops=dict(arrowstyle='->', color=CHICAGO_30),
                 fontsize=9, color=CHICAGO_30)

    # Title and Subtitle
    plt.title("A long cycle of divergence and recovery", 
              loc='left', fontsize=14, fontweight='bold', pad=25, color=LONDON_20)
    plt.text(0, 1.05, "S&P 500 index and US unemployment rate, 2007-26", 
             transform=ax1.transAxes, fontsize=11, color=LONDON_20)

    # Legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='lower center', 
               bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False, fontsize=9)

    # Source
    plt.figtext(0.1, 0.02, "Source: FRED, Yahoo Finance. Methodology: Daily close for S&P 500, monthly average for unemployment.", 
                fontsize=8, color=LONDON_20, ha='left')

    # Update date_markers for the table
    date_markers = [
        ('2007-10-01', 'GFC Pre-Crisis Peak'),
        ('2009-03-02', 'GFC Trough'),
        ('2009-10-01', 'GFC Labor Bottom'),
        ('2020-02-03', 'COVID-19 Pre-Shock'),
        ('2020-04-01', 'COVID-19 Trough'),
        ('2020-12-01', 'COVID-19 Divergence'),
        ('2026-03-31', 'Current Stability (2026)')
    ]
    results = []
    for date_str, label in date_markers:
        dt = pd.to_datetime(date_str)
        nearest_sp = sp500.index[sp500.index.get_indexer([dt], method='nearest')[0]]
        # For UNRATE, search unrate_viz
        nearest_un_idx = unrate_viz.index.get_indexer([dt], method='nearest')[0]
        nearest_un = unrate_viz.index[nearest_un_idx]
        
        sp_val = sp500.loc[nearest_sp, 'SP500']
        un_val = unrate_viz.loc[nearest_un, 'UNRATE']
        results.append({
            'Event': label,
            'Month': date_str[:7],
            'Date Marker': nearest_sp.strftime('%Y-%m-%d'),
            'SP500': f"{float(sp_val):,.2f}",
            'UNRATE': f"{float(un_val):.1f}%"
        })

    # Output table
    print("## Macro Divergence Table")
    print(pd.DataFrame(results).to_markdown(index=False))

    # Export to JSON for LLM consumption
    # We'll export the aligned dataframe and the markers
    export_data = {
        "metadata": {
            "title": "A long cycle of divergence and recovery",
            "description": "S&P 500 index and US unemployment rate, 2007-26",
            "source": "FRED, Yahoo Finance",
            "units": {"SP500": "Index", "UNRATE": "Percent"},
            "epochs": [
                {"name": "GFC", "start": "2007-10-01", "end": "2009-10-01", "color": "#D6DBF5"},
                {"name": "COVID-19", "start": "2020-02-01", "end": "2020-12-01", "color": "#F9D2DB"}
            ]
        },
        "markers": results,
        "time_series": combined.reset_index().rename(columns={"index": "date"}).to_dict(orient="records")
    }
    
    import json
    with open('analysis_data.json', 'w') as f:
        json.dump(export_data, f, default=str, indent=2)
    print("\nData exported to analysis_data.json")

    plt.tight_layout()
    plt.subplots_adjust(top=0.85, bottom=0.18)
    plt.savefig('analysis_plot.png', facecolor=LOS_ANGELES_95)
    print("Extended plot saved to analysis_plot.png")

if __name__ == "__main__":
    fetch_and_analyze()
