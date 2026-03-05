牛排 = 500
猪排 = 450
套餐 = 80

while True:
    点餐 = input("请问你要点什么餐？（A）牛排 (B) 猪排 (Q) 退出：").upper()

    if 点餐 == "Q":
        print("欢迎下次光临！")
        break

    升级 = input("你是否要升级套餐？（Y）是 (N) 否：").upper()

    if 点餐 == "A" and 升级 == "Y":
        print(f"你的餐点是牛排 + 套餐，价格是 {牛排 + 套餐} 元")
    elif 点餐 == "A" and 升级 == "N":
        print(f"你的餐点是牛排，价格是 {牛排} 元")
    elif 点餐 == "B" and 升级 == "Y":
        print(f"你的餐点是猪排 + 套餐，价格是 {猪排 + 套餐} 元")
    elif 点餐 == "B" and 升级 == "N":
        print(f"你的餐点是猪排，价格是 {猪排} 元")
    else:
        print("输入有误，请重新选择。")

    print("-" * 30)