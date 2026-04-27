"""
random 标准库学习
"""

import random
import threading

# 基础-1：基础随机数生成
# 生成随机数范围为【0，1）
print(f"[random.random]:{random.random()}")
# 自定义任意区间的随机浮点数
print(f"[random.uniform]:{random.uniform(1, 10)}")
# 生成随机整数，左闭右闭区间的随机整数
print(f"[random.randint]:{random.randint(1, 10)}")
# 左闭右开区间的随机整数
print(f"[random.randrange]:{random.randrange(0, 10, 2)}")
# 基础-2：序列的随机操作
# random.choice(iterable)：从非空可迭代对象之中随机返回一个元素
nums = ["aom", "som", "dom", "fom", "gom", "hom"]
print(f"[random.choice]:{random.choice(nums)}")
# （有放回操作）从可迭代对象之中有放回的抽取k个元素
print(f"[random.choices]:{random.choices(nums, weights=[1, 1, 1, 1, 1, 2], k=3)}")
# （无放回抽样）从可迭代对象之中无放回的抽取k个元素
print(f"[random.sample]:{random.sample(nums, k=3)}")
# 打乱可迭代对象
print(f"[before]:{nums}")
random.shuffle(nums)
print(f"[after]:{nums}")
# 基础-3：生成随机种子和结果复现
# 设置固定种子
random.seed(123456)
print(f"第一次randint:{random.randint(1, 100)}")
print(f"第一次random:{random.random()}")
print(f"第二次randint:{random.randint(1, 100)}")
print(f"第二次random:{random.random()}")
random.seed(123456)
print(f"第一次randint:{random.randint(1, 100)}")
print(f"第一次random:{random.random()}")
print(f"第二次randint:{random.randint(1, 100)}")
print(f"第二次random:{random.random()}")
# 进阶-1：常用概率分布随机数的生成
score = random.gauss(mu=80, sigma=10)
print(f"学生成绩:{score}")
# 指数分布 假设在一个商店之中，平均5分钟来1个顾客
interval = random.expovariate(lambd=1 / 5)
print(f"顾客到达时间间隔:{interval}")

# 进阶-2：高级随机状态管理
print("第一组随机数")
print(random.randint(1, 100))
# 保存状态
state_backup = random.getstate()
print(random.randint(1, 100))
print(random.randint(1, 100))
# 恢复状态
random.setstate(state_backup)
print(random.randint(1, 100))
print(random.randint(1, 100))
# 进阶-3：进阶功能和场景适配
# 随机字节的生成
res = random.randbytes(4)
print(f"[randbytes(4)]:{res}")


# 多线程的随机数安全
# 为每一个线程创建random.Random()实例
def thread_random_task(thread_name):
    thread_rng = random.Random(thread_name)
    print(f"{thread_name} 生成随机数: {thread_rng.randint(1, 100)}")


for i in range(3):
    t = threading.Thread(target=thread_random_task, args=(f"线程{i + 1}",))
    t.start()
# 不可变序列的打乱
# random.shuffle(iterable) list ： 不支持：元组、字符串
# random.sample(iterable)
data = (1, 2, 3, 4, 5, 6, 7, 8, 9)
new_data = tuple(random.sample(data, k=len(data)))
print(f"[打乱之后的元组]:{new_data}")


# 实战案例
# === 多功能年会抽奖系统 ===
# - 基础抽奖：从员工名单之中无放回的抽奖，1、2、3
# - 加权抽奖：设置不同部门的中奖权重
# - 公平和复现：支持设置随机种子
# - 颁奖顺序的打乱：随机打乱中将名单的颁奖顺序
class AnnualSystem:
    def __init__(self, staff_list, seed=None):
        self.staff_list = staff_list
        if seed is not None:
            random.seed(seed)
        else:
            seed = 123456
            random.seed(seed)
        self.won_staff = set()

    def base_lottery(self, prize_config):
        res = {}
        for prize_name, count in sorted(prize_config.items(), key=lambda x: x[1]):
            ava_staff = [
                staff
                for staff in self.staff_list
                if staff["name"] not in self.won_staff
            ]
            if len(ava_staff) < count:
                raise ValueError("参与人数不足")
            win_staff = random.sample(ava_staff, k=count)
            res[prize_name] = win_staff
            for staff in win_staff:
                self.won_staff.add(staff["name"])
        return res


if __name__ == "__main__":
    staff_data = [
        {"name": "jom1", "department": "jom"},
        {"name": "jom2", "department": "jom"},
        {"name": "jom3", "department": "jom"},
        {"name": "jom4", "department": "jom"},
        {"name": "jom5", "department": "jom"},
        {"name": "jom6", "department": "jom"},
        {"name": "jom7", "department": "jom"},
        {"name": "jom8", "department": "jom"},
        {"name": "jom9", "department": "jom"},
    ]
    my_sys = AnnualSystem(staff_list=staff_data, seed=20260427)
    config = {"一等奖": 1, "二等奖": 1, "三等奖": 1}
    base_res = my_sys.base_lottery(prize_config=config)
    print(base_res)
