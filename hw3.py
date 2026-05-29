import random
import time
import threading
from typing import List, Tuple, Dict

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


# =========================
# 資料產生
# =========================

def generate_unique_random_numbers(n: int, min_value: int = 10, max_value: int = 200) -> List[int]:
    """
    產生 n 個不重複的隨機數字。

    
    """
    if n > (max_value - min_value + 1):
        raise ValueError("n 太大，超過可產生的不重複數字範圍。")

    return random.sample(range(min_value, max_value + 1), n)


# =========================
# Selection Sort 選擇排序
# =========================

def selection_sort(data: List[int]) -> Tuple[List[List[int]], float]:
    """
    
    時間複雜度：
    Best / Average / Worst 都大約是 O(n^2)
    """
    arr = data.copy()
    history = [arr.copy()]
    start_time = time.perf_counter()

    n = len(arr)
    for i in range(n):
        min_index = i

        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j

        if min_index != i:
            arr[i], arr[min_index] = arr[min_index], arr[i]
            history.append(arr.copy())

    end_time = time.perf_counter()
    return history, end_time - start_time


# =========================
# Insertion Sort 插入排序
# =========================

def insertion_sort(data: List[int]) -> Tuple[List[List[int]], float]:
    """
    
    時間複雜度：
    Best: O(n)；Average / Worst: O(n^2)
    """
    arr = data.copy()
    history = [arr.copy()]
    start_time = time.perf_counter()

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
            history.append(arr.copy())

        arr[j + 1] = key
        history.append(arr.copy())

    end_time = time.perf_counter()
    return history, end_time - start_time


# =========================
# Quick Sort 快速排序
# =========================

def quick_sort(data: List[int]) -> Tuple[List[List[int]], float]:
    """
    
    Sub QuickSort(array, start, end):
        if array length == 1:
            return
        pivot = array[1] / array[start]
        left = start
        right = end
        while left != right:
            decrease right until array[right] < array[pivot] or left == right
            increase left until array[left] > array[pivot] or left == right
            swap(array[left], array[right])
        swap(array[pivot], array[right])
        QuickSort(array, start, pivot - 1)
        QuickSort(array, pivot + 1, end)

   
    arr = data.copy()
    history = [arr.copy()]
    start_time = time.perf_counter()

    def quick_sort_recursive(start: int, end: int) -> None:
        
        if start >= end:
            return

        
        pivot_index = start
        pivot_value = arr[pivot_index]
        left = start
        right = end

        # left 和 right 還沒相遇前，持續從兩邊往中間找需要交換的值
        while left != right:
            # 從右往左找：找到比 pivot 小的值才停下來
            # 如果還沒找到，而且 left/right 沒相遇，就繼續往左
            while arr[right] >= pivot_value and left != right:
                right -= 1

            # 從左往右找：找到比 pivot 大的值才停下來
            # 如果還沒找到，而且 left/right 沒相遇，就繼續往右
            while arr[left] <= pivot_value and left != right:
                left += 1

            # 如果 left 和 right 還沒相遇，交換兩邊不在正確區域的值
            if left != right:
                arr[left], arr[right] = arr[right], arr[left]
                history.append(arr.copy())

        # left/right 相遇後，把 pivot 放到正確位置
        # 此時 right 就是 pivot 排好後的位置
        arr[pivot_index], arr[right] = arr[right], arr[pivot_index]
        history.append(arr.copy())

        new_pivot_index = right

        # 遞迴排序 pivot 左邊與右邊
        quick_sort_recursive(start, new_pivot_index - 1)
        quick_sort_recursive(new_pivot_index + 1, end)

    quick_sort_recursive(0, len(arr) - 1)

    end_time = time.perf_counter()
    return history, end_time - start_time


# =========================
# 使用 Thread 執行排序
# =========================

def run_sorting_in_threads(data: List[int]) -> Dict[str, Dict[str, object]]:
    """
    用三個 thread 分別跑三個排序演算法。
    每個 thread 會把自己的排序歷史紀錄與執行時間存進 results。
    """
    results: Dict[str, Dict[str, object]] = {}

    def worker(name: str, sort_function) -> None:
        history, elapsed_time = sort_function(data)
        results[name] = {
            "history": history,
            "time": elapsed_time
        }

    threads = [
        threading.Thread(target=worker, args=("Selection Sort", selection_sort)),
        threading.Thread(target=worker, args=("Insertion Sort", insertion_sort)),
        threading.Thread(target=worker, args=("Quick Sort", quick_sort)),
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    return results


# =========================
# 產生 GIF 動畫
# =========================

def create_sorting_gif(results: Dict[str, Dict[str, object]], output_file: str = "sorting_comparison.gif") -> None:
    """
    將三種排序演算法的過程製作成 GIF。
    """
    algorithm_names = ["Selection Sort", "Insertion Sort", "Quick Sort"]
    histories = [results[name]["history"] for name in algorithm_names]
    times = [results[name]["time"] for name in algorithm_names]

    max_frames = max(len(history) for history in histories)
    max_value = max(max(history[0]) for history in histories)

    fig, axes = plt.subplots(3, 1, figsize=(10, 9))
    fig.suptitle("Sorting Algorithm Visualization", fontsize=16)

    def update(frame: int):
        for index, ax in enumerate(axes):
            ax.clear()

            history = histories[index]
            current_state = history[min(frame, len(history) - 1)]

            ax.bar(range(len(current_state)), current_state)
            ax.set_ylim(0, max_value + 10)
            ax.set_title(
                f"{algorithm_names[index]} | Steps: {len(history) - 1} | Time: {times[index]:.6f} sec"
            )
            ax.set_xlabel("Index")
            ax.set_ylabel("Value")

        return axes

    animation = FuncAnimation(
        fig,
        update,
        frames=max_frames,
        interval=120,
        repeat=False
    )

    writer = PillowWriter(fps=8)
    animation.save(output_file, writer=writer)
    plt.close(fig)


# =========================
# 檢查排序結果是否正確
# =========================

def is_sorted_ascending(arr: List[int]) -> bool:
    """
   
    """
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True


# =========================
# 主程式
# =========================

def main() -> None:
    
    N = 30

    data = generate_unique_random_numbers(N, 10, 200)

    print("Original data:")
    print(data)
    print()

    results = run_sorting_in_threads(data)

    for name, result in results.items():
        final_state = result["history"][-1]
        elapsed_time = result["time"]

        print(f"{name}")
        print(f"Execution time: {elapsed_time:.6f} seconds")
        print(f"Steps recorded: {len(result['history']) - 1}")
        print(f"Sorted correctly: {is_sorted_ascending(final_state)}")
        print(final_state)
        print("-" * 60)

    create_sorting_gif(results, "sorting_comparison.gif")
    print("GIF file created: sorting_comparison.gif")


if __name__ == "__main__":
    main()
