#adding this code to github repository
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

def classify_ai_risk(score):
    if score >= 4.2:
        return "Critical"
    elif score >= 3.5:
        return "Risk"
    elif score >= 2.8:
        return "Good"
    else:
        return "Excellent"

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
normal_cols = [
    "RCI",
    "AI_Adaptability",
    "Expectation_Clarity",
    "Authority_Clarity",
    "Manager_Effectiveness",
    "Execution_Clarity",
    "Cross_Function",
    "AI_Clarity",
    "AI_Usage",
    "AI_Capability",
    "AI_Support"
]

for col in normal_cols:
    filtered_df[f"{col}_Category"] = filtered_df[col].apply(classify_score)

# AI Risk uses reverse logic
filtered_df["AI_Risk_Category"] = filtered_df["AI_Risk"].apply(classify_ai_risk)
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

        risk_count = len(
            df[df[f"{col}_Category"].isin(["Risk", "Critical"])]
        )

        total = len(df)
        risk_percent = risk_count / total

        # Problem logic
        if risk_percent >= 0.20:
            problem_areas.append((label, avg, risk_count))

        elif category == "Good":
            improvement_areas.append((label, avg))

        elif category == "Excellent":
            strength_areas.append((label, avg))


    text = "🧠 Organizational Insight Report\n\n"

    # -------------------------
    # Problem Areas
    # -------------------------
    if problem_areas:
        text += "🔴 Key Problem Areas:\n\n"

        for p in problem_areas:

            # get actual column name
            col_name = [k for k, v in label_map.items() if v == p[0]][0]

            affected_df = df[
                df[f"{col_name}_Category"].isin(["Risk", "Critical"])
            ]

            affected_count = len(affected_df)
            total_count = len(df)

            affected_percent = round(
                (affected_count / total_count) * 100, 1
            )

            # severity logic
            if affected_percent >= 60:
                severity = "High Priority"
            elif affected_percent >= 35:
                severity = "Medium Priority"
            else:
                severity = "Low Priority"

            meaning = insight_map.get(p[0], "")
            root = logic_map.get(p[0], "")
            impact = impact_map.get(p[0], "")

            text += f"""
- {p[0]} ({round(p[1],2)})

  👥 Affected Employees: {affected_count}/{total_count} ({affected_percent}%)

  🚨 Severity: {severity}

  👉 {meaning}
  💡 Root Cause: {root}
  📉 Impact: {impact}

"""

    else:
        text += "🟢 No critical problem areas detected\n\n"


    # -------------------------
    # Improvement Areas
    # -------------------------
    if improvement_areas:
        text += "🟡 Improvement Opportunities:\n\n"

        for i in improvement_areas:
            meaning = insight_map.get(i[0], "")

            text += f"""
- {i[0]} ({round(i[1],2)})
  👉 {meaning}
  🚀 Can be improved further

"""


    # -------------------------
    # Strength Areas
    # -------------------------
    if strength_areas:
        text += "🟢 Strength Areas:\n\n"

        for s in strength_areas:
            text += f"""
- {s[0]} ({round(s[1],2)})
  💪 Strong performance, maintain this

"""

    return text

# =========================
# ANALYSIS TABS
# =========================


tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Basic Analysis",
    "🔍 Detailed Analysis",
    "🚨 Critical Analysis",
    "🛠  Targetted Analysis"
])

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
    
    color_map = {
        "Excellent": "#2E86DE",   # Blue
        "Good": "#27AE60",        # Green
        "Risk": "#F39C12",        # Orange
        "Critical": "#E74C3C"     # Red
    }
    # RCI Pie
    with col1:
        rci_dist = filtered_df["RCI"].apply(classify_score).value_counts()

        labels = rci_dist.index.tolist()
        values = rci_dist.values.tolist()

        fig_rci = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker=dict(
                colors=[color_map[label] for label in labels]
            )
        )])

        fig_rci.update_layout(title="RCI Distribution")
        st.plotly_chart(fig_rci)

    # AI Pie
    with col2:
        ai_dist = filtered_df["AI_Adaptability"].apply(classify_score).value_counts()

        labels = ai_dist.index.tolist()
        values = ai_dist.values.tolist()

        fig_ai = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker=dict(
                colors=[color_map[label] for label in labels]
            )
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

    labels = param_dist.index.tolist()
    values = param_dist.values.tolist()

    fig_param = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(
            colors=[color_map[label] for label in labels]
        )
    )])

    fig_param.update_layout(
        title=f"{selected_param} Distribution"
    )

    st.plotly_chart(fig_param)
    
    
    # =========================
    # SMART NARRATIVE OUTPUT
    # =========================

    st.subheader("🧠 Smart Insight Engine")
    
    
    insight_text = generate_full_narrative(filtered_df)
    st.info(insight_text)
    
with tab3:
    st.subheader("🚨 Manager Risk Analysis")

    # ------------------------
    # Manager Level Analysis
    # ------------------------
    manager_analysis = filtered_df.groupby("Manager").agg({
        "Expectation_Clarity":"mean",
        "Authority_Clarity":"mean",
        "Manager_Effectiveness":"mean",
        "Execution_Clarity":"mean",
        "Cross_Function":"mean",
        "RCI":"mean"
    }).reset_index()

    st.write("### Manager Performance Table")
    st.dataframe(
        manager_analysis.sort_values("RCI")
    )

    # ------------------------
    # Highest Risk Manager
    # ------------------------
    weakest_manager = manager_analysis.loc[
        manager_analysis["RCI"].idxmin()
    ]

    st.error(
        f"""
        Highest Risk Manager: {weakest_manager['Manager']}
        
        RCI Score: {round(weakest_manager['RCI'],2)}
        """
    )

    # ------------------------
    # Team Analysis
    # ------------------------
    team_analysis = filtered_df.groupby("Team").agg({
        "RCI":"mean",
        "AI_Adaptability":"mean"
    }).reset_index()

    st.write("### Team Level Analysis")
    st.dataframe(
        team_analysis.sort_values("RCI")
    )

    # ------------------------
    # Team vs Systemic Issue
    # ------------------------
    low_teams = team_analysis[
        team_analysis["RCI"] < 3.5
    ]

    if len(low_teams) == 1:
        st.warning(
            "Issue appears team-specific. Likely local leadership/process issue."
        )

    elif len(low_teams) > 1:
        st.error(
            "Multiple teams affected. This appears to be department-wide/systemic."
        )

    else:
        st.success(
            "No major team-level role clarity issues detected."
        )

    # ------------------------
    # Leadership Recommendations
    # ------------------------
    st.subheader("🛠 Leadership Recommendation")

    if weakest_manager["Manager_Effectiveness"] < 3.5:
        st.write("✅ Conduct manager coaching intervention")

    if weakest_manager["Expectation_Clarity"] < 3.5:
        st.write("✅ Redesign role expectations/KRAs")

    if weakest_manager["Execution_Clarity"] < 3.5:
        st.write("✅ Improve SOP/process clarity")

    if weakest_manager["Cross_Function"] < 3.5:
        st.write("✅ Improve cross-functional alignment")
    
    if weakest_manager["Authority_Clarity"] < 3.5:
        
        st.write("✅ Define decision ownership using RACI framework")

    # ------------------------
    # Heatmap
    # ------------------------
    import plotly.express as px

    heatmap_df = manager_analysis.set_index("Manager")

    fig = px.imshow(
        heatmap_df[
            [
                "Expectation_Clarity",
                "Authority_Clarity",
                "Manager_Effectiveness",
                "Execution_Clarity",
                "Cross_Function"
            ]
        ],
        text_auto=True,
        title="Manager Risk Heatmap"
    )

    st.plotly_chart(fig)

with tab4:
    st.subheader("🚨 Employee Flight Risk Analysis")
    with st.expander("ℹ️ How Flight Risk is Calculated"):
        st.write("""
    We identify potential flight-risk employees using a combined workforce stress model.

    An employee is flagged when:

    ✅ Role Clarity Index (RCI) is below benchmark (< 3.5)
    → Indicates role confusion, unclear expectations, or execution friction.

    ✅ AI Adaptability is below benchmark (< 3.5)
    → Indicates low readiness to adapt to AI-driven workflows.

    ✅ AI Risk/Anxiety is high (≥ 3.5)
    → Indicates fear, uncertainty, or resistance toward AI adoption.

    ### Why this matters:
    When employees simultaneously experience:

    - unclear roles
    - low future readiness
    - high AI anxiety

    they may feel insecure about their career path, leading to disengagement or potential attrition risk.

    This model helps HR teams proactively identify employees who may need:
    - role clarity interventions
    - AI upskilling
    - manager support
    - retention conversations
    """)

    # -------------------------
    # Flight Risk Logic
    # -------------------------
    flight_risk_df = filtered_df[
        (filtered_df["RCI"] < 3.5) &
        (filtered_df["AI_Adaptability"] < 3.5) &
        (filtered_df["AI_Risk"] >= 3.5)
    ]

    st.write("### High Flight Risk Employees")

    if len(flight_risk_df) > 0:
        st.dataframe(
            flight_risk_df[
                [
                    "Employee",
                    "Department",
                    "Team",
                    "Manager",
                    "Role_Level",
                    "Tenure",
                    "RCI",
                    "AI_Adaptability",
                    "AI_Risk"
                ]
            ].sort_values("AI_Risk", ascending=False)
        )

    else:
        st.success("No high flight-risk employees detected.")

    # -------------------------
    # Tenure Analysis
    # -------------------------
    st.subheader("📅 Tenure Risk Analysis")

    tenure_analysis = filtered_df.groupby("Tenure").agg({
        "RCI":"mean",
        "AI_Adaptability":"mean",
        "AI_Risk":"mean"
    }).reset_index()

    st.dataframe(tenure_analysis)

    highest_risk_tenure = tenure_analysis.loc[
        tenure_analysis["AI_Risk"].idxmax()
    ]

    st.warning(
        f"""
        Highest AI anxiety observed in:
        {highest_risk_tenure['Tenure']}
        
        AI Risk Score: {round(highest_risk_tenure['AI_Risk'],2)}
        """
    )

    # -------------------------
    # Role Level Analysis
    # -------------------------
    st.subheader("👔 Role Level Analysis")

    role_analysis = filtered_df.groupby("Role_Level").agg({
        "RCI":"mean",
        "AI_Adaptability":"mean",
        "AI_Risk":"mean"
    }).reset_index()

    st.dataframe(role_analysis)

    # -------------------------
    # AI Intervention Recommendation
    # -------------------------
    st.subheader("🤖 AI Intervention Recommendation")

    avg_ai_clarity = filtered_df["AI_Clarity"].mean()
    avg_ai_usage = filtered_df["AI_Usage"].mean()
    avg_ai_capability = filtered_df["AI_Capability"].mean()
    avg_ai_support = filtered_df["AI_Support"].mean()
    avg_ai_risk = filtered_df["AI_Risk"].mean()

    if avg_ai_clarity < 3.5:
        st.write("✅ Conduct AI awareness sessions")

    if avg_ai_usage < 3.5:
        st.write("✅ Improve AI adoption through workflow integration")

    if avg_ai_capability < 3.5:
        st.write("✅ Launch AI upskilling programs")

    if avg_ai_support < 3.5:
        st.write("✅ Provide better AI tools/resources")

    if avg_ai_risk >= 3.5:
        st.write("✅ HR should monitor attrition risk and create retention plans")