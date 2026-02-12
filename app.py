import math
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="MIVE Automation Value Engine",
    page_icon="✨",
    layout="wide"
)

# ======================================================
# BEAUTIFUL UI CSS
# ======================================================
st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif !important;
}

.big-score {
    border-radius: 15px;
    padding: 25px;
    background-color: #ffffff;
    text-align: center;
    border: 3px solid #4A90E2;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.12);
}

.big-number {
    font-size: 60px;
    font-weight: 900;
    color: #4A90E2;
}

.score-label {
    font-size: 20px;
    opacity: 0.75;
}

.section {
    background-color: #F7F9FC;
    padding: 16px;
    border-radius: 10px;
    border-left: 5px solid #4A90E2;
}

.metric-box {
    padding: 18px;
    border-radius: 10px;
    background-color: #ffffff;
    border: 2px solid #EBEBEB;
}

h1, h2, h3 {
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# HELPER FUNCTIONS
# ======================================================
def hours_saved_per_year(t_before_h, rework_pct, freq_week, t_after_h):
    before = (t_before_h * (1 + rework_pct)) * freq_week * 52
    after = (t_after_h * freq_week * 52)
    return max(before - after, 0), before, after

def clamp01(x):
    return max(0.0, min(1.0, float(x)))

# ======================================================
# TITLE + FORMULA
# ======================================================
st.title("✨ Mindware Intelligence Value Engine (MIVE)")
st.caption("Advanced automation scoring — Impact, Usage, Teams, Business, Quality, Future Growth.")

with st.expander("📘 **Click to view MIVE Formula**"):
    st.markdown(r"""
## 🔹 1. Impact Now – 40%

**Hours Saved Per Year**
$$
HoursSaved = (TimeBefore - TimeAfter) \times Frequency \times 52
$$

**Impact Score**
$$
Impact = \frac{HoursSaved}{2000}
$$

---

## 🔹 2. Usage & Reach – 20%
$$
UsageReach = 0.5 \times \frac{UsesPerWeek}{20} + 
0.5 \times \frac{Teams}{5}
$$

---

## 🔹 3. Business Strength – 15%
$$
Business = \frac{BusinessScore}{5}
$$

---

## 🔹 4. Quality & Risk – 10%
$$
Q\&R = \frac{Quality + (6 - Risk)}{10}
$$

---

## 🔹 5. Future Growth Factor – 15%
$$
FutureGrowth = 
\frac{
0.4 \cdot GrowthUsage +
0.3 \cdot Reusability +
0.3 \cdot NetworkEffect
}{5}
$$

---

# ⭐ Final MIVE Formula
$$
\textbf{MIVE} = 
0.40I +
0.20U +
0.15B +
0.10Q +
0.15F
$$
""")

# ======================================================
# INPUT SECTIONS
# ======================================================
col1, col2, col3 = st.columns(3)

# ---- COL 1: TIMING ----
with col1:
    st.markdown("### ⏱️ Process Timing")
    st.markdown('<div class="section">', unsafe_allow_html=True)

    unit = st.radio("Time unit", ["minutes", "hours"])
    t_before = st.number_input("Time BEFORE per occurrence", value=15.0, min_value=0.0)
    t_after = st.number_input("Time AFTER per occurrence", value=1.0, min_value=0.0)
    rework_pct = st.number_input("Rework %", value=5.0, min_value=0.0, max_value=100.0) / 100
    freq_week = st.number_input("Frequency per week", value=10.0, min_value=0.0)

    st.markdown('</div>', unsafe_allow_html=True)

# ---- COL 2: BUSINESS ----
with col2:
    st.markdown("### 🏢 Business & Quality")
    st.markdown('<div class="section">', unsafe_allow_html=True)

    business_score = st.slider("Business Value (1–5)", 1, 5, 4)
    quality_score = st.slider("Quality Improvement (1–5)", 1, 5, 4)
    risk_score = st.slider("Risk Level (1–5, lower = safer)", 1, 5, 2)
    human_score = st.slider("Human Benefit (1–5)", 1, 5, 4)

    st.markdown('</div>', unsafe_allow_html=True)

# ---- COL 3: USAGE + FUTURE ----
with col3:
    st.markdown("### 👥 Usage, Teams & Future Growth")
    st.markdown('<div class="section">', unsafe_allow_html=True)

    uses_per_week = st.number_input("Times used per week", value=10.0, min_value=0.0)
    teams_count = st.number_input("Teams using this automation", value=2, min_value=1)

    growth_usage = st.slider("Expected usage growth next year (1–5)", 1, 5, 3)
    reusability = st.slider("Reusability for future automations (1–5)", 1, 5, 3)
    network_effect = st.slider("Network effect / intelligence scaling (1–5)", 1, 5, 3)

    st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# CALCULATE
# ======================================================
if unit == "minutes":
    t_before_h = t_before / 60
    t_after_h = t_after / 60
else:
    t_before_h = t_before
    t_after_h = t_after

saved_yr, before_yr, after_yr = hours_saved_per_year(
    t_before_h, rework_pct, freq_week, t_after_h
)

impact_now = clamp01(saved_yr / 2000)
usage_reach = clamp01(0.5 * (uses_per_week / 20) + 0.5 * (teams_count / 5))
business_strength = business_score / 5
quality_risk = clamp01((quality_score + (6 - risk_score)) / 10)
future_growth = clamp01((0.4 * growth_usage + 0.3 * reusability + 0.3 * network_effect) / 5)

mive_score = (
    0.40 * impact_now +
    0.20 * usage_reach +
    0.15 * business_strength +
    0.10 * quality_risk +
    0.15 * future_growth
) * 100

# ======================================================
# OUTPUT
# ======================================================
st.markdown("---")
st.subheader("📊 Results")

c1, c2, c3 = st.columns([1.1, 1, 1])

with c1:
    st.markdown('<div class="big-score">', unsafe_allow_html=True)
    st.markdown(f"<div class='big-number'>{mive_score:.1f}</div>", unsafe_allow_html=True)
    st.markdown("<div class='score-label'>Final MIVE Score</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown('<div class="metric-box">', unsafe_allow_html=True)
    st.write("### ⏱️ Time Metrics")
    st.metric("Before (h/yr)", f"{before_yr:,.1f}")
    st.metric("After (h/yr)", f"{after_yr:,.1f}")
    st.metric("Saved (h/yr)", f"{saved_yr:,.1f}")
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="metric-box">', unsafe_allow_html=True)
    st.write("### 🧩 Component Scores")
    st.write(f"Impact: **{impact_now:.2f}**")
    st.write(f"Usage & Reach: **{usage_reach:.2f}**")
    st.write(f"Business Strength: **{business_strength:.2f}**")
    st.write(f"Quality & Risk: **{quality_risk:.2f}**")
    st.write(f"Future Growth: **{future_growth:.2f}**")
    st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# RADAR CHART
# ======================================================
st.markdown("---")
st.write("### 🕸️ Component Radar Chart")

categories = ["Impact", "Usage", "Business", "Quality", "Growth"]
values = [impact_now, usage_reach, business_strength, quality_risk, future_growth]
values.append(values[0])

angles = [n / float(len(categories)) * 2 * math.pi for n in range(len(categories))]
angles.append(angles[0])

fig = plt.figure(figsize=(6, 5))
ax = fig.add_subplot(111, polar=True)
plt.xticks(angles[:-1], categories)
ax.plot(angles, values, color="#4A90E2", linewidth=2)
ax.fill(angles, values, color="#4A90E2", alpha=0.3)
ax.set_ylim(0, 1)
st.pyplot(fig)