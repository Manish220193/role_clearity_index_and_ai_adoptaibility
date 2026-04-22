import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# Load data
df = pd.read_csv("rci_data.csv")
df.columns = df.columns.str.strip()

df.columns = [
    "Employee",
    "Q1","Q2","Q3","Q4","Q5","Q6","Q7","Q8","Q9","Q10",
    "AI1","AI2","AI3","AI4","AI5",
    "Department","Team","Manager","Role_Level","Tenure"
]

# RCI Calculation
df["Expectation_Clarity"] = df[["Q1","Q2","Q6"]].mean(axis=1)
df["Authority_Clarity"] = df[["Q3","Q4"]].mean(axis=1)
df["Manager_Effectiveness"] = df[["Q5","Q9"]].mean(axis=1)
df["Execution_Clarity"] = df[["Q7","Q8"]].mean(axis=1)
df["Cross_Function"] = df[["Q10"]].mean(axis=1)

df["RCI"] = df[
    ["Expectation_Clarity","Authority_Clarity","Manager_Effectiveness","Execution_Clarity","Cross_Function"]
].mean(axis=1)

# AI Calculation
df["AI_Clarity"] = df["AI1"]
df["AI_Usage"] = df["AI2"]
df["AI_Capability"] = df["AI3"]
df["AI_Support"] = df["AI4"]
df["AI_Risk"] = df["AI5"]

df["AI_Adaptability"] = df[
    ["AI_Clarity","AI_Usage","AI_Capability","AI_Support"]
].mean(axis=1)

# Classification
def classify_score(score):
    if score >= 4.2:
        return "Excellent"
    elif score >= 3.5:
        return "Good"
    elif score >= 2.8:
        return "Risk"
    else:
        return "Critical"

# Insight
def combined_insight(rci, ai):
    if rci >= 3.5 and ai >= 3.5:
        return "Ready for AI Implementation"
    elif rci >= 3.5 and ai < 3.5:
        return "Needs AI Training"
    elif rci < 3.5 and ai >= 3.5:
        return "Needs Role Clarity"
    else:
        return "Needs Role + AI Intervention"

# Department Summary
dept_summary = df.groupby("Department").agg({
    "RCI": "mean",
    "AI_Adaptability": "mean",
    "Employee": "count"
}).reset_index().rename(columns={"Employee": "Headcount"})

def root_cause_analysis(df_subset):
    components = {
        "Expectation Clarity": df_subset["Expectation_Clarity"].mean(),
        "Authority Clarity": df_subset["Authority_Clarity"].mean(),
        "Manager Effectiveness": df_subset["Manager_Effectiveness"].mean(),
        "Execution Clarity": df_subset["Execution_Clarity"].mean(),
        "Cross Function": df_subset["Cross_Function"].mean(),
        "AI Usage": df_subset["AI_Usage"].mean(),
        "AI Capability": df_subset["AI_Capability"].mean(),
        "AI Support": df_subset["AI_Support"].mean(),
        "AI Clarity": df_subset["AI_Clarity"].mean()
    }

    # Sort lowest scores first
    sorted_issues = sorted(components.items(), key=lambda x: x[1])

    problem_issues = [
        (k, v) for k, v in sorted_issues
        if classify_score(v) in ["Critical", "Risk"]
]

    return problem_issues  
# top 3 problems
# UI
st.title("🤖 RCI & AI Dashboard")

st.write("""
RCI (Role Clarity Index) helps assess clarity in roles, expectations, and execution.  
AI Adaptability shows how ready teams are for the future of work.
""")

# =========================
# KNOWLEDGE TABS (IMPORTANT)
# =========================

with st.expander("📘 What is RCI (Role Clarity Index)?"):
    st.write("""
RCI measures how clearly employees understand their roles, responsibilities, and expectations.

A higher RCI means:
- Better productivity
- Clear ownership
- Faster execution

A lower RCI indicates:
- Confusion in roles
- Dependency on managers
- Execution delays
""")

with st.expander("🤖 What is AI Adaptability?"):
    st.write("""
AI Adaptability measures how ready employees are to use AI tools in their work.

We evaluate:
- AI Clarity → Do employees understand AI?
- AI Usage → Are they using AI tools?
- AI Capability → Do they have skills?
- AI Support → Do they get support/resources?

Higher score = Future-ready workforce
""")

with st.expander("🧠 Our Hypothesis"):
    st.write("""
We believe:

1. High RCI + High AI → High-performing, future-ready teams  
2. High RCI + Low AI → Need AI training  
3. Low RCI + High AI → Role clarity issues  
4. Low RCI + Low AI → Requires full intervention  

This helps us identify *where to act*.
""")

with st.expander("📊 About the Data"):
    st.write("""
- Data is simulated for analysis purposes  
- Includes multiple departments and managers  
- Covers employee responses on:
  - Role clarity (RCI questions)
  - AI readiness (AI questions)

This structure helps in scalable organizational diagnostics.
""")

# =========================
# CLEAN VERTICAL FILTERS
# =========================

st.subheader("🔍 Select Filters")

# 1️⃣ Department
departments = ["All"] + sorted(df["Department"].unique().tolist())
selected_dept = st.selectbox("🏢 Select Department", departments)

# Apply Department Filter
if selected_dept == "All":
    filtered_df = df.copy()
else:
    filtered_df = df[df["Department"] == selected_dept]

# 2️⃣ Manager (dependent)
managers = ["All"] + sorted(filtered_df["Manager"].unique().tolist())
selected_manager = st.selectbox("👤 Select Manager", managers)

if selected_manager != "All":
    filtered_df = filtered_df[filtered_df["Manager"] == selected_manager]

# 3️⃣ Team (dependent)
teams = ["All"] + sorted(filtered_df["Team"].unique().tolist())
selected_team = st.selectbox("👥 Select Team", teams)

if selected_team != "All":
    filtered_df = filtered_df[filtered_df["Team"] == selected_team]

filtered_df = filtered_df.copy()

# Create category columns for all parameters
for col in [
    "RCI","AI_Adaptability",
    "Expectation_Clarity","Authority_Clarity","Manager_Effectiveness",
    "Execution_Clarity","Cross_Function",
    "AI_Clarity","AI_Usage","AI_Capability","AI_Support","AI_Risk"
]:
    filtered_df[f"{col}_Category"] = filtered_df[col].apply(classify_score)

st.markdown("---")

#Create parameter list
   
param_cols = [
   "Expectation_Clarity",
   "Authority_Clarity",
    "Manager_Effectiveness",
    "Execution_Clarity",
    "Cross_Function",
    "AI_Clarity",
    "AI_Usage",
    "AI_Capability",
    "AI_Support",
    "AI_Risk"
   ]


    #Identify employee patterns

def segment_by_parameter(df, focus_col):
    strong = 0
    mixed = 0
    weak = 0

    for _, row in df.iterrows():

        scores = [row[col] for col in param_cols]

        good = sum([1 for s in scores if classify_score(s) in ["Good", "Excellent"]])
        total_params = len(param_cols)
        good_ratio = good / total_params

        # ✅ Define condition
        is_weak_in_focus = classify_score(row[focus_col]) in ["Risk", "Critical"]

        
        if is_weak_in_focus:
            if good_ratio >= 0.7:
                strong += 1
            elif good_ratio >= 0.5:
                mixed += 1
            else:
                weak += 1

    return strong, mixed, weak

# label mapping
label_map = {
        "Expectation_Clarity": "Expectation Clarity",
        "Authority_Clarity": "Authority Clarity",
        "Manager_Effectiveness": "Manager Effectiveness",
        "Execution_Clarity": "Execution Clarity",
        "Cross_Function": "Cross Function",
        "AI_Clarity": "AI Clarity",
        "AI_Usage": "AI Usage",
        "AI_Capability": "AI Capability",
        "AI_Support": "AI Support",
        "AI_Risk": "AI Risk"
    }

def segment_overall(df):
    strong = 0
    mixed = 0
    weak = 0

    for _, row in df.iterrows():

        scores = [row[col] for col in param_cols]

        good = sum([1 for s in scores if classify_score(s) in ["Good", "Excellent"]])
        total_params = len(param_cols)
        good_ratio = good / total_params

        if good_ratio >= 0.7:
            strong += 1
        elif good_ratio >= 0.5:
            mixed += 1
        else:
            weak += 1

    return strong, mixed, weak

# Generate narrative
def generate_full_narrative(df):

    problem_areas = []
    improvement_areas = []
    strength_areas = []

    for col in param_cols:
        avg = df[col].mean()
        label = label_map[col]
        category = classify_score(avg)

        risk_count = len(df[df[f"{col}_Category"].isin(["Risk","Critical"])])
        total = len(df)

        # Better logic (important fix)
        if risk_count / total > 0.2:
            problem_areas.append((label, avg, risk_count))
        elif category == "Good":
            improvement_areas.append((label, avg))
        else:
            strength_areas.append((label, avg))

    text = "🧠 Organizational Insight Report\n\n"

    # 🔴 Problems
    # 🔴 Problems
    if problem_areas:
        text += "🔴 Key Problem Areas:\n"

        for p in problem_areas[:3]:

            # Get column name
            col_name = [k for k,v in label_map.items() if v == p[0]][0]

             # 👉 Affected employees (weak in this parameter)
            affected_df = df[df[f"{col_name}_Category"].isin(["Risk","Critical"])]
            affected_count = len(affected_df)
            total_count = len(df)

            # 👉 Segment affected employees
            if affected_count > 0:
                strong_a, mixed_a, weak_a = segment_overall(affected_df)
            else:
                strong_a, mixed_a, weak_a = 0, 0, 0

            # 👉 Segment total population
            strong_t, mixed_t, weak_t = segment_overall(df)

            # Insight maps
            meaning = insight_map.get(p[0], "")
            impact = impact_map.get(p[0], "")
            root = logic_map.get(p[0], "")

            text += f"""
- {p[0]} ({round(p[1],2)})

    👥 Affected Employees: {affected_count} / {total_count}

    🔎 Within affected employees:
    - {strong_a} → Strong overall but weak here
    - {mixed_a} → Mixed performers
    - {weak_a} → Consistently underperforming

    📊 Overall population:
    - {strong_t} → Strong
    - {mixed_t} → Mixed
    - {weak_t} → Weak

    👉 {meaning}
    💡 Root Cause: {root}
    📉 Impact: {impact}
    """
    else:
        text += "🟢 No critical problem areas detected\n"
        # 🟡 Improvements
        if improvement_areas:
            text += "\n🟡 Improvement Opportunities:\n"
        
            for i in improvement_areas[:3]:
                meaning = insight_map.get(i[0], "")

                text += f"""
- {i[0]} ({round(i[1],2)})
  👉 {meaning}
  🚀 Can be improved to excellence
"""

    # 🟢 Strengths
    if strength_areas:
        text += "\n🟢 Strength Areas:\n"
        
        for s in strength_areas[:3]:
            text += f"""
- {s[0]} ({round(s[1],2)})
  💪 Strong performance, maintain this
"""

    return text

# =========================
# ANALYSIS TABS
# =========================



tab1, tab2 = st.tabs(["📊 Basic Analysis", "🔍 Detailed Analysis"])
# --------------------------
#Inteventions
# --------------------------
def suggest_interventions(issues):

    interventions = {
        "Expectation Clarity": "Define clear KRAs, role expectations & success metrics",
        "Authority Clarity": "Empower decision-making, reduce approval layers",
        "Manager Effectiveness": "Train managers on feedback, coaching & communication",
        "Execution Clarity": "Improve SOPs, workflows & task ownership clarity",
        "Cross Function": "Introduce cross-team sync meetings & collaboration rituals",
        "AI Usage": "Conduct hands-on AI tool training sessions",
        "AI Capability": "Upskill team on AI tools & real use cases",
        "AI Support": "Provide access to tools, licenses & leadership support",
        "AI Clarity": "Educate employees on AI purpose, use cases & impact"
    }

    solutions = []

    for issue, score in issues:
        category = classify_score(score)

        solution_text = interventions.get(issue, "No intervention defined")

        solutions.append(f"{issue} ({category}) → {solution_text}")

    return solutions




with tab1:
    # --------------------------
    # PERFORMANCE SUMMARY
    # --------------------------

    rci_avg = filtered_df["RCI"].mean()
    ai_avg = filtered_df["AI_Adaptability"].mean()

    result = pd.DataFrame({
        "RCI": [rci_avg],
        "AI_Adaptability": [ai_avg],
        "Headcount": [len(filtered_df)],
        "Insight": [combined_insight(rci_avg, ai_avg)]
    })

    st.subheader("📊 Performance Summary")
    st.dataframe(result)

    st.subheader("📈 RCI & AI")
    
    st.markdown("### 📍 Where do you stand?")
    # =========================
    # RCI & AI BENCHMARK CHART
    # =========================

    chart_df = pd.DataFrame({
    "Metric": ["RCI", "AI Adaptability"],
    "Score": [rci_avg, ai_avg]
    })

    fig = go.Figure()

    # Add bars
    fig.add_trace(go.Bar(
        x=chart_df["Metric"],
        y=chart_df["Score"],
        text=[round(rci_avg,2), round(ai_avg,2)],
        textposition='auto'
    ))

    # Y-axis range
    fig.update_yaxes(range=[1,5])

    # Add benchmark zones (background colors)
    fig.add_shape(type="rect", x0=-0.5, x1=1.5, y0=1, y1=2.8,
                fillcolor="red", opacity=0.1, line_width=0)

    fig.add_shape(type="rect", x0=-0.5, x1=1.5, y0=2.8, y1=3.5,
                fillcolor="yellow", opacity=0.1, line_width=0)

    fig.add_shape(type="rect", x0=-0.5, x1=1.5, y0=3.5, y1=4.2,
                fillcolor="green", opacity=0.1, line_width=0)

    fig.add_shape(type="rect", x0=-0.5, x1=1.5, y0=4.2, y1=5,
                fillcolor="blue", opacity=0.1, line_width=0)

    fig.update_layout(
        title="📊 RCI vs AI Benchmark Position",
        yaxis_title="Score (1–5)",
        xaxis_title="Metrics"
    )

    st.plotly_chart(fig)
    # --------------------------
    # ROOT CAUSE ANALYSIS (NEW)
    # --------------------------

    st.subheader("🔍 Root Cause Analysis")

    issues = root_cause_analysis(filtered_df)

    if not issues:
        st.success("✅ No major issues detected. Performance is healthy.")
    else:
        for issue, score in issues:
            st.write(f"⚠ {issue} is low ({round(score,2)})")
    st.subheader("🛠 Suggested Interventions")

    if issues:
        solutions = suggest_interventions(issues)
        for sol in solutions:
            st.write(f"✅ {sol}")

param_map = {
    "Expectation Clarity": "Expectation_Clarity",
    "Authority Clarity": "Authority_Clarity",
    "Manager Effectiveness": "Manager_Effectiveness",
    "Execution Clarity": "Execution_Clarity",
    "Cross Function": "Cross_Function",
    "AI Clarity": "AI_Clarity",
    "AI Usage": "AI_Usage",
    "AI Capability": "AI_Capability",
    "AI Support": "AI_Support",
    "AI Risk": "AI_Risk"
}

# =========================
# SMART ANALYSIS MAPS
# =========================

# 1️⃣ Meaning (What it represents)
insight_map = {
    "Expectation Clarity": "Employees may not clearly understand their responsibilities.",
    "Authority Clarity": "Decision-making authority is unclear within the team.",
    "Manager Effectiveness": "Manager communication may be inconsistent or unclear.",
    "Execution Clarity": "Processes and workflows may not be well defined.",
    "Cross Function": "Expectations between teams are not clearly aligned.",
    
    "AI Clarity": "Employees do not fully understand how AI impacts their role.",
    "AI Usage": "Employees are not actively using AI tools in daily work.",
    "AI Capability": "Skill gap exists in using AI tools effectively.",
    "AI Support": "Organization is not providing enough tools or support for AI adoption.",
    "AI Risk": "Employees may feel insecure about AI, increasing attrition risk."
}

# 2️⃣ Root Cause (WHY)
logic_map = {
    "Expectation Clarity": "Poor job descriptions or informal role allocation.",
    "Authority Clarity": "No clear RACI or decision ownership defined.",
    "Manager Effectiveness": "Lack of structured communication or inconsistent messaging.",
    "Execution Clarity": "Absence of SOPs or structured workflows.",
    "Cross Function": "No defined inter-team processes or SLA agreements.",
    
    "AI Clarity": "Lack of communication about AI strategy.",
    "AI Usage": "No exposure or hands-on training with AI tools.",
    "AI Capability": "Insufficient training or upskilling initiatives.",
    "AI Support": "Limited access to tools, licenses, or leadership push.",
    "AI Risk": "Fear of job loss or uncertainty about future roles."
}

# 3️⃣ Business Impact (WHY IT MATTERS)
impact_map = {
    "Expectation Clarity": "Leads to confusion, low ownership, and reduced accountability.",
    "Authority Clarity": "Slows down decision-making and increases conflicts.",
    "Manager Effectiveness": "Creates misalignment and reduces team trust.",
    "Execution Clarity": "Causes inefficiency and dependency on individuals.",
    "Cross Function": "Results in delays and cross-team conflicts.",
    
    "AI Clarity": "Creates uncertainty and resistance to AI adoption.",
    "AI Usage": "Reduces productivity gains from AI.",
    "AI Capability": "Limits ability to leverage AI tools effectively.",
    "AI Support": "Slows down organization-wide AI transformation.",
    "AI Risk": "Increases attrition risk and talent loss."
}
with tab2:
    st.subheader("🔍 Detailed Analysis")
    st.info("Coming Soon 🚧")
    st.subheader("📊 Parameter Level Breakdown")

    param_means = pd.DataFrame({
        "Expectation Clarity": [filtered_df["Expectation_Clarity"].mean()],
        "Authority Clarity": [filtered_df["Authority_Clarity"].mean()],
        "Manager Effectiveness": [filtered_df["Manager_Effectiveness"].mean()],
        "Execution Clarity": [filtered_df["Execution_Clarity"].mean()],
        "Cross Function": [filtered_df["Cross_Function"].mean()],
        "AI Clarity": [filtered_df["AI_Clarity"].mean()],
        "AI Usage": [filtered_df["AI_Usage"].mean()],
        "AI Capability": [filtered_df["AI_Capability"].mean()],
        "AI Support": [filtered_df["AI_Support"].mean()],
        "AI Risk": [filtered_df["AI_Risk"].mean()]
    })

    # Add filter context as index
    context = f"{selected_dept} | {selected_manager} | {selected_team}"
    param_means.index = [context]

    st.dataframe(param_means)

    # --------------------------
    #RCI & AI PIE
    # --------------------------

    st.subheader("📊 Benchmark Distribution Overview")

    col1, col2 = st.columns(2)

    # RCI Pie
    with col1:
        rci_dist = filtered_df["RCI"].apply(classify_score).value_counts()
        fig_rci = go.Figure(data=[go.Pie(
            labels=rci_dist.index,
            values=rci_dist.values,
            hole=0.4
        )])
        fig_rci.update_layout(title="RCI Distribution")
        st.plotly_chart(fig_rci)

    # AI Pie
    with col2:
        ai_dist = filtered_df["AI_Adaptability"].apply(classify_score).value_counts()
        fig_ai = go.Figure(data=[go.Pie(
            labels=ai_dist.index,
            values=ai_dist.values,
            hole=0.4
        )])
        fig_ai.update_layout(title="AI Adaptability Distribution")
        st.plotly_chart(fig_ai)

    st.subheader("🔍 Deep Dive into Parameter")

    selected_param = st.selectbox(
        "Select Parameter",
        list(param_map.keys())
        )

    col_name = param_map[selected_param]
    category_col = f"{col_name}_Category"

    param_dist = filtered_df[category_col].value_counts()

    fig_param = go.Figure(data=[go.Pie(
        labels=param_dist.index,
        values=param_dist.values,
        hole=0.4
    )])

    fig_param.update_layout(title=f"{selected_param} Distribution")

    st.plotly_chart(fig_param)
    
    # =========================
    # SMART NARRATIVE OUTPUT
    # =========================

    st.subheader("🧠 Smart Insight Engine")
    
    
    insight_text = generate_full_narrative(filtered_df)
    st.info(insight_text)
    
