import tkinter as tk
import random
import time
import threading

# =====================================================
# Selection Sort（選擇排序）
# 概念：
# 每次從未排序區域中找出最小值
# 再放到最前面
# =====================================================

def selection_sort(arr, draw_callback, speed):

    # 取得陣列長度
    n = len(arr)

    # 外層迴圈控制目前排序位置
    for i in range(n):

        # 假設目前位置為最小值
        min_idx = i

        # 從後面尋找更小的元素
        for j in range(i + 1, n):

            # 如果找到更小值
            if arr[j] < arr[min_idx]:
                min_idx = j

            # 視覺化顯示
            # 黃色：目前比較位置
            # 紅色：目前最小值
            draw_callback(
                arr,
                [ "yellow" if x == j else
                    "red" if x == min_idx else
                    "skyblue"
                    for x in range(len(arr))  ]
            )
            # 延遲動畫速度
            time.sleep(speed)

        # 將最小值交換到前面
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

        # 綠色代表已排序完成
        draw_callback(
            arr,
            ["green" if x <= i else "skyblue"
                for x in range(len(arr))
            ]
        )

        time.sleep(speed)

    # 全部完成後全部變綠色
    draw_callback(arr, ["green"] * len(arr))

# =====================================================
# Bubble Sort（泡泡排序）
# 概念：
# 相鄰元素兩兩比較
# 大的數字慢慢往右邊移動
# =====================================================

def bubble_sort(arr, draw_callback, speed):

    n = len(arr)

    # 外層控制回合數
    for i in range(n):

        # 用來判斷是否有交換
        swapped = False

        # 每回合比較相鄰元素
        for j in range(0, n - i - 1):

            # 如果左邊比右邊大則交換
            if arr[j] > arr[j + 1]:

                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

            # 黃色表示正在比較
            draw_callback( arr,
                [  "yellow" if x == j or x == j + 1
                    else "skyblue"
                    for x in range(len(arr))
                ]
            )

            time.sleep(speed)

        # 已完成排序的部分顯示綠色
        draw_callback(
            arr,
            [
                "green" if x >= n - i - 1
                else "skyblue"
                for x in range(len(arr))
            ]
        )

        # 如果完全沒交換代表已排序完成
        if not swapped:
            break

    draw_callback(arr, ["green"] * len(arr))

# =====================================================
# Quick Sort（快速排序）
# 課堂版本：
# pivot 固定取最左邊元素
# left/right 指標往中間移動
# =====================================================

def quick_sort(arr, start, end, draw_callback, speed):

    # 如果區域只剩一個元素則停止
    if start >= end:
        return

    # pivot 設為最左邊元素
    pivot = start

    # left 從 pivot 右邊開始
    left = start + 1

    # right 從最右邊開始
    right = end

    # left 與 right 尚未交錯
    while left <= right:

        # left 尋找比 pivot 大的元素
        while left <= end and arr[left] <= arr[pivot]:
            left += 1

        # right 尋找比 pivot 小的元素
        while right > start and arr[right] >= arr[pivot]:
            right -= 1

        # left 與 right 尚未交錯則交換
        if left < right:

            arr[left], arr[right] = arr[right], arr[left]

            # 紫色：left
            # 橘色：right
            # 紅色：pivot
            draw_callback(
                arr,
                [
                    "purple" if x == left else
                    "orange" if x == right else
                    "red" if x == pivot else
                    "skyblue"
                    for x in range(len(arr))
                ]
            )

            time.sleep(speed)

    # 最後將 pivot 與 right 交換
    arr[pivot], arr[right] = arr[right], arr[pivot]

    # pivot 放到正確位置後標記綠色
    draw_callback(
        arr,
        [
            "green" if x == right else
            "skyblue"
            for x in range(len(arr))
        ]
    )

    time.sleep(speed)

    # 遞迴排序左半部
    quick_sort(arr, start, right - 1, draw_callback, speed)

    # 遞迴排序右半部
    quick_sort(arr, right + 1, end, draw_callback, speed)

# =====================================================
# GUI 視覺化介面
# =====================================================

class SortVisualizer:

    def __init__(self, root):

        self.root = root
        self.root.title("Sorting Algorithm Visualizer")

        # 資料數量
        self.data_size = 60

        # 動畫速度
        self.speed = 0.01

        # 建立隨機不重複資料
        self.original_data = random.sample(
            range(1, 301),
            self.data_size
        )

        self.setup_ui()

    # 建立介面
    def setup_ui(self):

        # 標題
        title = tk.Label(
            self.root,
            text="Selection Sort vs Bubble Sort vs Quick Sort",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)

        # 按鈕區域
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=5)

        # 重新產生資料按鈕
        tk.Button(
            control_frame,
            text="重新產生資料",
            command=self.generate_data,
            bg="#4CAF50",
            fg="white",
            width=15
        ).grid(row=0, column=0, padx=5)

        # 開始排序按鈕
        tk.Button(
            control_frame,
            text="開始排序",
            command=self.start_sorting,
            bg="#2196F3",
            fg="white",
            width=15
        ).grid(row=0, column=1, padx=5)

        # 狀態文字
        self.info_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 11)
        )
        self.info_label.pack(pady=5)

        # 畫布區域
        canvas_frame = tk.Frame(self.root)
        canvas_frame.pack()

        # Selection Sort 畫布
        self.selection_canvas = tk.Canvas(
            canvas_frame,
            width=350,
            height=250,
            bg="white"
        )
        self.selection_canvas.grid(row=0, column=0, padx=10)

        # Bubble Sort 畫布
        self.bubble_canvas = tk.Canvas(
            canvas_frame,
            width=350,
            height=250,
            bg="white"
        )
        self.bubble_canvas.grid(row=0, column=1, padx=10)

        # Quick Sort 畫布
        self.quick_canvas = tk.Canvas(
            canvas_frame,
            width=350,
            height=250,
            bg="white"
        )
        self.quick_canvas.grid(row=0, column=2, padx=10)

        # 演算法名稱
        label_frame = tk.Frame(self.root)
        label_frame.pack(pady=5)

        tk.Label(
            label_frame,
            text="Selection Sort",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=0, padx=95)

        tk.Label(
            label_frame,
            text="Bubble Sort",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=1, padx=95)

        tk.Label(
            label_frame,
            text="Quick Sort",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=2, padx=95)

        # 顯示執行時間
        result_frame = tk.Frame(self.root)
        result_frame.pack(pady=10)

        self.selection_time_label = tk.Label(
            result_frame,
            text="Selection: ",
            font=("Arial", 11)
        )
        self.selection_time_label.grid(row=0, column=0, padx=20)

        self.bubble_time_label = tk.Label(
            result_frame,
            text="Bubble: ",
            font=("Arial", 11)
        )
        self.bubble_time_label.grid(row=0, column=1, padx=20)

        self.quick_time_label = tk.Label(
            result_frame,
            text="Quick: ",
            font=("Arial", 11)
        )
        self.quick_time_label.grid(row=0, column=2, padx=20)

        # 初始資料繪圖
        self.draw_data(
            self.selection_canvas,
            self.original_data,
            ["skyblue"] * len(self.original_data)
        )

        self.draw_data(
            self.bubble_canvas,
            self.original_data,
            ["skyblue"] * len(self.original_data)
        )

        self.draw_data(
            self.quick_canvas,
            self.original_data,
            ["skyblue"] * len(self.original_data)
        )

    # 重新產生隨機資料
    def generate_data(self):

        self.original_data = random.sample(
            range(1, 301),
            self.data_size
        )

        self.draw_data(
            self.selection_canvas,
            self.original_data,
            ["skyblue"] * len(self.original_data)
        )

        self.draw_data(
            self.bubble_canvas,
            self.original_data,
            ["skyblue"] * len(self.original_data)
        )

        self.draw_data(
            self.quick_canvas,
            self.original_data,
            ["skyblue"] * len(self.original_data)
        )

        self.selection_time_label.config(text="Selection: ")
        self.bubble_time_label.config(text="Bubble: ")
        self.quick_time_label.config(text="Quick: ")

        self.info_label.config(text="已重新產生隨機資料")

    # 繪製長條圖
    def draw_data(self, canvas, data, color_array):

        # 清除畫布
        canvas.delete("all")

        canvas_width = 350
        canvas_height = 250

        # 每個長條寬度
        bar_width = canvas_width / len(data)

        # 找最大值
        max_data = max(data)

        # 開始畫圖
        for i, value in enumerate(data):

            x0 = i * bar_width
            y0 = canvas_height - (value / max_data) * 220

            x1 = (i + 1) * bar_width
            y1 = canvas_height

            canvas.create_rectangle(
                x0,
                y0,
                x1,
                y1,
                fill=color_array[i],
                outline=""
            )

        self.root.update_idletasks()

    # 開始排序
    def start_sorting(self):

        # 複製三份資料
        selection_data = self.original_data.copy()
        bubble_data = self.original_data.copy()
        quick_data = self.original_data.copy()

        self.info_label.config(text="排序中...")

        # 建立三個 thread
        t1 = threading.Thread(
            target=self.run_selection_sort,
            args=(selection_data,)
        )

        t2 = threading.Thread(
            target=self.run_bubble_sort,
            args=(bubble_data,)
        )

        t3 = threading.Thread(
            target=self.run_quick_sort,
            args=(quick_data,)
        )

        # 同時開始執行
        t1.start()
        t2.start()
        t3.start()

    # 執行 Selection Sort
    def run_selection_sort(self, data):
        start = time.perf_counter()
        selection_sort(
            data,
            lambda d, c:
            self.draw_data(self.selection_canvas, d, c),
            self.speed
        )

        end = time.perf_counter()

        self.selection_time_label.config(
            text=f"Selection: {end - start:.4f} 秒"
        )

    # 執行 Bubble Sort
    def run_bubble_sort(self, data):

        start = time.perf_counter()

        bubble_sort(
            data,
            lambda d, c:
            self.draw_data(self.bubble_canvas, d, c),
            self.speed
        )

        end = time.perf_counter()

        self.bubble_time_label.config(
            text=f"Bubble: {end - start:.4f} 秒"
        )

    # 執行 Quick Sort
    def run_quick_sort(self, data):

        start = time.perf_counter()

        quick_sort(
            data,
            0,
            len(data) - 1,
            lambda d, c:
            self.draw_data(self.quick_canvas, d, c),
            self.speed
        )

        # 排序完成後全部變綠色
        self.draw_data(
            self.quick_canvas,
            data,
            ["green"] * len(data)
        )

        end = time.perf_counter()

        self.quick_time_label.config(
            text=f"Quick: {end - start:.4f} 秒"
        )

        self.info_label.config(text="排序完成！")
# =====================================================
# 主程式
# =====================================================

if __name__ == "__main__":

    # 建立視窗
    root = tk.Tk()
    # 建立 GUI 物件
    app = SortVisualizer(root)
    # 執行 GUI
    root.mainloop()
