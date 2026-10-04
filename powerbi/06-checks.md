# 6. Checks: the numbers each page must show

Every number below comes from the notebook ([`analysis/analysis.ipynb`](../analysis/analysis.ipynb)) and is produced again by the SQL under it, run on the same two CSV files Power BI loads. If a visual shows something else, the build is wrong; the most likely causes are listed at the end.

To run a query: from the repo folder, `python`, then `import duckdb` and `duckdb.sql("""<paste the query>""").show()`.

## Page 1: Overview

| Visual | Must show |
|---|---|
| Customers | 5,832 |
| Revenue (purchases minus returns) | £16,361,570 |
| Purchase invoices | 36,573 |
| Customers who came back | 72.6% |

```sql
SELECT
    (SELECT COUNT(*) FROM 'data/customers.csv')                                AS customers,
    (SELECT ROUND(SUM(amount), 2) FROM 'data/invoices.csv')                    AS revenue,
    (SELECT COUNT(*) FROM 'data/invoices.csv' WHERE invoice_type = 'Purchase') AS purchase_invoices,
    (SELECT ROUND(100.0 * AVG(CASE WHEN orders >= 2 THEN 1 ELSE 0 END), 1)
       FROM 'data/customers.csv')                                              AS repeat_customers_pct
```

The bar chart and the table, one row per group:

| Group | Customers | Share of customers | Revenue | Share of revenue | Days since last order (median) | Orders (median) | Spend (median) |
|---|---|---|---|---|---|---|---|
| Champions | 1,772 | 30.4% | £12,619,473 | 77.1% | 22 | 9 | £3,102 |
| Loyal | 779 | 13.4% | £551,754 | 3.4% | 30 | 3 | £653 |
| New | 364 | 6.2% | £136,347 | 0.8% | 46 (45.5) | 1 | £266 |
| At risk | 631 | 10.8% | £1,978,042 | 12.1% | 226 | 6 | £1,972 |
| Lost | 2,286 | 39.2% | £1,075,954 | 6.6% | 396 | 1 | £341 |
| **Total** | **5,832** | **100.0%** | **£16,361,570** | **100.0%** | **96** | **3** | **£844** |

```sql
SELECT segment,
       COUNT(*)                                               AS customers,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1)     AS customer_share_pct,
       ROUND(SUM(spend))                                      AS revenue,
       ROUND(100.0 * SUM(spend) / SUM(SUM(spend)) OVER (), 1) AS revenue_share_pct,
       MEDIAN(recency_days)                                   AS median_days,
       MEDIAN(orders)                                         AS median_orders,
       ROUND(MEDIAN(spend))                                   AS median_spend
FROM 'data/customers.csv'
GROUP BY segment, segment_order
ORDER BY segment_order
```

Revenue by month, the last three columns: October 2011 £961,966, November 2011 £1,112,796, December 2011 £338,152 (the data stops on 9 December).

```sql
SELECT strftime(invoice_date, '%Y-%m') AS month, ROUND(SUM(amount)) AS revenue
FROM 'data/invoices.csv'
GROUP BY month
ORDER BY month DESC
LIMIT 3
```

## Pages 2 to 6: one page per group

The five cards on each page are the group's row in the table above. The first row of the "Who to call first" table:

| Page | Customer | Country | Last order | Days since | Orders | Spend |
|---|---|---|---|---|---|---|
| Champions | 18102 | United Kingdom | 9 Dec 2011 | 1 | 145 | £578,408.64 |
| Loyal | 13365 | United Kingdom | 6 Nov 2011 | 34 | 2 | £2,164.32 |
| New | 12752 | Norway | 19 Sep 2011 | 82 | 1 | £4,366.78 |
| At risk | 16754 | United Kingdom | 2 Dec 2010 | 373 | 29 | £54,692.82 |
| Lost | 13687 | United Kingdom | 27 Sep 2010 | 439 | 1 | £11,880.84 |

```sql
SELECT segment, customer_id, country, last_purchase, recency_days, orders, spend
FROM 'data/customers.csv'
QUALIFY ROW_NUMBER() OVER (PARTITION BY segment ORDER BY spend DESC) = 1
ORDER BY segment_order
```

## Page 7: Return by starting month

| Visual | Must show |
|---|---|
| New customers who bought again the next month | 20.8% |
| Customers who came back at least once | 72.6% |
| Matrix, column 0 | 100% on every row |
| Matrix, column 1 | Dec 2009 35.1%, Jan 2010 21.5%, Oct 2011 32.0%, Nov 2011 14.2%; Dec 2011 has no column 1 |

```sql
-- Column 1 of the matrix, row by row
SELECT strftime(c.cohort_month, '%Y-%m')                                               AS starting_month,
       COUNT(DISTINCT c.customer_id)                                                   AS customers,
       ROUND(100.0 * COUNT(DISTINCT i.customer_id) / COUNT(DISTINCT c.customer_id), 1) AS back_next_month_pct
FROM 'data/customers.csv' c
LEFT JOIN 'data/invoices.csv' i
       ON i.customer_id = c.customer_id AND i.invoice_type = 'Purchase' AND i.month_offset = 1
GROUP BY starting_month
ORDER BY starting_month

-- The card: starting months January 2010 to November 2011 together
SELECT ROUND(100.0 * COUNT(DISTINCT i.customer_id) / COUNT(DISTINCT c.customer_id), 1) AS back_next_month_pct
FROM 'data/customers.csv' c
LEFT JOIN 'data/invoices.csv' i
       ON i.customer_id = c.customer_id AND i.invoice_type = 'Purchase' AND i.month_offset = 1
WHERE c.cohort_month BETWEEN DATE '2010-01-01' AND DATE '2011-11-01'
```

## If a number is wrong

| Symptom | Likely cause |
|---|---|
| Every share shows 100% in the bar chart or table | `REMOVEFILTERS` in the share measures names `segment` but not `segment_order` |
| Every cell of the matrix shows 100% | The `customers` to `invoices` relationship is set to both directions, so the month filter also shrinks the group size |
| Revenue is 100 times too big, or dates fail to load | The `"en-US"` culture is missing from the Changed Type step |
| Groups in alphabetical order | `segment` is not sorted by `segment_order` |
