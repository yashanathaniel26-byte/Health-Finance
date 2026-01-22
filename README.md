# Financial Health & Loan Default Intelligence System
<img width="1919" height="750" alt="image" src="https://github.com/user-attachments/assets/d6e1c585-04be-4565-98b3-74f968d6d8a0" />
<img width="1731" height="865" alt="image" src="https://github.com/user-attachments/assets/877cb99a-8014-4505-b3cf-3db0c4706ad4" />
<img width="1919" height="878" alt="image" src="https://github.com/user-attachments/assets/d46bbbe2-f52d-4bc6-977f-332090618bc4" />
<img width="970" height="741" alt="image" src="https://github.com/user-attachments/assets/bc1fbb6f-6230-4264-b85f-80ba6d3c5817" />
<img width="1919" height="612" alt="image" src="https://github.com/user-attachments/assets/f365c46e-ab3b-4b97-8575-fa3589a4e324" />





## 🎯 Overview

A **next-generation decision intelligence framework** that goes beyond traditional rule-based scoring systems. This comprehensive ML-powered system provides:

1. **Multi-dimensional Financial Health Analysis** - Assess user's current financial state
2. **ML-Driven Loan Default Risk Prediction** - Predict probability using trained models
3. **Actionable Insights & Recommendations** - Context-aware guidance based on reasoning
4. **Interactive What-If Scenario Simulation** - Explore financial improvement paths

> **Sistem ini bukan sekadar algoritma logika atau scoring biasa, melainkan sebuah decision intelligence framework yang memisahkan fakta, prediksi, dan reasoning agar keputusan finansial menjadi adil, transparan, dan dapat dipahami manusia.**

---

## 🔍 Perbedaan dengan Logic Algorithm Biasa (Traditional Rule-Based Systems)

Sebagian besar sistem penilaian finansial tradisional menggunakan **logic algorithm statis**, seperti:

* Threshold tetap (contoh: *DTI > 40% → reject*)
* Skor linear sederhana
* Aturan tunggal yang langsung menghasilkan keputusan

Project ini **secara fundamental berbeda**, baik dari sisi **arsitektur, filosofi, maupun output**.

### 1️⃣ Pemisahan Antara *Assessment*, *Prediction*, dan *Reasoning*

| Logic Algorithm Biasa      | Project Ini                        |
| -------------------------- | ---------------------------------- |
| Satu alur → satu keputusan | Multi-layer intelligence           |
| Assessment = Decision      | Assessment ≠ Prediction ≠ Decision |
| Sulit ditelusuri           | Fully traceable                    |

📌 **Implikasi:** User tidak langsung "dihakimi" oleh satu aturan, tapi melalui **proses bertahap yang dapat dijelaskan**.

### 2️⃣ Bukan Sekadar If–Else atau Threshold Logic

**Logic algorithm biasa:**
```text
IF DTI > 40% AND savings < X → High Risk
```

**Project ini:**
* DTI, savings, expenses → dihitung sebagai **rasio**
* Dinilai secara **kontinu (continuous scoring)**
* Digabungkan dengan **contextual reasoning**
* Tidak ada satu variabel yang "mematikan" sistem

📌 **Hasil:** Sistem lebih **robust**, **tidak brittle**, dan **lebih adil**.

### 3️⃣ Explainability yang Nyata, Bukan Alasan Generik

| Traditional Logic                | Project Ini                                                                                  |
| -------------------------------- | -------------------------------------------------------------------------------------------- |
| "Risiko tinggi karena DTI besar" | "Risiko meningkat karena 62% pendapatan digunakan untuk cicilan, membatasi cashflow bulanan" |
| Hard-coded message               | Dynamic explanation                                                                          |

📌 Setiap output memiliki:
* Angka pendukung
* Konteks
* Dampak finansial

### 4️⃣ Menghindari Bias Nilai Absolut

**Logic algorithm biasa** sering bias terhadap:
* Income kecil
* User informal
* Early-career individuals

**Project ini:**
* Menggunakan **rasio & proporsi**
* Scale-invariant metrics
* Persona ditentukan oleh **pola**, bukan jumlah uang

📌 **Dampak:** User dengan income berbeda tetap bisa dibandingkan **secara adil**.

### 5️⃣ ML Digunakan Sebagai *Predictor*, Bukan *Decision Maker*

| Logic Algorithm Biasa        | Project Ini                   |
| ---------------------------- | ----------------------------- |
| Decision = Rule              | Decision = Insight Engine     |
| ML (jika ada) langsung final | ML hanya memberi probabilitas |
| Sulit diaudit                | Mudah diaudit                 |

📌 Model **tidak memutuskan**:
* Ia hanya menjawab: *"berapa kemungkinan gagal bayar?"*
* Reasoning tetap berada di layer terpisah

### 6️⃣ Mendukung What-If Analysis (Tidak Mungkin di Logic Biasa)

**Logic algorithm biasa:**
* Output statis
* Tidak bisa simulasi

**Project ini:**
* "Jika cicilan turun 10% → skor naik X"
* "Jika tabungan bertambah 3 bulan → risiko turun Y%"

📌 Ini mengubah sistem dari **judgment tool** menjadi **financial guidance tool**.

### 7️⃣ Persona Lebih Dari Sekadar Label Risiko

| Traditional              | Project Ini       |
| ------------------------ | ----------------- |
| Low / Medium / High Risk | Financial Persona |
| Judgmental               | Descriptive       |
| Tidak actionable         | Action-oriented   |

**Contoh:**
> "Stable but Overleveraged" → actionable insight
> 
> bukan
> 
> "High Risk User" → judgmental label

---

## 🏗️ System Architecture

The system consists of **3 independent but integrated modules**:

### Module 1: Financial Health Analyzer (Non-Credit ML)
- **Purpose**: Assess user's current financial health
- **Input**: Income, expenses, savings, existing debt
- **Output**: Health score (0-100), metrics, risk flags, financial persona
- **ML Techniques**: Unsupervised clustering, rule-based analysis
- **Key**: NO credit/default labels used here

### Module 2: Loan Default Prediction (Core ML)
- **Purpose**: Predict probability of loan default
- **Input**: Loan request + financial profile
- **Output**: Default probability, risk category, SHAP explanations
- **Model**: Pre-trained LightGBM (frozen, no retraining)
- **Key**: Pure prediction layer, no decision-making

### Module 3: Insight & Decision Intelligence
- **Purpose**: Integrate health + prediction for actionable insights
- **Input**: Results from Module 1 & 2
- **Output**: Root cause analysis, scenarios, recommendations
- **Key**: This is where reasoning happens

---

## 📁 Project Structure

```
financial_health_system/
│
├── config/                       # Configuration files
│   ├── __init__.py
│   ├── settings.py              # Global settings
│   ├── thresholds.py            # Business rules and thresholds
│   └── feature_schema.json      # Feature definitions from training
│
├── models/                       # Trained models (artifacts)
│   ├── loan_model.pkl           # Trained LightGBM model
│   ├── preprocessor.pkl         # Feature preprocessing pipeline
│   ├── cluster_model.pkl        # Financial persona clustering
│   └── model_metadata.json      # Model training information
│
├── src/                          # Source code
│   │
│   ├── module_1_health/         # Financial Health Analyzer
│   │   ├── __init__.py
│   │   ├── metrics.py           # Calculate financial metrics
│   │   ├── rules.py             # Rule-based health assessment
│   │   ├── clustering.py        # Financial persona clustering
│   │   └── health_analyzer.py   # Main orchestrator
│   │
│   ├── module_2_prediction/     # Loan Default Prediction
│   │   ├── __init__.py
│   │   ├── feature_assembly.py  # Prepare features for model
│   │   ├── model_inference.py   # Load & predict with model
│   │   ├── explainer.py         # SHAP explanations
│   │   └── loan_predictor.py    # Main orchestrator
│   │
│   ├── module_3_insights/       # Insight & Decision Intelligence
│   │   ├── __init__.py
│   │   ├── root_cause.py        # Root cause analysis
│   │   ├── scenarios.py         # What-if scenario simulation
│   │   ├── recommendations.py   # Recommendation engine
│   │   └── insight_engine.py    # Main orchestrator
│   │
│   └── utils/                    # Shared utilities
│       ├── __init__.py
│       ├── validators.py        # Input validation
│       ├── calculators.py       # Common calculations
│       └── visualization.py     # Plotting helpers
│
├── app/                          # Application layer
│   ├── __init__.py
│   ├── streamlit_app.py         # Streamlit UI
│   └── api.py                   # FastAPI endpoints (optional)
│
├── tests/                        # Unit tests
│   ├── __init__.py
│   ├── test_module_1.py
│   ├── test_module_2.py
│   ├── test_module_3.py
│   └── test_integration.py
│
├── notebooks/                    # Jupyter notebooks
│   ├── 01_health_analysis_demo.ipynb
│   ├── 02_loan_prediction_demo.ipynb
│   └── 03_full_system_demo.ipynb
│
├── docs/                         # Documentation
│   ├── architecture.md          # System architecture
│   ├── algorithms.md            # Detailed algorithms
│   ├── api_reference.md         # API documentation
│   └── user_guide.md            # User manual
│
├── data/                         # Data storage (gitignored)
│   ├── raw/                     # Original datasets
│   ├── processed/               # Processed data
│   └── user_data/               # User analysis history
│
├── requirements.txt              # Python dependencies
├── setup.py                      # Package setup
├── Dockerfile                    # Container configuration
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore rules
└── pytest.ini                    # Test configuration
```

---

## 🚀 Quick Start

### Option 1: One-Click Start (Windows)

```bash
# Start both backend and frontend automatically
start_all.bat
```

### Option 2: Manual Start

**Terminal 1 - Backend (FastAPI):**
```bash
# Windows
start_backend.bat

# Or manually:
venv\Scripts\activate
cd app
python api.py
```

**Terminal 2 - Frontend (Next.js):**
```bash
# Windows
start_frontend.bat

# Or manually:
cd app/web
npm install
npm run dev
```

### Access the Application

- **Frontend (UI):** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## 📖 Full Setup Guide

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed installation and deployment instructions.

---

### 1. Installation

```bash
# Clone repository
cd financial_health_system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup

```bash
# Copy environment template
cp .env.example .env

# Place trained models in models/ directory
# - loan_model.pkl
# - preprocessor.pkl
# - model_metadata.json
```

### 3. Run Application

```bash
# Streamlit UI
streamlit run app/streamlit_app.py

# Or FastAPI
uvicorn app.api:app --reload
```

---

## 🔬 Usage Examples

### Standalone Module Usage

```python
from src.module_1_health import HealthAnalyzer
from src.module_2_prediction import LoanPredictor
from src.module_3_insights import InsightEngine

# Step 1: Analyze financial health
health_analyzer = HealthAnalyzer()
health_result = health_analyzer.analyze({
    'income': 15_000_000,
    'fixed_expenses': 8_000_000,
    'variable_expenses': 3_000_000,
    'savings': 20_000_000,
    'debt': 50_000_000
})

# Step 2: Predict loan default
loan_predictor = LoanPredictor()
loan_result = loan_predictor.predict({
    'jumlah_pinjaman': 30_000_000,
    'durasi_hari': 90,
    'jenis_pinjaman': 'Multiguna',
    # ... other loan features
}, financial_profile=health_result['metrics'])

# Step 3: Generate insights
insight_engine = InsightEngine()
insights = insight_engine.analyze(
    health_result=health_result,
    loan_result=loan_result
)
```

### Integrated Pipeline

```python
from src.integrated_pipeline import FinancialIntelligenceSystem

system = FinancialIntelligenceSystem()

result = system.analyze(
    financial_profile={
        'income': 15_000_000,
        'expenses': {'fixed': 8_000_000, 'variable': 3_000_000},
        'savings': 20_000_000,
        'debt': 50_000_000
    },
    loan_request={
        'jumlah_pinjaman': 30_000_000,
        'durasi_hari': 90,
        'jenis_pinjaman': 'Multiguna',
        # ...
    }
)

print(result['decision'])
print(result['recommendations'])
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific module tests
pytest tests/test_module_1.py -v

# Run with coverage
pytest --cov=src --cov-report=html
```

---

## 📊 Key Principles & Design Philosophy

### Core Principles

1. **Separation of Concerns**: Each module is independent and has a single responsibility
2. **No Data Leakage**: Model is frozen, no runtime training - predictions are pure inference
3. **Explainability First**: Every output has reasoning - no black box decisions
4. **Production-Ready**: Modular, testable, deployable architecture
5. **Fairness by Design**: Scale-invariant metrics avoid bias against income levels
6. **Transparency**: Fully traceable decision path from input to recommendation

### Design Philosophy

```
Traditional System:          This System:
Input → Decision            Input → Assessment → Prediction → Reasoning → Decision
(1 step, opaque)           (4 steps, transparent)
```

**Why This Matters:**
- **Users** get actionable guidance, not just accept/reject
- **Auditors** can trace every decision component
- **Developers** can improve individual modules independently
- **Business** can adjust thresholds without model retraining

---

## 🎯 Key Differentiators Summary

| Aspect | Traditional Systems | This System |
|--------|-------------------|-------------|
| **Architecture** | Monolithic | Multi-layer (3 modules) |
| **Decision Logic** | Hard-coded rules | Context-aware reasoning |
| **Explainability** | Generic messages | Dynamic, data-backed |
| **Fairness** | Absolute thresholds | Ratio-based, scale-invariant |
| **ML Role** | Black box decider | Transparent predictor |
| **User Experience** | Pass/Fail judgment | Guidance + scenarios |
| **Auditability** | Difficult | Full traceability |
| **Adaptability** | Requires code changes | Configuration-driven |

---

## 🛠️ Tech Stack

- **ML Framework**: scikit-learn, LightGBM, SHAP
- **Core**: Python 3.9+
- **Data Processing**: Pandas, NumPy
- **Backend API**: FastAPI
- **Frontend**: Next.js (React), Streamlit
- **Testing**: Pytest, Coverage.py
- **Deployment**: Docker, Render, Streamlit Cloud
- **CI/CD**: GitHub Actions (optional)

---

## 🔬 Technical Highlights

### Module 1: Financial Health Analyzer
- **Unsupervised clustering** for persona identification
- **Rule-based scoring** with continuous metrics
- **Multi-dimensional assessment**: DTI, savings ratio, expense efficiency
- **No labels required** - purely analytical

### Module 2: Loan Default Predictor
- **Frozen pre-trained model** (no runtime learning)
- **SHAP explainability** for every prediction
- **Feature engineering** aligned with training pipeline
- **Probability calibration** for reliable risk estimates

### Module 3: Insight Engine
- **Root cause analysis** using multi-factor attribution
- **Scenario simulation** with sensitivity analysis
- **Context-aware recommendations** based on persona + risk
- **Natural language generation** for explanations

---

## 🚧 Future Enhancements

- [ ] Multi-language support (Bahasa Indonesia, English)
- [ ] Historical tracking & trend analysis
- [ ] Peer comparison (anonymized benchmarking)
- [ ] Advanced scenario optimization (ML-based suggestions)
- [ ] Integration with banking APIs
- [ ] Mobile application (React Native)
- [ ] Real-time monitoring dashboard for admins
- [ ] A/B testing framework for recommendation effectiveness

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

**Code Standards:**
- Follow PEP 8 for Python code
- Add unit tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting

---

## 📄 Documentation

- [Architecture Guide](docs/architecture.md) - Detailed system design
- [Algorithm Reference](docs/algorithms.md) - Math & logic behind each module
- [API Reference](docs/api_reference.md) - API endpoints documentation
- [User Guide](docs/user_guide.md) - End-user manual
- [Setup Guide](SETUP_GUIDE.md) - Installation & deployment
- [Deployment Guide](DEPLOYMENT_GUIDE.md) - Production deployment

---

## ⚠️ Important Notes

### Model Limitations
- Model is trained on specific data distribution
- Performance may degrade on out-of-distribution inputs
- Regular model monitoring and retraining recommended (every 6-12 months)

### Ethical Considerations
- This system provides **decision support**, not final decisions
- Human oversight is essential for high-stakes decisions
- Regular fairness audits recommended
- Transparency with users about how decisions are made

### Data Privacy
- User data should be encrypted at rest and in transit
- Comply with local data protection regulations (GDPR, etc.)
- Implement proper access controls
- Regular security audits recommended

---

## 📞 Support & Contact

For questions, issues, or suggestions:
- Create an issue on GitHub
- Email: [yasernurtaxiano@student.telkomuniversity.ac.id]
- Documentation: [link-to-docs]

---

## 🙏 Acknowledgments

- LightGBM team for the excellent gradient boosting framework
- SHAP library for model explainability
- FastAPI & Streamlit communities
- All contributors and testers

---

## 📝 License

MIT License

---

## 👥 Contributors

- just Allah and Me




