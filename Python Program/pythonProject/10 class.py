import random

class 游戏角色:
    生命值 = 500
    攻击力 = 200
    def __init__(self,姓名):
        self.姓名 = 姓名
    def 防卫(self,指令):
        if 指令 == "隔挡":
           print(f"{self.姓名}摆出隔挡姿势")
           return 0.5
        elif 指令 == "闪避"
           print(f"{self.姓名}尝试闪避攻击")
           return random.choice([0.1])
class 魔物(游戏角色):
    def 攻击 (self,指令):
        if 指令 == "普通攻击":
          print(f"{self.姓名}使出了利爪攻击！！！")
          return 200
        elif 指令 == "特殊攻击":
           print(f"{self.姓名}张出血口使用暗器！！！")
           return random.choice([300.100])
