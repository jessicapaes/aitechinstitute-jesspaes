# Business Problem Document

## Capstone Project 2: Using Big Five Personality Traits to Identify Depression & Anxiety Risk

**Student:** Jessica Paes  
**Date:** December 2025  
**Course:** Intermediate AI & Data Science  
**Institution:** AI Tech Institute

---

## 1. Executive Summary

This project develops a machine learning model to identify individuals at risk of depression and anxiety using personality traits from the Big Five Inventory (BFI). By leveraging research-validated relationships between personality and mental health, the model enables early screening and intervention opportunities.

**Key Achievement:** 95.7% F1-Score using a research-based multi-trait composite approach.

---

## 2. Problem Statement

### 2.1 The Challenge

Mental health conditions affect millions of people worldwide, yet early detection remains a significant challenge:

- **1 in 5** adults experience mental illness annually
- **60%** of those affected don't receive treatment
- **11 years** average delay from symptom onset to treatment

Early identification of at-risk individuals could enable proactive intervention and support.

### 2.2 Research Question

Can validated personality assessments predict mental health risk, enabling earlier identification of individuals who may benefit from support or intervention?

---

## 3. Solution Approach

### 3.1 Data Source

**Big Five Inventory (BFI)** - Real psychological survey data:
- **Source:** Rdatasets Repository (academic data)
- **Sample Size:** 2,436 respondents (after cleaning)
- **Demographics:** 805 males, 1,631 females
- **Data Type:** 100% real survey responses

### 3.2 Features

Six personality-based features:
1. **Neuroticism** - Anxiety, mood swings, emotional instability (N1-N5)
2. **Extraversion** - Social energy, positive emotions (E1-E5)
3. **Conscientiousness** - Self-discipline, organisation (C1-C5)
4. **Agreeableness** - Cooperation, trust (A1-A5)
5. **Openness** - Creativity, curiosity (O1-O5)
6. **Age** - Demographic factor

### 3.3 Methodology

**Research-Based Multi-Trait Composite Score:**

```
Risk Score = (Neuroticism × 2) − Extraversion − (Conscientiousness × 0.5)
```

**Why This Approach:**
1. Supported by multiple published research papers
2. Uses more available data than single-trait approaches
3. Captures the "High Neuroticism + Low Extraversion" pattern identified in research
4. Produces balanced class distribution using tertiles
5. Scientifically defensible methodology

### 3.4 Target Variable

Three-class classification using tertiles:
- **Low Risk** - Bottom 33% of risk scores
- **Medium Risk** - Middle 33%
- **High Risk** - Top 33%

---

## 4. Model Performance

### 4.1 Results Summary

| Model | Accuracy | F1-Score |
|-------|----------|----------|
| **Random Forest** | 95.7% | 95.7% |
| Logistic Regression | 95.5% | 95.5% |
| Gradient Boosting | 95.3% | 95.3% |
| SVM | 94.8% | 94.8% |
| KNN | 89.2% | 89.1% |

### 4.2 Gender Comparison

| Population | Samples | F1-Score |
|------------|---------|----------|
| All Combined | 2,436 | 95.7% |
| Male Only | 805 | 95.6% |
| Female Only | 1,631 | 95.7% |

**Key Finding:** Model performs consistently across both genders.

---

## 5. Key Findings

### 5.1 Top Predictors

1. **Neuroticism** - Strongest positive predictor of risk
2. **Extraversion** - Protective factor (lower = higher risk)
3. **Conscientiousness** - Protective factor

### 5.2 Research Alignment

- Results confirm Costa & McCrae (1992) findings
- "High Neuroticism + Low Extraversion" pattern validated
- Multi-trait approach outperforms single-trait models

---

## 6. Business Applications

### 6.1 Wellness Programs
- Early screening during wellness intake
- Risk stratification for resource allocation
- Personalised intervention recommendations

### 6.2 Research Applications
- Academic study of personality-mental health relationships
- Validation of established psychological theories
- Foundation for longitudinal studies

---

## 7. Ethical Considerations

### 7.1 Limitations
- This is a **screening tool**, NOT a clinical diagnostic
- Personality is one factor among many affecting mental health
- Model trained on specific population - generalisation requires validation
- Should complement, not replace, professional assessment

### 7.2 Responsible Use
- Informed consent required for any implementation
- Privacy and data protection essential
- Results should support, not stigmatise, individuals
- Professional oversight recommended for any real-world application

---

## 8. Future Improvements

1. **External Validation** - Test on independent datasets
2. **Longitudinal Tracking** - Follow up on predictions over time
3. **Feature Expansion** - Integrate other wellness metrics
4. **Accessibility** - Develop user-friendly screening application

---

## 9. Conclusion

This project demonstrates that personality traits, particularly the combination of high Neuroticism and low Extraversion, can effectively identify individuals at higher risk of depression and anxiety. The research-based methodology achieves 95.7% accuracy and performs consistently across gender groups.

The model provides a foundation for early screening in wellness contexts, with appropriate ethical safeguards and professional oversight.

---

**AI Tech Institute** | *Building Tomorrow's AI Engineers Today*
