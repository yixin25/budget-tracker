import datetime

# 每月資料格式：{ '2025-06': { 'budget': 15000, 'expenses': { date1: [...], date2: [...] } } }
monthly_data = {}

def get_month_key(date):
    return date.strftime("%Y-%m")

def set_budget_for_month(month):
    if month not in monthly_data:
        try:
            budget = float(input(f"請輸入 {month} 的預算（元）: "))
        except ValueError:
            print("❌ 金額格式錯誤")
            return
        monthly_data[month] = {
            "budget": budget,
            "expenses": {}
        }

def add_expense():
    # 日期輸入與解析
    date_str = input("請輸入支出日期（YYYY-MM-DD，預設今日）: ")
    if not date_str:
        date = datetime.date.today()
    else:
        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("❌ 日期格式錯誤")
            return

    month_key = get_month_key(date)
    set_budget_for_month(month_key)

    category = input("支出類別（例如: 食物、交通、娛樂）: ")
    try:
        amount = float(input("支出金額: "))
    except ValueError:
        print("❌ 金額格式錯誤")
        return

    # 加入支出
    month_data = monthly_data[month_key]
    month_data["expenses"].setdefault(date, []).append({
        "category": category,
        "amount": amount
    })
    print(f"✅ 已新增：{date} - {category} - ${amount:.0f}")

    # 預算檢查
    total_spent = sum(
        item["amount"] for day in month_data["expenses"].values() for item in day
    )
    budget = month_data["budget"]
    if total_spent > budget:
        print(f"⚠️ 你已超出 {month_key} 的預算 ${total_spent - budget:.0f} 元！")
    else:
        print(f"目前已花費 ${total_spent:.0f}，剩餘 ${budget - total_spent:.0f} 元預算。")

def show_monthly_summary():
    month = input("請輸入要查詢的月份（格式：YYYY-MM，預設本月）: ")
    if not month:
        month = datetime.date.today().strftime("%Y-%m")
    if month not in monthly_data:
        print(f"⚠️ {month} 尚未有任何支出紀錄")
        return

    month_data = monthly_data[month]
    print(f"\n📅 {month} 每日支出分類：")
    for date in sorted(month_data["expenses"].keys()):
        print(f"\n{date}：")
        category_total = {}
        for expense in month_data["expenses"][date]:
            category_total[expense["category"]] = category_total.get(expense["category"], 0) + expense["amount"]
        for cat, amt in category_total.items():
            print(f"  {cat}: ${amt:.0f}")

    total_spent = sum(
        item["amount"] for day in month_data["expenses"].values() for item in day
    )
    print(f"\n💰 預算：${month_data['budget']:.0f}")
    print(f"🧾 已花費：${total_spent:.0f}")
    print(f"💡 剩餘：${month_data['budget'] - total_spent:.0f}")

def main():
    while True:
        print("\n📘 功能選單：\n1. 新增支出\n2. 查詢某月支出統計\n3. 離開")
        choice = input("請選擇功能（1-3）: ")
        if choice == "1":
            add_expense()
        elif choice == "2":
            show_monthly_summary()
        elif choice == "3":
            print("👋 再見！記得節省開銷喔～")
            break
        else:
            print("❌ 請輸入有效選項（1-3）")

if __name__ == "__main__":
    main()

