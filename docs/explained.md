# The project explained, from zero

This page explains the whole project in plain words: what it does, what every word means, where every number comes from, and how to talk about it in an interview. You do not need to know Python, SQL or Power BI to read it.

[← Back to the README](../README.md)

## 1. The project in one minute

An online shop has a few thousand customers. Some buy every few weeks and spend a lot. Some bought once and never came back. Some used to buy a lot and have gone quiet. The shop treats them all the same: the same emails, the same discounts.

So the owner cannot answer simple questions:

- Which customers bring in most of the money?
- Which good customers have stopped buying, and who should be called first?
- How many new customers come back for a second order?

This project answers them. It reads the shop's invoice lines, cleans them, and gives every customer three scores: how recently they bought, how often, and how much they spent. Two plain questions then sort every customer into one of five groups, and each group gets its own action. The at-risk group becomes a call list, biggest spender first. A Power BI report shows it all.

Think of it like a gym's member list. Members who came this week and come often are the regulars to look after. Members who used to come three times a week but have not been seen for months are the ones to phone today, before they cancel. Members who came once and never again get one friendly email.

## 2. Words you will meet

| Word | What it means here |
|---|---|
| **Invoice line** | One row of the input file: one product on one invoice, with its quantity and unit price. The file has 1,067,371 of them. |
| **Invoice** | One order: all the lines with the same invoice number. Its total is the sum of its lines. |
| **Return** | An invoice whose number starts with `C`, for example `C551464`. Its quantities are negative, so its amount is taken off what the customer spent. A cancelled order is a return too. |
| **Customer ID** | The number that says who placed the invoice, for example `13085`. It is kept as text so a code like `01234` keeps its leading zero. |
| **GBP** | Pounds sterling, the currency of the data. "GBP 1,978,042" means about 1.98 million pounds. |
| **Spend** | What a customer bought minus what they returned. It is revenue, not profit. |
| **Revenue** | Here, the spend of all scored customers added up: GBP 16,361,570.13. |
| **RFM** | Recency, frequency, monetary: the standard way to score customers. This repo calls monetary "spend", so the three scores are `r_score`, `f_score` and `m_score`. |
| **Recency** | Days from a customer's last purchase to the snapshot date. Fewer days is better. |
| **Frequency** | The number of purchase invoices (orders) a customer placed. Returns do not count. |
| **Snapshot date** | "Today" for the analysis: the day after the last purchase in the data, 10 Dec 2011. |
| **Score (1 to 4)** | Customers are ranked on one measure and split into four equal shares (quarters). The best quarter gets 4, the worst gets 1. Customers with the same value get the same score. |
| **Still buying** | A recency score of 3 or 4. Here that means a last order within 95 days. |
| **Good customer** | Frequency score plus spend score is 6 or more. For example 4 + 2, or 3 + 3. |
| **Group (segment)** | One of five: **Champions**, **Loyal**, **New**, **At risk**, **Lost**. See the table in section 3. |
| **Median** | The middle value when you sort a list. Half the customers are above it, half below. It is not pulled up by one huge spender the way an average is. |
| **Cohort, starting month** | All customers whose first purchase fell in the same month. "The Jan 2010 cohort" is everyone who first bought in January 2010. |
| **Month offset** | How many calendar months after the starting month a purchase happened. 0 is the starting month itself, 1 is the next month. |
| **The six layers** | The names of the steps, in order. **Bronze layer:** the input file as received. **Silver layer:** clean rows, one row per invoice. **Gold layer:** the business rules, here the scores and the groups. **Semantic layer:** the fact and dimension tables Power BI loads. **Analytical layer:** the aggregates and KPIs, here the cohort table and the DAX measures. **Reporting layer:** the Power BI pages and the charts. The README's "For engineers" table says where each one is. |
| **Data health check** | The cleaning rules, one at a time, with how many lines each removes. Shown in `docs/data-health.png`. |
| **Exact duplicate** | A line that appears twice with every column the same. |
| **Product code** | The code of what was sold, for example `85048`. A real product has a code that starts with five digits; postage (`POST`), bank charges and manual adjustments (`M`) do not. |
| **Regular expression** | A short pattern for matching text. `^\d{5}` means "starts with five digits". It is the product rule in `config/client.yaml`. |
| **Python, pandas** | Python is a programming language. pandas is its library for tables. The notebook uses them for every step. |
| **Notebook** | `analysis/analysis.ipynb`, a file that mixes code, its output and notes. It computes every number in the README. |
| **SQL** | Structured Query Language, the standard language for asking questions of tables. Here it is used to compute the key numbers a second time. |
| **DuckDB** | A small database that runs inside Python, with no server to start. The notebook uses it to run SQL directly on its tables. |
| **CSV** | Comma-separated values: a plain text file of a table, one row per line. The notebook writes two of them for Power BI. |
| **Sheet** | One tab of an Excel file. The input file has two sheets, one per year. |
| **`config/client.yaml`** | The settings a client would change: the file name, its column headers, the rules, the currency, the colours. YAML is a simple text format for settings. |
| **Power BI** | Microsoft's tool for interactive reports and dashboards. |
| **Power Query, M** | The part of Power BI that loads and shapes data before the report uses it. M is its formula language. |
| **DAX** | Data Analysis Expressions, the formula language of Power BI, used to write **measures** (calculations like "Revenue" or "Customer Share %"). |
| **Fact table** | The big table of events you add up. Here `invoices`: one row per invoice, with its amount. |
| **Dimension table** | A table that describes the facts and is used to filter and group them. Here `customers` (one row per customer, with scores and group) and `Date`. |
| **Star schema** | One fact table in the middle with dimension tables around it. See [data-model.svg](data-model.svg). |
| **Grain** | What one row of a table stands for. The grain of `invoices` is "one invoice"; of `customers`, "one customer". |
| **Primary key (PK), foreign key (FK)** | The PK is the column that makes each row unique (`customer_id` in `customers`). An FK points to a row in another table (`customer_id` in `invoices`). |
| **Date table** | A table with one row per day, so every month exists in the report even if nothing was sold. Built in DAX. |
| **Slicer** | A filter on a Power BI page, here by country. |

## 3. How it works, file by file

Run in this order (the commands are in the README's "Run it" section). There is no database server and no `sql/` folder: the SQL lives in notebook cell 20 and in `powerbi/06-checks.md`.

| Step | File | What it does |
|---|---|---|
| 0 | `requirements.txt` | The Python libraries, with their versions. `pip install -r requirements.txt` installs them. |
| 1 | `data/demo/download.py` | Downloads the demo input file into `data/input/` (see Data in the README). A client copies their own file there instead. |
| 2 | `config/client.yaml`, `config.py` | Hold every setting. `load_config()` stops if a setting is missing. `read_transactions()` reads the file (every sheet), renames the client's headers to standard names, and stops with one line if the file, a column or a date is wrong. |
| 3 | `analysis/analysis.ipynb` cells 3 to 6 | Bronze and Silver layers: read the 1,067,371 lines and clean them, the data health check. The removed lines are counted, then dropped; no file keeps them. |
| 4 | cell 8 | Silver layer: adds the lines up to one row per invoice. |
| 5 | cell 10 | Gold layer: scores every customer on recency, frequency and spend. |
| 6 | cells 12 to 15 | Gold layer: sorts customers into the five groups and draws `segments.png` and the call list `at-risk.png`. |
| 7 | cells 17 and 18 | Analytical layer: cohorts, how many of each month's new customers come back. Draws `cohorts.png`. |
| 8 | cell 20 | Recomputes the key numbers in SQL with DuckDB. If any differs, the notebook stops. This check is not a layer. |
| 9 | cell 22 | Semantic layer: writes `data/invoices.csv` and `data/customers.csv`, the two tables Power BI loads. |
| 10 | `theme.py` | Writes the Power BI theme (`powerbi/05-theme.json`) from the colours in `client.yaml`. |
| 11 | `powerbi/` | Step-by-step instructions to build the 7-page report: queries, model, the 14 measures (the rest of the Analytical layer), pages (the Reporting layer), and the numbers each page must show (`06-checks.md`). |

### The two questions

| | Good customer (F + M is 6 or more) | Not (yet) |
|---|---|---|
| **Still buying** (R is 3 or 4) | **Champions** | **Loyal** if 2 or more orders, **New** if 1 order |
| **Stopped** (R is 1 or 2) | **At risk** | **Lost** |

### The rules, with an example

One real customer, `13085`. It is the customer on the very first line of the input file, the example row in [`data/input/README.md`](../data/input/README.md). All the values below were checked against the input file and `data/customers.csv`.

1. **Raw lines.** The file holds 92 lines for this customer. The first one is invoice `489434`, product `85048`: 12 × GBP 6.95 = GBP 83.40.
2. **Clean.** One of the 92 lines is removed: return `C527339`, product code `M`, a manual adjustment of GBP 830.12. `M` does not start with five digits, so it is "not a product". 91 lines are left. None was a duplicate, and all have a customer ID.
3. **One row per invoice.** The 8 lines of invoice `489434` add up to GBP 505.30. In total this customer has 8 purchase invoices and 1 return (`C551464`, 28 Apr 2011, GBP −143.70).
4. **Spend.** The 8 purchases add up to GBP 2,433.28. Minus the return: 2,433.28 − 143.70 = **GBP 2,289.58**.
5. **Recency.** The last purchase was on 5 Jul 2011. From 5 Jul to the snapshot date, 10 Dec 2011, is **158 days**.
6. **Scores.** Notebook cell 10 prints the range of each score. 158 days falls in 96 to 377, so **R = 2**. 8 orders falls in 8 to 373, so **F = 4**. GBP 2,289.58 is above 2,180, so **M = 4**.
7. **Group.** R = 2, so the customer has **stopped** buying. F + M = 4 + 4 = 8, which is 6 or more, so it is a **good customer**. Stopped and good: **At risk**. A customer who placed 8 orders and has gone quiet for five months is exactly who the shop should call.
8. **Cohort.** The first purchase was on 1 Dec 2009, so the starting month is Dec 2009. The customer bought again on 29 Jan 2010, month offset 1, so they count in the Dec 2009 row's "next month" share (35%).

## 4. Every number, explained

All of these are printed by the notebook ([`analysis/analysis.ipynb`](../analysis/analysis.ipynb)) unless the row says otherwise. The cell numbers below count from 0, the first cell. A few divisions show amounts the notebook keeps but does not print on their own; those are marked "worked out here". The notebook's group table rounds amounts to whole pounds; the amounts with pence below are the same sums taken from `data/customers.csv`, which the notebook writes.

### The headline and the results table

| Number | What it means | How it is worked out | Where |
|---|---|---|---|
| **1,067,371 invoice lines** | Every line in the input file, both sheets. | Count of rows read. | cell 3 |
| **December 2009 to December 2011** | The time the data covers. | First and last invoice date: 1 Dec 2009 to 9 Dec 2011. | cell 3 |
| **5,832 customers** | Every customer who was scored. | Customers with at least one purchase whose spend is above zero. | cell 10 |
| **36,573 purchase invoices** | The orders of those 5,832 customers. | Count of invoices not starting with `C`, after cleaning, for scored customers only. | cell 24 |
| **GBP 16,361,570.13** | The total revenue the shares are taken from. | Sum of spend over the 5,832 customers. Also the sum of `amount` in `invoices.csv`. | cell 24 |
| **10 Dec 2011** | The snapshot date. | The last purchase date (9 Dec 2011) plus one day. | cell 10 |
| **Champions: 1,772 (30.4%) bring 77.1%** | A third of the customers bring three quarters of the money. | 1,772 / 5,832 = 30.4%. Their spend GBP 12,619,473.10 / 16,361,570.13 = 77.1%. | cells 12 and 20 |
| **631 good customers (10.8%) have stopped buying** | The at-risk group: the call list. | 631 / 5,832 = 10.8%. | cells 15 and 20 |
| **12.1% of the revenue** | What the at-risk customers spent. | GBP 1,978,041.75 / 16,361,570.13 = 12.1%. | cell 15 |
| **226 days** | How long ago the typical at-risk customer last ordered. | The median recency of the 631. | cell 12 |
| **72.6% ordered more than once** | Most customers came back at least once. | Customers with 2 or more orders / all customers: 4,233 / 5,832 = 72.6%. The notebook prints only the share; the 4,233 is counted here from `customers.csv`. | cell 17 |
| **20.8% buy again the next month** | Of new customers, about one in five orders again in the very next calendar month. | 1,009 / 4,856 new customers who first bought between Jan 2010 and Nov 2011. | cell 17; again in SQL in cell 20 |
| **95 days** | What "still buying" means in days. | The longest recency among customers with R = 3 or 4. | cell 12 |
| **1 to 4, 3 or 4, 6 or more** | The score levels and the two thresholds. | Settings: `rules.score_levels`, `rules.still_buying_min_recency_score`, `rules.good_customer_min_frequency_plus_spend` in `config/client.yaml`. A client can change them. | `config/client.yaml` |

The other three groups, from the same cells: **Loyal** 779 customers (13.4%) with GBP 551,754.13 (3.4%), **New** 364 (6.2%) with GBP 136,347.47 (0.8%), **Lost** 2,286 (39.2%) with GBP 1,075,953.68 (6.6%).

### The data health check

| Number | What it means | How it is worked out | Where |
|---|---|---|---|
| **34,335 duplicates** | Lines that appear twice, every column the same. | 1,067,371 − 1,033,036 lines left. | cell 5 |
| **1 to 9 December 2010** | Where most duplicates come from: the first sheet ends on 9 Dec 2010 and the second starts on 1 Dec 2010, so both hold these days. | 22,844 of the 34,335 duplicates are dated 1 to 9 Dec 2010; the other 11,491 are spread across the rest. Worked out here from the input file; the notebook does not print it. | input file |
| **235,151 lines with no customer ID** | Lines nobody can be scored or called for. | 1,033,036 − 797,885. | cell 5 |
| **13.6% of the revenue** | What those lines are worth. | GBP 2,565,542.41 / 18,855,533.70: quantity × price on lines with no ID, over all lines after duplicates are removed (fees and returns included). The notebook prints the share; the two amounts are worked out here. | cell 5 |
| **3,662 not a product** | Postage, bank charges, fees, manual adjustments. | 797,885 − 794,223. | cell 5 |
| **60 missing quantity or zero price** | Free lines or numbers that could not be read. | 794,223 − 794,163. | cell 5 |
| **794,163 lines left** | The clean lines everything else is built on. | After the four rules. | cell 5 |
| **7,282 returns take GBP 709,953 off GBP 17,068,568** | Returns are kept and taken off spend. | Sum of return amounts and of purchase amounts on the clean lines. | cell 6 |
| **80,995 units** | A single order cancelled 12 minutes later. | Invoice `581483` at 9:15 on 9 Dec 2011, 80,995 × GBP 2.08 = GBP 168,469.60, cancelled by `C581484` at 9:27. Customer `16446` really spent GBP 2.90 and is in Loyal. Counting the order without the return would make them the 8th biggest spender. Found here in the input file; the notebook does not print it. | input file |

### The charts and diagrams

| Number | Where you see it | What it means |
|---|---|---|
| **30%, 13%, 6%, 11%, 39%** | header.svg, top bar | Each group's share of customers, rounded: 30.4%, 13.4%, 6.2%, 10.8%, 39.2%. |
| **77%, 12%, 7%** | header.svg, bottom bar | Share of revenue for Champions, At risk and Lost. The Loyal (3.4%) and New (0.8%) slices are too thin to carry a label. |
| **1,772 (30%), 779, 364, 631, 2,286** | mental-model.svg | Customers per group, from cell 12. |
| **77%, 3%, 1%, 12%, 7%** | mental-model.svg | Share of revenue per group, rounded from 77.1%, 3.4%, 0.8%, 12.1%, 6.6%. |
| **1 to 4, F + M 6 or more, R 3 or 4, 95 days** | mental-model.svg | The scores and the two questions, as in section 3. |
| **01 to 06** | how-it-works.svg | The six layers: Bronze, Silver, Gold, Semantic, Analytical, Reporting. The notebook builds layers 1 to 4 and the cohort table; Power BI adds the measures and the pages. |
| **1,067,371, −34,335, −235,151, −3,662, −60, 794,163** | data-flow.svg | The data health check, from cell 5. |
| **43,876** | data-flow.svg | Invoices in the Silver layer, before the 69 invoices of customers who are not scored are left out (see below). Cell 8. |
| **631** | data-flow.svg | The at-risk call list in the Gold layer. Cell 15. |
| **20 with spend ≤ 0** | data-flow.svg | Customers whose returns cancel out their purchases, left out of the Gold layer. Cell 10. |
| **25 rows** | data-flow.svg | The cohort table in the Analytical layer: one row per starting month, Dec 2009 to Dec 2011. Cell 17. |
| **43,807** | data-flow.svg, data-model.svg | Rows in `invoices.csv`: one per invoice of a scored customer (36,573 purchases + 7,234 returns). |
| **5,832** | data-flow.svg, data-model.svg | Rows in `customers.csv`: one per scored customer. |
| **section 1, sections 2, 3, sections 4, 5, section 8, section 6, section 7** | data-flow.svg | The notebook's numbered headings under each layer, not cell numbers. Section 2 (cleaning) is cells 4 to 6. Section 6 runs before section 8 but reads only the columns section 8 saves. |
| **4 charts** | data-flow.svg | `data-health.png`, `segments.png`, `at-risk.png`, `cohorts.png`. |
| **7 pages** | data-flow.svg | Overview, one page per group, and the return-by-starting-month page. |
| **761 days** | data-model.svg | Rows in the DAX Date table: 1 Dec 2009 to 31 Dec 2011, every day of every month in the data (31 + 365 + 365). Worked out here; the table is built in Power BI. |
| **14 measures, in 3 display folders** | data-model.svg, data-flow.svg | Counted in `powerbi/03-measures.dax`: 6 in Customers, 5 in Revenue, 3 in Cohorts. |
| **1 and \*** | data-model.svg | One customer, or one day, links to many invoices. |
| **Customer 16754, GBP 54,692.82, 373 days** | at-risk.png, top bar | The biggest at-risk customer: 29 orders, last one on 2 Dec 2010. Cell 15. |
| **about 21%** | cohorts.png title | 20.8%, rounded. |

### Things that can look wrong but are not

- **Cell 8 says 36,594 purchases and 43,876 invoices; the README says 36,573 and `invoices.csv` has 43,807.** The 69 missing invoices (21 purchases, 48 returns) belong to 43 customers whose returns cancel out everything they bought. 20 of them bought something and are dropped in cell 10 ("20 customers ... are left out"). The other 23 only have returns, so they never enter the customer table. Cell 17 then keeps only the invoices of scored customers. The 43, 21 and 48 were counted here from the input file.
- **Cell 6 gives 17,068,568 − 709,953 = 16,358,615, but the revenue is 16,361,570.13.** The same 43 customers had a net spend of GBP −2,955.59. Taking them out raises the total: 16,358,614.54 + 2,955.59 = 16,361,570.13.
- **Row counts shrink from layer to layer, on purpose.** 1,067,371 lines (Bronze layer) → 794,163 clean lines → 43,876 invoices (Silver layer) → 5,832 customers (Gold layer) → 43,807 invoices for scored customers and 5,832 customers (Semantic layer). Customers: 5,875 in the clean lines → 5,852 with a purchase → 5,832 with spend above zero.
- **The quarters are not exactly equal.** Frequency scores 1 to 4 hold 1,599, 1,603, 1,340 and 1,290 customers. Every customer with one order gets the same score, and there are many of them. Recency and spend are close to even (1,465 / 1,452 / 1,475 / 1,440 and about 1,458 each). Counted here from `customers.csv`.
- **The score ranges in cell 10 seem to touch** (844 tops spend score 2 and starts score 3). The table rounds spend to whole pounds; the real values do not overlap.
- **30 + 13 + 6 + 11 + 39 = 99, not 100**, in the header. Each share is rounded. The exact shares add up to 100.0%.
- **72.6% came back, but only 20.8% the next month.** Different questions: 72.6% is "ever placed a second order", over all 5,832 customers. 20.8% is "ordered in the very next calendar month", over the 4,856 new customers from Jan 2010 to Nov 2011.
- **The Dec 2009 row of the cohort chart (35% next month) is much higher than the rest.** The data starts in December 2009, so that row also holds long-standing customers buying for the first time *in this data*. That is why it, and Dec 2011 (no next month yet), are left out of the 20.8%.

## 5. What the results mean for the business

- **A third of the customers carry the shop.** Champions are 30.4% of customers and 77.1% of revenue. Losing a few of them hurts more than losing hundreds of others. Keep them close and ask them for referrals.
- **The most urgent money is with the at-risk group.** 631 customers who used to buy often and spend well have stopped. They brought 12.1% of the revenue, GBP 1.98 million. A phone call to the top of that list costs little next to what each one used to spend.
- **Lost customers are many but small.** 2,286 customers (39.2%) brought only 6.6% of the revenue. One win-back email is enough; calls would cost more than they bring.
- **The second order is the hard part.** Only 20.8% of new customers order again the next month, yet 72.6% of all customers order at least twice in the end. A follow-up soon after the first order is where the shop can win.
- **Returns must count.** One customer ordered 80,995 units and cancelled 12 minutes later. Without taking returns off spend, a GBP 2.90 customer would look like a top-10 one.

## 6. Interview questions you can expect

**Explain the project in 30 seconds.**
A shop treated every customer the same and did not notice good customers leaving. I cleaned about a million invoice lines in a Python notebook, scored every customer on recency, frequency and spend from 1 to 4, and used two plain questions to sort them into five groups with one action each. The notebook checks every key number again in SQL, and a Power BI report shows the groups and a call list. Result: 30% of customers bring 77% of revenue, and 631 good customers worth 12% of revenue have stopped buying.

**Why score by quarters of customers and not by fixed limits like "over GBP 1,000"?**
Quarters work for any shop without anyone choosing limits: a wholesaler and a small shop both get four even groups. The trade-off is that the groups are relative, so a customer's group depends on everyone else. The README says so in Limits.

**Why five groups from two questions, and not the usual long RFM segment list or a clustering model?**
Each group has to lead to an action someone can take on Monday. Two yes-or-no questions are easy to explain to a sales team, and the thresholds sit in `config/client.yaml` so a client can change them. A clustering model can find groups, but nobody can say in one sentence why a customer is in one.

**Why keep the returns and take them off spend?**
Because some big orders were cancelled minutes later. Customer `16446` ordered 80,995 units and cancelled 12 minutes later; counting only the order would turn a GBP 2.90 customer into the 8th biggest spender.

**Lines with no customer ID carry 13.6% of the revenue. Why remove them?**
A customer who cannot be identified cannot be scored or called. The share is printed by the notebook and listed in Limits, so nobody mistakes the analysed revenue for all of it.

**How do you know the numbers are right?**
Cell 20 recomputes recency, frequency and spend for all 5,832 customers, the group shares and the 20.8% in plain SQL with DuckDB, and the notebook stops if any number differs. `powerbi/06-checks.md` lists the number each Power BI page must show, with the SQL that produces it from the same two CSV files.

**Why a notebook and DuckDB, not a database server?**
One million lines fit easily in memory, so pandas does the work and DuckDB runs SQL on the same tables with nothing to install or start. If the shop sent new invoices every day, I would load them into a warehouse on a schedule and keep the same rules.

**Why are the scores and groups computed in the notebook, not in DAX?**
So they are written once and everything reads the same answer. Power BI loads them as plain columns with no calculated columns; the measures only add up and divide.

**Why leave December 2009 and December 2011 out of the 20.8%?**
December 2009 is the first month of the data, so it mixes new customers with older ones seen for the first time. December 2011 has no next month yet. Keeping either would bend the average.

**How would you set it up for a real client?**
Put their transactions file in `data/input/`, set its name, headers and date format in `config/client.yaml`, and run the notebook. `config.py` stops with one clear line if a column or a date is wrong. No code changes.

## 7. Limits, in plain words

- The groups are relative. Scores are quarters of these customers, so a customer's group depends on everyone else's.
- Spend is revenue, not profit. The data has no costs.
- The December 2009 starting month also holds older customers, because the data starts there.
- 13.6% of the revenue has no customer ID and is outside the analysis.
- The snapshot date is fixed at the end of the data. On live data, recency would be counted from today.
