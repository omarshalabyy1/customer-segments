# New client

This repo is a GitHub template. A new client gets a **private** repo from it (Use this template > Create a new repository > Private); client data never goes into this public repo.
Everything that changes per client is in two places: `config/client.yaml` and the transactions file in `data/input/`. There is no secret, so there is no `.env`.

## Done in the template

What the client gets with no work. Hours are an estimate of building each part from scratch.

| # | Part | Estimate (hours) |
|---|---|---|
| A | Transactions reader: `.csv` or every sheet of an `.xlsx`, the client's headers mapped to standard names, IDs kept as text, dates read only in the set format, one-line stops (`config.py`, `read_transactions()`) | 1.5 |
| B | Data health check: duplicates, missing customers, non-product lines and zero prices removed and counted, returns taken off spend, the revenue with no customer, the health chart (notebook sections 2 and 3) | 2 |
| C | Recency, frequency and spend scores by equal shares with ties kept together, the five groups from two questions, the score table in plain numbers, the groups chart (sections 4 and 5) | 2.5 |
| D | The call list: at-risk customers, biggest spend first, and its chart | 0.5 |
| E | Cohorts: starting month, month offsets, the return table, the next-month return rate with the first and last month left out, the heatmap (section 6) | 2 |
| F | SQL recount in DuckDB of every customer's recency, frequency and spend, the groups and the return rate, with the dates as parameters; the two tables Power BI loads (sections 7 and 8) | 1.5 |
| G | Client settings: `config/client.yaml`, `load_config()`, the Power BI theme written from the config (`theme.py`) | 1 |
| H | Power BI build pack: 2 queries, the model, 14 measures, 7 pages with 62 visuals, interactions, 16 checks, a 36-step checklist (`powerbi/`) | 6 |
| I | README with its diagrams, and the input file guide (`data/input/README.md`) | 3 |
| | **Total** | **20** |

## Configure

Per client, file by file. Hours are an estimate.

| File | Key | Example | Estimate (hours) |
|---|---|---|---|
| `config/client.yaml` | `client.name`, `client.currency`, `report.title`, `report.colours` | `EGP`, `"#0F766E"` | 0.25 |
| `config/client.yaml` | `inputs.transactions`, `inputs.date_format`, the seven `columns` | `delta_sales.csv`, `"%d/%m/%Y"`, `customer_id: Client Code` | 0.5 |
| `config/client.yaml` | `rules.return_invoice_prefix`, `rules.product_code_pattern`: read the client's codes for returns, fees and postage | `RET-`, `'^CF-'` | 0.5 |
| `config/client.yaml` | `rules.score_levels`, `rules.still_buying_min_recency_score`, `rules.good_customer_min_frequency_plus_spend`: agree them with the client after the first run, from the score table | `3`, `2`, `5` | 0.5 |
| Run `theme.py` and the notebook; go through the health table and the groups with the client | | | 1 |
| | **Subtotal without Power BI** | | **2.75** |
| `powerbi/` | build from `08-build-checklist.md`: the file path in the two queries, the currency in the format strings, the five group descriptions; fill `06-checks.md` from the notebook | | 3.5 |
| | **Total with Power BI** | | **6.25** |

## Custom, by offering

Template hours count only the parts (A to I above) that the offering delivers. Hours are estimates.

### Customer segments analysis (the project card)

Who brings the revenue, who is slipping away and who to call first, with a Power BI page per group. Uses A to I (20 hours); configure 6.25 hours.

| Work | Estimate (hours) |
|---|---|
| The group names and "what to do" lines in the client's words, agreed in one call | 1 |
| One extra column the client sells by (branch, channel, salesperson) as a slicer on every page | 1.5 |
| A one-page summary for the owner: the numbers, the call list, three actions | 1 |
| **Total** | **3.5** |

The same analysis without Power BI (the notebook, its charts and the two output tables) uses A to G and I (14 hours), configure 2.75 hours and custom 2 hours (the names call and the summary).

### 19. Data health check: where your data is costing you money

Uses A, B, G and the input guide in I (5.5 hours: 1.5 + 2 + 1 + 1); configure 2 hours (name and currency, the file and headers, the two cleaning rules, one review run). Most of this offering is investigation the template cannot do in advance: this repo checks one transactions export, while the offering ranks fixes across the client's data.

| Work | Estimate (hours) |
|---|---|
| The same checks on the client's other exports (products, customers, stock): duplicates, missing keys, codes that do not match | 4 |
| What each problem costs: staff time from two short interviews, revenue that cannot be traced (like the share with no customer ID) | 2 |
| The ranked list of fixes with the time each would save, and the plan | 3 |
| A short report and a walk-through call | 2 |
| **Total** | **11** |

## Share already done (estimate)

Template hours ÷ (template + configure + custom) hours:

| Offering | Arithmetic | Share already done |
|---|---|---|
| Customer segments analysis, with the Power BI report | 20 ÷ (20 + 6.25 + 3.5) = 20 ÷ 29.75 | **67%** (67.2%) |
| Customer segments analysis, notebook only | 14 ÷ (14 + 2.75 + 2) = 14 ÷ 18.75 | **75%** (74.7%) |
| 19. Data health check | 5.5 ÷ (5.5 + 2 + 11) = 5.5 ÷ 18.5 | **30%** (29.7%) |

These are estimates, not measured times.

## Steps

1. Create the private repo from the template and clone it.
2. Copy the client's transactions export into `data/input/` ([columns and an example](../data/input/README.md)). Everything in that folder except its README is ignored by git.
3. Add `data/customers.csv` and `data/invoices.csv` to `.gitignore` and run `git rm --cached data/customers.csv data/invoices.csv`: in a client repo they hold customer-level results. `data/demo/` can be deleted.
4. Edit `config/client.yaml`.
5. `pip install -r requirements.txt`, `python theme.py`, then run `analysis/analysis.ipynb` (Run All). It stops with one line if a key, the file, a column or a date is wrong; fix and run again.
6. Go through the health table, the score table and the groups with the client; change the cut points if they agree, and run again.
7. Build the Power BI report from `powerbi/08-build-checklist.md`, and copy the notebook's numbers into `powerbi/06-checks.md`.

## Gaps

What the template does not cover, with the custom hours if a client needs it:

- **The analysis date** is the day after the last purchase in the file, not a configured date: the export date is the natural "today". A fixed "as of" date: 0.25 hours.
- **The group names** are fixed (champions, loyal, new, at risk, lost): the notebook, the two at-risk measures and the page filters use them. Other names or another language: 0.5 hours. They were left out of the config because the method defines them.
- **The return window** is the next calendar month. "Within 90 days" instead: 1 hour.
- **A country column is required.** A client without one adds a column with one value to the export, or 0.25 hours of custom work.
- **The README diagrams** (`header.svg`, `mental-model.svg`) are drawn by hand for the demo; the notebook charts redraw themselves. Client versions: 1 hour.
- **The Power Query file path** is typed in both queries (no parameter), part of the Power BI configure step.

## Second-client drill (2026-10-05)

The acceptance test of the template: a clone of the repo, a made-up second client, a run from scratch.

**Client B (drill):** "Delta Coffee Roasters", currency `EGP`, title "Delta Coffee segments", teal colours (`#0F766E` main, page `#F0FDFA`, danger `#B45309`).

- One CSV, `delta_sales.csv`, 50 rows, with its own headers: `Bill No`, `SKU`, `Qty`, `Bill Date` (text, `dd/mm/yyyy`), `Unit Price`, `Client Code` (leading zeros: `00101`), `Governorate`, and an extra `Cashier` column.
- Returns start with `RET-`; products start with `CF-` (a `DLV-01` delivery fee is not a product).
- Other cut points: `score_levels: 3`, still buying from recency score 2, good customer from frequency plus spend 5.
- One case for each rule: an exact duplicate line, a line with no customer, two delivery-fee lines, a free sample at price 0, a quantity typed `n/a`, two returns, and a customer whose return cancels the only purchase.

| What | Demo | Client B (drill) |
|---|---|---|
| Lines read; left after cleaning | 1,067,371; 794,163 | 50; 44 |
| Removed by rule | 34,335 duplicates, 235,151 no customer, 3,662 non-product, 60 zero price | 1 duplicate, 1 no customer, 2 non-product, 2 zero price or no quantity |
| Revenue with no customer ID | 13.6% | 2.6% |
| Returns | 7,282 invoices take GBP 709,953 off GBP 17,068,568 | 2 invoices take EGP 250 off EGP 7,570 |
| Customers scored (left out: returns cancel purchases) | 5,832 (20) | 11 (1) |
| Snapshot date | 10 Dec 2011 | 26 Apr 2026 |
| Purchase invoices; revenue | 36,573; GBP 16,361,570.13 | 24; EGP 7,320.00 |
| Champions: customers, share of customers, share of revenue | 1,772, 30.4%, 77.1% | 2, 18.2%, 44.7% |
| At risk: customers, revenue, share | 631, GBP 1,978,041.75, 12.1% | 2, EGP 2,280.00, 31.1% |
| Repeat customers; new customers back the next month | 72.6%; 20.8% | 63.6%; 25.0% (1 of 4) |
| IDs | text | text, `00101` kept |
| Power BI theme | "Customer Segments", `#2563EB` | "Delta Coffee segments", `#0F766E`, page `#F0FDFA`, danger `#B45309` |
| Notebook | 14 of 14 cells, 0 errors, SQL recount matches | 14 of 14 cells, 0 errors, SQL recount matches; titles name Delta Coffee Roasters, amounts in EGP |

**By hand** (snapshot 26 Apr 2026, the day after the last purchase on 25 Apr):

| Customer | Orders | Spend (EGP) | Days since | Scores R, F, M | Group |
|---|---|---|---|---|---|
| 00101 | 4 | 500 + 200 + 530 + 360 = 1,590 | 6 | 3, 3, 3 | Champions |
| 00109 | 5 | 450 + 380 + 400 + 100 + 350 = 1,680 | 4 | 3, 3, 3 | Champions |
| 00104 | 2 | 80 + 180 = 260 | 11 | 2, 2, 2 | Loyal |
| 00106 | 2 | 250 + 200 = 450 | 55 | 2, 2, 2 | Loyal |
| 00110 | 2 | 80 + 100 = 180 | 8 | 3, 2, 1 | Loyal |
| 00103 | 1 | 280 | 1 | 3, 1, 2 | New |
| 00107 | 1 | 160 | 47 | 2, 1, 1 | New |
| 00112 | 1 | 360 | 36 | 2, 1, 2 | New |
| 00102 | 3 | 800 + 500 + 300 - 100 return = 1,500 | 91 | 1, 3, 3 | At risk |
| 00111 | 2 | 530 + 250 = 780 | 68 | 1, 2, 3 | At risk |
| 00105 | 1 | 80 | 101 | 1, 1, 1 | Lost |

- Scores with 3 levels and 11 customers: rank 1 to 3 scores 1, rank 4 to 7 scores 2, rank 8 to 11 scores 3 (rank ÷ 11 × 3, rounded up); the four one-order customers share rank 1, the four two-order customers rank 5.
- Revenue 7,320; champions 1,590 + 1,680 = 3,270 ÷ 7,320 = 44.7%; at risk 1,500 + 780 = 2,280 ÷ 7,320 = 31.1%; repeat 7 ÷ 11 = 63.6%.
- New customers started in February (00106, 00110) or March (00107, 00112); only 00106 bought in the next month: 1 ÷ 4 = 25.0%.

Every output number matched.

**Clear failures**, one line each, run on the Client B copy:

```
config/client.yaml is missing rules.score_levels
config/client.yaml is not valid YAML near line 4 (quote a value with # or :)
missing data/input/delta_sales.csv (inputs.transactions in config/client.yaml)
data/input/delta_sales.csv: missing column(s): Client Code (columns in config/client.yaml)
data/input/delta_sales.csv: 23 invoice date(s) not readable, e.g. '20/04/2026' (inputs.date_format in config/client.yaml)
```

There is no `.env` and no mapping file, so those two tests do not apply.

**Nothing client-specific is hard-coded.** A search of `config.py`, `theme.py`, the notebook's source cells and the Power BI query, model, measure, page, interaction and checklist files for the demo's name, currency, file name, headers, return prefix, product pattern, score levels and cut points, colours and years finds one hit: the call-list column label "Country" in `powerbi/04-pages.md`, a display name that is the same for every client. The README, the diagrams and `powerbi/06-checks.md` describe the demo run and keep its values.

**Demo rerun** from the template: 14 of 14 cells, 0 errors, the same totals (5,832 customers, 36,573 purchase invoices, GBP 16,361,570.13, champions 30.4% of customers and 77.1% of revenue, 631 at risk, 20.8% back the next month), and `data/customers.csv` and `data/invoices.csv` byte for byte the same as before the template.

The first rerun did not match: with only the seven standard columns, two pairs of demo lines that differ only in their product description looked like exact duplicates (34,337 removed instead of 34,335, revenue GBP 551.85 lower). The reader now keeps the client's extra columns, so an exact duplicate means the whole line as sent; Client B's numbers did not change.
