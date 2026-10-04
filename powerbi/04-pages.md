# 4. Pages and visuals

Canvas: 16:9, 1280 × 720 (**Format page → Canvas settings**). Positions are x, y, width, height in pixels (**Format → General → Properties**). Every visual's title is on, with the text given here.

## The country slicer (on every page)

Build it once on the Overview page, then copy it to the other pages and choose **Sync** when Power BI asks.

| Setting | Value |
|---|---|
| Visual | Slicer, style **Dropdown**, multi-select with Ctrl |
| Field | `customers[country]` |
| Position | 1000, 16, 256, 56 |
| Title | Country |
| Sync slicers (**View → Sync slicers**) | Synced and visible on all seven pages |

## Page 1: Overview

| # | Visual | Position | Fields | Settings |
|---|---|---|---|---|
| 1 | Text box | 24, 16, 940, 56 | "Who brings the revenue, and who is slipping away" | 20 pt, Segoe UI Semibold |
| 2 | Card | 24, 88, 296, 96 | `[Customers]` | Title "Customers" |
| 3 | Card | 336, 88, 296, 96 | `[Revenue]` | Title "Revenue (purchases minus returns)" |
| 4 | Card | 648, 88, 296, 96 | `[Purchase Invoices]` | Title "Purchase invoices" |
| 5 | Card | 960, 88, 296, 96 | `[Repeat Customers %]` | Title "Customers who came back" |
| 6 | Clustered bar chart | 24, 200, 616, 300 | Y-axis `customers[segment]`; X-axis `[Customer Share %]`, `[Revenue Share %]` | Title "Share of customers against share of revenue". Sort by `segment`, ascending. Data labels on. Colours: Customer Share % `#CBD5E1`, Revenue Share % `#1E3A8A` |
| 7 | Stacked column chart | 656, 200, 600, 300 | X-axis `Date[Month Start]` (type Categorical); Y-axis `[Revenue]`; Legend `customers[segment]` | Title "Revenue by month, by group". Legend top. Colours from the theme: Champions `#1D4ED8`, Loyal `#60A5FA`, New `#94A3B8`, At risk `#F59E0B`, Lost `#64748B` (set them under **Columns → Colors** if the order differs) |
| 8 | Table | 24, 516, 1232, 188 | `customers[segment]`, `[Customers]`, `[Customer Share %]`, `[Revenue]`, `[Revenue Share %]`, `[Median Days Since Last Purchase]`, `[Median Orders]`, `[Median Spend]` | Sort by `segment`, ascending. Column headers renamed to plain words ("Group", "Days since last order (median)"…). Conditional formatting: **data bars** on `[Revenue Share %]`, bar colour `#1D4ED8`. Totals on |

Interactions: keep the default (each visual cross-filters the others). Clicking a group in the bar chart filters the table and the column chart to that group; the share measures keep the full total as the denominator.

## Pages 2 to 6: one page per group

Build the Champions page, then right-click its tab → **Duplicate page** four times and change only the page filter, the two text boxes and the data-bar colour.

| # | Visual | Position | Fields | Settings |
|---|---|---|---|---|
| 1 | Text box | 24, 16, 940, 40 | Group name and who they are (table below) | 20 pt, Segoe UI Semibold |
| 2 | Text box | 24, 56, 940, 32 | "What to do: …" (table below) | 12 pt, colour `#334155` |
| 3 | Card | 24, 104, 233, 96 | `[Customers]` | Title "Customers" |
| 4 | Card | 273, 104, 233, 96 | `[Customer Share %]` | Title "Share of customers" |
| 5 | Card | 522, 104, 233, 96 | `[Revenue Share %]` | Title "Share of revenue" |
| 6 | Card | 771, 104, 233, 96 | `[Median Days Since Last Purchase]` | Title "Days since last order (median)" |
| 7 | Card | 1020, 104, 236, 96 | `[Median Orders]` | Title "Orders (median)" |
| 8 | Table | 24, 216, 1232, 488 | `customers[customer_id]`, `customers[country]`, `customers[last_purchase]`, `customers[recency_days]`, `customers[orders]`, `customers[spend]`, `customers[r_score]`, `customers[f_score]`, `customers[m_score]` | Title "Who to call first: biggest spend at the top". Sort by `spend`, descending. Headers: "Customer", "Country", "Last order", "Days since", "Orders", "Spend", "R", "F", "M". Conditional formatting: **data bars** on `spend` (colour in the table below). Totals off |

**Page filter** (Filters pane → Filters on this page): `customers[segment]` is the page's group.

| Page | Page filter | Text box 1 | Text box 2 | Data bars |
|---|---|---|---|---|
| Champions | Champions | Champions: still buying, top half on orders and spend | What to do: keep them close. Thank them, give early access, ask for referrals. | `#1D4ED8` |
| Loyal | Loyal | Loyal: still buying and coming back, with smaller or fewer orders | What to do: grow the basket. Bundles and reorder reminders. | `#60A5FA` |
| New | New | New: first and only order in the last three months | What to do: earn the second order. A follow-up within weeks of the first. | `#94A3B8` |
| At risk | At risk | At risk: good customers who stopped buying | What to do: call them first, biggest spend at the top, before they are lost. | `#F59E0B` |
| Lost | Lost | Lost: not a top customer, and no order for more than three months | What to do: low priority. One win-back email, no calls. | `#64748B` |

## Page 7: Return by starting month

| # | Visual | Position | Fields | Settings |
|---|---|---|---|---|
| 1 | Text box | 24, 16, 940, 56 | "How many of each month's new customers come back" | 20 pt, Segoe UI Semibold |
| 2 | Card | 24, 88, 400, 96 | `[New Customers Back Next Month %]` | Title "New customers who bought again the next month" |
| 3 | Card | 440, 88, 400, 96 | `[Repeat Customers %]` | Title "Customers who came back at least once" |
| 4 | Text box | 856, 88, 400, 96 | "December 2009 also holds older customers (the data starts there). December 2011 has no next month yet." | 10 pt, colour `#64748B` |
| 5 | Matrix | 24, 200, 1232, 504 | Rows `customers[cohort_month]`; Columns `invoices[month_offset]`; Values `[Return Rate %]` | Title "Share of each starting month's customers who bought again, by months after the first purchase". **Filters on this visual:** `invoices[month_offset]` is not blank. Row and column subtotals off. Values 9 pt. Conditional formatting: **background colour**, Format style Gradient, Minimum = Number 0 colour `#FFFFFF`, Maximum = Number 0.5 colour `#1D4ED8` (month 0 is always 100% and would wash out the scale otherwise) |

## Not used

No bookmarks, drill-through pages or custom tooltips: the page tabs are the navigation, and the default tooltips show the measure values.

## Screenshots

**File → Export → Export to PDF** is not needed. On each finished page, take a screenshot of the canvas and save it as:

`screenshots/1-overview.png`, `2-champions.png`, `3-loyal.png`, `4-new.png`, `5-at-risk.png`, `6-lost.png`, `7-return-by-starting-month.png`
