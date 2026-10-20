# Diabetes Digital Twin (Happiest Health Digital Twin Challenge 2026)

A physiological digital twin research prototype that fuses static electronic health record (EHR) priors with dynamic, high-frequency continuous multi-sensor telemetry to forecast whether continuous glucose monitoring (CGM) readings will cross a clinical threshold (>180 mg/dL) within the next 2 hours ($t \to t + 120\text{min}$) with strict zero data leakage.

---

## 🏆 Project Overview & Challenge Context

> **Important research limitation:** This project uses synthetic telemetry and predefined scoring weights. Displayed metrics are exploratory results on synthetic generated episodes, not evidence of clinical utility, human validation, or real-world predictive accuracy. The evaluation seed offset does not by itself establish a patient-held-out split. The forecast uncertainty band is heuristic, not a validated 95% confidence interval.



- **Competition**: Happiest Health Digital Twin Challenge 2026
- **Architecture**: Dual-stream physiological digital twin prototype with rule-based risk scoring & counterfactual simulation
- **Research Scope**: Exploratory computational research prototype designed for demonstration and algorithmic evaluation on reproducible synthetic cohorts.
- **Zero Data Leakage Guarantee**: Features evaluated at time $t$ are mathematically restricted to data points where $t' \le t$. Future sensor timestamps are strictly walled off from feature extraction.
- **Ground Truth Target Formulation**: Binary label $Y(t) = \mathbb{I}\left(\max_{t < t' \le t + 120\text{min}} G(t') \ge \theta\right)$ derived strictly from held-out future measurements, avoiding circular label leakage.

---

## 🔬 Core Features & Interactive Capabilities

1. **Dashboard Overview**:
   - Comprehensive multi-patient view covering diverse synthetic archetypes (Eleanor Vance - T2D, Marcus Chen - Prediabetes, Aisha Patel - LADA, David Miller - T2D with GLP-1).
   - Custom patient creator to evaluate custom clinical markers (HbA1c, BMI, age, medications).
   - Continuous Glycemic Curve with a dynamic 2-hour illustrative projection and heuristic uncertainty band (not a statistically validated confidence interval).
   - Dual-sensor overlay (interstitial glucose + heart rate or step activity).

2. **Physiological Forecasting vs Rule-Based Simulation**:
   - **Rule-Based Logistic Scoring Model**: Uses predefined weights and a logistic transform to produce an experimental risk score for $P(Y(t)=1 \mid \mathbf{X}(t))$. It is not a model trained on clinical data, and its probabilities are not clinically calibrated.
   - **Explainable AI (XAI)**: SHAP-style local feature attribution detailing whether factors (glycemic velocity, sleep debt, physical activity sink, medication) push risk up or provide protective buffering.
   - **Bergman-Inspired Trajectory Dynamics**: Forward continuous trajectory modeled with meal absorption kinetics, endogenous clearance, and counterfactual intervention comparison.

3. **What-If Interactive Simulator & Counterfactual Interventions**:
   - Live sliders to adjust current glucose, rate of change ($dG/dt$), physical activity (steps), heart rate elevation, and sleep debt.
   - **GLP-1 Receptor Agonist Pharmacotherapy Panel**: Toggle GLP-1 RA therapy on/off with dynamic gastric emptying delay multipliers (0.40x to 0.90x), comparing live attenuated trajectories with unmedicated and exercise counterfactuals.
   - One-click intervention presets: 15-minute brisk walk (+1,800 steps), high-GI carb surge (+50g), GLP-1 RA therapy activation, and acute stress.

4. **3D Organ & Cell Twin (Procedural Educational Model)**:
   - Interactive Three.js WebGL visualization of vascular lumen perfusion, red blood cells, interstitial glucose diffusion, and insulin/contraction-mediated GLUT4 transporter translocation.
   - *Clear Disclosure*: This 3D viewport is an illustrative conceptual animation for educational demonstration, **not** a clinically or bio-mechanically validated organ or tissue model.

5. **Doctor Clinical Dossier & Audit Trail**:
   - 5-minute sampling interval telemetry inspection.
   - Timestamped retrospective audit log comparing past 2-hour forecasts against observed ground-truth outcomes.
   - CSV export for regulatory and clinical audit review.

6. **Honest Model Evaluation & Benchmark**:
   - Evaluated on a held-out test split of 500 patient episodes across diverse archetypes using seed offsets.
   - Interactive Classification Decision Threshold slider ($\tau \in [0.10, 0.90]$) demonstrating sensitivity vs specificity trade-offs.
   - **Actual Held-Out Performance ($\tau = 0.50$, Threshold = 180 mg/dL)**:
     - **Accuracy**: 62.0%
     - **Sensitivity (Recall)**: 38.1% (detecting rapid upward surges)
     - **Specificity**: 98.5% (very low false positive rate on stable periods)
     - **Precision (PPV)**: 97.5%
     - **F1-Score**: 0.548
     - **ROC-AUC**: A value is displayed by the app from its current synthetic evaluation routine. Treat it as exploratory synthetic-benchmark output, not evidence of clinical performance; rerun the app/tests to reproduce it.
     - **Brier Calibration Score**: 0.288
   - Transparent reporting of dataset size, positive/negative prevalence, and limitations.

---

## 🛠️ Technology Stack & Architecture

- **Frontend Application**: React 19, TypeScript, Tailwind CSS v4, Lucide Icons
- **3D Visualization**: Three.js (WebGL, PBR material pipeline with RoomEnvironment)
- **ML & Kinetics Engine**: Pure TypeScript mathematical functions decoupled in `src/ml/`:
  - `syntheticData.ts`: Bergman minimal model ODE approximation with Mulberry32 deterministic RNG
  - `twinPredictor.ts`: Backward-looking feature extraction, predefined-weight rule-based logistic scoring, local attributions, and illustrative trajectory simulation
  - `evaluation.ts`: Synthetic episode evaluation, confusion matrix, ROC-AUC trapezoidal integration, and Brier score. The current seed-offset evaluation is not a patient-held-out validation design.
- **Testing**: Node test runner through `tsx` (`tsx --test src/ml/twinPredictor.test.ts`); verify the actual test count when running.
- **Build / Bundler**: Vite 8

---

## 🚀 Setup & Execution Instructions

### Prerequisites
- Node.js 20+ (Node.js 22 recommended)
- npm or bun

### 1. Installation
```bash
npm install
```

### 2. Run Development Server
```bash
npm run dev
```
Open `http://localhost:3000` in your web browser.

### 3. Run Automated Unit Tests
```bash
npm test
# runs the TypeScript test file through tsx
```
Runs the automated test suite in `src/ml/twinPredictor.test.ts`, verifying:
1. Seeded RNG determinism across patient episodes.
2. Synthetic telemetry continuity and physiological bounds ($40 \le G \le 450$ mg/dL).
3. **Strict Zero Data Leakage invariant**: verifies that mutating future readings does not alter feature vectors at time $t$.
4. Prediction probability bounds ($P \in [0, 1]$) and 9-point forward trajectory generation.
5. High-glucose rapid positive velocity triggers elevated/critical excursion alerts.
6. Normoglycemic stable velocity yields low excursion risk.
7. Confusion matrix and metric calculation accuracy (handling single-class edge cases).
8. GLP-1 RA therapy dynamically dampens absorption coefficient and lowers predicted risk.

### 4. Build Production Bundle
```bash
npm run build
```

---

## 📋 Data Generation & Zero-Leakage Formulation

### Two Data Streams
1. **Stream A (Static EHR Clinical Priors)**: Age, baseline HbA1c, BMI, diabetes duration, medication class & compliance.
2. **Stream B (High-Frequency Wearable Telemetry)**: 5-minute CGM interstitial glucose, optical PPG heart rate, accelerometer physical steps, and nocturnal sleep recovery.

### Zero-Leakage Mathematical Formulation
At any prediction timestamp $t$:
$$\forall \text{ feature } \in \mathbf{X}(t), \quad \text{timestamp}(\text{feature}) \le t$$

Target Label:
$$Y(t) = \mathbb{I}\left(\max_{t < t' \le t + 120\text{min}} G(t') \ge \theta\right)$$
Where $\theta$ is the defined threshold (default: 180 mg/dL).

### Dynamic Counterfactual Formulation (GLP-1 RA & Physical Activity)
- **GLP-1 Receptor Agonist Absorption Dampening**:
  $$\frac{dG_{\text{effective}}}{dt} = \frac{dG}{dt} \times \alpha_{\text{absorption}}$$
  where $\alpha_{\text{absorption}} \in [0.40, 0.90]$ represents the pharmacological delay in gastric emptying.
- **Physical Activity GLUT4 Translocation**:
  $$\text{ExerciseSink}(t) = \kappa \cdot \text{Steps}_{60\text{m}}$$
  promoting non-insulin dependent skeletal muscle glucose disposal.

---

## ⚠️ Clinical & Regulatory Disclaimer

**RESEARCH PROTOTYPE ONLY — NOT A CLINICAL OR DIAGNOSTIC TOOL**

1. **Synthetic Data Performance**: All patient profiles, clinical histories, and telemetry time-series in this application are 100% synthetic and generated for research simulation. Synthetic benchmark performance **does not establish clinical validity** in human populations.
2. **Real-World Factors**: Human in-vivo glycemic physiology involves complex unmodeled factors, including interstitial-to-blood glucose lag dynamics (typically 5–15 minutes), unpredictable gastroparesis, acute subclinical infection, stress-induced counterregulatory hormones, and unannounced dietary intake.
3. **Regulatory Status**: This application has not been evaluated, cleared, or approved by the US Food and Drug Administration (FDA), the European Medicines Agency (EMA), or any national medical regulatory authority.
4. **Intended Use**: This software must **never** be used to guide therapeutic insulin dosing, adjust prescribed pharmacotherapy, triage patients, or replace professional medical advice.

---

## 📄 Deliverables & Challenge Checklist

- [x] **Reproducible Synthetic Data Engine**: Minimal model kinetics with deterministic pseudo-random seeds.
- [x] **Zero-Leakage Feature Extraction**: Mathematically verified in unit tests.
- [x] **Experimental Rule-Based Risk Scoring**: 2-hour excursion scoring with explainable feature attributions; not clinically validated or calibrated.
- [x] **What-If Simulator & Counterfactual Testing**: Interactive sliders, brisk walk simulation, GLP-1 RA therapy toggle with dynamic absorption coefficient adjustment.
- [x] **3D Organ & Cell Twin**: Illustrative Three.js visualization of vascular and cellular glucose transport.
- [x] **Doctor Clinical Dossier & Audit Log**: Historical ground-truth verification and CSV export.
- [x] **Model Evaluation View**: Confusion matrix, ROC curve, decision threshold slider, transparent reporting of held-out test metrics and class balance without artificial floors.
- [x] **Automated Test Suite**: Native `node:test` suite verifying all core ML and data invariants.
- [ ] **Prospective Multi-Center Clinical Trial Validation**: Requires real-world clinical CGM trial data and Institutional Review Board (IRB) approval (beyond current synthetic hackathon scope).
- [ ] **Closed-Loop Automated Insulin Delivery (AID) Integration**: Requires certified medical device hardware integration.

---

## 📜 License

This project is licensed under the **Apache License, Version 2.0**. See the [LICENSE](LICENSE) file or the license headers in source files for details.
