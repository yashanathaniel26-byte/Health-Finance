# Dokumentasi Algoritma - Financial Health System
**Sistem Analisis Kesehatan Finansial & Prediksi Risiko Pinjaman**

---

## 📋 Gambaran Umum Sistem

Sistem ini adalah platform analisis finansial berbasis AI yang mengintegrasikan **tiga mesin kecerdasan** untuk memberikan insight komprehensif tentang kesehatan finansial dan risiko pinjaman.

### Arsitektur 3-Module

```
┌─────────────────────────────────────────────────────────────┐
│                    INPUT: Data Pengguna                     │
│   • Profil Finansial (Income, Expenses, Debt, Savings)     │
│   • Permintaan Pinjaman (Amount, Duration, Type)           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              MODULE 1: Health Assessment Engine             │
│  Algoritma: Rule-Based Metrics + Clustering Analysis       │
│  Output: Health Score (0-100) + Financial Persona          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│           MODULE 2: Loan Default Prediction Engine          │
│  Algoritma: LightGBM Machine Learning Model                │
│  Output: Default Probability + Risk Category               │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│         MODULE 3: Insight & Recommendation Engine           │
│  Algoritma: Root Cause Analysis + What-If Scenarios        │
│  Output: Actionable Recommendations + Simulations          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                 OUTPUT: Decision Intelligence               │
│  • Risk Assessment Report                                   │
│  • Personalized Recommendations                             │
│  • Financial Improvement Roadmap                            │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Filosofi Desain: Mengapa Berbeda dari Logika Biasa?

### 1. **Hybrid Intelligence Architecture**
Sistem ini menggabungkan pendekatan berbeda untuk memanfaatkan kekuatan masing-masing:

| Pendekatan | Kegunaan | Kelebihan |
|-----------|----------|-----------|
| **Rule-Based (Module 1)** | Health Assessment | Transparan, explainable, no training data needed |
| **Machine Learning (Module 2)** | Risk Prediction | Pattern recognition dari data historis, non-linear relationships |
| **Reasoning Logic (Module 3)** | Decision Support | Contextual insight, causal analysis, actionable |

**Logika Biasa:** Hanya menggunakan satu pendekatan (biasanya IF-THEN rules atau pure ML)
**Sistem Ini:** Kombinasi optimal dari ketiga pendekatan untuk hasil yang lebih robust

### 2. **Anti-Bias by Design**
Sistem dirancang untuk menghindari bias sosial-ekonomi:

- **Scale-Invariant Metrics:** Menggunakan rasio, bukan nilai absolut
  - Contoh: DTI Ratio = Debt/Income (BUKAN: "Debt > 50 juta = High Risk")
  - Seseorang dengan income 10 juta dan debt 30 juta memiliki DTI = 3.0
  - Seseorang dengan income 100 juta dan debt 300 juta juga DTI = 3.0
  - Keduanya diperlakukan sama, tidak bias terhadap kelas ekonomi

- **Persona bukan Label:**
  - Tidak menggunakan label judgemental seperti "Creditworthy" vs "High Risk Borrower"
  - Menggunakan deskripsi behavioral: "Conservative Saver", "Cashflow Challenged"
  - Fokus pada pola perilaku finansial, bukan penilaian karakter

### 3. **Explainability First**
Setiap keputusan sistem dapat dijelaskan kepada pengguna:

- **Module 1:** Mengapa health score Anda 65? → Karena DTI ratio 4.5x (warning level)
- **Module 2:** Mengapa default probability 15%? → Feature X, Y, Z berkontribusi sekian persen
- **Module 3:** Apa yang harus dilakukan? → Reduce debt 30% akan improve score ke 78

**Logika Biasa (Black Box ML):** Model ML memberikan prediksi tanpa penjelasan
**Sistem Ini:** Setiap angka dapat dirunut ke akar penyebabnya

### 4. **Separation of Concerns**
Setiap module memiliki tanggung jawab yang jelas:

```
Module 1: "What is the current health?" (Assessment)
Module 2: "What will happen?" (Prediction)
Module 3: "What should we do?" (Recommendation)
```

**Logika Biasa:** Semua tercampur dalam satu fungsi/model
**Sistem Ini:** Modular, testable, maintainable, scalable

### 5. **Production-Ready Engineering**
Dirancang untuk deployment production, bukan hanya research:

- Input validation & error handling
- Frozen models (no online training)
- Stateless transformations (no side effects)
- Reproducible predictions (deterministic)
- Comprehensive testing & documentation

---

## 🔬 Perbedaan Fundamental: Rule-Based vs Machine Learning

### Kapan Menggunakan Rule-Based? (Module 1)
✅ **Gunakan ketika:**
- Domain knowledge sudah jelas (e.g., DTI ratio thresholds)
- Transparansi sangat penting (regulatory compliance)
- Data training terbatas atau tidak tersedia
- Hasil harus deterministik dan reproducible

❌ **Jangan gunakan ketika:**
- Relationship antar variabel sangat kompleks dan non-linear
- Pola tersembunyi yang tidak dapat diformulasikan dengan rules
- Membutuhkan adaptasi dari data historis

### Kapan Menggunakan Machine Learning? (Module 2)
✅ **Gunakan ketika:**
- Ada data training yang cukup dan berkualitas
- Relationship antar features kompleks dan non-linear
- Ingin menangkap pola yang tidak terlihat (latent patterns)
- Accuracy prediction lebih penting daripada explainability

❌ **Jangan gunakan ketika:**
- Data training bias atau tidak representatif
- Tidak bisa menjelaskan hasil ke stakeholders
- Membutuhkan hasil yang 100% deterministik

### Mengapa Sistem Ini Menggabungkan Keduanya?
Sistem ini menggunakan **complementary strengths**:

1. **Module 1 (Rule-Based)** memberikan baseline assessment yang transparan
2. **Module 2 (ML)** menangkap kompleksitas yang tidak bisa di-capture oleh rules
3. **Module 3 (Reasoning)** menggabungkan keduanya untuk actionable insight

---

## 📊 Contoh Nyata: Perbedaan Pendekatan

### Scenario: Menilai Risiko Pinjaman

**Pendekatan Tradisional (Logika Biasa):**
```
IF (income > 10_000_000) THEN approved = TRUE
ELSE approved = FALSE
```
- ❌ Bias terhadap high income
- ❌ Tidak memperhitungkan debt burden
- ❌ Tidak memperhitungkan expense pattern

**Pendekatan Rule-Based Sederhana:**
```
DTI = debt / income
IF (DTI < 3.0) THEN risk = "low"
ELSE risk = "high"
```
- ✅ Scale-invariant (tidak bias terhadap income level)
- ❌ Oversimplified (hanya melihat satu metric)
- ❌ Tidak memperhitungkan savings, expenses, dll

**Pendekatan Machine Learning Murni:**
```
Model learns: default_probability = f(income, debt, expenses, ...)
```
- ✅ Menangkap complex patterns
- ✅ Belajar dari data historis
- ❌ Black box, sulit dijelaskan
- ❌ Bisa bias jika training data bias

**Pendekatan Sistem Ini (Hybrid):**
```
Module 1: Calculate DTI, Expense Ratio, Savings Ratio → Health Score
Module 2: Predict default_probability using ML dengan semua features
Module 3: Explain WHY risk is high → Recommend HOW to improve
```
- ✅ Comprehensive assessment
- ✅ Explainable results
- ✅ Actionable recommendations
- ✅ Anti-bias design

---

## 🧩 Key Innovations

### 1. Financial Persona Clustering (Module 1)
Bukan kredit scoring tradisional, tapi behavioral profiling:
- "Conservative Saver" vs "High Earner - High Spender"
- Memberikan context untuk recommendations
- Membantu personalisasi financial advice

### 2. SHAP-Based Explainability (Module 2)
Setiap prediksi dilengkapi dengan penjelasan:
- Feature apa yang paling berkontribusi?
- Bagaimana jika feature X berubah?
- Mengapa probability-nya sekian persen?

### 3. What-If Scenario Simulation (Module 3)
Bukan hanya diagnosis, tapi juga treatment planning:
- "Bagaimana jika saya increase income 20%?"
- "Bagaimana jika saya reduce debt 30%?"
- "Mana yang lebih impactful untuk health score saya?"

---

## 📖 Struktur Dokumentasi

Dokumentasi ini terdiri dari:

1. **01_OVERVIEW_SISTEM.md** (file ini) - Gambaran umum dan filosofi
2. **02_MODULE_1_HEALTH_ASSESSMENT.md** - Detail algoritma Module 1
3. **03_MODULE_2_LOAN_PREDICTION.md** - Detail algoritma Module 2
4. **04_MODULE_3_INSIGHTS_RECOMMENDATIONS.md** - Detail algoritma Module 3
5. **05_INTEGRATION_WORKFLOW.md** - Bagaimana ketiga module bekerja bersama

---

**Catatan Penting:**
Dokumentasi ini fokus pada **penjelasan konseptual dan algoritma**, BUKAN implementasi code. Tujuannya adalah memberikan pemahaman mendalam tentang "WHY" dan "HOW" sistem bekerja, bukan "WHAT" code-nya.
