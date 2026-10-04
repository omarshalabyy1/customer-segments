# Power BI build

This folder lets you build the report in Power BI Desktop from nothing, by copying and pasting, and get the same numbers as the notebook.

## What the report answers

1. Which customers bring the revenue? (champions: a third of the customers, most of the revenue)
2. Which good customers are slipping away, and who should be called first?
3. How many of each month's new customers come back?

## Pages

| Page | What it shows |
|---|---|
| Overview | Totals, each group's share of customers against its share of revenue, revenue by month by group |
| Champions | The group's numbers and its customers, biggest spend first |
| Loyal | Same layout |
| New | Same layout |
| At risk | Same layout: this is the "who to call first" list |
| Lost | Same layout |
| Return by starting month | The cohort table: the share of each month's new customers who bought again in each later month |

## Order to follow

Run the notebook first (or use the `data/*.csv` files already in the repo), then:

1. [`01-power-query.md`](01-power-query.md): load the two tables
2. [`02-model.md`](02-model.md): the Date table, the measures table, relationships and column settings
3. [`03-measures.dax`](03-measures.dax): every measure, with its format string and display folder
4. [`05-theme.json`](05-theme.json): **View → Themes → Browse for themes** (do this before placing visuals so they pick up the colours)
5. [`04-pages.md`](04-pages.md): every page and visual
6. [`06-checks.md`](06-checks.md): the numbers each page must show

Save the report as `powerbi/customer-segments.pbix`, export one screenshot per page into `powerbi/screenshots/` (names listed in `04-pages.md`), and commit both.
