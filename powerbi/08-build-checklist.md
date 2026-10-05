# 8. Build checklist

Follow it top to bottom. At each **Check** step, compare with `06-checks.md`; stop and fix before going on if a number differs (the end of `06-checks.md` lists the usual causes).

## Set up

1. Make sure `data/customers.csv` and `data/invoices.csv` exist (they are in the repo; rerun `analysis/analysis.ipynb` only if you changed it).
2. Open Power BI Desktop → **Blank report**.
3. File → Options and settings → Options → **Current File → Data Load** → untick **Auto date/time** → OK.
4. **View → Themes → Browse for themes** → pick `powerbi/05-theme.json`.
5. **Format page → Canvas settings**: 16:9, 1280 × 720.
6. **File → Save as** `powerbi/customer-segments.pbix`. Save again after every section.

## Load the data (`01-power-query.md`)

7. **Home → Get data → Blank query**, rename it `customers`, **Advanced Editor**, paste the `customers` code, **Done**.
8. Same for `invoices`.
9. **Close & Apply**. In the Data pane: `customers` and `invoices`, both loaded.

## Build the model (`02-model.md`)

10. **Modeling → New table**, paste the `Date` code. **Table tools → Mark as date table** → `Date`.
11. **Home → Enter data**, name it `_Measures`, **Load**.
12. **Model view → Manage relationships**: delete any relationship Power BI created on its own, then add the two in the table, single direction.
13. Apply every row of "Column settings": sort-by columns, hidden columns, formats, summarization, data category.

## Add the measures (`03-measures.dax`)

14. Select `_Measures`. For each of the 14 measures: **New measure**, paste, set the format string from its comment and the display folder from its section. In a format string, replace `<client.currency>` with `client.currency` from `config/client.yaml`.
15. Hide `_Measures[Column1]`.

## Page 1: Overview (`04-pages.md`)

16. Rename the page **Overview**.
17. Add visuals 1 to 8 (title, country slicer, six cards).
18. **Check C1 to C6.**
19. Add visual 9 (bar chart) and visual 11 (table).
20. **Check C7 and C8.**
21. Add visual 10 (column chart).
22. **Check C9** (hover the last three columns).

## Pages 2 to 6: one page per group

23. New page, rename it **Champions**. Add visuals 1 to 9. Copy the country slicer from Overview and paste it here; choose **Sync**.
24. Add the page filter `customers[segment]` = Champions.
25. **Check C10 and C11** for Champions.
26. Duplicate the page four times. For each copy: rename it (Loyal, New, At risk, Lost), change the page filter, the two text boxes and the data-bar colour.
27. **Check C10 and C11** for each of the four pages.

## Page 7: Return by starting month

28. New page, rename it **Return by starting month**. Add visuals 1 to 6; paste the synced slicer.
29. **Check C12 to C15.**

## Interactions and slicer (`07-interactions.md`)

30. Set the interactions on each page as in the tables.
31. **View → Sync slicers**: the country slicer synced and visible on all seven pages.
32. Set the slicer to United Kingdom on Overview. **Check C16**, then clear the slicer.

## Finish

33. Page order: Overview, Champions, Loyal, New, At risk, Lost, Return by starting month. Open the Overview page.
34. Save `powerbi/customer-segments.pbix`.
35. Screenshot each page into `powerbi/screenshots/` with the names at the end of `04-pages.md`.
36. Commit the `.pbix` and the seven screenshots.
