# Module 2: Loan Default Prediction Engine
**Mesin Prediksi Risiko Gagal Bayar Berbasis Machine Learning**

---

## 📌 Tujuan Module

Module 2 bertanggung jawab untuk:
1. **Memprediksi probabilitas default** pinjaman berdasarkan karakteristik peminjam dan pinjaman
2. **Mengklasifikasikan risk category** (Low/Medium/High)
3. **Menjelaskan prediksi** menggunakan feature importance dan SHAP values
4. **Mengintegrasikan financial health metrics** dari Module 1 untuk prediksi yang lebih akurat

---

## 🏗️ Arsitektur Module 2

```
Input: Loan Request + Financial Metrics (from Module 1)
    ├── Loan Data:
    │   ├── jumlah_pinjaman
    │   ├── durasi_hari
    │   ├── jenis_pinjaman
    │   ├── provinsi
    │   ├── status_peminjam (Baru/Lama)
    │   ├── sektor_usaha
    │   ├── pendidikan
    │   └── jenis_jaminan
    │
    └── Financial Metrics (from Module 1):
        ├── debt_to_income_ratio
        ├── expense_ratio
        ├── savings_ratio
        └── disposable_income_ratio

         ↓

[1] FEATURE ASSEMBLY
    └── Combine & Engineer Features
        • Clean & impute missing values
        • Engineer derived features
        • Aggregate statistics
        • Ensure feature schema consistency

         ↓

[2] MODEL INFERENCE
    └── LightGBM Gradient Boosting Model
        • Frozen pre-trained model
        • 30+ features input
        • Output: Default probability (0.0 - 1.0)

         ↓

[3] EXPLAINER
    └── Generate Explanations
        • SHAP values for feature contributions
        • Risk category classification
        • Confidence scoring
        • Top risk & protective factors

         ↓

Output: Prediction + Explanation
    ├── default_prediction: 0 or 1
    ├── default_probability: 0.0 to 1.0
    ├── risk_category: "low" / "medium" / "high"
    ├── confidence: "low" / "medium" / "high"
    └── explanation:
        ├── feature_contributions
        ├── top_risk_factors
        └── top_protective_factors
```

---

## 🔧 Component 1: Feature Assembly

### Prinsip Desain
- **Stateless Transformation:** No side effects, reproducible
- **Consistent with Training:** Feature engineering HARUS sama dengan training pipeline
- **Handle Missing Values:** Imputation strategy yang sama dengan training
- **No Data Leakage:** Hanya gunakan informasi yang tersedia saat prediction time

### Step 1: Data Cleaning

**Masalah yang Sering Ditemui:**
1. **Negative Duration:** `durasi_hari = -90`
   - Fix: Ambil absolute value
   - Rationale: Kemungkinan input error, maksudnya 90 hari

2. **Future Dates:** `tanggal_pencairan = "2025-12-25"` (saat sistem berjalan di 2024)
   - Fix: Kurangi 1 tahun
   - Rationale: Input error tahun

3. **Missing Tanggal:** Tidak ada `tanggal_pencairan`
   - Fix: Gunakan tanggal saat ini
   - Rationale: Default ke current date

### Step 2: Imputation Strategy

**Prinsip Imputation:**
- Gunakan **median ratio dari training data**, BUKAN median absolut
- Mengapa? Karena scale-invariant dan lebih robust

**Contoh Imputation:**

**❌ Pendekatan Naive (Median Absolut):**
```
Missing total_pengembalian → Impute dengan median = 30,000,000
```
Problem: User yang pinjam 5 juta vs 500 juta mendapat imputation yang sama!

**✅ Pendekatan Sistem Ini (Median Ratio):**
```
Dari training data: total_pengembalian / jumlah_pinjaman ≈ 1.15 (median)

Missing total_pengembalian:
→ Impute dengan: jumlah_pinjaman × 1.15

User A: Pinjam 5 juta → Impute total_pengembalian = 5.75 juta
User B: Pinjam 500 juta → Impute total_pengembalian = 575 juta
```

**Imputation Rules:**
```
MEDIAN_RETURN_RATIO = 1.15  (dari training data)
MEDIAN_LENDER_RATIO = 0.95  (dari training data)
MEDIAN_DURATION = 90        (dari training data)

IF total_pengembalian is missing:
    total_pengembalian = jumlah_pinjaman × 1.15

IF porsi_pengembalian_lender is missing:
    porsi_pengembalian_lender = total_pengembalian × 0.95

IF durasi_hari is missing:
    durasi_hari = 90

IF categorical fields missing:
    Fill with "Unknown"
```

### Step 3: Feature Engineering

**Derived Features yang Dihasilkan:**

#### 1. Temporal Features
**Mengapa Penting?**
Seasonality dan time trends dapat mempengaruhi default rate.

```
From tanggal_pencairan:
├── month: Bulan pencairan (1-12)
├── quarter: Quarter (1-4)
├── day_of_week: Hari dalam minggu (0-6)
└── is_month_end: Boolean (hari 25-31)
```

**Insight:**
- Pinjaman yang dicairkan akhir bulan mungkin lebih risky (cashflow tight)
- Seasonality: Default rate mungkin berbeda per quarter

#### 2. Financial Ratios
```
daily_payment = total_pengembalian / durasi_hari
payment_burden = daily_payment / (income / 30)  # Assuming monthly income
```

**Insight:**
- `payment_burden` mengukur berapa persen dari daily income yang harus dialokasikan untuk cicilan
- Semakin tinggi, semakin berat beban cicilan

#### 3. Loan Characteristics
```
loan_intensity = jumlah_pinjaman / durasi_hari
```

**Insight:**
- Pinjaman short-term dengan amount besar memiliki risk profile berbeda
- High loan_intensity = high daily payment pressure

#### 4. Aggregation Features (Statistical Encoding)

**Mengapa Diperlukan?**
Categorical features seperti `provinsi` memiliki banyak unique values. Jika di-encode dengan one-hot, akan menghasilkan ratusan features (curse of dimensionality).

**Pendekatan Traditional (One-Hot Encoding):**
```
provinsi:
├── provinsi_DKI_Jakarta: 1/0
├── provinsi_Jawa_Barat: 1/0
├── provinsi_Jawa_Timur: 1/0
└── ... (34 columns untuk 34 provinsi)
```
Problem: Sparse matrix, overfitting, tidak generalize

**✅ Pendekatan Sistem Ini (Aggregation/Target Encoding):**
```
Dari training data, hitung rata-rata default rate per provinsi:

provinsi_avg_default_rate:
├── DKI Jakarta: 0.08  (8% default rate di DKI Jakarta)
├── Jawa Barat: 0.12   (12% default rate di Jawa Barat)
└── Papua: 0.15        (15% default rate di Papua)

Untuk prediction:
IF provinsi = "DKI Jakarta":
    provinsi_default_rate_feature = 0.08
```

**Keunggulan:**
- ✅ Single numeric feature, bukan puluhan binary features
- ✅ Capture regional risk differences
- ✅ Handle unseen categories ("Unknown" → use global average)

**Aggregation Features yang Dibuat:**
```
1. provinsi_avg_default_rate
2. jenis_pinjaman_avg_default_rate
3. sektor_usaha_avg_default_rate
4. pendidikan_avg_default_rate
5. jenis_jaminan_avg_default_rate
```

#### 5. Integration dengan Module 1 (Financial Health Features)

**Critical Integration Point:**

Module 2 menerima financial metrics dari Module 1:
```
financial_metrics (from Module 1):
├── debt_to_income_ratio
├── expense_ratio
├── savings_ratio
└── disposable_income_ratio
```

**Ditambahkan ke feature set:**
```
features_df['debt_to_income_ratio'] = financial_metrics['debt_to_income_ratio']
features_df['expense_ratio'] = financial_metrics['expense_ratio']
...
```

**Mengapa Ini Powerful?**

Tanpa Module 1:
- Model hanya melihat loan characteristics (amount, duration, type)
- Tidak tahu financial capacity borrower

Dengan Module 1:
- Model tahu DTI ratio, expense pattern, savings adequacy
- Bisa assess affordability, bukan hanya loan characteristics
- **Contoh:** Pinjaman 50 juta untuk user dengan DTI 2.0 vs DTI 8.0 akan diprediksi berbeda

### Step 4: Feature Schema Consistency

**Critical Requirement:**
Feature order dan naming HARUS persis sama dengan training.

**Mengapa?**
Model di-train dengan feature order tertentu:
```
Training: [jumlah_pinjaman, durasi_hari, dti_ratio, ...]
```

Jika prediction menggunakan order berbeda:
```
Prediction: [durasi_hari, jumlah_pinjaman, dti_ratio, ...]
```
→ Model akan salah interpretasi features → Prediksi kacau!

**Solusi:**
Sistem menyimpan expected feature schema dan melakukan validation:
```
expected_features = [
    'jumlah_pinjaman',
    'durasi_hari',
    'debt_to_income_ratio',
    ...
]

# Reorder features to match expected schema
features_df = features_df[expected_features]
```

---

## 🤖 Component 2: Model Inference (LightGBM)

### Mengapa LightGBM?

**Algoritma Alternatives:**
| Algorithm | Pros | Cons |
|-----------|------|------|
| Logistic Regression | Simple, explainable | Linear, can't capture complex patterns |
| Random Forest | Robust, handles non-linearity | Slower, larger model size |
| XGBoost | High accuracy | Computationally expensive |
| **LightGBM** | Fast, accurate, handles categorical, memory efficient | Needs careful tuning |

**Keunggulan LightGBM untuk Use Case Ini:**
1. **Gradient Boosting:** Iteratively improve predictions
2. **Leaf-wise Growth:** More accurate than level-wise
3. **Categorical Support:** Native handling of categorical features
4. **Fast Inference:** Critical untuk production
5. **Feature Importance:** Built-in explainability

### Bagaimana LightGBM Bekerja?

**Konsep Dasar: Ensemble of Decision Trees**

**❌ Single Decision Tree (Overfitting):**
```
Tree 1:
    IF jumlah_pinjaman > 50M THEN default = 1
    ELSE default = 0
```
Problem: Terlalu simplistic, overfitting

**✅ Gradient Boosting (Ensemble of Weak Trees):**
```
Tree 1: Makes initial prediction
    → Error = Actual - Prediction

Tree 2: Learns to predict the error from Tree 1
    → New Prediction = Tree1 + Tree2

Tree 3: Learns to predict remaining error
    → New Prediction = Tree1 + Tree2 + Tree3

... (100-1000 trees)

Final Prediction = Σ(all trees)
```

**Mengapa Powerful?**
- Setiap tree fokus pada memperbaiki error dari tree sebelumnya
- Kombinasi weak learners → Strong learner
- Capture non-linear relationships

### Model Architecture

**Training Configuration:**
```
num_trees: ~100-500 (optimal dari tuning)
max_depth: 6-10 (prevent overfitting)
learning_rate: 0.01-0.1 (step size untuk learning)
num_leaves: 31-127 (complexity control)
```

**Features Used (~30+ features):**
```
Loan Characteristics:
├── jumlah_pinjaman
├── durasi_hari
├── daily_payment
├── loan_intensity
├── month, quarter, day_of_week

Categorical (Encoded):
├── provinsi_default_rate
├── jenis_pinjaman_default_rate
├── sektor_usaha_default_rate
├── pendidikan_default_rate
├── jenis_jaminan_default_rate

Financial Health (from Module 1):
├── debt_to_income_ratio
├── expense_ratio
├── savings_ratio
└── disposable_income_ratio
```

### Model Output

**Probability Output:**
```
Model outputs: Raw probability (0.0 to 1.0)

Example:
└── 0.15 → 15% probability of default
```

**Classification Threshold:**
```
IF probability >= 0.5:
    prediction = 1 (Default)
ELSE:
    prediction = 0 (Non-Default)
```

**Risk Category:**
```
IF probability < 0.15:
    risk_category = "low"
ELIF probability < 0.35:
    risk_category = "medium"
ELSE:
    risk_category = "high"
```

---

## 📊 Component 3: Explainer (SHAP-based)

### Mengapa Perlu Explainability?

**Black Box Problem:**
```
User: "Mengapa default probability saya 25%?"
Black Box Model: "Karena model mengatakan begitu."
User: "???"
```

**With Explainability:**
```
User: "Mengapa default probability saya 25%?"
Explainer:
├── DTI ratio tinggi (4.5) → +8% contribution to default risk
├── Loan amount besar (100M) → +5% contribution
├── Duration pendek (30 hari) → +4% contribution
├── Savings ratio rendah (1.0) → +3% contribution
└── Provinsi risk sedang → +2% contribution
    Total Impact: Baseline 5% + 22% = 27% ≈ 25%
```

### SHAP (SHapley Additive exPlanations)

**Konsep Dasar:**
SHAP values menjelaskan kontribusi setiap feature terhadap prediksi.

**Formula (Simplified):**
```
Prediction = Base Value + Σ(SHAP values untuk setiap feature)

Example:
Base Value (Average default rate) = 0.05 (5%)

SHAP values:
├── debt_to_income_ratio: +0.08
├── jumlah_pinjaman: +0.05
├── savings_ratio: -0.02 (protective factor)
└── ...

Final Prediction = 0.05 + 0.08 + 0.05 - 0.02 + ... = 0.25 (25%)
```

**Interpretasi SHAP Values:**
- **Positive SHAP value:** Feature ini MENINGKATKAN risk
- **Negative SHAP value:** Feature ini MENURUNKAN risk
- **Magnitude:** Seberapa besar kontribusinya

### Feature Contributions Breakdown

**Output dari Explainer:**

```json
{
    "prediction_probability": 0.25,
    "baseline_probability": 0.05,
    "feature_contributions": [
        {
            "feature": "debt_to_income_ratio",
            "value": 4.5,
            "importance": 0.15,
            "contribution": 0.08,
            "impact": "increases_risk"
        },
        {
            "feature": "savings_ratio",
            "value": 1.2,
            "importance": 0.08,
            "contribution": -0.02,
            "impact": "decreases_risk"
        },
        ...
    ],
    "top_risk_factors": [
        "High DTI ratio (4.5x income)",
        "Large loan amount (100M)",
        "Short duration (30 days)"
    ],
    "top_protective_factors": [
        "Good expense control (60% expense ratio)",
        "Positive cashflow"
    ]
}
```

### Confidence Scoring

**Bagaimana Confidence Dihitung?**

```
Prediction probability distribution:

High Confidence:
├── probability very low (< 0.10) → Clearly low risk
└── probability very high (> 0.70) → Clearly high risk

Medium Confidence:
├── 0.10 - 0.30 or 0.50 - 0.70

Low Confidence:
└── 0.30 - 0.50 (Borderline, uncertain)
```

**Mengapa Penting?**
- Borderline cases memerlukan human review
- High confidence predictions bisa di-automate
- Transparent risk management

---

## 🎯 Keunggulan Machine Learning di Module 2

### 1. Capture Complex Patterns

**Rule-Based Tidak Bisa:**
```
"High risk IF jumlah_pinjaman > 50M"
```
Problem: Pinjaman 100M untuk orang dengan income 1M vs 100M sangat berbeda!

**ML Bisa:**
```
Model learns: Risk = f(jumlah_pinjaman, income, dti_ratio, interactions, ...)

Capture non-linear interactions:
├── Large loan + Low DTI → Low risk
├── Large loan + High DTI → High risk
├── Large loan + Short duration → Very high risk
└── Large loan + Short duration + High savings → Medium risk
```

### 2. Learn from Historical Data

**Rule-Based:**
- Manually define: "DTI > 6.0 = High Risk"
- Based on domain knowledge

**ML:**
- Automatically discovers: "DTI > 6.0 correlates with 35% default rate"
- Plus: Discovers interactions you didn't know
- Example: "High DTI in Jakarta less risky than in remote areas"

### 3. Adaptive Feature Importance

**Different Features Matter for Different Users:**

For high-income users:
- Savings ratio → More important
- Loan amount → Less important

For low-income users:
- DTI ratio → Most critical
- Duration → Very important

ML automatically learns these nuances.

### 4. Probability Output (Not Binary)

**Rule-Based:**
```
Risk = "High" or "Low" (Binary)
```

**ML:**
```
Default Probability = 0.25 (25%)
→ Can set different thresholds untuk different risk appetites
→ Can price loans based on risk (higher rate for higher risk)
```

---

## ⚠️ Limitations & Mitigations

### Limitation 1: Black Box Nature
**Problem:** Model kompleks sulit dijelaskan

**Mitigation:**
- ✅ SHAP explainability
- ✅ Feature importance ranking
- ✅ Individual prediction breakdowns

### Limitation 2: Training Data Dependency
**Problem:** Model hanya sebaik training data-nya

**Mitigation:**
- ✅ Careful data quality checks
- ✅ Outlier detection & handling
- ✅ Bias detection & mitigation

### Limitation 3: Concept Drift
**Problem:** Patterns berubah seiring waktu

**Mitigation:**
- ✅ Model monitoring (track prediction accuracy)
- ✅ Periodic retraining schedule
- ✅ Alert system untuk performance degradation

### Limitation 4: Overfitting Risk
**Problem:** Model too complex, memorize training data

**Mitigation:**
- ✅ Cross-validation during training
- ✅ Regularization (max_depth, min_samples_leaf)
- ✅ Out-of-sample testing

---

## 🔄 Integration dengan Module Lain

### Input dari Module 1
```
Module 1 Output → Module 2 Input:
├── debt_to_income_ratio → Critical feature
├── expense_ratio → Affordability indicator
├── savings_ratio → Buffer capacity
└── disposable_income_ratio → Cashflow indicator
```

**Impact:**
Tanpa Module 1 metrics, model accuracy drop ~10-15%!

### Output ke Module 3
```
Module 2 Output → Module 3 Input:
├── default_probability → Risk assessment
├── explanation → Root cause identification
└── feature_contributions → Scenario impact analysis
```

---

## 🔬 Model Performance Metrics

### Classification Metrics

**1. AUC-ROC (Area Under Curve - Receiver Operating Characteristic):**
- Measures: Ability untuk distinguish default vs non-default
- Target: > 0.80 (good), > 0.85 (excellent)
- Interpretation: 0.85 means 85% probability model ranks a random defaulter higher than random non-defaulter

**2. Precision & Recall Trade-off:**
```
Precision = TP / (TP + FP)
└── "Among predicted defaults, how many actually defaulted?"

Recall = TP / (TP + FN)
└── "Among actual defaults, how many did we catch?"
```

**Business Impact:**
- High Precision: Few false alarms (don't reject good borrowers)
- High Recall: Catch most defaulters (minimize losses)
- Trade-off: Adjust threshold based on business priority

**3. Calibration:**
- Predicted 20% default → Actually observe ~20% default?
- Important untuk probability interpretation

---

## 🎯 Model vs Rules: Complementary Roles

**Module 1 (Rules):**
- ✅ Transparent baseline
- ✅ Explainable thresholds
- ✅ No training data needed
- ❌ Can't capture complexity

**Module 2 (ML):**
- ✅ Capture complex patterns
- ✅ Learn from data
- ✅ Probabilistic output
- ❌ Black box (mitigated with SHAP)

**Together:**
- Module 1 provides explainable health assessment
- Module 2 provides accurate risk prediction
- Module 3 combines both untuk actionable insights

---

## 📝 Summary

**Module 2 adalah prediction engine dari sistem:**

✅ **Strengths:**
- High accuracy dari gradient boosting
- Capture complex non-linear patterns
- Probabilistic output (risk quantification)
- SHAP-based explainability
- Integration dengan Module 1 untuk comprehensive assessment

⚠️ **Limitations:**
- Requires quality training data
- Black box nature (mitigated)
- Potential for concept drift
- Computational overhead

🎯 **Role dalam Sistem:**
- Core prediction engine
- Risk quantification (probability)
- Pattern discovery yang tidak bisa ditangkap rules
- Foundation untuk Module 3 recommendations

**Next:** Module 3 akan mengintegrasikan output dari Module 1 & 2 untuk generate actionable insights dan recommendations.
