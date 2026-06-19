# 🚚 Supply Chain Delay & Logistics Performance Analysis

> *"More than half of all shipments were arriving late — but the real problem wasn't the carriers, the routes, or the products. It was a broken promise baked into the system from day one."*

---

## The Business Problem

Imagine you run a global logistics company. Every day, thousands of orders go out across 23 countries. Your customers are promised delivery in 1 day, 2 days, or 4 days depending on the shipping tier they paid for.

Now imagine your operations team tells you that **57 out of every 100 shipments are arriving late.**

That's not a bad week. That's not a seasonal spike. That's every single day, across every region, every product type, every shipping route — consistently, reliably, late.

Your leadership team wants answers:

- **Is it a geography problem?** Are certain countries or regions causing delays?
- **Is it a product problem?** Are certain items — bulky, fragile, heavy — harder to ship?
- **Is it a carrier problem?** Are our shipping partners simply not delivering on time?
- **How much is this actually costing us?**

This project set out to answer every one of those questions — using 172,765 real shipment records, structured data analysis, and statistical testing to separate fact from assumption.

---

## The Dataset

**Source:** DataCo Smart Supply Chain Dataset (Kaggle)

Think of this as the complete shipment ledger of a global supply chain company. Every row is one order. Every column tells us something about that order — where it went, what was in it, how it was shipped, when it was promised, and when it actually arrived.

```
172,765 orders  ·  23 global regions  ·  4 shipping modes  ·  53 data points per order
```

Before any analysis, 7,754 cancelled orders were removed — you cannot measure delivery performance on an order that was never shipped. That left a clean working dataset of **172,765 orders** ready for analysis.

---

## How We Approached It — The Three Questions

### Step 1 — Understand the Scale

Before asking *why*, we needed to understand *how bad*.

The numbers were stark:

| Metric | Value |
|---|---|
| Total orders analysed | 172,765 |
| Orders delivered late | 98,977 |
| Global SLA breach rate | **57.3%** |
| Total economic cost of delays | **$13,841,971** |
| Average cost per delayed order | $82.43 |

More than half of all shipments were missing their promised delivery window. And the financial cost of that — calculated as the daily carrying cost of each delayed order — was nearly **$14 million.**

That $14 million is not the cost of sending a shipment. It is the cost of *promising one thing and delivering another.*

---

### Step 2 — Identify the Root Cause

With $14 million on the table, the natural question is: *where do we point the finger?*

We tested three suspects systematically.

---

#### Suspect 1 — Geography 🌍

> *"Maybe certain regions have poor infrastructure, customs delays, or unreliable local carriers."*

We measured delay rates across all 23 global markets — from Central Africa to Canada, Western Europe to Southeast Asia.

**What we found:**

Every single region showed a delay rate between **51% and 60%.** The entire planet, across wildly different infrastructure, carrier networks, and regulatory environments, produced almost identical delay rates.

```
Canada (best):          51.60% delayed
Central Africa (worst): 60.15% delayed
Difference:             8.55 percentage points
```

When every region looks the same, geography is not the cause. We confirmed this with a formal statistical test (ANOVA) which showed the regional differences were so small they could easily be explained by random chance.

**Verdict: Geography is ruled out.**

---

#### Suspect 2 — Product Type 📦

> *"Maybe certain products — heavy items, fragile goods, bulky shipments — are structurally harder to deliver on time."*

We measured delay rates across the top 15 highest-delay product categories — everything from Golf Bags to Electronics to Pet Supplies.

**What we found:**

All categories clustered between **58% and 69%** delay rate. The highest-delay categories (Golf Bags at 68.85%, Lacrosse at 62.61%) had fewer than 400 orders each — too small a sample to draw conclusions from.

A statistical test (Kruskal-Wallis) confirmed: product category has **no significant effect** on delay. The p-value was 0.689 — meaning there is a 69% chance these small differences were pure random noise.

Why? Because the delivery window is already adjusted for product complexity. A piano gets a 7-day window. A book gets a 2-day window. The promise already accounts for the difficulty.

**Verdict: Product type is ruled out.**

---

#### Suspect 3 — Shipping Mode 🚛

> *"Maybe the problem is in how orders are being shipped — the service tier chosen."*

This is where everything changed.

We looked at four shipping modes: Same Day, First Class, Second Class, and Standard Class. We compared what was *promised* versus what was *delivered*:

| Shipping Mode | Promised | Actually Delivered | Delay Rate | SLA Compliance |
|---|---|---|---|---|
| First Class | 1 day | 2 days | **100%** | **0%** |
| Second Class | 2 days | 4 days | **79.8%** | **20.2%** |
| Same Day | 0 days | 0.5 days | 47.9% | 52.1% |
| Standard Class | 4 days | 4 days | 39.8% | **60.2%** |

The pattern is impossible to miss.

**First Class has a 100% delay rate.** Every single one of 26,513 First Class orders in this dataset was late. Not most. Not many. Every one.

**Standard Class — the slowest, cheapest option — performs best.** Nearly 40,000 orders delivered, 60% on time.

The difference between the best and worst performers is not carrier quality, route efficiency, or product type. It is one thing: **whether the promised delivery window matches what operations can actually achieve.**

---

### Step 3 — The Real Discovery

When we dug into the numbers behind the shipping modes, we found something that reframes the entire problem:

**Every shipping mode delivers in approximately double its scheduled window — except Standard Class.**

```
First Class:    Promised 1 day  →  Always delivers in 2 days
Second Class:   Promised 2 days →  Always delivers in 4 days
Standard Class: Promised 4 days →  Delivers in 4 days  ✓
```

Standard Class is the only mode where someone set a realistic, achievable promise. Every other tier was configured with a window that operations cannot meet — not occasionally, but *structurally, always.*

This is not a carrier failure. This is not a logistics failure.

**This is a promise-setting failure.**

Someone, at some point, configured the system to promise 1-day First Class delivery when the operation consistently takes 2 days. That single configuration decision created a guaranteed, automatic, irreversible SLA breach for every First Class order placed — forever — until the setting is changed.

---

## The Financial Impact

Once the root cause was clear, the economic picture came into sharp focus:

**First Class alone:**
- 26,513 orders · 100% breach rate · $183.34 average cost per order
- **Total: $4,860,949 in delay costs**
- Cause: a 1-day promise on a 2-day operation

**Second Class worst corridors:**
- Western Europe: $1,030,156
- Caribbean: $287,490
- South Asia: $277,664
- Cause: a 2-day promise on a 4-day operation

**Two misconfigured shipping tiers account for over 50% of the entire $13.84M delay cost.**

---

## What the Statistics Confirmed

Every finding in this project was validated with a formal statistical test — not to show off, but because *"the numbers look different"* is not the same as *"the difference is real."*

| Question | Test Used | Result | What It Means |
|---|---|---|---|
| Does region drive delay? | ANOVA | Significant but tiny effect | Geography is not actionable |
| Does shipping mode drive delay? | Chi-Square | χ² = 40,058 — overwhelming | Strongest signal in the dataset |
| Does product category matter? | Kruskal-Wallis | Not significant (p = 0.689) | Category is not a factor |
| Is Standard Class genuinely better than Same Day? | Z-Test | 15 standard deviations apart | Yes — the window explains it |
| Does order value predict delay cost? | Spearman Correlation | Weak (ρ = 0.22) | Value is not the driver |

The Chi-Square statistic of 40,058 deserves a moment. For context, statisticians consider values above 15 to be highly significant for this type of test. A value of 40,058 means the probability of shipping mode and delay being unrelated — by random chance — is effectively zero. The data is speaking as clearly as data can speak.

---

## The Recommendations

### Recommendation 1 — Fix the Promise (Immediate, Zero Cost)

Reset delivery window commitments to match operational reality:

| Mode | Current Promise | Reality | Fix |
|---|---|---|---|
| First Class | 1 day | 2 days | Promise 1–2 days |
| Second Class | 2 days | 4 days | Promise 3–4 days |
| Same Day | 0 days | 0.5 days | Promise 1 day |

**Expected impact:** First Class SLA compliance goes from 0% to 95%+ immediately. No new carriers. No operational changes. No investment. Just an honest promise.

---

### Recommendation 2 — Audit the Three Highest-Cost Corridors (Medium Term)

Western Europe, Central America, and the Caribbean together account for over $4M in delay costs. These markets should be the first to have carrier contracts reviewed — not to assign blame, but to determine whether achieving true 1-day First Class delivery is operationally and financially feasible in these high-volume markets.

---

### Recommendation 3 — Underpromise, Overdeliver (Strategic)

The smartest long-term approach is not to lower expectations — it is to set honest ones with upside built in.

> Instead of: *"First Class — Delivered in 1 day"*
> Say: *"First Class — Usually 1 day, guaranteed within 2"*

When delivery arrives in 1 day → customer is delighted, exceeded expectations.
When delivery arrives in 2 days → customer expected it, promise was kept.

This is the approach used by the most trusted logistics brands in the world. It protects customer relationships while eliminating structural SLA breaches — and it costs nothing to implement.

---

### Recommendation 4 — Build a Monitoring System (Strategic)

This dashboard should not be a one-time analysis. It should run weekly, automatically flag any shipping mode that drops below 70% SLA compliance, and surface to operations leadership before a bad week becomes a bad quarter.

The cost of catching a compliance problem early is a conversation. The cost of catching it late is another $14 million.

---

## Project Summary

```
Problem:   57.3% of 172,765 global shipments missed their SLA
Cost:      $13,841,971 in delay-related costs
Suspects:  Geography · Product Type · Shipping Mode
Ruled Out: Geography (ANOVA, negligible effect)
           Product Type (Kruskal-Wallis, p = 0.689)
Root Cause: SLA windows configured at 50% of operational delivery time
           for First Class and Second Class modes
Fix:       Recalibrate promised windows · Audit top corridors · Monitor weekly
Impact:    First Class compliance: 0% → 95%+ with zero operational change
```

---

## Technical Stack

| Layer | Tools |
|---|---|
| Data Cleaning | Python · Pandas · NumPy |
| Analysis | SQL · PostgreSQL |
| Statistics | SciPy · ANOVA · Chi-Square · Kruskal-Wallis · Z-Test · Spearman |
| Dashboard | Streamlit · Plotly |

---

## About

**Naren Karthikeyan** · Integrated MTech, Computer Science (Data Science)
Vellore Institute of Technology · [LinkedIn](https://linkedin.com/in/narenkarthikeyana/) · [GitHub](https://github.com/coderfox-cap)
