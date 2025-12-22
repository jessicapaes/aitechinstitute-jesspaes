# Capstone Project 2: Using Big Five Personality Traits to Identify Depression & Anxiety Risk

## 📋 Project Overview

This project develops a machine learning model to identify individuals at risk of depression and anxiety using personality traits from the Big Five Inventory (BFI). The model uses a research-based multi-trait composite approach that achieves 95.7% accuracy.

**Author:** Jessica Paes  
**Date:** December 2025  
**Course:** Intermediate AI & Data Science  
**Institution:** AI Tech Institute

---

## 🎯 Key Results

| Metric | Value |
|--------|-------|
| Best Model | Random Forest |
| Accuracy | 95.7% |
| F1-Score | 95.7% |
| Dataset | 2,436 real survey responses |

---

## 📊 Dataset

**Source:** Big Five Inventory (BFI) from Rdatasets Repository

The BFI is a validated psychological assessment measuring five personality dimensions:
- **Neuroticism (N1-N5)** - Anxiety, mood swings, emotional instability
- **Extraversion (E1-E5)** - Social energy, positive emotions
- **Conscientiousness (C1-C5)** - Self-discipline, organisation
- **Agreeableness (A1-A5)** - Cooperation, trust
- **Openness (O1-O5)** - Creativity, curiosity

**URL:** `https://vincentarelbundock.github.io/Rdatasets/csv/psych/bfi.csv`

---

## 🔬 Methodology

### Research-Based Multi-Trait Composite

```
Risk Score = (Neuroticism × 2) − Extraversion − (Conscientiousness × 0.5)
```

**Why This Approach:**
1. ✅ Supported by multiple published research papers
2. ✅ Captures the "High Neuroticism + Low Extraversion" pattern
3. ✅ Produces balanced class distribution
4. ✅ Scientifically defensible

### Classification
- **Low Risk:** Bottom 33% (tertile)
- **Medium Risk:** Middle 33%
- **High Risk:** Top 33%

---

## 🚀 How to Run

### Requirements

```bash
pip install numpy pandas scikit-learn matplotlib seaborn plotly
```

### Optional (for XGBoost)
```bash
pip install xgboost
```

### Running the Notebook

1. Open `Paes_Jessica_Capstone2_Code.ipynb` in Jupyter Notebook or VS Code
2. Run all cells sequentially
3. The notebook will:
   - Load data from the online source
   - Process and create features
   - Train multiple models
   - Compare performance across genders
   - Display visualisations

---

## 📁 Project Structure

```
capstone2_jessica_paes/
├── Paes_Jessica_Capstone2_Code.ipynb      # Main Jupyter notebook
├── Paes_Jessica_Capstone2_BusinessDoc.md  # Business problem document
├── Paes_Jessica_Capstone2_Presentation.html # HTML presentation
├── Paes_Jessica_Capstone2_README.md       # This file
└── Presentation_Script.md                  # Presentation speaking notes (optional)
```

---

## 📤 Submission Instructions

### Generate PDF Files (Required)

1. **Business Doc PDF:**
   - Open `Paes_Jessica_Capstone2_BusinessDoc.md` in VS Code
   - Press `Ctrl+Shift+P` → "Markdown: Export to PDF"
   - Or use https://md2pdf.netlify.app/

2. **Presentation PDF:**
   - Open `Paes_Jessica_Capstone2_Presentation.html` in Chrome
   - Press `Ctrl+P` → Save as PDF
   - Save as `Paes_Jessica_Capstone2_Presentation.pdf`

3. **Model Files:**
   - Run the complete notebook to generate `.pkl` files

---

## 📈 Model Comparison

| Model | Accuracy | F1-Score |
|-------|----------|----------|
| Random Forest | 95.7% | 95.7% |
| Logistic Regression | 95.5% | 95.5% |
| Gradient Boosting | 95.3% | 95.3% |
| SVM | 94.8% | 94.8% |
| KNN | 89.2% | 89.1% |

### Gender Comparison

| Group | Samples | F1-Score |
|-------|---------|----------|
| All | 2,436 | 95.7% |
| Male | 805 | 95.6% |
| Female | 1,631 | 95.7% |

---

## ⚠️ Ethical Disclaimer

This model is developed for **educational and research purposes only**. It is NOT intended for clinical diagnosis or real-world deployment without professional oversight.

- Mental health assessment should only be conducted by qualified professionals
- The predictions made by this model should not be used to make decisions affecting individuals
- Privacy and informed consent are essential for any application

---

## 📚 References

1. Costa, P. T., & McCrae, R. R. (1992). *Revised NEO Personality Inventory (NEO-PI-R) and NEO Five-Factor Inventory (NEO-FFI) professional manual.* Psychological Assessment Resources.

2. BMC Psychiatry - Studies on personality traits and depression/anxiety

3. American Psychological Association - Ethical guidelines for psychological assessment

---

## 📞 Contact

**Jessica Paes**  
AI Tech Institute  
December 2025
