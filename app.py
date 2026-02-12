import math
import streamlit as st
import matplotlib.pyplot as plt

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="MIVE+Dev Automation Value Engine",
    page_icon="✨",
    layout="wide"
)

# ======================================================
# CSS (fixed real <style>)
# ======================================================
st.markdown("""
<style>
html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif !important; }

.big-score {
  border-radius: 15px; padding: 25px; background-color: #ffffff;
  text-align: center; border: 3px solid #4A90E2;
  box-shadow: 0 4px 12px rgba(0,0,0,0.12);
}
.big-number { font-size: 60px; font-weight: 900; color: #4A90E2; }
.score-label { font-size: 20px; opacity: 0.75; }

.section {
  background-color: #F7F9FC; padding: 16px; border-radius: 10px;
  border-left: 5px solid #4A90E2;
}
.metric-box {
  padding: 18px; border-radius: 10px; background-color: #ffffff;
  border: 2px solid #EBEBEB;
}
h1, h2, h3 { font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ======================================================
# HELPERS
# ======================================================
def hours_saved_per_year(t_before_h, rework_pct, freq_week, t_after_h):
    before = (t_before_h * (1 + rework_pct)) * freq_week * 52
    after  = (t_after_h  * freq_week * 52)
    return max(before - after, 0), before, after

def clamp01(x): return max(0.0, min(1.0, float(x)))


# ======================================================
# TITLE
# ======================================================
st.title("✨ MIVE+Dev — Mindware Automation Value Engine")
st.caption("Impact • Usage • Business • Quality • Growth • Development Effort")


# ======================================================
# FORMULA (Professional + Simple)
# ======================================================
with st.expander("📘 Formula (simple & clean)"):
    st.markdown(r"""
### **Development Effort NOW included in the score**

---

### **Impact (I) — 35%**
$$
I = \min\left(1,\ \frac{HoursSaved}{2000}\right)
$$
$$
HoursSaved = (t_{before}(1+r)-t_{after}) \times F \times 52
$$

---

### **Usage & Reach (U) — 18%**
$$
U = 0.5\frac{Uses/week}{20} + 0.5\frac{Teams}{5}
$$

---

### **Business (B) — 14%**
$$
B = \frac{BusinessScore}{5}
$$

---

### **Quality & Risk (Q) — 10%**
$$
Q = \min\!\left(1,\ \frac{Quality + (6 - Risk)}{10}\right)
$$

---

### **Future Growth (F) — 13%**
$$
F = clamp\left(\frac{0.4G + 0.3R + 0.3N}{5},\ 0,\ 1\right)
$$

---

### **Development Effort (D) — 10%**
Lower effort = higher score  
$$
D = \max\left(0,\ 1 - \frac{DevHours}{200}\right)
$$

---

### ⭐ **FINAL SCORE**
$$
\textbf{MIVE+Dev} = 100\left(
0.35I + 0.18U + 0.14B + 0.10Q + 0.13F + 0.10D
\right)
$$
""")


# ======================================================
# INPUTS
# ======================================================
col1, col2, col3 = st.columns(3)

# ---- TIMING ----
with col1:
    st.markdown("### ⏱️ Process Timing")
    st.markdown('<div class="section">', unsafe_allow_html=True)

    unit = st.radio("Time unit", ["minutes", "hours"], horizontal=True)
    t_before = st.number_input("Time BEFORE per occurrence", value=15.0)
    t_after  = st.number_input("Time AFTER per occurrence",  value=1.0)
    rework_pct = st.number_input("Rework %", value=5.0) / 100.0
    freq_week  = st.number_input("Frequency per week", value=10.0)

    # DEVELOPMENT EFFORT (NOW INCLUDED)
    dev_hours = st.number_input("Development Effort (hours)", value=60.0, step=5.0)

    st.markdown('</div>', unsafe_allow_html=True)

# ---- BUSINESS ----
with col2:
    st.markdown("### 🏢 Business & Quality")
    st.markdown('<div class="section">', unsafe_allow_html=True)

    business_score = st.slider("Business Value (1–5)", 1, 5, 4)
    quality_score  = st.slider("Quality Improvement (1–5)", 1, 5, 4)
    risk_score     = st.slider("Risk Level (1–5, lower=safe)", 1, 5, 2)

    st.markdown('</div>', unsafe_allow_html=True)

# ---- USAGE & FUTURE ----
with col3:
    st.markdown("### 👥 Usage & Future Growth")
    st.markdown('<div class="section">', unsafe_allow_html=True)

    uses_per_week  = st.number_input("Times used per week", value=10.0)
    teams_count    = st.number_input("Teams using it", value=2)

    growth_usage   = st.slider("Usage Growth (1–5)", 1, 5, 3)
    reusability    = st.slider("Reusability (1–5)", 1, 5, 3)
    network_effect = st.slider("Network effect (1–5)", 1, 5, 3)

    st.markdown('</div>', unsafe_allow_html=True)


# ======================================================
# CALCULATION
# ======================================================
# Convert minutes → hours
if unit == "minutes":
    t_before_h = t_before / 60.0
    t_after_h  = t_after / 60.0
else:
    t_before_h = t_before
    t_after_h  = t_after

saved_yr, before_yr, after_yr = hours_saved_per_year(
    t_before_h, rework_pct, freq_week, t_after_h
)

# Components
I = clamp01(saved_yr / 2000.0)
U = clamp01(0.5 * (uses_per_week / 20.0) + 0.5 * (teams_count / 5.0))
B = business_score / 5.0
Q = clamp01((quality_score + (6 - risk_score)) / 10.0)
F = clamp01((0.4 * growth_usage + 0.3 * reusability + 0.3 * network_effect) / 5.0)

# DEVELOPMENT EFFORT SCORE (included in formula)
D = max(0, 1 - dev_hours / 200.0)

# Final weighted score
final_score = 100 * (0.35*I + 0.18*U + 0.14*B + 0.10*Q + 0.13*F + 0.10*D)


# ======================================================
# OUTPUT
# ======================================================
st.markdown("---")
st.subheader("📊 Results")

c1, c2, c3 = st.columns([1.1, 1, 1])

with c1:
    st.markdown('<div class="big-score">', unsafe_allow_html=True)
    st.markdown(f"<div class='big-number'>{final_score:.1f}</div>", unsafe_allow_html=True)
    st.markdown("<div class='score-label'>Final MIVE+Dev Score</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown('<div class="metric-box">', unsafe_allow_html=True)
    st.write("### ⏱️ Time Metrics")
    st.metric("Before (h/year)", f"{before_yr:,.1f}")
    st.metric("After (h/year)",  f"{after_yr:,.1f}")
    st.metric("Saved (h/year)",  f"{saved_yr:,.1f}")
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="metric-box">', unsafe_allow_html=True)
    st.write("### ⚙️ Effort & Components")
    st.metric("Dev Effort (hours)", f"{dev_hours:,.0f}")
    st.metric("Dev Effort (days ≈ h/8)", f"{dev_hours/8:,.1f}")
    st.metric("Delivery Score (D)", f"{D:.2f}")
    st.write(f"Impact (I): **{I:.2f}**")
    st.write(f"Usage (U): **{U:.2f}**")
    st.write(f"Business (B): **{B:.2f}**")
    st.write(f"Quality (Q): **{Q:.2f}**")
    st.write(f"Growth (F): **{F:.2f}**")
    st.markdown('</div>', unsafe_allow_html=True)


# ======================================================
# RADAR (value only — best practice)
# ======================================================
st.markdown("---")
st.write("### 🕸️ Value Radar Chart")

categories = ["Impact", "Usage", "Business", "Quality", "Growth"]
values = [I, U, B, Q, F, I]  # close loop

angles = [n / float(len(categories)) * 2 * math.pi for n in range(len(categories))]
angles.append(angles[0])

fig = plt.figure(figsize=(6, 5))
ax = fig.add_subplot(111, polar=True)
plt.xticks(angles[:-1], categories)
ax.plot(angles, values, color="#4A90E2", linewidth=2)
ax.fill(angles, values, color="#4A90E2", alpha=0.3)
ax.set_ylim(0,1)
st.pyplot(fig)