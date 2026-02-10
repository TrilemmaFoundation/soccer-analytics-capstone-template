# Exploratory Data Analysis Outline

## 📦 Deliverable: Exploratory Data Analysis Package (Due Feb 26, 2026 at 2:00 am ET)

Each team will submit an EDA package inside this official capstone template repository. The goal is to communicate meaningful insights through a clear narrative that serves both technical and non-technical audiences.

All EDA work must live inside the `EDA` folder of your forked template repository.

---

## ✅ Submission Instructions

- All work must be completed inside your fork of the official template repo
  [https://github.com/TrilemmaFoundation/soccer-analytics-capstone-template.git](https://github.com/TrilemmaFoundation/soccer-analytics-capstone-template.git)

- Place all EDA related notebooks inside the `EDA` folder

- Your submission will consist of **two primary notebooks**

### 1. Required: [`EDA_Executive.ipynb`](EDA_Executive.ipynb)

This is the notebook we will read first.

It should be a polished, narrative driven summary of your most engaging insights.

- Focus on storytelling and interpretation
- Highlight only your strongest findings
- Reference deeper work stored in other notebooks when appropriate

### 2. Required: [`EDA.ipynb`](EDA.ipynb)

This notebook serves as your comprehensive EDA reference.

- Include all important exploratory work
- Show intermediate analysis, experiments, and supporting results
- Use this file as a technical appendix that supports `EDA_Executive.ipynb`

Push your work to your forked GitHub repository by the announced deadline. The latest commit before the deadline is what will be viewed for feedback.

---

## 📋 Notebook Structure

### 1. Executive Summary

Begin `EDA_Executive.ipynb` with an executive bullet point summary of your most novel and non-trivial findings.

A reader should understand your key conclusions in under one minute.

Clearly state the path your team will take for the final deliverable, informed by the direction of your EDA:

- **Track 1:** Final report covering soccer analytics and prediction markets.
- **Track 2:** Deployed soccer analytics dashboard.

### 2. Data Retrieval

Load data using the official scripts and utilities provided in the template repository:

After running [`download_data.py`](../data/download_data.py) (following the instructions in the root [`README.md`](../README.md)), you can simply use `pandas` to read the CSV or Parquet files from your local `data/` directory (see [`eda_starter_template.py`](eda_starter_template.py) for an example).

Clearly state:

- What data sources you used
- Any preprocessing steps
- Assumptions or limitations

### 3. General Dataset Overview

Provide a high level understanding of the dataset.

Include:

- Data integrity checks
- Data types and ranges
- Missingness and completeness
- Descriptive statistics
- Initial exploratory visualizations

### 4. (Track 1) Soccer Prediction Market Exploration

Utilize Polymarket prediction market data and StatsBomb event data to perform a detailed exploration of Soccer prediction markets. Here are some examples of questions that can motivate your investigation:

- Can we model team ability (e.g., with an ELO-like rating) from event data and compare it to prediction market implied probabilities?
- When the market probability differs from our modeled ability, is that an inefficiency or are we missing external information (e.g., injuries or tactics)?
- How well can we explain past market odds using event-level data, and where do unexplained gaps remain?
- Can we cluster prediction market participants based on their behavior and outcomes, and relate these archetypes to patterns we see in the event data?
- How do market odds shift after key events like goals or red cards, and how do these shifts compare to the statistical impact of those events in the data?
- Are there specific event-driven metrics, like expected goals after a red card, that differ from how prediction markets adjust?
- Do prediction markets over- or under-react to certain events, and how does that bias show up when we analyze the event data’s predictive power?

### 5. (Track 2) Soccer Analytics Dashboard Exploration

Investigate Statsbomb data to uncover novel and non-trivial insights on players and teams. These insights must be robust and reproducible across different time periods and matches, incentivizing the development of a dashboard for the final deliverable to showcase the insights.

Here are some examples of questions that can motivate your investigation:

- How can metrics like expected goals, expected threat, PPDA, and defensive tilt be combined to identify and quantify a team's playing style?
- Can we analyze how different playing styles match up head-to-head, and predict whether certain styles tend to produce more attacking or defensive matches?
- Can we use event data to define player or team styles, and then see how different styles interact or combine when players switch from club to national teams?
- How can we extrapolate likely playing styles for teams, even when we have limited data, by inferring from player club-level patterns—and what uncertainties (like tactics or coaching) should we account for?
- Can we formalize patterns of specific playing styles—such as pressing or counterattacking—and see how consistently teams and players fit these patterns over time?

## 📋 Notebook Tips

### Insight Showcase

Demonstrate your strongest analytical thinking.

Examples include:

- Rigorous statistical tests
- Creative or informative visualizations
- Novel metrics or transformations
- Thoughtful comparisons across time or regimes
- Reference supporting work in `EDA.ipynb` when needed.

### Narrative Driven Analysis

Organize your notebook as a clear story.

- Use descriptive section headers, markdown text, and visualizations
- Explain your reasoning and decisions (every output should support your narrative)
- Connect observations to future work and potential modeling approaches

Avoid presenting isolated plots without interpretation, or messy outputs without context.

### Success Tips

- Write with clarity and intention
- Use strong titles and captions
- Prioritize insight over code quantity
- Assume your reader has five minutes to review your work
- Link to additional notebooks in the `EDA` folder for deeper dives
- Include references to additional EDA notebooks for extended analysis

Your goal is to produce an EDA that is both technically rigorous and compelling to read.

---

## 📊 Evaluation Rubric

| Category              | Description                                          |
| --------------------- | ---------------------------------------------------- |
| Readability           | Can a layperson follow the high level narrative      |
| Technical Depth       | Can another data scientist build on your work        |
| Visualization Quality | Are plots clean, labeled, and informative            |
| Statistical Rigor     | Do you investigate deeper structure in the data      |
| Executive Summary     | Is your summary concise and insightful               |
| Engagement            | Is the notebook interesting to explore               |
| Reproducibility       | Can the notebook run top to bottom without errors    |
| Motivating            | Does the EDA motivate future work                    |

---
