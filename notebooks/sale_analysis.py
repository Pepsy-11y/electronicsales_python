"""
Day 2 - Sales Analytics Without Pandas
Squad Python Specialization - Data Science, AI & Analytics

Tasks 1-7 use only the standard library. pandas is allowed in task 8, to check your work.
"""
import csv
import re
import os
from decimal import Decimal, InvalidOperation
from collections import Counter
from pathlib import Path

os.chdir(Path(r"C:\Users\ADMIN\Downloads\sales_project"))

DATA_PATH = Path("data") / "electronics_sales.csv"

# print("Current directory:",Path.cwd())
# print("File path:",DATA_PATH.resolve())
# print("Does file exist?",DATA_PATH.exists())
def read_sales(path: Path = DATA_PATH) -> list[dict[str, str]]:
    """Read the CSV with the csv module and return the raw rows."""
    with open(path, mode="r",newline="",encoding="utf-8-sig") as file:
        sale_file=csv.DictReader(file)
        rows=list(sale_file)
        columns=sale_file.fieldnames

    print(f"Rows: {len(rows)}")
    print(f"Number of columns: {columns}")

    return rows


def parse_number(value: str) -> float | None:
    """Convert a messy numeric string to a float, or return None if it cannot be trusted."""
    if value is None:
        return None

    value=str(value).strip()

    if not value:
        return None

    value=re.sub(
        r"^(KES|KSHS?)\s*",
        "",
        value,
        flags=re.IGNORECASE
    )

    argument=r"^[+-]?(?:\d+|\d{1,3}(?:,\d{3})+)(?:\.\d+)?$"

    if not re.fullmatch(argument, value):
        return None

    try:
        return Decimal(value.replace(",",""))
    except InvalidOperation:
        return None


def convert_rows(rows: list[dict[str, str]]) -> tuple[list[dict], list[dict]]:
    """Return (clean_rows, skipped_rows). Clean rows have numeric quantity, unit price and revenue."""
    clean_rows=[]
    skipped_rows=[]
    for row_number, row in enumerate(rows,start=1):
        quantity=parse_number(row.get("quantity"))
        unit_price=parse_number(row.get("unit_price_kes"))

        responses=[]

        if quantity is None:
            responses.append("Missing or invalid quantity value")

        if unit_price is None:
            responses.append("Missing or invalid unit_price value")

        if quantity is not None and quantity <=0:
            responses.append("Value must be a non_negative and more than zero")

        if unit_price is not None and unit_price < 0:
            responses.append("Value must be a non_negative number")

        if responses:
            skipped_rows.append({
                "row_number":row_number,
                "row":row,
                "response":";".join(responses)
            })
            continue

        cleaned_row=row.copy()

        cleaned_row["quantity"]=quantity
        cleaned_row["unit_price_kes"]=unit_price

        clean_rows.append(cleaned_row)

    print(f"Clean rows: {len(clean_rows)}")
    print(f"Skipped rows: {len(skipped_rows)}")

    return clean_rows, skipped_rows


def total_revenue(rows: list[dict]) -> float:
    total=sum(
        (row["quantity"] * row["unit_price_kes"] for row in rows),
        Decimal("0")
    )
    return total


def revenue_by(rows: list[dict], field: str) -> dict[str, float]:
    """Total revenue grouped by any column (product, store, payment_method...)."""
    totals={}
    for row in rows:
        category=row[field]
        revenue = row["quantity"] * row["unit_price_kes"]
        if category not in totals:
            totals[category] = Decimal("0")

        totals[category]+=revenue

    return totals


def top_n(totals: dict[str, float], n: int = 3) -> list[tuple[str, float]]:
    """Return the n highest (key, value) pairs, highest first."""
    rank=sorted(
        totals.items(),
        key=lambda item:(-item[1],str(item[0]).casefold())
    )

    return rank[:n]


def high_value(rows: list[dict], threshold: float) -> list[dict]:
    """Transactions whose revenue is at or above threshold (use a comprehension)."""
    return [
        row for row in rows
        if row["quantity"] * row["unit_price_kes"]>threshold
    ]


# Reusable statistics - implement these yourself, no statistics module.
def mean(values: list[float]) -> float:
    if not values:
        raise ValueError("No calculation of mean for an empty list")
    return sum(values)/len(values)


def median(values: list[float]) -> float:
    if not values:
        raise ValueError("No calculation of median for an empty list")
    ordered_values=sorted(values)
    middle=len(ordered_values)//2

    if len(ordered_values)%2==1:
        return ordered_values[middle]
    
    return (ordered_values[middle-1] + ordered_values[middle])/2
    


def minimum_maximum(values: list[float]) -> tuple[float, float]:
    if not values:
        raise ValueError("No calculation of minimum and maximum for an empty list")
    least=values[0]
    highest=values[0]

    for value in values[1:]:
        if value < least:
            least=value

        if value > highest:
            highest=value

    return least, highest

def verify_with_pandas(path: Path, my_results: dict) -> None:
    """Recompute the headline numbers with pandas and print whether each one matches."""
    import pandas as pd
    df=pd.read_csv(path, encoding="utf-8-sig", dtype=str)
    df["quantity"]=df["quantity"].apply(parse_number)
    df["unit_price_kes"]=df["unit_price_kes"].apply(parse_number)

    valid_mask=(
        df["quantity"].notna()
        & df["unit_price_kes"].notna()
        & (df["quantity"]>0)
        & (df["unit_price_kes"]>=0)
    )

    clean_df=df.loc[valid_mask].copy()

    clean_df["revenue"]=(clean_df["quantity"] * clean_df["unit_price_kes"])

    pandas_results = {
        "total_revenue":pd.to_numeric(clean_df["revenue"], errors="coerce").fillna(0).sum(),
        "transaction_count":len(clean_df),
        "mean":mean(clean_df["revenue"].tolist()),
        "median":median(clean_df["revenue"].tolist()),
        "minimum":minimum_maximum(clean_df["revenue"].tolist())[0],
        "maximum":minimum_maximum(clean_df["revenue"].tolist())[1]
    }

    print("\n===Pandas Verification===")
    for key,my_value in my_results.items():
        pandas_value=pandas_results[key]
        if my_value==pandas_value:
            print(f"{key}: MATCH")
        else:
            print(f"{key}: MISMATCH")
            print(f"Result:{my_value}")
            print(f"Pandas result:{pandas_value}")

    return pandas_results

def save_report(results):
    output_dir=Path(__file__).resolve().parent.parent/"output"
    output_dir.mkdir(parents=True,exist_ok=True)
    report_path=output_dir/"sales_report.txt"
    with open(report_path,"w",encoding="utf-8") as file:
        file.write("Report on Sales Analysis\n")
        file.write("="*40+"\n\n")

        for section, values in results.items():
            file.write(f"\n{section.upper()}\n")
            file.write("="*30+"\n")

            if isinstance(values,dict):
                for key,value in values.items():
                    file.write(f"{key}:{value}\n")

            elif isinstance(values,list):
                for item in values:
                    file.write(f"{item}\n")

            else:
                file.write(f"{values}\n")

    print(f"\nSaved report to: {report_path}")


def main():    
    path="data/electronics_sales.csv"
    rows=read_sales(path)
    clean1_rows,skipped_rows=convert_rows(rows)
    print("\n===Skipped rows===")
    for item in skipped_rows:
        print(item)

    total=total_revenue(clean1_rows)

    print("\n===Total Revenue===")
    print(f"KES {total:,.2f}")

    product_totals=revenue_by(clean1_rows,"product")
    store_totals=revenue_by(clean1_rows,"store")
    payment_totals=revenue_by(clean1_rows,"payment_method")

    print("\n===Revenue by Product===")
    for product,revenue in sorted(
        product_totals.items(),
        key=lambda item: (-item[1],str(item[0]).casefold())
    ):
        print(f"{product}: KES {revenue:,.2f}")

    print("\n===Revenue by Store===")
    for store,revenue in store_totals.items():
        print(f"{store}: KES {revenue:,.2f}")

    print("\n===Revenue by Payment method===")
    for method,revenue in payment_totals.items():
        print(f"{method}: KES {revenue:,.2f}")

    print("\n===Top three products===")
    for product,revenue in top_n(product_totals,3):
        print(f"{product}: KES {revenue:,.2f}")

    threshold=Decimal("50000")
    qualifying_sales=high_value(clean1_rows,threshold)

    print("\n===high_value transactions===")
    for row in qualifying_sales:
        revenue=row["quantity"] * row["unit_price_kes"]
        print(f"{row['product']}: KES {revenue:,.2f}")

    print(f"Number of qualifying sales: {len(qualifying_sales)}")

    stores={row["store"] for row in clean1_rows}
    store_counts={
        store: sum(
            1 for row in qualifying_sales
            if row["store"]==store
        )
        for store in stores
    }

    print("\n===High_value sales by store===")
    for store, count in store_counts.items():
        print(f"{store}: {count}")

    revenues=[
        row["quantity"] * row["unit_price_kes"]
        for row in clean1_rows
    ]

    print("\n===Transaction Revenue Statistics===")
    print(f"Mean: KES {mean(revenues):,.2f}")
    print(f"Median: KES {median(revenues):,.2f}")

    least, highest=minimum_maximum(revenues)

    print(f"Minimum: KES {least:,.2f}")
    print(f"Maximum: KES {highest:,.2f}")

    my_results={
        "total_revenue":total,
        "transaction_count":len(clean1_rows),
        "mean":mean(revenues),
        "median":median(revenues),
        "minimum":least,
        "maximum":highest
    }

    pandas_results=verify_with_pandas(path, my_results)

    report_results={
        "Summary":{
            "Total Revenue":f"KES {total:,.2f}",
            "Clean Transactions":len(clean1_rows),
            "Skipped Transactions":len(skipped_rows)
        },
        "Revenue by Product":product_totals,
        "Revenue by Store":store_totals,
        "Revenue by Payment Method":payment_totals,
        "Top Three Products":top_n(product_totals,3),
        "High Value Transactions":len(qualifying_sales),
        "Statistics on Transaction":{
            "Mean":mean(revenues),
            "Median":median(revenues),
            "Minimum":least,
            "Maximum":highest
        },

        "Verification of Pandas":{
            key:"MATCH" if my_results[key]==pandas_results[key]
            else "MISMATCH"
            for key in my_results
        }
    }

    save_report(report_results)


if __name__ == "__main__":
    main()


