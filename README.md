
# DIGIVOTE Adaptivity Analysis Demo

This project demonstrates a research-inspired experiment applying concepts from the paper:  
**“Program analysis for adaptive data analysis”** by Liu, Qu, Gaboardi, Garg, and Ullman (2024)  
[Link to Paper → https://doi.org/10.1145/3656414](https://doi.org/10.1145/3656414)

---

## 🎯 Project Goal  
The goal is to apply the **AdaptFun framework’s static adaptivity analysis** to a blockchain-based voting system I’m developing called **DIGIVOTE**, and to simulate how bounded adaptivity influences generalization error under various mechanisms.

---

## ✅ Key Contributions

### 1️⃣ Static Program Analysis  
- Annotated DIGIVOTE components using `@query`, `@depends_on`, and `@weight` inspired by AdaptFun.  
- Built a **weighted dependency graph** of DIGIVOTE’s pipeline:
    - Voter Authentication → Eligibility Check → Vote Submission → Audit Review → Finalize Count  
- Computed the **Adaptivity Bound (AdaptBD)** using strongly connected component traversal.  
    - Result: Provable bound of **5 dependent queries**.

### 2️⃣ Empirical Error Simulation  
- Created a synthetic multi-dimensional Gaussian population dataset as a stand-in for private data.  
- Simulated adaptive data analysis by generating 400 adaptive queries using an analyst strategy (selecting queries based on prior responses).
- Compared mechanisms:
    - Data Splitting (DS)
    - Gaussian Noise (GS)
    - Thresholdout (TS)
    - Overfitting (OF)

The simulation replicates the error growth trends described in the AdaptFun paper’s Fig. 2.

---

## 📊 Outputs
- **Adaptivity Flow Graph (DIGIVOTE pipeline structure)**  
  Displays:
    - Nodes: Functions in DIGIVOTE pipeline  
    - Weights: Max number of times components can be queried  
    - Critical path in bold red  
    - Weights table included for clarity

- **Generalization Error Plot**  
  Path: `outputs/generalization_errors.png`  
  Visualizes RMSE vs number of adaptive queries per mechanism.

- **Optional Outputs**
    - Synthetic population dataset: `outputs/population.csv`
    - Per-round error values: `outputs/errors.csv`

---

## 🚀 How to Run the Demo

### 1. Visualize the Adaptivity Graph
```bash
python -m src.visualize_demo
```

### 2. Run the Simulation of Generalization Errors
```bash
python -m src.simulate_errors
```

### 3. Run the Full Pipeline (Static + Simulation Together)
```bash
python -m src.demo_pipeline
```

---

## 🎓 Inspiration and Acknowledgment

This work is **deeply inspired by Prof. Deepak Garg’s AdaptFun paper**:  
> Liu, J., Qu, W., Gaboardi, M., Garg, D., & Ullman, J. (2024). Program analysis for adaptive data analysis. *Proceedings of the ACM on Programming Languages*, 8(PLDI), 914–938.  
> [https://doi.org/10.1145/3656414](https://doi.org/10.1145/3656414)

This project implements their key contribution:  
👉 Static analysis of adaptivity bounds applied to a real-world-like system (DIGIVOTE)  
👉 Empirical validation of adaptivity’s role in generalization error control

---

## 📚 What You Can Learn from This Repo
- How to construct weighted dependency graphs from annotated programs.  
- How to compute AdaptFun’s AdaptBD static adaptivity bound.  
- How adaptive data analysis impacts generalization error under different mechanisms.  
- How to tie theoretical research into practical system design.

---

## 🔧 Requirements
- Python 3.8+  
- Packages: `numpy`, `matplotlib`, `networkx`

---

## 🤝 Contact
Ananya Sharma  
[[LinkedIn Profile]([url](https://www.linkedin.com/in/sharma-ananya/))] | [[Portfolio Link]]([url](https://ananyasharma05.netlify.app/)) | ananyasharma.connect@gmail.com  
