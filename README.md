# GST Compliance Copilot

> 🚧 **Work in progress.** It's being built in small iterations. This README is updated as features land.

An AI copilot that helps accountants reconcile **GSTR-2B against the purchase register**, explains *why* each mismatch happened, and answers plain-English questions about GST data, with an evaluation harness that checks every change.

> ⚠️ **Not tax advice.** This is a portfolio project built **only on synthetic data**. All GSTINs and vendors are fake and marked `DEMO`. Anything it drafts needs review by a Chartered Accountant.

---

## The problem

Every month, CA firms and in-house accountants match the invoices in their books against GSTR-2B, usually by hand in Excel. Mismatched Input Tax Credit (ITC) is one of the most common reasons for GST notices. When the ITC claimed in GSTR-3B is too far above GSTR-2B, a **DRC-01C** intimation follows, and the taxpayer has only a short window to pay or explain the difference.

## What it does (MVP)

| Component | What it does |
|---|---|
| **Synthetic data generator** | Creates fake clients, vendors, purchase registers and GSTR-2B data with labelled, injected mismatches (format differences, rounding, amount differences, tax-head mix-ups, missing invoices). |
| **Deterministic matcher** | A multi-pass, rule-based reconciliation: exact → normalised → tolerance. **The matcher alone decides whether invoices match; the LLM never does.** |
| **DataPilot agent** | Answers questions like *"show invoices in books but not in 2B over ₹50k for client A"* by writing **read-only, guarded SQL**, then explains the results. |
| **AgentEval Gate** | An eval suite (SQL accuracy, GST task set, safety checks) that runs in CI and blocks regressions. |

## Design principles

- **Deterministic where it matters:** matching is plain code with tests, not model output.
- **Read-only by design:** agent SQL goes through a parser-based guard (single `SELECT`, approved views only, row limit) on a read-only connection.
- **Synthetic data only:** no real GSTINs, no client data.
- **Measured, not vibes:** every change is checked against labelled data and eval sets.

## Tech stack

Python · SQLite · sqlglot · LangGraph · Gemini · Streamlit · pytest · GitHub Actions

## Getting started

*Setup instructions will be added once the first runnable version lands.*

## Roadmap

- [ ] v0.1: end-to-end skeleton (generate data → reconcile → ask a question → see the answer)
- [ ] v0.2: richer mismatch types, explanations and DRC-01C draft reasons
- [ ] v0.3: AgentEval Gate in CI
- [ ] Later: cite-or-refuse assistant over the CGST Act, Rules and circulars

## License

To be added.
