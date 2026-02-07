# Module 1: Health Assessment Engine
**Mesin Analisis Kesehatan Finansial Berbasis Rule-Based System**

---

## 📌 Tujuan Module

Module 1 bertanggung jawab untuk:
1. **Mengukur kesehatan finansial** seseorang berdasarkan profil keuangannya
2. **Mengidentifikasi risk flags** yang perlu diperhatikan
3. **Menentukan financial persona** untuk personalisasi insight
4. **Memberikan baseline assessment** yang transparan dan explainable

---

## 🏗️ Arsitektur Module 1

```
Input: Financial Profile
    ├── income: Pendapatan bulanan
    ├── fixed_expenses: Pengeluaran tetap bulanan
    ├── variable_expenses: Pengeluaran variabel bulanan
    ├── savings: Total tabungan
    └── debt: Total utang

         ↓

[1] METRICS CALCULATOR
    └── Calculate 8 key metrics
        • DTI Ratio
        • Expense Ratio
        • Savings Ratio
        • Disposable Income & Ratio
        • Net Cashflow

         ↓

[2] RULES ENGINE
    └── Apply thresholds & business rules
        • Assess each metric
        • Assign scores (0-100)
        • Flag risks

         ↓

[3] CLUSTERING ENGINE
    └── Assign Financial Persona
        • Pattern matching
        • Behavioral profiling

         ↓

Output: Health Assessment
    ├── score: 0-100
    ├── status: "Healthy" / "Warning" / "At Risk"
    ├── metrics: All calculated metrics
    ├── risk_flags: List of identified risks
    ├── persona: Financial persona
    └── insights: Actionable insights
```

---

## 🔢 Component 1: Metrics Calculator

### Prinsip Desain
- **Scale-Invariant:** Semua metrics berbasis rasio, bukan nilai absolut
- **Safe Division:** Handle edge cases (income = 0, dll)
- **Pure Functions:** No side effects, stateless
- **Anti-Bias:** Tidak diskriminasi berdasarkan income level

### Metric 1: Debt-to-Income (DTI) Ratio
**Formula:**
```
DTI Ratio = Total Debt / Monthly Income
```

**Interpretasi:**
- DTI = 2.0 → Debt adalah 2x pendapatan bulanan
- DTI = 5.0 → Debt adalah 5x pendapatan bulanan

**Mengapa Rasio, Bukan Absolut?**

❌ **Pendekatan Absolut (Bias):**
```
IF debt > 50_000_000 THEN high_risk = TRUE
```
- User A: Income 5 juta, Debt 60 juta → High risk
- User B: Income 50 juta, Debt 60 juta → High risk
- Padahal User B jauh lebih mampu membayar!

✅ **Pendekatan Rasio (Anti-Bias):**
```
DTI_A = 60_000_000 / 5_000_000 = 12.0 (Very High Risk)
DTI_B = 60_000_000 / 50_000_000 = 1.2 (Low Risk)
```
- Penilaian adil berdasarkan kemampuan bayar relatif

**Threshold Guidelines:**
| DTI Ratio | Level | Penjelasan |
|-----------|-------|------------|
| < 1.0 | Excellent | Debt sangat ringan |
| 1.0 - 3.0 | Good | Debt terkendali |
| 3.0 - 6.0 | Warning | Debt mulai berat |
| 6.0 - 12.0 | At Risk | Debt sangat berat |
| > 12.0 | Critical | Debt tidak sustainable |

---

### Metric 2: Expense Ratio
**Formula:**
```
Expense Ratio = (Fixed Expenses + Variable Expenses) / Monthly Income
```

**Interpretasi:**
- Expense Ratio = 0.70 → 70% income terpakai untuk expenses
- Semakin tinggi, semakin sedikit ruang untuk savings/debt payment

**Threshold Guidelines:**
| Expense Ratio | Level | Penjelasan |
|---------------|-------|------------|
| < 0.50 | Excellent | Sangat efisien, banyak ruang untuk saving |
| 0.50 - 0.70 | Good | Efisien, cukup ruang untuk saving |
| 0.70 - 0.85 | Warning | Kurang efisien, ruang saving terbatas |
| 0.85 - 1.00 | At Risk | Sangat tinggi, hampir tidak ada ruang |
| > 1.00 | Critical | Defisit, pengeluaran > pendapatan |

---

### Metric 3: Savings Ratio
**Formula:**
```
Savings Ratio = Total Savings / Monthly Income
```

**Interpretasi:**
- Savings Ratio = 3.0 → Savings setara 3 bulan income (emergency fund 3 bulan)
- Savings Ratio = 6.0 → Savings setara 6 bulan income (emergency fund ideal)

**Mengapa Penting?**
Emergency fund adalah "shock absorber" untuk kejadian tak terduga:
- Kehilangan pekerjaan
- Sakit
- Kerusakan aset
- Tanpa emergency fund, kejadian ini langsung jadi financial crisis

**Threshold Guidelines:**
| Savings Ratio | Level | Emergency Fund Coverage |
|---------------|-------|------------------------|
| ≥ 6.0 | Excellent | 6+ bulan, sangat aman |
| 3.0 - 6.0 | Good | 3-6 bulan, cukup aman |
| 1.0 - 3.0 | Warning | 1-3 bulan, kurang aman |
| < 1.0 | Critical | < 1 bulan, sangat rentan |

---

### Metric 4: Disposable Income
**Formula:**
```
Disposable Income = Income - Fixed Expenses - Variable Expenses
Disposable Income Ratio = Disposable Income / Income
```

**Interpretasi:**
- Disposable Income Ratio = 0.25 → 25% income tersisa setelah semua expenses
- Ini adalah "ruang bernafas" untuk savings, investasi, atau cicilan debt baru

**Threshold Guidelines:**
| Disposable Ratio | Level | Penjelasan |
|------------------|-------|------------|
| ≥ 0.30 | Excellent | 30%+ tersisa, sangat sehat |
| 0.15 - 0.30 | Good | 15-30% tersisa, sehat |
| 0.05 - 0.15 | Warning | 5-15% tersisa, tipis |
| < 0.05 | Critical | < 5% atau negatif, tidak sustainable |

---

### Metric 5: Net Cashflow
**Formula:**
```
Net Cashflow = Income - Fixed Expenses - Variable Expenses
```

**Interpretasi:**
- Net Cashflow > 0 → Surplus (sehat)
- Net Cashflow = 0 → Break-even (rentan)
- Net Cashflow < 0 → Defisit (tidak sustainable)

---

## ⚖️ Component 2: Rules Engine

### Prinsip Desain
- **Deterministic:** Input yang sama selalu menghasilkan output yang sama
- **Transparent:** Setiap keputusan bisa dijelaskan dengan jelas
- **Threshold-Based:** Menggunakan threshold yang telah divalidasi
- **Weighted Scoring:** Tidak semua metric sama pentingnya

### Weighted Scoring System

```
Final Health Score = Weighted Average dari 4 Komponen:

1. DTI Assessment      (Weight: 30%)
2. Expense Assessment  (Weight: 25%)
3. Savings Assessment  (Weight: 25%)
4. Cashflow Assessment (Weight: 20%)
```

**Mengapa DTI Paling Tinggi?**
Debt burden adalah predictor terkuat dari financial distress. Seseorang dengan debt tinggi:
- Rentan terhadap interest rate shocks
- Terbatas flexibility finansialnya
- Berisiko spiral debt jika ada shock

### Contoh Perhitungan

**User Profile:**
```
Income: 15,000,000
Fixed Expenses: 8,000,000
Variable Expenses: 3,000,000
Savings: 20,000,000
Debt: 50,000,000
```

**Step 1: Calculate Metrics**
```
DTI Ratio = 50,000,000 / 15,000,000 = 3.33
Expense Ratio = (8,000,000 + 3,000,000) / 15,000,000 = 0.733 (73.3%)
Savings Ratio = 20,000,000 / 15,000,000 = 1.33 months
Disposable Income Ratio = 4,000,000 / 15,000,000 = 0.267 (26.7%)
```

**Step 2: Assess Each Metric**
```
DTI = 3.33 → "Warning" level → Score: 50/100
Expense = 0.733 → "Warning" level → Score: 50/100
Savings = 1.33 → "Warning" level → Score: 50/100
Cashflow = 0.267 → "Good" level → Score: 80/100
```

**Step 3: Calculate Weighted Score**
```
Final Score = (50 × 0.30) + (50 × 0.25) + (50 × 0.25) + (80 × 0.20)
            = 15 + 12.5 + 12.5 + 16
            = 56 / 100
```

**Step 4: Assign Status**
```
Score 56 → "Warning" (Status range: 50-74)
```

### Risk Flag Identification

Sistem mengidentifikasi risk flags spesifik:

| Risk Flag | Condition | Impact |
|-----------|-----------|--------|
| `high_debt_burden` | DTI > 6.0 | Critical - Debt tidak sustainable |
| `excessive_expenses` | Expense Ratio > 0.85 | High - Tidak ada ruang untuk saving |
| `insufficient_savings` | Savings Ratio < 1.0 | Medium - Rentan terhadap shock |
| `negative_cashflow` | Disposable Income < 0 | Critical - Defisit bulanan |

---

## 👥 Component 3: Clustering Engine (Financial Persona)

### Mengapa Persona, Bukan Credit Score?

**Credit Score Tradisional:**
- ❌ Label judgemental: "Good Credit" vs "Bad Credit"
- ❌ Binary classification: Approved vs Rejected
- ❌ Tidak memberikan insight actionable

**Financial Persona:**
- ✅ Deskriptif, bukan judgemental
- ✅ Menggambarkan behavioral pattern
- ✅ Memberikan context untuk recommendations

### 9 Financial Personas

#### 1. Conservative Saver
**Pattern:**
- DTI < 1.0 (Low debt)
- Expense Ratio < 0.60 (Efficient spending)
- Savings Ratio ≥ 6.0 (Strong emergency fund)

**Profile:**
- Risk-averse
- Prioritize security over growth
- Strong financial discipline

**Recommendations:**
- Consider investing surplus for growth
- Balance safety with opportunity cost
- Explore low-risk investment options

---

#### 2. Stable & Balanced
**Pattern:**
- DTI < 3.0 (Moderate debt)
- Expense Ratio < 0.75 (Controlled spending)
- Savings Ratio ≥ 3.0 (Adequate emergency fund)
- Disposable Ratio ≥ 0.15 (Healthy cashflow)

**Profile:**
- Well-balanced financial management
- Sustainable lifestyle
- Good financial habits

**Recommendations:**
- Maintain current trajectory
- Consider gradual debt reduction
- Explore additional income streams

---

#### 3. High Earner - High Spender
**Pattern:**
- DTI < 2.0 (Low debt relative to income)
- Expense Ratio ≥ 0.70 (High spending)
- Savings Ratio ≥ 2.0 (Despite high spending, still saves)

**Profile:**
- High income, high lifestyle
- Can afford expenses
- But vulnerable to income shocks

**Recommendations:**
- Build larger emergency fund (income shock protection)
- Review discretionary spending
- Automate savings to prevent lifestyle inflation

---

#### 4. Debt Pressured
**Pattern:**
- DTI ≥ 6.0 (Very high debt burden)

**Profile:**
- Struggling with debt
- Most income goes to debt servicing
- Limited financial flexibility

**Recommendations:**
- Priority: Debt reduction strategy
- Consider debt consolidation
- Cut non-essential expenses
- Seek additional income sources

---

#### 5. Cashflow Challenged
**Pattern:**
- Disposable Ratio ≤ 0.05 (Very low or negative cashflow)

**Profile:**
- Living paycheck to paycheck
- No buffer for unexpected expenses
- High financial stress

**Recommendations:**
- Urgent: Expense optimization
- Identify income increase opportunities
- Create strict budget
- Build minimal emergency fund (1-2 weeks expenses)

---

#### 6. Building Financial Foundation
**Pattern:**
- Savings Ratio < 3.0 (Low savings)
- Expense Ratio < 0.75 (Controlled expenses)
- Disposable Ratio ≥ 0.10 (Some cashflow)

**Profile:**
- Early career or rebuilding finances
- Good habits, but not yet accumulated wealth
- On the right track

**Recommendations:**
- Automate savings (10-15% of income)
- Focus on emergency fund building
- Avoid new debt
- Invest in skills for income growth

---

#### 7. Frugal & Low Savings
**Pattern:**
- Expense Ratio < 0.50 (Very low expenses)
- Savings Ratio < 2.0 (But low savings)

**Profile:**
- Might be low income
- Extremely frugal, but can't accumulate savings
- Need income boost, not expense cuts

**Recommendations:**
- Focus on income increase (skills, side hustle)
- Expense cuts won't help much (already minimal)
- Explore opportunities for career advancement

---

#### 8. Needs Expense Optimization
**Pattern:**
- Expense Ratio ≥ 0.85 (Very high expenses)
- DTI < 6.0 (Moderate debt)

**Profile:**
- Spending problem, not necessarily debt problem
- Likely lifestyle inflation
- Quick wins available through budgeting

**Recommendations:**
- Expense audit and categorization
- Identify top 3 expense categories
- Target 15-20% reduction in discretionary spending
- Implement zero-based budgeting

---

#### 9. General Financial Profile
**Default Category:**
- Doesn't fit specific patterns above

**Profile:**
- Mixed financial characteristics
- Needs customized analysis

---

## 🎯 Keunggulan Rule-Based Approach di Module 1

### 1. Explainability
Setiap keputusan dapat dijelaskan:
```
"Mengapa health score saya 56?"
→ Karena DTI ratio Anda 3.33 (warning level, score 50)
→ Expense ratio Anda 73.3% (warning level, score 50)
→ Savings ratio Anda hanya 1.33 bulan (warning level, score 50)
→ Weighted average = 56
```

### 2. Deterministic & Reproducible
Input yang sama SELALU menghasilkan output yang sama:
- Tidak ada randomness
- Tidak ada variasi karena model training
- Tidak ada dependency pada data training

### 3. No Training Data Needed
Tidak memerlukan historical data untuk bekerja:
- Bisa langsung deployed
- Tidak perlu menunggu data accumulation
- Tidak terpengaruh data bias

### 4. Transparent Thresholds
Threshold bisa di-justify dan di-adjust:
- DTI > 6.0 = High Risk → Bisa dijelaskan kenapa 6.0
- Bisa disesuaikan dengan regulasi/policy
- Bisa di-customize per market/segment

### 5. Regulatory Compliance
Mudah untuk audit dan compliance:
- Setiap decision dapat dirunut
- Tidak ada "black box"
- Fair lending compliance

---

## ⚠️ Limitations & Trade-offs

### Limitations
1. **Tidak bisa capture complex patterns:**
   - Misalnya: Interaksi non-linear antar variabel
   - Contoh: "High debt MUNGKIN OK jika income growth rate tinggi"

2. **Threshold bersifat rigid:**
   - DTI = 5.99 vs 6.01 diperlakukan sangat berbeda
   - Padahal sebenarnya hampir sama

3. **Tidak belajar dari data:**
   - Tidak improve seiring waktu
   - Tidak adapt dengan changing patterns

### Trade-offs yang Dipilih
**Kita memilih explainability over accuracy:**
- Module 1 memberikan baseline yang jelas dan transparan
- Module 2 (ML) akan capture complexity yang tidak bisa ditangkap Module 1
- Kombinasi keduanya memberikan best of both worlds

---

## 🔄 Integration dengan Module Lain

### Output ke Module 2 (Loan Prediction)
Module 1 menghasilkan metrics yang menjadi input features untuk Module 2:
```
Module 1 Output → Module 2 Input:
├── debt_to_income_ratio
├── expense_ratio
├── savings_ratio
├── disposable_income_ratio
└── (Used as features for ML model)
```

### Output ke Module 3 (Insights)
Module 1 menghasilkan insights yang digunakan Module 3 untuk recommendations:
```
Module 1 Output → Module 3 Input:
├── risk_flags → Root cause analysis
├── persona → Personalized recommendations
└── metrics → Scenario simulation baseline
```

---

## 📊 Validation & Calibration

### Bagaimana Threshold Ditentukan?
Threshold di Module 1 berdasarkan:

1. **Financial best practices:**
   - Savings Ratio ≥ 6.0 → Standar industry untuk emergency fund
   - Expense Ratio < 0.70 → 50-30-20 budgeting rule

2. **Empirical validation:**
   - DTI thresholds divalidasi dengan data default historis
   - User dengan DTI > 6.0 memiliki default rate signifikan lebih tinggi

3. **Regulatory guidelines:**
   - Beberapa threshold align dengan regulasi perbankan

---

## 📝 Summary

**Module 1 adalah fondasi dari keseluruhan sistem:**

✅ **Strengths:**
- Transparent & explainable
- Anti-bias design
- No training data needed
- Regulatory compliant
- Deterministic & reproducible

⚠️ **Limitations:**
- Tidak capture complex non-linear patterns
- Rigid thresholds
- Tidak adaptive

🎯 **Role dalam Sistem:**
- Baseline assessment yang dapat dipercaya
- Foundation untuk Module 2 & 3
- Explainability anchor untuk keseluruhan sistem

**Next:** Module 2 akan menambahkan machine learning intelligence untuk capture complexity yang tidak bisa ditangkap oleh rules.
