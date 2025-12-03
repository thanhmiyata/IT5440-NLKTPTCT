# Bài Tập 3: Phân Tích Chương Trình Động

**Môn học:** IT5440 - Nguyên Lý và Kỹ Thuật Phân Tích Chương Trình  
**Sinh viên:** Phạm Tiến Thành - 20242422M  
**Ngày:** Tháng 11 năm 2025

## 📋 Tổng Quan Dự Án

Dự án này triển khai **4 kỹ thuật phân tích động cốt lõi** và **1 thử thách nâng cao** sử dụng `sys.settrace` của Python:

1. ✅ **Tracing (Theo Dấu)** - Thu thập lossless trace của quá trình thực thi
2. ✅ **Dynamic Slicing (Cắt Lát Động)** - Phân tích phụ thuộc ngược  
3. ✅ **Execution Indexing (Đánh Chỉ Mục Thực Thi)** - Định danh duy nhất cho điểm thực thi
4. ✅ **Fault Localization (Định Vị Lỗi)** - Tìm lỗi dựa trên phổ (Tarantula/Ochiai)
5. ✅ **Heisenbug** - Demo race condition với perturbation

---

## 📁 Cấu Trúc Dự Án

```
homework3_dynamic_analysis/
├── tracer_engine.py       # Khái niệm 1: Tracing Core (sys.settrace)
├── execution_indexer.py   # Khái niệm 3: Execution Indexing
├── dynamic_slicer.py      # Khái niệm 2: Thuật toán Dynamic Slicing
├── fault_localization.py  # Khái niệm 4: Fault Localization (Tarantula/Ochiai)
├── heisenbug_demo.py      # Thử thách: Heisenbug với Race Condition
├── target_programs.py     # Các hàm test có lỗi
├── main_runner.py         # Chương trình chính (chạy file này!)
└── README.md              # File này
```

---

## 🚀 Hướng Dẫn Nhanh

### Yêu Cầu Hệ Thống
- Python 3.7 trở lên
- Không cần thư viện bên ngoài (chỉ dùng thư viện chuẩn)

### Chạy Demo Đầy Đủ

```bash
cd homework3_dynamic_analysis
python main_runner.py
```

Lệnh này sẽ chạy tất cả 5 demo một cách tương tác với giải thích chi tiết.

### Chế Độ Nhanh (Không Dừng)

```bash
python main_runner.py --quick
```

### Chạy Từng Component Riêng Lẻ

```bash
# Test Tracer
python tracer_engine.py

# Test Execution Indexer
python execution_indexer.py

# Test Dynamic Slicer
python dynamic_slicer.py

# Test Fault Localizer
python fault_localization.py

# Test Heisenbug Demo
python heisenbug_demo.py

# Test Target Programs
python target_programs.py
```

---

## 📚 Mô Tả Chi Tiết Các Component

### 1. Tracer Engine (`tracer_engine.py`)

**Khái niệm:** Thu Thập Lossless Trace

**Triển khai:**
- Sử dụng `sys.settrace` để chặn mọi dòng code được thực thi
- Thu thập:
  - **Control Flow:** Số dòng được thực thi
  - **Giá Trị Biến:** Biến cục bộ tại mỗi bước
  - **Truy Cập Bộ Nhớ:** Các thao tác đọc/ghi

**Các Class Chính:**
- `TraceEvent`: Đại diện cho một sự kiện thực thi
- `Tracer`: Engine theo dấu chính

**Ví Dụ Sử Dụng:**
```python
from tracer_engine import Tracer

def my_function(n):
    result = 0
    for i in range(n):
        result += i
    return result

tracer = Tracer()
output = tracer.trace_execution(my_function, 5)
tracer.print_trace()
```

**Ánh Xạ Với Bài Tập:**
- ✅ Triển khai lossless trace (Slide: Tracing Concepts)
- ✅ Thu thập control flow và data flow
- ✅ Mô phỏng truy cập bộ nhớ

---

### 2. Dynamic Slicer (`dynamic_slicer.py`)

**Khái niệm:** Thuật Toán Backward Slicing

**Triển khai:**
- Tính toán dynamic slice cho một biến mục tiêu tại một dòng mục tiêu
- **Thuật toán:**
  1. Bắt đầu từ dòng mục tiêu
  2. Tìm lần ghi cuối cùng vào biến mục tiêu
  3. Truy ngược phụ thuộc dữ liệu
  4. Truy ngược phụ thuộc điều khiển

**Các Class Chính:**
- `DynamicSlicer`: Engine slicing chính
- `SliceResult`: Chứa các dòng liên quan và phụ thuộc

**Ví Dụ Sử Dụng:**
```python
from tracer_engine import Tracer
from dynamic_slicer import DynamicSlicer

# Theo dấu thực thi
tracer = Tracer()
tracer.trace_execution(my_function, 5)

# Tính toán slice
slicer = DynamicSlicer()
slice_result = slicer.compute_dynamic_slice(
    tracer.get_trace_log(),
    target_line=4,
    target_var='result'
)

print(f"Các dòng liên quan: {slice_result.relevant_lines}")
```

**Ánh Xạ Với Bài Tập:**
- ✅ Thuật toán backward traversal (Slide: Dynamic Slicing)
- ✅ Theo dấu phụ thuộc dữ liệu
- ✅ Theo dấu phụ thuộc điều khiển

---

### 3. Execution Indexer (`execution_indexer.py`)

**Khái niệm:** Định Danh Duy Nhất Cho Điểm Thực Thi

**Triển khai:**
- Gán ID duy nhất cho mỗi điểm thực thi
- **Định dạng:** `<Calling Context, Statement (Line), Instance>`
  - **Context:** Ngăn xếp gọi hàm
  - **Statement:** Số dòng
  - **Instance:** Số lần lặp (cho vòng lặp)

**Các Class Chính:**
- `ExecutionPoint`: Đại diện cho một điểm thực thi duy nhất
- `ExecutionIndexer`: Quản lý việc đánh chỉ mục
- `IndexedTracer`: Kết hợp tracing với indexing

**Ví Dụ Sử Dụng:**
```python
from execution_indexer import ExecutionIndexer

indexer = ExecutionIndexer()
indexer.push_context("my_function")

# Ghi lại các lần thực thi
point1 = indexer.record_execution(line_number=3)
point2 = indexer.record_execution(line_number=3)  # Instance khác

print(point1)  # <my_function, L3, #1>
print(point2)  # <my_function, L3, #2>
```

**Ánh Xạ Với Bài Tập:**
- ✅ Execution indexing với <Context, Statement, Instance> (Slide: Execution Indexing)
- ✅ Quản lý ngăn xếp context
- ✅ Đếm instance cho vòng lặp

---

### 4. Fault Localizer (`fault_localization.py`)

**Khái niệm:** Định Vị Lỗi Dựa Trên Phổ

**Triển khai:**
- Chạy nhiều test case (pass/fail)
- Xây dựng **Ma Trận Phổ** (tests × lines)
- Áp dụng **Công Thức Tarantula:**
  ```
  Suspiciousness(s) = failed(s)/total_failed / 
                      (passed(s)/total_passed + failed(s)/total_failed)
  ```
- Cũng triển khai **Công Thức Ochiai:**
  ```
  Suspiciousness(s) = failed(s) / sqrt(total_failed * (failed(s) + passed(s)))
  ```

**Các Class Chính:**
- `FaultLocalizer`: Engine định vị lỗi chính
- `TestCase`: Đại diện cho một test case
- `SuspiciousnessScore`: Điểm số cho mỗi dòng

**Ví Dụ Sử Dụng:**
```python
from fault_localization import FaultLocalizer

def buggy_function(a, b, c):
    max_val = a
    if b > max_val:
        max_val = b
    if c > max_val:
        max_val = b  # LỖI: Nên là c
    return max_val

localizer = FaultLocalizer()
localizer.add_test_case("test1", (1, 2, 3), 3)
localizer.add_test_case("test2", (5, 3, 1), 5)

localizer.run_tests(buggy_function)
localizer.print_results()
```

**Ánh Xạ Với Bài Tập:**
- ✅ Định vị lỗi dựa trên phổ (Slide: Fault Localization)
- ✅ Triển khai công thức Tarantula
- ✅ Triển khai công thức Ochiai
- ✅ Xây dựng ma trận coverage

---

### 5. Heisenbug Demo (`heisenbug_demo.py`)

**Khái niệm:** Heisenbug - Lỗi biến mất khi bạn cố quan sát nó

**Triển khai:**
- **Kịch bản:** Chuyển tiền tài khoản ngân hàng với race condition
- **Ba Lần Chạy:**
  1. **Thực Thi Bình Thường:** Nhanh, lỗi có thể không xuất hiện
  2. **Thực Thi Có Perturbation:** Inject delay buộc race condition xảy ra
  3. **Thực Thi An Toàn:** Dùng lock ngăn lỗi

**Các Class Chính:**
- `BankAccount`: Tài khoản có lỗi race condition
- `Perturbator`: Inject delay tại các điểm thực thi cụ thể

**Ví Dụ Kết Quả:**
```
KỊCH BẢN 1: Thực Thi Bình Thường (Nhanh, Không Perturbation)
Số dư cuối: $700 (Mong đợi: $700) ✓ ĐÚNG

KỊCH BẢN 2: Thực Thi Có Perturbation (Buộc Race Condition)
Số dư cuối: $800 (Mong đợi: $700) ✗ SAI - Mất $100

KỊCH BẢN 3: Thực Thi An Toàn (Với Thread Locks)
Số dư cuối: $700 (Mong đợi: $700) ✓ ĐÚNG
```

**Ánh Xạ Với Bài Tập:**
- ✅ Demo Heisenbug (Slide: Heisenbugs)
- ✅ Race condition trong code đa luồng
- ✅ Perturbation sử dụng execution indexing
- ✅ Chứng minh việc debug có thể che giấu lỗi

---

## 🎯 Ánh Xạ Với Yêu Cầu Bài Tập

| Yêu Cầu | File | Trạng Thái |
|---------|------|-----------|
| **Khái niệm 1: Tracing** | `tracer_engine.py` | ✅ Hoàn thành |
| - Lossless trace | Class `Tracer` | ✅ |
| - Thu thập control flow | `TraceEvent.line_number` | ✅ |
| - Giá trị biến | `TraceEvent.local_vars` | ✅ |
| - Truy cập bộ nhớ | `TraceEvent.memory_access` | ✅ |
| **Khái niệm 2: Dynamic Slicing** | `dynamic_slicer.py` | ✅ Hoàn thành |
| - Backward traversal | `_backward_traverse()` | ✅ |
| - Phụ thuộc dữ liệu | `data_deps` | ✅ |
| - Phụ thuộc điều khiển | `control_deps` | ✅ |
| **Khái niệm 3: Execution Indexing** | `execution_indexer.py` | ✅ Hoàn thành |
| - Theo dấu context | `context_stack` | ✅ |
| - Statement (dòng) | `ExecutionPoint.statement` | ✅ |
| - Đếm instance | `instance_counters` | ✅ |
| **Khái niệm 4: Fault Localization** | `fault_localization.py` | ✅ Hoàn thành |
| - Ma trận phổ | `spectra_matrix` | ✅ |
| - Công thức Tarantula | `_compute_tarantula()` | ✅ |
| - Công thức Ochiai | `_compute_ochiai()` | ✅ |
| **Thử thách: Heisenbug** | `heisenbug_demo.py` | ✅ Hoàn thành |
| - Race condition | `BankAccount` | ✅ |
| - Perturbation | `Perturbator` | ✅ |
| - Tích hợp execution indexing | `ExecutionPoint` | ✅ |

---

## 📊 Kết Quả Mong Đợi

Khi bạn chạy `python main_runner.py`, bạn sẽ thấy:

1. **Demo 1 (Tracing):**
   - Trace đầy đủ của `loop_example(5)`
   - Lịch sử biến `result`
   - Log truy cập bộ nhớ

2. **Demo 2 (Slicing):**
   - Dynamic slice cho biến `result`
   - Phụ thuộc dữ liệu và điều khiển
   - Các số dòng liên quan

3. **Demo 3 (Indexing):**
   - Các điểm thực thi duy nhất với format `<Context, Line, Instance>`
   - Thống kê hiển thị số lần instance cho các vòng lặp

4. **Demo 4 (Fault Localization):**
   - Kết quả test case (pass/fail)
   - Điểm nghi ngờ (Tarantula & Ochiai)
   - Xác định dòng lỗi trong `buggy_max`

5. **Demo 5 (Heisenbug):**
   - Ba kịch bản hiển thị hành vi race condition
   - Log giao dịch
   - Chứng minh perturbation làm lộ lỗi

---

## 🔬 Chi Tiết Kỹ Thuật

### Tại Sao Dùng `sys.settrace`?

`sys.settrace` của Python cho phép chúng ta:
- Chặn mọi dòng code được thực thi
- Truy cập biến cục bộ tại mỗi bước
- Theo dấu lời gọi hàm và return
- Xây dựng trace thực thi hoàn chỉnh

### Hạn Chế

- **Hiệu năng:** Tracing thêm overhead đáng kể
- **Phân tích đơn giản hóa:** Một số phân tích (ví dụ: phụ thuộc điều khiển) được đơn giản hóa
- **Chỉ cho Python:** Chỉ hoạt động với code Python

### Quyết Định Thiết Kế

1. **Kiến trúc modular:** Mỗi khái niệm trong file riêng để rõ ràng
2. **Tập trung giáo dục:** Comment và docstring chi tiết
3. **Ví dụ có thể chạy:** Mỗi file có block `__main__` để test
4. **Demo tuần tự:** Main runner hiển thị các khái niệm theo thứ tự logic

---

## 🧪 Kiểm Thử

Tất cả các component đã được test với:
- ✅ Hàm đơn giản (vòng lặp, điều kiện)
- ✅ Hàm có lỗi (lỗi cố ý)
- ✅ Code đa luồng (race conditions)

### Độ Bao Phủ Test

- `tracer_engine.py`: ✅ Đã test với `loop_example`
- `execution_indexer.py`: ✅ Đã test với các vòng lặp
- `dynamic_slicer.py`: ✅ Đã test với chuỗi phụ thuộc
- `fault_localization.py`: ✅ Đã test với `buggy_max` (7 test cases)
- `heisenbug_demo.py`: ✅ Đã test với 3 kịch bản

---

## 📖 Tài Liệu Tham Khảo

- **Slide Môn Học:** IT5440 - Dynamic Program Analysis
- **Tài Liệu Python:** `sys.settrace` - https://docs.python.org/3/library/sys.html#sys.settrace
- **Bài Báo:**
  - Jones & Harrold (2005) - Tarantula fault localization
  - Abreu et al. (2007) - Ochiai coefficient for fault localization

---

## 👨‍💻 Ghi Chú Tác Giả

Dự án này demo tất cả các khái niệm yêu cầu với:
- ✅ Code sạch, modular
- ✅ Tài liệu chi tiết
- ✅ Ví dụ có thể chạy
- ✅ Ánh xạ rõ ràng với yêu cầu bài tập

**Thành Tựu Chính:**
1. Triển khai tracing engine hoàn chỉnh với `sys.settrace`
2. Xây dựng thuật toán backward slicing với theo dấu phụ thuộc
3. Tạo execution indexing với tuple context/statement/instance
4. Triển khai Tarantula và Ochiai fault localization
5. Demo Heisenbug với race condition và perturbation

---

## 📝 Giấy Phép

Dự án này được tạo cho mục đích giáo dục như một phần của bài tập IT5440.

---

**Chúc bạn khám phá vui vẻ với phân tích chương trình động! 🚀**
