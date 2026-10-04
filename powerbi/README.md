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

Follow [`08-build-checklist.md`](08-build-checklist.md): 36 numbered steps from a blank report to the last screenshot, pointing to the file for each part and to the check numbers to verify on the way.

| File | Contents |
|---|---|
| [`01-power-query.md`](01-power-query.md) | The two queries, paste-ready M code |
| [`02-model.md`](02-model.md) | Date table, measures table, relationships and column settings, each with its reason |
| [`03-measures.dax`](03-measures.dax) | The 14 measures with format strings, display folders and the page each one serves |
| [`04-pages.md`](04-pages.md) | 7 pages and 62 visuals: type, position, fields, sort, labels, formatting |
| [`05-theme.json`](05-theme.json) | The theme in the portfolio's colours; import with **View → Themes → Browse for themes** before placing visuals |
| [`06-checks.md`](06-checks.md) | Checks C1 to C16: the numbers each page must show, with the SQL behind them |
| [`07-interactions.md`](07-interactions.md) | Edit-interactions per page, filters, drill-through, bookmarks and tooltips |
| [`08-build-checklist.md`](08-build-checklist.md) | The build, step by step |

Save the report as `powerbi/customer-segments.pbix`, export one screenshot per page into `powerbi/screenshots/` (names listed in `04-pages.md`), and commit both.
