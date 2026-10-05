# 1. Power Query

Two queries, both loaded into the model. They read the two files the notebook writes to `data/`, so the cleaning lives in one place (the notebook) and Power Query only sets the types.

For each query: **Home → Get data → Blank query**, rename it, then **Advanced Editor**, paste the code and click **Done**. If your clone is not at `C:\Users\DELL\GitHub\customer-segments`, change the path in both queries.

## customers

One row per customer, with their scores and group. 5,832 rows.

```m
let
    Source = Csv.Document(
        File.Contents("C:\Users\DELL\GitHub\customer-segments\data\customers.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    #"Changed Type" = Table.TransformColumnTypes(
        #"Promoted Headers",
        {
            {"customer_id", type text},
            {"country", type text},
            {"first_purchase", type date},
            {"last_purchase", type date},
            {"cohort_month", type date},
            {"recency_days", Int64.Type},
            {"orders", Int64.Type},
            {"spend", Currency.Type},
            {"r_score", Int64.Type},
            {"f_score", Int64.Type},
            {"m_score", Int64.Type},
            {"segment", type text},
            {"segment_order", Int64.Type}
        },
        "en-US"
    )
in
    #"Changed Type"
```

| Step | What it does |
|---|---|
| Source | Reads the CSV as UTF-8 |
| Promoted Headers | The first row becomes the column names |
| Changed Type | Sets each column's type, reading dates and decimals the US way (`2026-01-31`, `1234.56`) whatever your Windows region is. Money is `Currency.Type` (fixed decimal) so sums are exact. `customer_id` stays text so leading zeros are kept |

## invoices

One row per invoice: purchases and returns. 43,807 rows. Returns have a negative amount and no `month_offset`.

```m
let
    Source = Csv.Document(
        File.Contents("C:\Users\DELL\GitHub\customer-segments\data\invoices.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    #"Blank Offset To Null" = Table.ReplaceValue(#"Promoted Headers", "", null, Replacer.ReplaceValue, {"month_offset"}),
    #"Changed Type" = Table.TransformColumnTypes(
        #"Blank Offset To Null",
        {
            {"invoice", type text},
            {"customer_id", type text},
            {"invoice_date", type date},
            {"invoice_type", type text},
            {"amount", Currency.Type},
            {"month_offset", Int64.Type}
        },
        "en-US"
    )
in
    #"Changed Type"
```

| Step | What it does |
|---|---|
| Source | Reads the CSV as UTF-8 |
| Promoted Headers | The first row becomes the column names |
| Blank Offset To Null | Returns have an empty `month_offset`; this makes it a real blank instead of an error |
| Changed Type | Sets each column's type. `invoice` stays text: return numbers start with `C` |

## Summary

| Query | Source file | Columns | Renames | Load |
|---|---|---|---|---|
| `customers` | `data/customers.csv` | 13 | None: the CSV headers are already the model names | Enabled |
| `invoices` | `data/invoices.csv` | 6 | None | Enabled |

There are no staging or disabled queries. Click **Close & Apply**.
