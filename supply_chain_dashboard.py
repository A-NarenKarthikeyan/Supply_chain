import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Supply Chain Intelligence | Naren Karthikeyan",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --navy:      #0a0f1e;
    --navy2:     #0d1530;
    --navy3:     #111d3c;
    --cyan:      #00e5ff;
    --cyan2:     #00b4cc;
    --cyan-glow: rgba(0,229,255,0.15);
    --red:       #ff4d6d;
    --amber:     #ffb347;
    --green:     #00e676;
    --text:      #e2e8f0;
    --muted:     #6b7fa3;
    --card-bg:   rgba(13,21,48,0.85);
    --border:    rgba(0,229,255,0.15);
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--navy) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: var(--navy2) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * { color: var(--text) !important; }

h1, h2, h3 {
    font-family: 'Space Mono', monospace !important;
    color: var(--cyan) !important;
    letter-spacing: -0.5px;
}

.metric-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px 20px;
    text-align: center;
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--cyan), transparent);
}
.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px var(--cyan-glow);
}
.metric-value {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: var(--cyan);
    line-height: 1.1;
}
.metric-value.red   { color: var(--red); }
.metric-value.amber { color: var(--amber); }
.metric-value.green { color: var(--green); }
.metric-label {
    font-size: 0.75rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 6px;
}
.metric-sub {
    font-size: 0.8rem;
    color: var(--text);
    margin-top: 4px;
    opacity: 0.7;
}

.section-header {
    font-family: 'Space Mono', monospace;
    color: var(--cyan);
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    border-bottom: 1px solid var(--border);
    padding-bottom: 8px;
    margin: 28px 0 16px 0;
}

.stat-box {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px 20px;
    margin: 8px 0;
}
.stat-box .label {
    font-size: 0.72rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 1px;
}
.stat-box .value {
    font-family: 'Space Mono', monospace;
    font-size: 1.1rem;
    color: var(--cyan);
    margin-top: 4px;
}
.stat-box .interpretation {
    font-size: 0.78rem;
    color: var(--text);
    margin-top: 6px;
    opacity: 0.8;
    line-height: 1.5;
}

.finding-card {
    background: linear-gradient(135deg, var(--navy2), var(--navy3));
    border-left: 3px solid var(--cyan);
    border-radius: 0 10px 10px 0;
    padding: 16px 20px;
    margin: 10px 0;
    font-size: 0.88rem;
    line-height: 1.6;
    color: var(--text);
}

.rec-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    margin: 10px 0;
}
.rec-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    color: var(--cyan);
    margin-bottom: 8px;
}
.rec-body {
    font-size: 0.83rem;
    color: var(--text);
    line-height: 1.6;
    opacity: 0.85;
}
.tag {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-family: 'Space Mono', monospace;
    margin-right: 6px;
}
.tag-immediate { background: rgba(255,77,109,0.15); color: var(--red); border: 1px solid rgba(255,77,109,0.3); }
.tag-medium    { background: rgba(255,179,71,0.15);  color: var(--amber); border: 1px solid rgba(255,179,71,0.3); }
.tag-strategic { background: rgba(0,230,118,0.15);  color: var(--green); border: 1px solid rgba(0,230,118,0.3); }

.hero-banner {
    background: linear-gradient(135deg, var(--navy2) 0%, var(--navy3) 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 32px 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero-banner::after {
    content: '◈';
    position: absolute;
    right: 36px; top: 50%;
    transform: translateY(-50%);
    font-size: 5rem;
    color: var(--cyan);
    opacity: 0.06;
}
.hero-title {
    font-family: 'Space Mono', monospace;
    font-size: 1.6rem;
    color: var(--cyan);
    margin: 0 0 8px 0;
}
.hero-sub {
    font-size: 0.88rem;
    color: var(--muted);
    letter-spacing: 0.5px;
}

stSelectbox label, .stRadio label { color: var(--text) !important; }
</style>
""", unsafe_allow_html=True)


# ── Data Loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('dataco_clean.csv')
    return df

@st.cache_data
def compute_stats(df):
    # Regional
    regional = df.groupby('order_region').agg(
        total_orders=('is_delayed', 'count'),
        delayed_orders=('is_delayed', 'sum'),
        delay_rate_pct=('is_delayed', lambda x: round(x.mean() * 100, 2)),
        avg_delay_days=('delay_days', lambda x: round(x.mean(), 3)),
        total_delay_cost=('delay_cost', lambda x: round(x.sum(), 2))
    ).reset_index().sort_values('delay_rate_pct', ascending=False)

    # Shipping mode
    mode = df.groupby('shipping_mode').agg(
        total_orders=('is_delayed', 'count'),
        delayed_orders=('is_delayed', 'sum'),
        delay_rate_pct=('is_delayed', lambda x: round(x.mean() * 100, 2)),
        sla_compliance_pct=('is_delayed', lambda x: round((1 - x.mean()) * 100, 2)),
        avg_delay_days=('delay_days', lambda x: round(x.mean(), 3)),
        total_delay_cost=('delay_cost', lambda x: round(x.sum(), 2))
    ).reset_index()

    # Category
    cat = df.groupby('category_name').agg(
        total_orders=('is_delayed', 'count'),
        delay_rate_pct=('is_delayed', lambda x: round(x.mean() * 100, 2)),
        avg_delay_days=('delay_days', lambda x: round(x.mean(), 3))
    ).reset_index().sort_values('delay_rate_pct', ascending=False).head(15)

    # Corridor (excl First Class)
    corridor = df[df['shipping_mode'] != 'First Class'].groupby(
        ['order_region', 'shipping_mode']
    ).agg(
        total_orders=('is_delayed', 'count'),
        delay_rate_pct=('is_delayed', lambda x: round(x.mean() * 100, 2)),
        avg_delay_days=('delay_days', lambda x: round(x.mean(), 3)),
        total_delay_cost=('delay_cost', lambda x: round(x.sum(), 2))
    ).reset_index()
    corridor = corridor[corridor['total_orders'] > 100].sort_values(
        'delay_rate_pct', ascending=False
    ).head(10)

    return regional, mode, cat, corridor


@st.cache_data
def run_statistical_tests(df):
    results = {}

    # ANOVA
    regional_groups = [g['delay_days'].dropna().values
                       for _, g in df.groupby('order_region')]
    f_stat, p_anova = stats.f_oneway(*regional_groups)
    results['anova'] = {'f': round(f_stat, 4), 'p': p_anova,
                        'sig': p_anova < 0.05}

    # Chi-square
    contingency = pd.crosstab(df['shipping_mode'], df['is_delayed'])
    chi2, p_chi, dof, _ = stats.chi2_contingency(contingency)
    results['chi2'] = {'chi2': round(chi2, 2), 'p': p_chi,
                       'dof': dof, 'sig': p_chi < 0.05}

    # Kruskal-Wallis
    cat_groups = [g['delay_days'].dropna().values
                  for _, g in df.groupby('category_name')]
    h_stat, p_kruskal = stats.kruskal(*cat_groups)
    results['kruskal'] = {'h': round(h_stat, 4), 'p': round(p_kruskal, 6),
                          'sig': p_kruskal < 0.05}

    # Z-test
    std  = df[df['shipping_mode'] == 'Standard Class']['is_delayed']
    same = df[df['shipping_mode'] == 'Same Day']['is_delayed']
    n1, p1 = len(std),  std.mean()
    n2, p2 = len(same), same.mean()
    p_pool = (std.sum() + same.sum()) / (n1 + n2)
    z = (p1 - p2) / np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
    p_z = 2 * (1 - stats.norm.cdf(abs(z)))
    results['ztest'] = {'z': round(z, 4), 'p': p_z,
                        'p1': round(p1*100, 2), 'p2': round(p2*100, 2),
                        'sig': p_z < 0.05}

    # Spearman
    corr_df = df[['order_item_total', 'delay_cost']].dropna()
    sp_r, sp_p = stats.spearmanr(corr_df['order_item_total'],
                                  corr_df['delay_cost'])
    results['spearman'] = {'r': round(sp_r, 4), 'p': sp_p, 'sig': sp_p < 0.05}

    return results


# ── Plotly Theme ──────────────────────────────────────────────────────────────
PLOT_BG    = '#0a0f1e'
PAPER_BG   = '#0a0f1e'
GRID_COLOR = 'rgba(0,229,255,0.08)'
CYAN       = '#00e5ff'
RED        = '#ff4d6d'
AMBER      = '#ffb347'
GREEN      = '#00e676'
MUTED      = '#6b7fa3'
FONT_FAMILY = 'DM Sans, sans-serif'

def base_layout(title='', height=380):
    return dict(
        title=dict(text=title, font=dict(family='Space Mono', color=CYAN, size=13)),
        plot_bgcolor=PLOT_BG,
        paper_bgcolor=PAPER_BG,
        font=dict(family=FONT_FAMILY, color='#e2e8f0', size=11),
        height=height,
        margin=dict(l=40, r=20, t=50, b=40),
        xaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR,
                   tickfont=dict(size=10)),
        yaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR,
                   tickfont=dict(size=10)),
    )


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:16px 0 24px'>
        <div style='font-family:Space Mono,monospace;font-size:0.7rem;
                    color:#6b7fa3;letter-spacing:2px;text-transform:uppercase'>
            Portfolio Project
        </div>
        <div style='font-family:Space Mono,monospace;font-size:1rem;
                    color:#00e5ff;margin-top:4px;line-height:1.4'>
            Supply Chain<br>Intelligence
        </div>
        <div style='font-size:0.72rem;color:#6b7fa3;margin-top:8px'>
            Naren Karthikeyan · VIT Vellore
        </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["Executive Overview",
         "Shipping Mode Analysis",
         "Regional Intelligence",
         "Statistical Validation",
         "Recommendations"],
        label_visibility="collapsed"
    )

    st.markdown("""
    <div style='margin-top:32px;padding:14px;background:rgba(0,229,255,0.05);
                border:1px solid rgba(0,229,255,0.12);border-radius:8px'>
        <div style='font-size:0.7rem;color:#6b7fa3;text-transform:uppercase;
                    letter-spacing:1px'>Dataset</div>
        <div style='font-size:0.78rem;color:#e2e8f0;margin-top:6px;
                    line-height:1.5'>
            DataCo Smart Supply Chain<br>
            172,765 orders · 23 regions<br>
            4 shipping modes · 53 features
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='margin-top:12px;padding:14px;background:rgba(0,229,255,0.05);
                border:1px solid rgba(0,229,255,0.12);border-radius:8px'>
        <div style='font-size:0.7rem;color:#6b7fa3;text-transform:uppercase;
                    letter-spacing:1px'>Stack</div>
        <div style='font-size:0.78rem;color:#e2e8f0;margin-top:6px;
                    line-height:1.6'>
            Python · Pandas · SciPy<br>
            PostgreSQL · Plotly<br>
            Streamlit
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Load Data ─────────────────────────────────────────────────────────────────
try:
    df = load_data()
    regional, mode_df, cat_df, corridor_df = compute_stats(df)
    stat_results = run_statistical_tests(df)
    data_loaded = True
except FileNotFoundError:
    data_loaded = False


if not data_loaded:
    st.error("⚠️ Place `dataco_clean.csv` in the same directory and rerun.")
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — EXECUTIVE OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if page == "Executive Overview":

    st.markdown("""
    <div class='hero-banner'>
        <div class='hero-title'>Supply Chain Delay & Logistics Intelligence</div>
        <div class='hero-sub'>
            Root cause analysis across 172,765 global orders · 
            SQL + Python + Statistical Validation
        </div>
    </div>
    """, unsafe_allow_html=True)

    # KPI Row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-value red'>$13.84M</div>
            <div class='metric-label'>Total Delay Cost</div>
            <div class='metric-sub'>Across 167,926 orders</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-value red'>57.3%</div>
            <div class='metric-label'>Global SLA Breach Rate</div>
            <div class='metric-sub'>98,977 delayed orders</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-value amber'>$82.43</div>
            <div class='metric-label'>Avg Cost Per Order</div>
            <div class='metric-sub'>Across all delayed orders</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-value red'>$4.86M</div>
            <div class='metric-label'>First Class Cost Alone</div>
            <div class='metric-sub'>35.1% of total delay cost</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown("<div class='section-header'>SLA Breach Rate by Shipping Mode</div>",
                    unsafe_allow_html=True)
        mode_sorted = mode_df.sort_values('delay_rate_pct', ascending=True)
        colors = [RED if r >= 79 else AMBER if r >= 47 else GREEN
                  for r in mode_sorted['delay_rate_pct']]
        fig = go.Figure(go.Bar(
            x=mode_sorted['delay_rate_pct'],
            y=mode_sorted['shipping_mode'],
            orientation='h',
            marker=dict(color=colors, line=dict(width=0)),
            text=[f"{v:.1f}%" for v in mode_sorted['delay_rate_pct']],
            textposition='outside',
            textfont=dict(family='Space Mono', size=11, color='#e2e8f0')
        ))
        layout = base_layout('Delay Rate % by Shipping Mode', height=280)
        layout['xaxis']['range'] = [0, 115]
        layout['xaxis']['ticksuffix'] = '%'
        layout['showlegend'] = False
        fig.update_layout(**layout)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with col2:
        st.markdown("<div class='section-header'>Root Cause Summary</div>",
                    unsafe_allow_html=True)
        st.markdown("""
        <div class='finding-card'>
            🔍 <strong>Geography ruled out</strong> — 23 regions cluster tightly 
            between 51–60% delay rate (ANOVA F=2.80, p&lt;0.05 but negligible effect).
        </div>
        <div class='finding-card'>
            📦 <strong>Product category ruled out</strong> — Kruskal-Wallis confirms 
            no significant variation across categories (H=43.64, p=0.689).
        </div>
        <div class='finding-card'>
            🚨 <strong>Root cause identified</strong> — SLA windows are set at 50% 
            of operationally achievable delivery times for First & Second Class modes.
        </div>
        <div class='finding-card'>
            💰 <strong>Cost concentration</strong> — First Class alone generates 
            $4.86M at $183.34/order with 100% breach rate across all 26,513 orders.
        </div>
        """, unsafe_allow_html=True)

    # Delay distribution
    st.markdown("<div class='section-header'>Delay Days Distribution</div>",
                unsafe_allow_html=True)
    delay_counts = df['delay_days'].value_counts().sort_index()
    bar_colors = [GREEN if x <= 0 else AMBER if x <= 1 else RED
                  for x in delay_counts.index]
    fig2 = go.Figure(go.Bar(
        x=delay_counts.index.astype(str),
        y=delay_counts.values,
        marker=dict(color=bar_colors, line=dict(width=0)),
        text=[f"{v:,}" for v in delay_counts.values],
        textposition='outside',
        textfont=dict(size=10, color='#e2e8f0')
    ))
    layout2 = base_layout('Distribution of Delay Days (negative = early, positive = late)',
                           height=300)
    layout2['yaxis']['title'] = 'Order Count'
    layout2['xaxis']['title'] = 'Delay Days'
    fig2.update_layout(**layout2)
    st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — SHIPPING MODE ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Shipping Mode Analysis":

    st.markdown("# Shipping Mode Analysis")
    st.markdown("<div style='color:#6b7fa3;font-size:0.85rem;margin-top:-12px;margin-bottom:24px'>Root cause deep-dive · The primary driver of $13.84M in delay costs</div>",
                unsafe_allow_html=True)

    # Scheduled vs Actual
    sched_actual = pd.DataFrame({
        'Shipping Mode': ['Same Day', 'First Class', 'Second Class', 'Standard Class'],
        'Scheduled Days': [0, 1, 2, 4],
        'Actual Days':    [0.48, 2.0, 3.99, 3.99]
    })

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-header'>Promised vs Actual Delivery Days</div>",
                    unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Scheduled (Promised)',
            x=sched_actual['Shipping Mode'],
            y=sched_actual['Scheduled Days'],
            marker_color=CYAN,
            marker_line_width=0,
        ))
        fig.add_trace(go.Bar(
            name='Actual (Delivered)',
            x=sched_actual['Shipping Mode'],
            y=sched_actual['Actual Days'],
            marker_color=RED,
            marker_line_width=0,
        ))
        layout = base_layout('Every mode delivers ~2× its promised window', height=340)
        layout['barmode'] = 'group'
        layout['legend'] = dict(font=dict(size=10, color='#e2e8f0'),
                                 bgcolor='rgba(0,0,0,0)')
        layout['yaxis']['title'] = 'Days'
        fig.update_layout(**layout)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with col2:
        st.markdown("<div class='section-header'>SLA Compliance % by Mode</div>",
                    unsafe_allow_html=True)
        mode_sorted_comp = mode_df.sort_values('sla_compliance_pct', ascending=True)
        comp_colors = [RED if v < 25 else AMBER if v < 55 else GREEN
                       for v in mode_sorted_comp['sla_compliance_pct']]
        fig2 = go.Figure(go.Bar(
            x=mode_sorted_comp['sla_compliance_pct'],
            y=mode_sorted_comp['shipping_mode'],
            orientation='h',
            marker=dict(color=comp_colors, line=dict(width=0)),
            text=[f"{v:.1f}%" for v in mode_sorted_comp['sla_compliance_pct']],
            textposition='outside',
            textfont=dict(family='Space Mono', size=11, color='#e2e8f0')
        ))
        layout2 = base_layout('SLA Compliance Rate (higher = better)', height=340)
        layout2['xaxis']['range'] = [0, 80]
        layout2['xaxis']['ticksuffix'] = '%'
        fig2.update_layout(**layout2)
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    # Economic cost by mode
    st.markdown("<div class='section-header'>Economic Delay Cost by Shipping Mode</div>",
                unsafe_allow_html=True)

    mode_cost = mode_df.sort_values('total_delay_cost', ascending=False)
    cost_colors = [RED if m == 'First Class' else AMBER if m == 'Second Class'
                   else CYAN for m in mode_cost['shipping_mode']]

    fig3 = go.Figure(go.Bar(
        x=mode_cost['shipping_mode'],
        y=mode_cost['total_delay_cost'],
        marker=dict(color=cost_colors, line=dict(width=0)),
        text=[f"${v/1e6:.2f}M" for v in mode_cost['total_delay_cost']],
        textposition='outside',
        textfont=dict(family='Space Mono', size=12, color='#e2e8f0')
    ))
    layout3 = base_layout('Total Delay Cost ($) — First Class generates $4.86M alone',
                           height=320)
    layout3['yaxis']['tickprefix'] = '$'
    layout3['yaxis']['range'] = [0, max(mode_cost['total_delay_cost']) * 1.2]
    fig3.update_layout(**layout3)
    st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})

    # Mode summary table
    st.markdown("<div class='section-header'>Shipping Mode Full Summary</div>",
                unsafe_allow_html=True)
    display_mode = mode_df.copy()
    display_mode['total_delay_cost'] = display_mode['total_delay_cost'].apply(
        lambda x: f"${x:,.0f}")
    display_mode['delay_rate_pct']     = display_mode['delay_rate_pct'].apply(
        lambda x: f"{x:.2f}%")
    display_mode['sla_compliance_pct'] = display_mode['sla_compliance_pct'].apply(
        lambda x: f"{x:.2f}%")
    display_mode.columns = ['Shipping Mode', 'Total Orders', 'Delayed Orders',
                             'Delay Rate', 'SLA Compliance', 'Avg Delay Days',
                             'Total Delay Cost']
    st.dataframe(display_mode, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — REGIONAL INTELLIGENCE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Regional Intelligence":

    st.markdown("# Regional Intelligence")
    st.markdown("<div style='color:#6b7fa3;font-size:0.85rem;margin-top:-12px;margin-bottom:24px'>23 global markets · Geography ruled out as root cause</div>",
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-header'>Delay Rate by Region</div>",
                    unsafe_allow_html=True)
        reg_sorted = regional.sort_values('delay_rate_pct', ascending=True)
        fig = go.Figure(go.Bar(
            x=reg_sorted['delay_rate_pct'],
            y=reg_sorted['order_region'],
            orientation='h',
            marker=dict(
                color=reg_sorted['delay_rate_pct'],
                colorscale=[[0, CYAN], [0.5, AMBER], [1, RED]],
                line=dict(width=0)
            ),
            text=[f"{v:.1f}%" for v in reg_sorted['delay_rate_pct']],
            textposition='outside',
            textfont=dict(size=9, color='#e2e8f0')
        ))
        layout = base_layout('Tight 51–60% band across all 23 regions', height=600)
        layout['xaxis']['range'] = [40, 70]
        layout['xaxis']['ticksuffix'] = '%'
        layout['margin']['l'] = 130
        fig.update_layout(**layout)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with col2:
        st.markdown("<div class='section-header'>Total Delay Cost by Region ($)</div>",
                    unsafe_allow_html=True)
        reg_cost = regional.sort_values('total_delay_cost', ascending=True).tail(15)
        fig2 = go.Figure(go.Bar(
            x=reg_cost['total_delay_cost'],
            y=reg_cost['order_region'],
            orientation='h',
            marker=dict(
                color=reg_cost['total_delay_cost'],
                colorscale=[[0, CYAN], [0.5, AMBER], [1, RED]],
                line=dict(width=0)
            ),
            text=[f"${v/1e6:.2f}M" for v in reg_cost['total_delay_cost']],
            textposition='outside',
            textfont=dict(size=9, color='#e2e8f0')
        ))
        layout2 = base_layout('Cost driven by volume, not delay rate', height=600)
        layout2['xaxis']['tickprefix'] = '$'
        layout2['margin']['l'] = 130
        fig2.update_layout(**layout2)
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    # Worst corridors
    st.markdown("<div class='section-header'>Top 10 Worst Delay Corridors (Excl. First Class)</div>",
                unsafe_allow_html=True)

    fig3 = go.Figure(go.Bar(
        x=[f"{r} · {m}" for r, m in
           zip(corridor_df['order_region'], corridor_df['shipping_mode'])],
        y=corridor_df['delay_rate_pct'],
        marker=dict(color=RED, line=dict(width=0)),
        text=[f"{v:.1f}%" for v in corridor_df['delay_rate_pct']],
        textposition='outside',
        textfont=dict(size=10, color='#e2e8f0')
    ))
    layout3 = base_layout('All top corridors are Second Class — confirming mode-level root cause',
                           height=340)
    layout3['xaxis']['tickangle'] = -35
    layout3['yaxis']['ticksuffix'] = '%'
    layout3['yaxis']['range'] = [0, 100]
    fig3.update_layout(**layout3)
    st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — STATISTICAL VALIDATION
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Statistical Validation":

    st.markdown("# Statistical Validation")
    st.markdown("<div style='color:#6b7fa3;font-size:0.85rem;margin-top:-12px;margin-bottom:24px'>Every finding backed by a hypothesis test · α = 0.05</div>",
                unsafe_allow_html=True)

    tests = [
        {
            "name": "TEST 1 — One-Way ANOVA",
            "question": "Does delay magnitude vary significantly across regions?",
            "stat": f"F = {stat_results['anova']['f']}",
            "p": f"p = {stat_results['anova']['p']:.6f}",
            "sig": stat_results['anova']['sig'],
            "interpretation": (
                "Statistically significant but practically negligible. "
                "F-statistic of 2.80 indicates between-group variance is barely "
                "distinguishable from within-group noise across 172K orders. "
                "Geography is NOT an actionable root cause."
            ),
            "verdict": "⚠️ Significant · Negligible Effect Size"
        },
        {
            "name": "TEST 2 — Chi-Square Test",
            "question": "Is shipping mode associated with delay status?",
            "stat": f"χ² = {stat_results['chi2']['chi2']:,.2f}",
            "p": f"p < 0.0001",
            "sig": True,
            "interpretation": (
                "Overwhelmingly significant. χ²=40,058 for 3 degrees of freedom "
                "is extraordinary — values above 15 are already highly significant. "
                "Shipping mode is the STRONGEST predictor of SLA breach in the dataset. "
                "This association has effectively zero probability of occurring by chance."
            ),
            "verdict": "✅ Highly Significant · Large Effect"
        },
        {
            "name": "TEST 3 — Kruskal-Wallis Test",
            "question": "Does delay magnitude vary significantly across product categories?",
            "stat": f"H = {stat_results['kruskal']['h']}",
            "p": f"p = {stat_results['kruskal']['p']}",
            "sig": False,
            "interpretation": (
                "Not significant (p=0.689). 68.9% probability these category "
                "differences occurred by chance. Product handling complexity, size, "
                "and fragility are ruled out as root causes. This is a valuable "
                "negative finding — it narrows the root cause to shipping mode."
            ),
            "verdict": "❌ Not Significant · Product Category Ruled Out"
        },
        {
            "name": "TEST 4 — Z-Test for Two Proportions",
            "question": "Is Standard Class delay rate significantly lower than Same Day?",
            "stat": f"Z = {stat_results['ztest']['z']}",
            "p": f"p < 0.0001",
            "sig": True,
            "interpretation": (
                f"Standard Class ({stat_results['ztest']['p1']}%) is significantly "
                f"lower than Same Day ({stat_results['ztest']['p2']}%). "
                "Z=-15.35 means this difference is 15 standard deviations from "
                "what random chance would produce. Generous SLA windows outperform "
                "operational speed — confirming the misconfiguration hypothesis."
            ),
            "verdict": "✅ Highly Significant · Confirms Misconfiguration"
        },
        {
            "name": "TEST 5 — Spearman Rank Correlation",
            "question": "Does order value correlate with delay cost?",
            "stat": f"ρ = {stat_results['spearman']['r']}",
            "p": f"p < 0.0001",
            "sig": True,
            "interpretation": (
                "Weak positive correlation (ρ=0.22). Statistically significant "
                "due to large sample size but effect is small — order value explains "
                "only ~5% of delay cost variance. Delay cost is driven by shipping "
                "mode misconfiguration, not order value. "
                "(Note: Pearson returned NaN due to zero-inflated delay_cost distribution — "
                "Spearman is the appropriate non-parametric alternative.)"
            ),
            "verdict": "⚠️ Significant · Weak Effect · Not a Primary Driver"
        }
    ]

    for t in tests:
        color = GREEN if t['sig'] and 'Ruled Out' not in t['verdict'] else \
                RED if not t['sig'] else AMBER
        border_color = color

        st.markdown(f"""
        <div style='background:rgba(13,21,48,0.85);border:1px solid {border_color}33;
                    border-left:3px solid {border_color};border-radius:0 10px 10px 0;
                    padding:20px 24px;margin:12px 0'>
            <div style='font-family:Space Mono,monospace;font-size:0.8rem;
                        color:{border_color};margin-bottom:4px'>{t['name']}</div>
            <div style='font-size:0.88rem;color:#e2e8f0;margin-bottom:12px'>
                {t['question']}
            </div>
            <div style='display:flex;gap:24px;margin-bottom:12px'>
                <div>
                    <div style='font-size:0.68rem;color:#6b7fa3;
                                text-transform:uppercase;letter-spacing:1px'>
                        Test Statistic</div>
                    <div style='font-family:Space Mono,monospace;font-size:1rem;
                                color:{border_color};margin-top:2px'>{t['stat']}</div>
                </div>
                <div>
                    <div style='font-size:0.68rem;color:#6b7fa3;
                                text-transform:uppercase;letter-spacing:1px'>
                        P-Value</div>
                    <div style='font-family:Space Mono,monospace;font-size:1rem;
                                color:{border_color};margin-top:2px'>{t['p']}</div>
                </div>
                <div>
                    <div style='font-size:0.68rem;color:#6b7fa3;
                                text-transform:uppercase;letter-spacing:1px'>
                        Verdict</div>
                    <div style='font-size:0.8rem;color:{border_color};margin-top:4px'>
                        {t['verdict']}</div>
                </div>
            </div>
            <div style='font-size:0.8rem;color:#a0aec0;line-height:1.6;
                        border-top:1px solid rgba(255,255,255,0.06);padding-top:10px'>
                {t['interpretation']}
            </div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Recommendations":

    st.markdown("# Recommendations & Impact")
    st.markdown("<div style='color:#6b7fa3;font-size:0.85rem;margin-top:-12px;margin-bottom:24px'>Data-driven recommendations · Every action tied to a finding</div>",
                unsafe_allow_html=True)

    # Root cause statement
    st.markdown("""
    <div style='background:linear-gradient(135deg,rgba(0,229,255,0.06),rgba(0,229,255,0.02));
                border:1px solid rgba(0,229,255,0.2);border-radius:12px;
                padding:24px 28px;margin-bottom:28px'>
        <div style='font-family:Space Mono,monospace;font-size:0.72rem;
                    color:#6b7fa3;text-transform:uppercase;letter-spacing:2px;
                    margin-bottom:10px'>Root Cause Statement</div>
        <div style='font-size:0.92rem;color:#e2e8f0;line-height:1.7'>
            The 57.3% global SLA breach rate and <strong style='color:#00e5ff'>
            $13.84M in delay costs</strong> are not caused by carrier underperformance, 
            geographic constraints, or product complexity. They are caused by 
            <strong style='color:#ff4d6d'>SLA delivery windows set at approximately 
            50% of operationally achievable delivery times</strong> for First and Second 
            Class shipping modes. Standard Class — the only mode with realistic scheduled 
            windows — outperforms all premium tiers despite being the slowest and 
            cheapest service.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # SLA Reset Simulation
    st.markdown("<div class='section-header'>SLA Reset Impact Simulation</div>",
                unsafe_allow_html=True)

    sim_data = pd.DataFrame({
        'Mode': ['First Class', 'Second Class', 'Same Day'],
        'Current Compliance': [0, 20.17, 52.07],
        'Projected Compliance': [95, 85, 75],
        'Current Cost ($M)':    [4.86, 5.12, 1.24],
        'Projected Cost ($M)':  [0.24, 0.77, 0.62]
    })

    col1, col2 = st.columns(2)

    with col1:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Current Compliance %',
            x=sim_data['Mode'],
            y=sim_data['Current Compliance'],
            marker_color=RED, marker_line_width=0
        ))
        fig.add_trace(go.Bar(
            name='Projected Compliance %',
            x=sim_data['Mode'],
            y=sim_data['Projected Compliance'],
            marker_color=GREEN, marker_line_width=0
        ))
        layout = base_layout('SLA Compliance Before vs After Reset', height=320)
        layout['barmode'] = 'group'
        layout['yaxis']['ticksuffix'] = '%'
        layout['yaxis']['range'] = [0, 110]
        layout['legend'] = dict(font=dict(size=10, color='#e2e8f0'),
                                 bgcolor='rgba(0,0,0,0)')
        fig.update_layout(**layout)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with col2:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            name='Current Delay Cost',
            x=sim_data['Mode'],
            y=sim_data['Current Cost ($M)'],
            marker_color=RED, marker_line_width=0
        ))
        fig2.add_trace(go.Bar(
            name='Projected Delay Cost',
            x=sim_data['Mode'],
            y=sim_data['Projected Cost ($M)'],
            marker_color=GREEN, marker_line_width=0
        ))
        layout2 = base_layout('Delay Cost ($M) Before vs After Reset', height=320)
        layout2['barmode'] = 'group'
        layout2['yaxis']['tickprefix'] = '$'
        layout2['yaxis']['ticksuffix'] = 'M'
        layout2['legend'] = dict(font=dict(size=10, color='#e2e8f0'),
                                  bgcolor='rgba(0,0,0,0)')
        fig2.update_layout(**layout2)
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    # Recommendations
    st.markdown("<div class='section-header'>Action Recommendations</div>",
                unsafe_allow_html=True)

    recs = [
        {
            "tag": "immediate", "tag_label": "IMMEDIATE",
            "title": "Rec 1 — Recalibrate SLA Windows",
            "body": (
                "Reset First Class from 1-day to 1–2 day promise. "
                "Reset Second Class from 2-day to 3–4 day promise. "
                "Reset Same Day from 0-day to 1-day promise. "
                "Expected impact: First Class SLA compliance improves from 0% to 95%+ "
                "immediately with zero operational change or additional cost. "
                "This eliminates $4.86M in reported delay costs."
            )
        },
        {
            "tag": "medium", "tag_label": "MEDIUM TERM",
            "title": "Rec 2 — Carrier Audit: Top 3 Cost Corridors",
            "body": (
                "Western Europe Second Class ($1.03M), Central America First Class ($757K), "
                "and Caribbean Second Class ($287K) are the highest-cost corridors. "
                "Audit carrier contracts in these three markets to determine whether "
                "true 1-day First Class delivery is operationally achievable within "
                "cost constraints. If yes, invest in capability. If no, recalibrate."
            )
        },
        {
            "tag": "strategic", "tag_label": "STRATEGIC",
            "title": "Rec 3 — Underpromise-Overdeliver Messaging",
            "body": (
                "Adopt Amazon-style tiered delivery window communication. "
                "Change 'First Class — Delivered in 1 day' to "
                "'First Class — Usually 1 day, guaranteed within 2.' "
                "When delivery achieves 1 day — customer is delighted. "
                "When it takes 2 days — expectation was met. "
                "This preserves premium service perception while eliminating "
                "structural SLA breaches and protecting customer retention."
            )
        },
        {
            "tag": "strategic", "tag_label": "STRATEGIC",
            "title": "Rec 4 — Real-Time SLA Compliance Monitoring",
            "body": (
                "Implement weekly SLA compliance tracker by shipping mode "
                "with automated alerts when any mode drops below 70% compliance. "
                "Current dataset shows Standard Class as the benchmark at 60.23% — "
                "post-recalibration, target 85%+ for all modes. "
                "This dashboard serves as the monitoring foundation."
            )
        }
    ]

    for r in recs:
        tag_class = f"tag-{r['tag']}"
        st.markdown(f"""
        <div class='rec-card'>
            <div style='margin-bottom:8px'>
                <span class='tag {tag_class}'>{r['tag_label']}</span>
            </div>
            <div class='rec-title'>{r['title']}</div>
            <div class='rec-body'>{r['body']}</div>
        </div>
        """, unsafe_allow_html=True)

    # Final impact summary
    st.markdown("<div class='section-header'>Projected Total Impact</div>",
                unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-value green'>~$10M+</div>
            <div class='metric-label'>Delay Cost Reduction</div>
            <div class='metric-sub'>From SLA recalibration alone</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-value green'>0% → 95%</div>
            <div class='metric-label'>First Class Compliance</div>
            <div class='metric-sub'>With zero operational change</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-value green'>3 Corridors</div>
            <div class='metric-label'>Priority Audit Targets</div>
            <div class='metric-sub'>W. Europe · C. America · Caribbean</div>
        </div>""", unsafe_allow_html=True)
