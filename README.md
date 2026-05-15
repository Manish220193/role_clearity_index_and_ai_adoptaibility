# Role Clarity Index (RCI) + AI Adaptability Dashboard

An HR analytics dashboard built using Python, Pandas, Streamlit, and Plotly that helps organizations identify role clarity gaps, AI readiness issues, manager risks, and employee flight risks during AI transformation.

## Problem Statement

Organizations are rapidly adopting AI tools, but many fail because employees face two hidden problems:

- Unclear role expectations
- Low AI adaptability

This creates:
- Productivity loss
- Manager dependency
- Poor execution
- Resistance to AI adoption
- Potential employee attrition

Traditional HR surveys measure engagement but often fail to identify operational role clarity issues and AI readiness gaps.

This project attempts to solve that problem.

## Solution

This dashboard introduces a dual workforce diagnostic framework:

### Role Clarity Index (RCI)
Measures:

- Expectation Clarity
- Authority Clarity
- Manager Effectiveness
- Execution Clarity
- Cross-functional clarity

### AI Adaptability Index
Measures:

- AI Clarity
- AI Usage
- AI Capability
- AI Support

### AI Risk Score
Measures employee anxiety/fear regarding AI adoption.

By combining these metrics, organizations can identify:

- Teams ready for AI transformation
- Teams needing AI training
- Teams facing role clarity issues
- Employees at flight risk

## Core Hypothesis

| RCI Score | AI Adaptability Score | Business Meaning |
|------------|------------------------|-------------------|
| High | High | Ready for AI implementation |
| High | Low | Needs AI training |
| Low | High | Needs role clarity intervention |
| Low | Low | Needs both interventions |

## Features

### Basic Analysis
- RCI score calculation
- AI adaptability calculation
- Benchmark visualization
- Root cause identification
- Intervention recommendations

### Detailed Analysis
- Parameter breakdown
- Distribution charts
- Smart narrative insights

### Critical Analysis
- Manager-level risk analysis
- Team-level diagnostics
- Leadership recommendations
- Heatmap visualization

### Targeted Analysis
- Employee flight risk detection
- Tenure risk analysis
- Role-level analysis
- AI intervention recommendations

## Tech Stack

- Python
- Pandas
- Streamlit
- Plotly

## Dataset

This project uses simulated employee survey data containing:

- Employee
- Department
- Team
- Manager
- Role Level
- Tenure
- RCI survey questions
- AI adaptability survey questions

## Workflow

1. Employee survey data collection
2. Data preprocessing
3. RCI score calculation
4. AI adaptability calculation
5. Risk segmentation
6. Dashboard visualization
7. Intervention recommendations

## Future Improvements

- PDF report download feature
- Predictive attrition model
- Real employee survey integration

## Key Business Outcomes

This dashboard helps organizations:

- Identify role ambiguity across teams
- Improve manager effectiveness
- Increase AI adoption readiness
- Reduce employee resistance to AI transformation
- Detect early flight-risk employees
- Design targeted HR interventions

## Why This Project Matters

AI transformation is often discussed from a technology perspective.

This project explores AI transformation from a workforce perspective by combining:

- HR analytics
- Organizational development
- Employee behavior
- AI readiness

This aligns with future HR transformation needs.
