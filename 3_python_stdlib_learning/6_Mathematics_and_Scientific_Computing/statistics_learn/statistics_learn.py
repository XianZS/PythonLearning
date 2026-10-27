"""
statistics 标准库学习
"""

import statistics as st

# 基础-1：集中趋势度量
# 中位数、众数、各种平均数、多众数
# 测试数据，学生成绩
scores = [87, 31, 32, 53, 65, 88, 75, 12, 78, 90, 90, 90, 78, 78]
# 算术平均数
number1 = st.mean(scores)
# 加权平均数：st.fmean()
# 几何平均数：st.geometric_mean()
# 调和平均数：st.harmonic_mean()
# 中位数
med = st.median(scores)
# 众数
mode_number = st.mode(scores)
als_mode_number = st.multimode(scores)
print(number1, med, mode_number, als_mode_number)
# 基础-2：离散程度度量
class_a = [82, 67, 54, 66]
class_b = [34, 99, 56, 89]
# 总体标准差
print(f"a班级总体标准差:{st.pstdev(class_a)}")
print(f"b班级总体标准差:{st.pstdev(class_b)}")
print(f"a班级样本标准差:{st.stdev(class_a):.1f}")
print(f"b班级的四分位数:{st.quantiles(class_b, n=4, method='inclusive')}")
# 连续型数据：exclusive
# 离散型数据：inclusive
# 基础-3：基础异常处理
# st.StatisticsError
datas = []
try:
    avg = st.mean(datas)
    print(f"[avg]:{avg}")
except st.StatisticsError as e:
    print(e)
# 进阶-1：双变量统计分析
# Python version >=3.10
# 协方差、相关系数、最小二乘法线性回归
study_hours = [5, 8, 10, 12, 6, 15]
exam_scores = [72, 78, 85, 90, 75, 96]
# 协方差计算
cov = st.covariance(study_hours, exam_scores)
print(f"学习时长和学习成绩之间的协方差:{cov}")
# 皮尔逊相关系数
corr = st.correlation(study_hours, exam_scores)
print(f"学习时长和学习成绩之间的皮尔逊相关系数:{corr}")
# 线性回归的拟合
k, b = st.linear_regression(study_hours, exam_scores)
print(f"回归方程：成绩={k:.2f}*x+{b:.2f}")
# 学习时间为15小时，预测成绩：
print(f"学习时间为15小时，预测成绩为：{k * 13.5 + b}")
# 进阶-2：正态分布的高级操作
# st.NormalDist()
# 创建正态分布：均值80，标准差是10
score_dist = st.NormalDist(mu=80, sigma=10)
print(f"分布均值:{score_dist._mu},分布标准差:{score_dist._sigma}")  # type:ignore
# 计算不及格率
fail_prob = score_dist.cdf(60)
print(f"不及格率:{fail_prob:.2f}")
# 计算优秀率
exce_prob = 1 - score_dist.cdf(90)
print(f"优秀率:{exce_prob}")
# 从数据来拟合正态分布
datas = [82, 78, 85, 90, 76, 88, 81, 79, 84, 86]
fit_dist = st.NormalDist.from_samples(datas)
print(fit_dist._mu)  # type:ignore
res = score_dist + fit_dist
print(res)
# 进阶-3：进阶异常值识别和稳健统计
scores = [1, 2, 89, 88, 70, 90, 99, 10000]  # 存在异常值
quartiles = st.quantiles(scores, method="inclusive")
q1, q2, q3 = quartiles[0], quartiles[1], quartiles[2]
iqr = q3 - q1
# 异常数值边界
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr
outlines = [s for s in scores if s < lower_bound or s > upper_bound]
print(f"[异常数值]:{outlines}")
# 稳健统计对比
print(f"含异常值的算术平均数:{st.mean(scores):.1f}")
print(f"含异常值的中位数:{st.median(scores):.1f}")


# 实战案例
# 学生成绩统计分析系统
class ScoreSystem:
    def __init__(self, stu_data):
        """
        [(学习时长,成绩),(学习时长,成绩),......]
        """
        self.stu_data = stu_data
        self.hours = [item[0] for item in stu_data]
        self.score = [item[1] for item in stu_data]

    def base_statistics(self):
        print(f"中位数:{st.median(self.score)}")
        print(f"平均数:{st.mean(self.score)}")

    def corr_regression(self):
        corr = st.correlation(self.hours, self.score)
        print(f"学习时长和学习成绩之间的皮尔逊相关系数:{corr}")
        if abs(corr) > 0.8:
            corr_level = "极强相关性"
        elif abs(corr) >= 0.5:
            corr_level = "中等相关性"
        elif abs(corr) >= 0.3:
            corr_level = "弱相关性"
        else:
            corr_level = "无相关性"
        print(f"[相关性水平]:{corr_level}")
        k, b = st.linear_regression(self.hours, self.score)
        print(f"[线性回归方程]:y={k}*x+{b}")


if __name__ == "__main__":
    stu_data = [(1, 46), (4, 76), (5, 89), (6, 89), (9, 92), (12, 99)]
    analyzer = ScoreSystem(stu_data)
    analyzer.base_statistics()
    analyzer.corr_regression()
