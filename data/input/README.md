# Input file

What the client supplies, in this folder: one transactions export. Its name, its headers and the date format are set in `config/client.yaml`. The notebook's first step (`read_transactions()` in `config.py`) checks the file before anything is computed and stops with one line naming the problem.

## Transactions (`inputs.transactions`)

- One file, `.csv` or `.xlsx`. In an `.xlsx`, every sheet is read and stacked, and every sheet must have the columns.
- One row per invoice line: a product on an invoice, with its quantity and unit price.
- Returns and cancelled orders are rows too, with a negative quantity and an invoice number that starts with `rules.return_invoice_prefix`.
- Every column below must be there, under the header set in `columns`. Extra columns are used only to tell an exact duplicate (the whole line sent twice) from two different lines.

| Standard column (`columns.*`) | Type | Example (demo header) | Used for |
|---|---|---|---|
| `invoice` | text | `489434`, a return `C489449` (Invoice) | Orders counted once; returns told apart by the prefix |
| `product_code` | text | `85048` (StockCode) | Lines whose code does not match `rules.product_code_pattern` (postage, fees) are removed |
| `quantity` | number, negative on a return | `12` (Quantity) | Amount = quantity × price |
| `invoice_date` | an Excel date, ISO text, or text in `inputs.date_format` | `2009-12-01 07:45` (InvoiceDate) | Recency, starting month |
| `price` | number, the unit price | `6.95` (Price) | Lines with a zero or unreadable price are removed |
| `customer_id` | text, leading zeros kept | `13085` (Customer ID) | The customer; lines without one are removed |
| `country` | text | `United Kingdom` (Country) | The country slicer in Power BI |

One example row, as the demo file sends it:

| Invoice | StockCode | Description | Quantity | InvoiceDate | Price | Customer ID | Country |
|---|---|---|---|---|---|---|---|
| 489434 | 85048 | 15CM CHRISTMAS GLASS BALL 20 LIGHTS | 12 | 2009-12-01 07:45:00 | 6.95 | 13085 | United Kingdom |

**Limits:** a text date is read only in the `inputs.date_format` format (or ISO), never guessed: `05/10/2026` can be May or October. Numbers use a dot for decimals and no currency sign. A quantity or price that cannot be read is removed with the zero-price lines and counted in the data health check.

## What stops the run

One line each, before anything is computed:

```
config/client.yaml is missing rules.score_levels
config/client.yaml is not valid YAML near line 12 (quote a value with # or :)
missing data/input/<file> (inputs.transactions in config/client.yaml)
data/input/<file>, sheet <sheet>: missing column(s): <headers> (columns in config/client.yaml)
data/input/<file>: <n> invoice date(s) not readable, e.g. '<value>' (inputs.date_format in config/client.yaml)
```

A wrong value inside a row does not stop the run: the row is removed by one of the cleaning rules and counted in the data health check.

## The demo file

The demo's file (about 45 MB) is not committed. Download it with `python data/demo/download.py`. Everything in this folder except this README is ignored by git, so client data is never committed.
