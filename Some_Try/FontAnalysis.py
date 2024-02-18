from typing import List

from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

import fontTools.ttLib as ttLib

import json


def get_all_chars_labels(font_name: str):

    # set
    font_set = ttLib.TTFont("./Fonts/临海隶书.ttf")

    # 获取所有的Unicode字符集
    unicode_chars = []
    for cmap in font_set['cmap'].tables:
        for key in cmap.cmap:
            # print(cmap.cmap[key])
            unicode_chars.append(cmap.cmap[key])

    # all_exist_chars: list[str] = font.getGlyphOrder()

    '''
    all_exist_chars: list[str] = []

    # print(all_exist_chars)

    # 打印所有可用字符
    for char in sorted(unicode_chars):
        # 转为字符
        char = chr(char)
        # 添加到列表
        all_exist_chars.append(char)
    '''

    # 返回
    return unicode_chars


# 加载字体
def get_commands_each_char(char_label, font_name) -> list[str]:  # text 文本 lg 语言
    font = TTFont("./Fonts/" + font_name + ".ttf")
    # 与 7.1.1 相同 -- 提取绘制命令语句
    glyphset = font.getGlyphSet()

    pen = SVGPathPen(glyphset)

    try:
        glyph = glyphset[char_label]
    except:
        return []

    glyph.draw(pen)

    # paths: str = pen.getCommands()

    paths: list[str] = pen._commands

    # print(paths)

    return paths


def simple_separate(path: list[str]) -> list[list[str]]:

    output: list[list[str]] = []

    # 先按空格分隔
    for each_step in path:
        each_step: str
        if each_step[0].isnumeric():
            # 如果是数字，说明是连续的坐标
            each_step: list[str] = each_step.split(' ')

        else:
            # 如果是字母，
            operation: str = each_step[0]
            each_step: list[str] = each_step[1:].split(' ')

            if each_step == [""]:
                each_step: list[str] = [operation]
            else:
                each_step.insert(0, operation)

        output.append(each_step)
        # print(each_step)
    return output


# 处理所有操作到向量
'''
[ [斜率向量, 下一个点相对当前点的坐标向量], ...]
'''
def process_commands_to_vector(path: list[list[str]]) -> list[list[list[float, float], list[float, float]]]:
    # 将绘制命令转换为向量
    current_point: list[float, float] = [0, 0]
    # 斜率向量
    slope_vector: list[float, float] = [0, 0]
    # 下一个点相对当前点的坐标向量
    next_point_vector: list[float, float] = [0, 0]

    # 斜率向量和下一个点相对当前点的坐标向量
    slope_and_next_point_vector: list[list[list[float, float], list[float, float]]] = []

    record_M = [0, 0]

    for i in range(len(path)):
        # 每一个命令语句
        each_signal_command: list[str] = path[i]

        # 命令
        operation: str = each_signal_command[0]

        # 坐标列表
        coordinates: list[str] = each_signal_command[1:]

        # print(each_signal_command)

        if operation == 'M':
            # 移动到
            # 有一个坐标差向量，但是没有斜率向量，所以斜率向量是 0
            # 斜率向量
            slope_vector = [0, 0]
            # 下一个点相对当前点的坐标向量
            next_point_vector = [float(coordinates[0]),
                                 float(coordinates[1])]

            next_point_vector = [next_point_vector[0] - current_point[0],
                              next_point_vector[1] - current_point[1]]

            # 记录 M 命令的位置
            record_M = next_point_vector

        elif operation == 'Q':
            # 二次贝塞尔曲线
            # 斜率向量
            slope_vector = [float(coordinates[0]), float(coordinates[1])]
            # 下一个点相对当前点的坐标向量
            next_point_vector = [float(coordinates[2])-current_point[0],
                                 float(coordinates[3])-current_point[1]]

        elif operation == 'C':
            raise Exception("三次贝塞尔曲线暂时不支持")

        elif operation == 'L':
            # 直线
            # 斜率向量，指向下一个点的向量
            slope_vector = [float(coordinates[0])-current_point[0],
                            float(coordinates[1])-current_point[1]]
            # 下一个点相对当前点的坐标向量
            next_point_vector = slope_vector

        elif operation == 'V':
            # 垂直线
            # 斜率向量，指向下一个点的向量
            slope_vector = [0, float(coordinates[0])-current_point[1]]
            # 下一个点相对当前点的坐标向量
            next_point_vector = slope_vector

        elif operation == 'H':
            # 水平线
            # 斜率向量，指向下一个点的向量
            slope_vector = [float(coordinates[0])-current_point[0], 0]
            # 下一个点相对当前点的坐标向量
            next_point_vector = slope_vector

        elif operation == 'Z':
            # 闭合路径
            # 找到 M 命令的位置
            next_point_vector = [record_M[0] - current_point[0],
                                 record_M[1] - current_point[1]]
            slope_vector = next_point_vector




        # 移动到下一个点
        current_point = next_point_vector

        combined = [slope_vector, next_point_vector]

        # 加入到列表
        slope_and_next_point_vector.append(combined)


    return slope_and_next_point_vector


def get_path_pairs():
    output  = []
    # text_svg("马", "PlangothicP1-Regular.allideo")
    font_path: str = "./Fonts/PlangothicP1-Regular.allideo.ttf"
    font_name: str = "PlangothicP1-Regular.allideo"
    # #
    # font_path: str = "./Fonts/临海隶书.ttf"
    # font_name: str = "临海隶书"

    all_chars = get_all_chars_labels("./Fonts/临海隶书.ttf")
    # 取 100 个CJK字符标签
    all_chars = [char for char in all_chars if char[:3] == 'uni'
                 and int(char[3:], 16) >= 0x4e00 and int(char[3:], 16) <= 0x9fa5][:100]
    # 保存所有字符的 SVG
    for char in all_chars:
        original_path: list[str] = get_commands_each_char(char, font_name)
        original_path_2: list[str] = get_commands_each_char(char, "临海隶书")

        organized_paths_data = simple_separate(original_path)
        organized_paths_data_2 = simple_separate(original_path_2)
        # print(organized_paths_data)

        # organized_paths_data: list[list[list[str, list[str]]]] = divide_paths_to_individual(original_path)

        # 进一步处理成神经网络可以理解的向量数据
        organized_paths_data = process_commands_to_vector(organized_paths_data)
        organized_paths_data_2 = process_commands_to_vector(organized_paths_data_2)

        if organized_paths_data and organized_paths_data_2:
            output.append([organized_paths_data, organized_paths_data_2])

    return output

if __name__ == '__main__':
    # text_svg("马", "PlangothicP1-Regular.allideo")
    font_path: str = "./Fonts/PlangothicP1-Regular.allideo.ttf"
    font_name: str = "PlangothicP1-Regular.allideo"
    # #
    # font_path: str = "./Fonts/临海隶书.ttf"
    # font_name: str = "临海隶书"

    all_chars = get_all_chars_labels("./Fonts/临海隶书.ttf")
    # 保存所有字符的 SVG
    for char in all_chars:
        original_path: list[str] = get_commands_each_char(char, font_name)

        organized_paths_data = simple_separate(original_path)
        # print(organized_paths_data)

        # organized_paths_data: list[list[list[str, list[str]]]] = divide_paths_to_individual(original_path)

        # 进一步处理成神经网络可以理解的向量数据
        organized_paths_data = process_commands_to_vector(organized_paths_data)

        print(organized_paths_data)

        # 过滤掉空字符（没有任何路径的未定义字符）
        # if organized_paths_data:
        #     # 保存到文件
        #     with open("./data/" + font_name + "/" + char + ".json", "w") as f:
        #         json.dump(organized_paths_data, f)
