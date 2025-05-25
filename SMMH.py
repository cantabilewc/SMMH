from math import floor, log2
import random
class Unit:
    def __init__(self, id, erase_count):
        self.id = id
        self.erase_count = erase_count

    def __repr__(self):
        return f"(ID:{self.id}, EC:{self.erase_count})"
    
class SMMH:
    def __init__(self):
        self.heap = [None, None] #index 0, 1 不放值，pair從index 2(最min) 3(最max) 開始
    def check_validity(self):
        ok = True
        n = len(self.heap)

        for i in range(2, n, 2):  # 遍歷所有偶數 index（min-side）
            # P1: 左 ≤ 右
            if i + 1 < n:
                if self.heap[i].erase_count > self.heap[i + 1].erase_count:
                    print(f"❌ P1 violated at ({i},{i+1}): {self.heap[i].erase_count} > {self.heap[i+1].erase_count}")
                    ok = False

            
            if i >= 4:
                # P2: 祖父左子 ≤ 我（min-side
                gpc = (i // 4) * 2
                if gpc >= 2 and self.heap[gpc].erase_count > self.heap[i].erase_count:
                    print(f"❌ P2 violated at {i} (min-side): grandparent's child {gpc} = {self.heap[gpc].erase_count} > {self.heap[i].erase_count}")
                    ok = False

                # P3: 祖父右子 ≥ 我（max-side
                if i + 1 < n:
                    gpc = ((i + 1) // 4) * 2 + 1
                    if self.heap[gpc].erase_count < self.heap[i + 1].erase_count:
                        print(f"❌ P3 violated at {i+1} (max-side): grandparent's child {gpc} = {self.heap[gpc].erase_count} < {self.heap[i+1].erase_count}")
                        ok = False

        if ok:
            print("✅ Heap is valid under P1, P2, P3 conditions.")
        else:
            print("❌❌❌ Heap has violations.")
        return ok

    def print_heap_tree(self):

        n = len(self.heap)  # 有效元素數量（去掉 index 0,1）
        total_level = floor(log2(n))
        level = 1
        idx = 2
        while idx < len(self.heap):
            count = 2 ** level
            row = ""
            for _ in range(count):
                if idx >= len(self.heap):
                    break
                unit = self.heap[idx]
                spacing = total_level - level
                row += f"{unit.erase_count} "
                if idx % 2:
                    row += " "*spacing
                else:
                    row += " "*spacing
                idx += 1
            print("  " * (total_level*2 - level) + row)
            level += 1

    def swap(self, idx_1, idx_2):
        temp = self.heap[idx_1]
        self.heap[idx_1] = self.heap[idx_2]
        self.heap[idx_2] = temp

    def push(self, unit):
        print(unit)
        self.heap.append(unit)
        last_idx = len(self.heap) - 1
        if last_idx % 2 == 1:  # last_idx 是右邊（奇數） → 有兄弟
            left = last_idx - 1
            right = last_idx
            if self.heap[left].erase_count > self.heap[right].erase_count:
                self.swap(left, right)
                last_idx = left

        if last_idx >= 4:
            current_idx = last_idx
            grand_parent = current_idx // 4
            while(grand_parent):
                left_child_idx = grand_parent * 2
                right_child_idx = left_child_idx + 1
                if self.heap[left_child_idx].erase_count > self.heap[current_idx].erase_count:
                    self.swap(left_child_idx, current_idx)
                    current_idx = left_child_idx
                elif self.heap[right_child_idx].erase_count < self.heap[current_idx].erase_count:
                    self.swap(right_child_idx, current_idx)
                    current_idx = right_child_idx
                else:
                    break
                grand_parent = current_idx // 4

    def pop_at(self, idx):
        last_unit = self.heap.pop()
        if idx == len(self.heap):  # 正好刪掉尾巴，無需再補
            return
        self.heap[idx] = last_unit
        #   Trickle Down 的目的，是先讓補進來的節點
        #   確保這個被抽換節點的index的子孫落在合法的區間中(找出該子樹的最min(偶數)或最max(奇數))
        #   這樣「它以下的世界」就穩定了，
        #   才有資格再trickle down以後回頭去微調「它以上的祖先結構」，也就是 Bubble Up。
        current_idx = idx # <- trickle down的用意是確保此節點仍然為其子孫中的最min(偶數)或最max(奇數) (符合P2P3定義)
        last_idx = len(self.heap) - 1
        if idx % 2: #odd, find max
            while True:
                left = (current_idx - 1) * 2 + 1
                right = current_idx * 2 + 1
                largest = current_idx

                if left <= last_idx and self.heap[left].erase_count > self.heap[largest].erase_count:
                    largest = left
                if right <= last_idx and self.heap[right].erase_count > self.heap[largest].erase_count:
                    largest = right

                if largest == current_idx:
                    break  # ✅ 目前已經是最大值 → 結束
                self.swap(current_idx, largest)
                current_idx = largest
            if self.heap[current_idx - 1].erase_count > self.heap[current_idx].erase_count:
                self.swap(current_idx - 1, current_idx)
                print('swap brother',current_idx - 1 )
                print('trickle down to last index',current_idx )
                print('[swap]trickle down to last index',current_idx )
                current_idx = current_idx - 1
        else:
            #even, find min
            while True:
                left = current_idx * 2
                right = current_idx * 2 + 2
                smallest = current_idx
                if left <= last_idx and self.heap[left].erase_count < self.heap[smallest].erase_count:
                    smallest = left
                if right <= last_idx and self.heap[right].erase_count < self.heap[smallest].erase_count:
                    smallest = right
                if smallest == current_idx:
                    break  # ✅ 目前已經是最大值 → 結束
                self.swap(current_idx, smallest)
                current_idx = smallest
            if (current_idx + 1 <= (len(self.heap) - 1)) and self.heap[current_idx].erase_count > self.heap[current_idx + 1].erase_count:
                self.swap(current_idx, current_idx + 1)
                print('swap brother',current_idx + 1 )
                print('[swap]trickle down to last index',current_idx )
                current_idx = current_idx + 1
        print('[pop] trickle down to last index',current_idx )
        self.check_validity()
        self.print_heap_tree()
        #now check bubble up
        if current_idx >= 4:
            grand_parent = current_idx // 4
            while(grand_parent):
                left_child_idx = grand_parent * 2
                right_child_idx = left_child_idx + 1
                if self.heap[left_child_idx].erase_count > self.heap[current_idx].erase_count:
                    self.swap(left_child_idx, current_idx)
                    current_idx = left_child_idx
                elif self.heap[right_child_idx].erase_count < self.heap[current_idx].erase_count:
                    self.swap(right_child_idx, current_idx)
                    current_idx = right_child_idx
                else:
                    break
                grand_parent = current_idx // 4
        print('[pop] bubble up to last index',current_idx )
        ok = self.check_validity()
        self.print_heap_tree()
        if not ok:
            print('❌Test Fail❌')
            while True:
                pass
smmh = SMMH()
test_loop = 1
my_range = 100
unit_num = 36
for j in range(0,test_loop):
    smmh.heap = [None, None]
    for i in range(1, unit_num + 1):  # id 1~20
        ec = random.randint(1, my_range)
        smmh.push(Unit(i, ec))
        if not smmh.check_validity():
            break
    smmh.print_heap_tree()
    pop_at_random_position = random.randint(2, unit_num)
    pop_at_random_position = 4
    print('[pop] index',pop_at_random_position)
    smmh.pop_at(pop_at_random_position)
    print(len(smmh.heap))

# for i in range(2, len(smmh.heap)):
#     print(f"{i}: {smmh.heap[i]}")

# smmh.print_heap_tree()
    # def pop_at(self, index):


    # def trickle_down(self, index):
    #     # 你可以根據 min-side / max-side 決定要往左 or 右子孫修復
    #     # 這裡你先回傳 False 讓 bubble_up 也能測試到
    #     return False

    # def bubble_up(self, index):
    #     # 這裡要補上你自己的上浮修復邏輯（檢查祖父節點 P2/P3）
    #     pass