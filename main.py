"""API for the Data.go.th zoo attendance CSV."""

import csv
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException


class VisitorCsv:
    def __init__(self, filename: Path) -> None:
        self.filename = filename

    @staticmethod
    def _value(cell: str | None) -> Any:
        if cell is None or not cell.strip():
            return None
        cell = cell.strip()
        try:
            return int(cell.replace(",", ""))
        except ValueError:
            return cell

    def rows(self) -> list[dict[str, Any]]:
        if not self.filename.exists():
            raise HTTPException(status_code=500, detail="Visitor CSV was not found")

        try:
            with self.filename.open(encoding="utf-8-sig", newline="") as csv_file:
                reader = csv.DictReader(csv_file)
                records = []
                for raw in reader:
                    row = {
                        header.strip(): self._value(value)
                        for header, value in raw.items()
                        if header and header.strip()
                    }
                    if row and any(value is not None for value in row.values()):
                        records.append(row)
                return records
        except (OSError, UnicodeError, csv.Error) as error:
            raise HTTPException(status_code=500, detail=f"Failed to read CSV: {error}") from error


BASE_DIR = Path(__file__).resolve().parent
repository = VisitorCsv(BASE_DIR / "zoo_visitors_january_2569.csv")
app = FastAPI(title="Zoo Visitor Data Service", version="1.0.0")


@app.get("/api/zoo-visitors", tags=["Visitors"])
def get_visitors() -> dict[str, Any]:
    records = repository.rows()
    return {
        "source": "Data.go.th - Open Government Data of Thailand",
        "dataset": "ข้อมูลรายงานสถิติจำนวนผู้เข้าชมสวนสัตว์ ปีงบประมาณ 2569",
        "dataset_url": "https://data.go.th/dataset/zoo-visitors2569",
        "dataset_id": "970c2632-1669-44aa-80c5-2c20cb2295e4",
        "resource_id": "0ecc96cf-d914-42a1-b184-dbbd013c3c9c",
        "resource": "ข้อมูลรายงานสถิติจำนวนผู้เข้าชมสวนสัตว์ อสส มกราคม 2569",
        "fiscal_year": 2569,
        "records_count": len(records),
        "records": records,
    }


@app.get("/", include_in_schema=False)
def welcome() -> dict[str, str]:
    return {"service": "Zoo Visitor Data Service", "docs": "/docs"}
