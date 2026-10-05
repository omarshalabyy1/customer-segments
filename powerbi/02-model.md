# 2. The model

A small star: one fact table (`invoices`), two dimensions (`customers` and `Date`) and a table that only holds the measures.

**Before anything else:** File → Options and settings → Options → **Current File → Data Load** → untick **Auto date/time**. Why: the model has its own Date table; the hidden automatic ones only add size and confusion.

```
customers (1) ──► (*) invoices (*) ◄── (1) Date
```

## Tables

| Table | Grain (one row per) | Key | Rows | Comes from |
|---|---|---|---|---|
| `invoices` | invoice (purchase or return) | `invoice` | 43,807 in the demo | Power Query |
| `customers` | customer | `customer_id` | 5,832 in the demo | Power Query |
| `Date` | day, from the first to the last month in the data | `Date` | 761 in the demo | DAX calculated table (below) |
| `_Measures` | holds the measures only | none | 0 | Enter data |

## The Date table

**Modeling → New table**, paste:

```dax
Date =
VAR _first = MIN ( invoices[invoice_date] )
VAR _last = MAX ( invoices[invoice_date] )
RETURN
ADDCOLUMNS (
    CALENDAR ( DATE ( YEAR ( _first ), MONTH ( _first ), 1 ), EOMONTH ( _last, 0 ) ),
    "Year", YEAR ( [Date] ),
    "Month Start", DATE ( YEAR ( [Date] ), MONTH ( [Date] ), 1 ),
    "Month", FORMAT ( [Date], "mmm yyyy" )
)
```

Then select the table, **Table tools → Mark as date table**, and pick the `Date` column.

Why: one row per day across the whole data range lets the revenue-by-month chart show every month, and marking it lets time intelligence work if it is added later. It runs from the first day of the first month to the last day of the last month, so every month is complete.

No calculated columns. The scores, groups and month offsets are computed once in the notebook and loaded as plain columns.

## The measures table

**Home → Enter data**, name the table `_Measures`, leave the one column empty and click **Load**. After you add the first measure to it (file 3), hide its `Column1`. It moves to the top of the Data pane.

## Relationships

**Model view → Manage relationships → New**:

| From (one side) | To (many side) | Cardinality | Cross-filter direction | Active | Why |
|---|---|---|---|---|---|
| `customers[customer_id]` | `invoices[customer_id]` | One to many | Single (customers filters invoices) | Yes | A group or country choice filters that group's invoices, so revenue follows the group |
| `Date[Date]` | `invoices[invoice_date]` | One to many | Single (Date filters invoices) | Yes | Months on the revenue chart come from the Date table |

Single direction matters for the cohort page: a filter on `invoices[month_offset]` must not shrink the `customers` count, because that count is the size of the starting-month group.

## Column settings

| Column | Setting | Why |
|---|---|---|
| `customers[segment]` | **Sort by column:** `segment_order` (Champions, Loyal, New, At risk, Lost) | Best group first, not alphabetical |
| `customers[segment_order]` | Hide | Only used for sorting |
| `customers[cohort_month]` | Format `mmm yyyy` | Matrix rows read like "Jan 2026" |
| `customers[first_purchase]`, `customers[last_purchase]` | Format `d mmm yyyy` | Readable dates in the call lists |
| `customers[spend]`, `invoices[amount]` | Format `"<client.currency> "#,0.00` (demo: `"GBP "#,0.00`); **Summarization:** Don't summarize | Totals come from measures, never from dragged columns |
| `customers[recency_days]`, `customers[orders]`, the three `_score` columns | **Summarization:** Don't summarize | Each row in a call list shows the customer's own value, not a sum |
| `customers[country]` | **Data category:** Country/Region | Power BI treats it as a place |
| `Date[Month]` | **Sort by column:** `Month Start` | Months sort by date, not alphabetically |
| `Date[Month Start]` | Format `mmm yyyy` | Axis labels on the revenue chart |
| `invoices[customer_id]`, `invoices[invoice_date]` | Hide | Use `customers` and `Date` instead, so every filter goes through a dimension |
| `invoices[month_offset]` | **Summarization:** Don't summarize | It is a column header in the matrix, not a number to add |

## Display folders

In the measures table, set each measure's **Display folder** (Properties pane) to the folder named in `03-measures.dax`: `Customers`, `Revenue` or `Cohorts`. Why: 14 measures are easier to find in three folders than in one list.
