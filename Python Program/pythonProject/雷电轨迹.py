import matplotlib.pyplot as plt
import random


def generate_lightning(start_point, end_point, max_distance):
    points = [start_point, end_point]
    while True:
        all_within_max_distance = True
        new_points = []
        for i in range(len(points) - 1):
            p1 = points[i]
            p2 = points[i + 1]
            distance = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
            if distance > max_distance:
                all_within_max_distance = False
                midpoint = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
                offset_x = random.uniform(-distance / 4, distance / 4)
                offset_y = random.uniform(-distance / 4, distance / 4)
                new_midpoint = (midpoint[0] + offset_x, midpoint[1] + offset_y)
                new_points.extend([p1, new_midpoint])
            else:
                new_points.append(p1)
        new_points.append(points[-1])
        points = new_points

        if all_within_max_distance:
            break

    return points


def add_forks(lightning_points, max_distance):
    all_points = lightning_points.copy()
    # 在原闪电上选一个点
    point_on_main = random.choice(lightning_points)
    # 在所选点的左上或左下空白处选一个点
    x_offset = random.uniform(-30, -5)
    y_offset = random.uniform(-30, 30)
    blank_point = (point_on_main[0] + x_offset, point_on_main[1] + y_offset)
    fork_points = generate_lightning(point_on_main, blank_point, max_distance)
    all_points.extend(fork_points[1:])
    return all_points


# 设置起始点和终点坐标以及最大距离
start_point = (0, 0)
end_point = (100, 100)
max_distance = 1

# 生成主体闪电轨迹的点列表
lightning_points = generate_lightning(start_point, end_point, max_distance)
lightning_points_with_forks = lightning_points
# 设置添加分叉的参数
num_forks = 3  # 要添加的分叉数量
x_range = (0, 100)  # x坐标范围，用于确保所选空白点在合理范围内
y_range = (0, 100)  # y坐标范围，用于确保所选空白点在合理范围内

# 添加分叉
for i in range(0, num_forks):
    lightning_points_with_forks = add_forks(lightning_points_with_forks, max_distance)

# 绘制闪电（包括分叉）
x_coords, y_coords = zip(*lightning_points_with_forks)
plt.plot(x_coords, y_coords, 'b-')

# 设置图形的坐标轴范围等
plt.xlim(min(x_coords) - 1, max(x_coords) + 1)
plt.ylim(min(y_coords) - 1, max(y_coords) + 1)

# 显示图形
plt.show()