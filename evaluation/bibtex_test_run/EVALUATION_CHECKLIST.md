# BibTeX Export Evaluation - Quick Checklist

## ⏱️ Time Required: 15-20 minutes

---

## 📋 Pre-Test Setup

- [ ] Copy `bibtex_evaluation.py` to `C:\AI_Agent_draft\`
- [ ] Ensure `main.py` is working
- [ ] Ensure `papers.db` has data (433 papers)
- [ ] Clear any old .bib files (optional)

---

## 🧪 Test Execution

### Run each query in `main.py`:

**Basic (2 tests)**
- [ ] `Export all papers to all_papers.bib` → 433 papers
- [ ] `Export all papers to test.bib` → 433 papers

**Keywords (4 tests)**
- [ ] `Export transformer papers to transformers.bib` → 58 papers
- [ ] `Export survey papers to surveys.bib` → 17 papers
- [ ] `Export review papers to reviews.bib` → 9 papers
- [ ] `Export attention papers to attention.bib` → ~40 papers

**Years (3 tests)**
- [ ] `Export papers from 2020 onwards to recent_2020.bib`
- [ ] `Export papers from 2023 onwards to very_recent.bib`
- [ ] `Export papers from 2024 to papers_2024.bib`

**Combined (2 tests)**
- [ ] `Export transformer papers from 2023 onwards to recent_transformers.bib` → 23 papers
- [ ] `Export survey papers from 2022 onwards to recent_surveys.bib`

**Source (2 tests)**
- [ ] `Export only arxiv papers to arxiv_papers.bib` → ~330 papers
- [ ] `Export only openalex papers to openalex_papers.bib` → ~103 papers

**Edge Cases (2 tests)**
- [ ] `Export papers about quantum_blockchain_ai_xyz to empty.bib` → 0 papers
- [ ] `Export all papers to my_papers_2024.bib` → 433 papers

---

## 📊 Run Evaluation

- [ ] Run: `python bibtex_evaluation.py`
- [ ] Review on-screen results
- [ ] Check generated files:
  - [ ] `bibtex_evaluation_results.json`
  - [ ] `bibtex_evaluation_report.txt`
  - [ ] `bibtex_test_outputs/` directory

---

## ✅ Success Criteria

- [ ] Overall success rate ≥ 80% (12/15 tests)
- [ ] All basic functionality tests pass
- [ ] Keyword filtering works
- [ ] Year filtering works
- [ ] Combined filters work
- [ ] Source filtering works
- [ ] No format errors

---

## 📝 Documentation

- [ ] Save evaluation reports
- [ ] Note any failures and reasons
- [ ] Record performance metrics
- [ ] Take screenshots (optional)
- [ ] Update thesis notes

---

## 🎯 Expected Numbers (Your Database)

Total: 433 papers
- Transformer: 58
- Survey: 17
- Review: 9
- Attention: ~40
- ArXiv: ~330
- OpenAlex: ~103
- Recent (2023+): varies

---

## 🚀 After Testing

- [ ] Archive test results
- [ ] Update progress document
- [ ] Decide on next feature
- [ ] Move forward confidently!

---

## 🎉 Done!

When all boxes are checked, you have:
✅ Comprehensive test coverage
✅ Validated functionality
✅ Performance metrics
✅ Documentation for thesis
✅ Confidence to move forward

**Time to build the next feature!** 🚀
