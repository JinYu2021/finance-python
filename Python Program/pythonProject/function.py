
def 总金额 (售价,运费=50):
    global 折扣
    折扣 = 0.9
    return  int(售价*折扣+运费)
    print("忽略")
print(f"总金额为{总金额(售价 = 1000,运费=80)}元")
print(f"目前折扣为{int(折扣*10)}折")