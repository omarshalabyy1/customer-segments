"""The one place client values come from: config/client.yaml, and the check of the client's input file."""

from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).parent
REQUIRED = [
    "client.name", "client.currency",
    "inputs.transactions", "inputs.date_format",
    "columns.invoice", "columns.product_code", "columns.quantity", "columns.invoice_date",
    "columns.price", "columns.customer_id", "columns.country",
    "rules.return_invoice_prefix", "rules.product_code_pattern", "rules.score_levels",
    "rules.still_buying_min_recency_score", "rules.good_customer_min_frequency_plus_spend",
    "report.title",
    "report.colours.data", "report.colours.text", "report.colours.muted",
    "report.colours.page", "report.colours.line", "report.colours.danger",
]
TEXT_COLUMNS = ["invoice", "product_code", "customer_id"]  # read as text: codes keep their leading zeros


def load_config():
    try:
        cfg = yaml.safe_load((ROOT / "config" / "client.yaml").read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        line = error.problem_mark.line + 1 if getattr(error, "problem_mark", None) else "?"
        raise SystemExit(f"config/client.yaml is not valid YAML near line {line} (quote a value with # or :)")
    for key in REQUIRED:
        node = cfg
        for part in key.split("."):
            if not isinstance(node, dict) or part not in node:
                raise SystemExit(f"config/client.yaml is missing {key}")
            node = node[part]
    cfg["input_dir"] = ROOT / "data" / "input"
    return cfg


def read_transactions(cfg):
    """The client's invoice lines with the standard column names, or a one-line stop."""
    path = cfg["input_dir"] / cfg["inputs"]["transactions"]
    if not path.exists():
        raise SystemExit(f"missing data/input/{path.name} (inputs.transactions in config/client.yaml)")
    headers = cfg["columns"]  # standard name -> the client's header
    as_text = {headers[c]: str for c in TEXT_COLUMNS}
    if path.suffix.lower() == ".csv":
        frames = {"": pd.read_csv(path, dtype=as_text)}
    else:
        frames = pd.read_excel(path, sheet_name=None, dtype=as_text)
    for sheet, frame in frames.items():
        missing = [h for h in headers.values() if h not in frame.columns]
        if missing:
            where = f"data/input/{path.name}" + (f", sheet {sheet}" if sheet else "")
            raise SystemExit(f"{where}: missing column(s): {', '.join(missing)} (columns in config/client.yaml)")

    # Extra columns stay, so an exact duplicate means the whole line as sent, not just the standard columns.
    lines = pd.concat(list(frames.values()), ignore_index=True)
    lines = lines.rename(columns={header: name for name, header in headers.items()})
    for c in TEXT_COLUMNS:
        lines[c] = lines[c].str.strip().replace("", pd.NA)
    lines["quantity"] = pd.to_numeric(lines["quantity"], errors="coerce")
    lines["price"] = pd.to_numeric(lines["price"], errors="coerce")
    dates = pd.to_datetime(lines["invoice_date"], format=cfg["inputs"]["date_format"], errors="coerce")
    unreadable = dates.isna() & lines["invoice_date"].notna()
    if unreadable.any():
        example = lines.loc[unreadable, "invoice_date"].iloc[0]
        raise SystemExit(f"data/input/{path.name}: {unreadable.sum()} invoice date(s) not readable, e.g. {example!r} (inputs.date_format in config/client.yaml)")
    lines["invoice_date"] = dates
    return lines
