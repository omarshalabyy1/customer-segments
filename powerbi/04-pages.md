# 4. Pages and visuals

Canvas: 16:9, 1280 × 720 (**Format page → Canvas settings**). Positions are x, y, width, height in pixels (**Format → General → Properties**). Build the visuals in the order listed. Every visual's title is on, with the text given here. Number formats come from the measures (file 3) unless a row says otherwise. Tooltips: the default ones (the fields on the visual) unless a row lists extra tooltip fields.

7 pages, 62 visuals: Overview 11, each group page 9 (× 5), Return by starting month 6.

## The country slicer (on every page)

Build it once on the Overview page, then copy it to the other pages and choose **Sync** when Power BI asks.

| Setting | Value |
|---|---|
| Visual | Slicer, style **Dropdown** |
| Field | `customers[country]` |
| Selection | Single select **off** (several countries with Ctrl), "Select all" **on** |
| Position | 1000, 16, 256, 56 |
| Title | Country |
| Sync slicers (**View → Sync slicers**) | Synced and visible on all seven pages |

## Page 1: Overview

| # | Visual | Position | Fields | Settings |
|---|---|---|---|---|
| 1 | Text box | 24, 16, 940, 56 | "Who brings the revenue, and who is slipping away" | 20 pt, Segoe UI Semibold, `#0E1630` |
| 2 | Slicer | 1000, 16, 256, 56 | `customers[country]` | As above |
| 3 | Card | 24, 88, 192, 96 | `[Customers]` | Title "Customers". Display units None |
| 4 | Card | 232, 88, 192, 96 | `[Revenue]` | Title "Revenue, net of returns". Display units None |
| 5 | Card | 440, 88, 192, 96 | `[Purchase Invoices]` | Title "Purchase invoices". Display units None |
| 6 | Card | 648, 88, 192, 96 | `[Repeat Customers %]` | Title "Customers who came back" |
| 7 | Card | 856, 88, 192, 96 | `[At-Risk Customers]` | Title "Good customers at risk". Callout colour `#C2410C` |
| 8 | Card | 1064, 88, 192, 96 | `[At-Risk Revenue]` | Title "Revenue from at-risk customers". Display units None. Callout colour `#C2410C` |
| 9 | Clustered bar chart | 24, 200, 616, 300 | Y-axis `customers[segment]`; X-axis `[Customer Share %]`, `[Revenue Share %]`; Tooltips `[Customers]`, `[Revenue]` | Title "Share of customers against share of revenue". Sort by `segment`, ascending. Legend on, top. X-axis off. Data labels on (0.0% from the measures). Colours: Customer Share % `#CBD5E1`, Revenue Share % `#0E1630` |
| 10 | Stacked column chart | 656, 200, 600, 300 | X-axis `Date[Month Start]` (type Categorical); Y-axis `[Revenue]`; Legend `customers[segment]`; Tooltips `[Revenue Share %]` | Title "Revenue by month, by group". Sort by `Month Start`, ascending. Y-axis display units Thousands. Data labels off. Legend top. Colours from the theme: Champions `#2563EB`, Loyal `#60A5FA`, New `#94A3B8`, At risk `#C2410C`, Lost `#64748B` (set them under **Columns → Colors** if the order differs) |
| 11 | Table | 24, 516, 1232, 188 | `customers[segment]`, `[Customers]`, `[Customer Share %]`, `[Revenue]`, `[Revenue Share %]`, `[Median Days Since Last Purchase]`, `[Median Orders]`, `[Median Spend]` | Title "The five groups". Sort by `segment`, ascending. Headers renamed (double-click the field in the Columns well): "Group", "Customers", "Share of customers", "Revenue", "Share of revenue", "Days since last order (median)", "Orders (median)", "Spend (median)". Conditional formatting: **data bars** on `[Revenue Share %]`, positive bar colour `#2563EB`. Totals on |

## Pages 2 to 6: one page per group

Build the Champions page, then right-click its tab → **Duplicate page** four times and change only the page name, the page filter, the two text boxes and the data-bar colour.

| # | Visual | Position | Fields | Settings |
|---|---|---|---|---|
| 1 | Text box | 24, 16, 940, 40 | Group name and who they are (table below) | 20 pt, Segoe UI Semibold, `#0E1630` |
| 2 | Text box | 24, 56, 940, 32 | "What to do: …" (table below) | 12 pt, colour `#4A5675` |
| 3 | Slicer | 1000, 16, 256, 56 | `customers[country]` | Synced copy of the Overview slicer |
| 4 | Card | 24, 104, 233, 96 | `[Customers]` | Title "Customers" |
| 5 | Card | 273, 104, 233, 96 | `[Customer Share %]` | Title "Share of customers" |
| 6 | Card | 522, 104, 233, 96 | `[Revenue Share %]` | Title "Share of revenue" |
| 7 | Card | 771, 104, 233, 96 | `[Median Days Since Last Purchase]` | Title "Days since last order (median)" |
| 8 | Card | 1020, 104, 236, 96 | `[Median Orders]` | Title "Orders (median)" |
| 9 | Table | 24, 216, 1232, 488 | `customers[customer_id]`, `customers[country]`, `customers[last_purchase]`, `customers[recency_days]`, `customers[orders]`, `customers[spend]`, `customers[r_score]`, `customers[f_score]`, `customers[m_score]` | Title "Who to call first: biggest spend at the top". Sort by `spend`, descending. Headers: "Customer", "Country", "Last order", "Days since", "Orders", "Spend", "R", "F", "M". `customer_id` format `0` (no thousands separator). Conditional formatting: **data bars** on `spend` (colour in the table below). Totals off |

**Page filter** (Filters pane → Filters on this page): `customers[segment]` is the page's group, basic filtering, one value ticked.

| Page name | Page filter | Text box 1 | Text box 2 | Data bars |
|---|---|---|---|---|
| Champions | Champions | Champions: still buying, top half on orders and spend | What to do: keep them close. Thank them, give early access, ask for referrals. | `#2563EB` |
| Loyal | Loyal | Loyal: still buying and coming back, with smaller or fewer orders | What to do: grow the basket. Bundles and reorder reminders. | `#60A5FA` |
| New | New | New: first and only order in the last three months | What to do: earn the second order. A follow-up within weeks of the first. | `#94A3B8` |
| At risk | At risk | At risk: good customers who stopped buying | What to do: call them first, biggest spend at the top, before they are lost. | `#C2410C` |
| Lost | Lost | Lost: not a top customer, and no order for more than three months | What to do: low priority. One win-back email, no calls. | `#64748B` |

## Page 7: Return by starting month

| # | Visual | Position | Fields | Settings |
|---|---|---|---|---|
| 1 | Text box | 24, 16, 940, 56 | "How many of each month's new customers come back" | 20 pt, Segoe UI Semibold, `#0E1630` |
| 2 | Slicer | 1000, 16, 256, 56 | `customers[country]` | Synced copy of the Overview slicer |
| 3 | Card | 24, 88, 400, 96 | `[New Customers Back Next Month %]` | Title "New customers who bought again the next month" |
| 4 | Card | 440, 88, 400, 96 | `[Repeat Customers %]` | Title "Customers who came back at least once" |
| 5 | Text box | 856, 88, 400, 96 | "December 2009 also holds older customers (the data starts there). December 2011 has no next month yet." | 10 pt, colour `#4A5675` |
| 6 | Matrix | 24, 200, 1232, 504 | Rows `customers[cohort_month]`; Columns `invoices[month_offset]`; Values `[Return Rate %]` | Title "Share of each starting month's customers who bought again, by months after the first purchase". **Filters on this visual:** `invoices[month_offset]` is not blank. Rows sorted by `cohort_month` ascending, columns by `month_offset` ascending. Row and column subtotals off. Values 9 pt (0.0% from the measure). Conditional formatting: **background colour**, Format style Gradient, Minimum = Number 0 colour `#FFFFFF`, Maximum = Number 0.5 colour `#2563EB` (month 0 is always 100% and would wash out the scale otherwise) |

## Not used

No bookmarks, buttons, drill-through pages, tooltip pages or report-level filters: the page tabs are the navigation. Interactions between visuals are in `07-interactions.md`.

## Screenshots

On each finished page, take a screenshot of the canvas and save it in `powerbi/screenshots/` as:

`1-overview.png`, `2-champions.png`, `3-loyal.png`, `4-new.png`, `5-at-risk.png`, `6-lost.png`, `7-return-by-starting-month.png`
