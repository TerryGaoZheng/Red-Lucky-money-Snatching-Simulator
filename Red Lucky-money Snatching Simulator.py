import random
import json
from tkinter import Tk, Label, Entry, Button, messagebox, Text, Frame, Scrollbar, END
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 全局变量存储历史记录
history = []

def draw_red_packet(total_amount, num_people):
    """
    模拟微信抽红包
    :param total_amount: 红包总金额
    :param num_people: 抢红包的人数
    :return: 每个人抢到的金额列表
    """
    amounts = []
    remaining_amount = total_amount
    for i in range(num_people - 1):
        # 随机生成一个金额，范围在0.01到剩余金额的2倍之间
        amount = round(random.uniform(0.01, remaining_amount * 2 / (num_people - i)), 2)
        amounts.append(amount)
        remaining_amount -= amount
    amounts.append(round(remaining_amount, 2))  # 最后一个人拿到剩余金额
    random.shuffle(amounts)  # 打乱顺序，模拟随机抢红包
    return amounts

def plot_red_packet(amounts, frame):
    """
    可视化红包金额分布
    :param amounts: 每个人抢到的金额列表
    :param frame: 用于嵌入图表的Frame
    """
    for widget in frame.winfo_children():
        widget.destroy()  # 清空之前的图表

    fig = plt.Figure(figsize=(5, 3), dpi=100)
    ax = fig.add_subplot(111)
    ax.bar(range(1, len(amounts) + 1), amounts, color='red')
    ax.set_xlabel('抢红包的人')
    ax.set_ylabel('金额 (元)')
    ax.set_title('微信抽红包金额分布')
    ax.set_xticks(range(1, len(amounts) + 1))
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

def run_simulation():
    """
    运行红包模拟并显示结果
    """
    try:
        total_amount = float(entry_amount.get())
        num_people = int(entry_people.get())

        if total_amount <= 0 or num_people <= 0:
            messagebox.showerror("错误", "金额或人数必须大于0！")
            return

        amounts = draw_red_packet(total_amount, num_people)
        result_text.delete(1.0, END)  # 清空文本框
        result_text.insert(END, "每个人抢到的金额如下：\n")
        for i, amount in enumerate(amounts, start=1):
            result_text.insert(END, f"第{i}个人抢到了：{amount:.2f}元\n")

        # 添加到历史记录
        history.append({"总金额": total_amount, "人数": num_people, "金额分布": amounts})
        update_history()

        # 更新图表
        plot_red_packet(amounts, chart_frame)
    except ValueError:
        messagebox.showerror("错误", "请输入有效的数字！")

def update_history():
    """
    更新历史记录显示
    """
    history_text.delete(1.0, END)
    for idx, record in enumerate(history, start=1):
        history_text.insert(END, f"记录 {idx}:\n")
        history_text.insert(END, f"总金额: {record['总金额']}元, 人数: {record['人数']}\n")
        for i, amount in enumerate(record['金额分布'], start=1):
            history_text.insert(END, f"第{i}个人抢到了：{amount:.2f}元\n")
        history_text.insert(END, "-" * 30 + "\n")

def save_history():
    """
    保存历史记录到本地文件
    """
    try:
        with open("red_packet_history.json", "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("保存成功", "历史记录已保存到 red_packet_history.json")
    except Exception as e:
        messagebox.showerror("保存失败", f"保存时发生错误：{str(e)}")

# 创建主窗口
root = Tk()
root.title("微信抽红包模拟器")
root.geometry("800x600")

# 输入区域
input_frame = Frame(root)
input_frame.pack(pady=10)

Label(input_frame, text="红包总金额（元）：").grid(row=0, column=0, padx=10, pady=10)
entry_amount = Entry(input_frame)
entry_amount.grid(row=0, column=1, padx=10, pady=10)

Label(input_frame, text="抢红包的人数：").grid(row=1, column=0, padx=10, pady=10)
entry_people = Entry(input_frame)
entry_people.grid(row=1, column=1, padx=10, pady=10)

Button(input_frame, text="开始模拟", command=run_simulation).grid(row=2, column=0, columnspan=2, pady=10)

# 结果显示区域
result_frame = Frame(root)
result_frame.pack(pady=10)

result_text = Text(result_frame, height=10, width=50)
result_text.pack(side="left", fill="y")

scrollbar = Scrollbar(result_frame, command=result_text.yview)
scrollbar.pack(side="right", fill="y")
result_text.config(yscrollcommand=scrollbar.set)

# 图表区域
chart_frame = Frame(root)
chart_frame.pack(pady=10)

# 历史记录区域
history_frame = Frame(root)
history_frame.pack(pady=10)

Label(history_frame, text="历史记录：").pack()
history_text = Text(history_frame, height=10, width=80)
history_text.pack(side="left", fill="y")

scrollbar_history = Scrollbar(history_frame, command=history_text.yview)
scrollbar_history.pack(side="right", fill="y")
history_text.config(yscrollcommand=scrollbar_history.set)

# 保存按钮
Button(root, text="保存历史记录", command=save_history).pack(pady=10)

# 运行主循环
root.mainloop()