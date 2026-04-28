import re
import json
import os

def money_to_float(s):
    return float(s.replace(" ", "").replace("\xa0", "").replace(",", "."))

def parse_receipt(text):
    dt = None
    m_dt = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})", text)
    if m_dt:
        dt = {"date": m_dt.group(1), "time": m_dt.group(2)}

    payment_method = None
    paid_amount = None
    m_pay = re.search(r"(Банковская карта|Наличные)\s*:\s*([\d \xa0]+,\d{2})", text, flags=re.IGNORECASE)
    if m_pay:
        payment_method = m_pay.group(1)
        paid_amount = money_to_float(m_pay.group(2))

    total = None
    m_total = re.search(r"ИТОГО\s*:\s*([\d \xa0]+,\d{2})", text, flags=re.IGNORECASE)
    if m_total:
        total = money_to_float(m_total.group(1))

    item_pattern = re.compile(
        r"(?ms)^\s*(\d+)\.\s*\n"
        r"(.*?)\n"
        r"(\d+,\d{3})\s*x\s*([\d \xa0]+,\d{2})\s*\n"
        r"([\d \xa0]+,\d{2})\s*\n"
        r"Стоимость\s*\n"
    )

    items = []
    for m in item_pattern.finditer(text):
        idx = int(m.group(1))
        raw_name = m.group(2).strip()
        name = re.sub(r"\s*\n\s*", " ", raw_name).strip()
        qty = float(m.group(3).replace(",", "."))
        unit_price = money_to_float(m.group(4))
        line_total = money_to_float(m.group(5))

        items.append({
            "no": idx,
            "name": name,
            "qty": qty,
            "unit_price": unit_price,
            "line_total": line_total
        })

    sum_items = round(sum(i["line_total"] for i in items), 2) if items else None

    return {
        "branch": (re.search(r"Филиал\s+(.+)", text).group(1).strip()
                   if re.search(r"Филиал\s+(.+)", text) else None),
        "bin": (re.search(r"\bБИН\s+(\d+)", text).group(1)
                if re.search(r"\bБИН\s+(\d+)", text) else None),
        "datetime": dt,
        "payment_method": payment_method,
        "paid_amount": paid_amount,
        "total": total,
        "items": items,
        "items_sum_check": sum_items
    }

def main():
    path = os.path.join(os.path.dirname(__file__), "raw.txt")

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    data = parse_receipt(text)
    print(json.dumps(data, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()