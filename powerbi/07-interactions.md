# 7. Interactions

Select a source visual, then **Format → Edit interactions** and set the icon on each target: **Filter** (funnel), **Highlight** (chart icon) or **None** (circle with a line). Cards, text boxes and the matrix are never sources here. Visual numbers are the `#` column in `04-pages.md`.

## Page 1: Overview

| Source ↓ / Target → | 3–6 Cards (Customers, Revenue, Invoices, Came back) | 7–8 Cards (at risk) | 9 Bar chart | 10 Column chart | 11 Table |
|---|---|---|---|---|---|
| 2 Country slicer | Filter | Filter | Filter | Filter | Filter |
| 9 Bar chart (click a group) | Filter | None | (itself) | Filter | Filter |
| 10 Column chart (click a month or group) | None | None | None | (itself) | None |
| 11 Table (click a group row) | Filter | None | Highlight | Filter | (itself) |

Why: the at-risk cards always show the at-risk group, so a group click must not change them. A month click on the column chart is for reading the trend only; letting it filter would mix one month with all-time scores.

## Pages 2 to 6: one page per group

| Source ↓ / Target → | 4–8 Cards | 9 Table |
|---|---|---|
| 3 Country slicer | Filter | Filter |
| 9 Table (click a customer row) | None | (itself) |

Why: clicking a customer should not turn the group's cards into one customer's numbers.

## Page 7: Return by starting month

| Source ↓ / Target → | 3–4 Cards | 6 Matrix |
|---|---|---|
| 2 Country slicer | Filter | Filter |
| 6 Matrix (click a cell) | None | (itself) |

## Filters, drill-through, bookmarks, tooltips

| Item | Setting |
|---|---|
| Report-level filters | None |
| Page-level filters | Pages 2 to 6 only: `customers[segment]` is the page's group (`04-pages.md`) |
| Visual-level filters | Page 7 matrix only: `invoices[month_offset]` is not blank |
| Drill-through pages | None |
| Bookmarks and buttons | None; the page tabs are the navigation |
| Tooltip pages | None; default tooltips plus the extra fields listed in `04-pages.md` |
| Slicer sync | The country slicer is synced and visible on all seven pages |
