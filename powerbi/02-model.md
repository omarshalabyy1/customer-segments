# 2. The model

A small star: one fact table (`invoices`), two dimensions (`customers` and `Date`) and a table that only holds the measures.

```
customers (1) ──► (*) invoices (*) ◄── (1) Date
```

## Tables

| Table | Grain (one row per) | Key | Rows | Comes from |
|---|---|---|---|---|
| `invoices` | invoice (purchase or return) | `invoice` | 43,807 | Power Query |
| `customers` | customer | `customer_id` | 5,832 | Power Query |
| `Date` | day, 1 Dec 2009 to 31 Dec 2011 | `Date` | 761 | DAX calculated table (below) |
| `_Measures` | holds the measures only | none | 0 | Enter data |

## The Date table

**Modeling → New table**, paste:

```dax
Date =
ADDCOLUMNS (
    CALENDAR ( DATE ( 2009, 12, 1 ), DATE ( 2011, 12, 31 ) ),
    "Year", YEAR ( [Date] ),
    "Month Start", DATE ( YEAR ( [Date] ), MONTH ( [Date] ), 1 ),
    "Month", FORMAT ( [Date], "mmm yyyy" )
)
```

Then select the table, **Table tools → Mark as date table**, and pick the `Date` column.

## The measures table

**Home → Enter data**, name the table `_Measures`, leave the one column empty and click **Load**. After you add the first measure to it (file 3), hide its `Column1`. It moves to the top of the Data pane.

## Relationships

**Model view → Manage relationships → New**:

| From (one side) | To (many side) | Cardinality | Cross-filter direction | Active |
|---|---|---|---|---|
| `customers[customer_id]` | `invoices[customer_id]` | One to many | Single (customers filters invoices) | Yes |
| `Date[Date]` | `invoices[invoice_date]` | One to many | Single (Date filters invoices) | Yes |

Single direction matters for the cohort page: a filter on `invoices[month_offset]` must not shrink the `customers` count, because that count is the size of the starting-month group.

## Column settings

| Column | Setting |
|---|---|
| `customers[segment]` | **Sort by column:** `segment_order` (Champions, Loyal, New, At risk, Lost) |
| `customers[segment_order]` | Hide |
| `customers[cohort_month]` | Format `mmm yyyy` |
| `customers[first_purchase]`, `customers[last_purchase]` | Format `d mmm yyyy` |
| `customers[spend]`, `invoices[amount]` | Format `£#,0.00`; **Summarization:** Don't summarize |
| `customers[customer_id]`, `customers[recency_days]`, `customers[orders]`, the three `_score` columns | **Summarization:** Don't summarize |
| `customers[country]` | **Data category:** Country/Region |
| `Date[Month]` | **Sort by column:** `Month Start` |
| `Date[Month Start]` | Format `mmm yyyy` |
| `invoices[customer_id]`, `invoices[invoice_date]` | Hide (use `customers` and `Date` instead) |
| `invoices[month_offset]` | **Summarization:** Don't summarize |

## Display folders

In the measures table, set each measure's **Display folder** (Properties pane) to the folder named in `03-measures.dax`: `Customers`, `Revenue` or `Cohorts`.
