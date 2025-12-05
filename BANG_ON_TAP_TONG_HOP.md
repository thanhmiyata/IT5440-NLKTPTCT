# 📚 BẢNG ÔN TẬP TỔNG HỢP - IT5440
## Nguyên Lý và Kỹ Thuật Phân Tích Chương Trình

---

## 📋 MỤC LỤC

1. [Homework 3: Phân Tích Động (Dynamic Analysis)](#homework-3)
2. [HWASanIO: Memory Safety với Memory Shading](#hwasanio)
3. [So Sánh Các Kỹ Thuật](#so-sanh)
4. [Khái Niệm Lý Thuyết](#ly-thuyet)
5. [Kết Quả Thực Nghiệm](#ket-qua)

---

## 🎯 HOMEWORK 3: PHÂN TÍCH ĐỘNG {#homework-3}

### Tổng Quan

| **Thông Tin** | **Chi Tiết** |
|---------------|--------------|
| **Môn học** | IT5440 - Nguyên Lý và Kỹ Thuật Phân Tích Chương Trình |
| **Sinh viên** | Phạm Tiến Thành - 20242422M |
| **Ngày** | Tháng 11 năm 2025 |
| **Công nghệ** | Python 3.7+, `sys.settrace` |
| **Số kỹ thuật** | 4 kỹ thuật cốt lõi + 1 thử thách nâng cao |

---

### 1. TRACING (Theo Dấu Thực Thi)

| **Khía Cạnh** | **Mô Tả** |
|---------------|-----------|
| **File** | `tracer_engine.py` |
| **Khái niệm** | Thu thập lossless trace của quá trình thực thi |
| **Công cụ** | `sys.settrace` - chặn mọi dòng code được thực thi |
| **Thu thập** | • Control Flow (số dòng) <br> • Giá trị biến (local variables) <br> • Truy cập bộ nhớ (read/write) |
| **Class chính** | `TraceEvent`, `Tracer` |
| **Ví dụ** | Trace hàm `loop_example(5)` - thu thập toàn bộ lịch sử thực thi |
| **Ánh xạ bài tập** | ✅ Lossless trace <br> ✅ Control flow & data flow <br> ✅ Mô phỏng truy cập bộ nhớ |

**Cách sử dụng:**
```python
from tracer_engine import Tracer
tracer = Tracer()
output = tracer.trace_execution(my_function, 5)
tracer.print_trace()
```

---

### 2. DYNAMIC SLICING (Cắt Lát Động)

| **Khía Cạnh** | **Mô Tả** |
|---------------|-----------|
| **File** | `dynamic_slicer.py` |
| **Khái niệm** | Thuật toán backward slicing - tìm phụ thuộc ngược |
| **Thuật toán** | 1. Bắt đầu từ dòng mục tiêu <br> 2. Tìm lần ghi cuối cùng vào biến mục tiêu <br> 3. Truy ngược phụ thuộc dữ liệu <br> 4. Truy ngược phụ thuộc điều khiển |
| **Class chính** | `DynamicSlicer`, `SliceResult` |
| **Kết quả** | Danh sách các dòng liên quan và phụ thuộc |
| **Ánh xạ bài tập** | ✅ Backward traversal <br> ✅ Phụ thuộc dữ liệu <br> ✅ Phụ thuộc điều khiển |

**Cách sử dụng:**
```python
from dynamic_slicer import DynamicSlicer
slicer = DynamicSlicer()
slice_result = slicer.compute_dynamic_slice(
    trace_log, target_line=4, target_var='result'
)
```

---

### 3. EXECUTION INDEXING (Đánh Chỉ Mục Thực Thi)

| **Khía Cạnh** | **Mô Tả** |
|---------------|-----------|
| **File** | `execution_indexer.py` |
| **Khái niệm** | Định danh duy nhất cho mỗi điểm thực thi |
| **Định dạng** | `<Calling Context, Statement (Line), Instance>` |
| **Thành phần** | • **Context**: Ngăn xếp gọi hàm <br> • **Statement**: Số dòng <br> • **Instance**: Số lần lặp (cho vòng lặp) |
| **Class chính** | `ExecutionPoint`, `ExecutionIndexer`, `IndexedTracer` |
| **Ví dụ** | `<my_function, L3, #1>` vs `<my_function, L3, #2>` (instance khác) |
| **Ánh xạ bài tập** | ✅ Execution indexing với tuple <br> ✅ Quản lý ngăn xếp context <br> ✅ Đếm instance cho vòng lặp |

**Cách sử dụng:**
```python
from execution_indexer import ExecutionIndexer
indexer = ExecutionIndexer()
point1 = indexer.record_execution(line_number=3)  # <func, L3, #1>
point2 = indexer.record_execution(line_number=3)  # <func, L3, #2>
```

---

### 4. FAULT LOCALIZATION (Định Vị Lỗi)

| **Khía Cạnh** | **Mô Tả** |
|---------------|-----------|
| **File** | `fault_localization.py` |
| **Khái niệm** | Định vị lỗi dựa trên phổ (spectrum-based) |
| **Quy trình** | 1. Chạy nhiều test case (pass/fail) <br> 2. Xây dựng Ma Trận Phổ (tests × lines) <br> 3. Áp dụng công thức Tarantula/Ochiai |
| **Công thức Tarantula** | `Suspiciousness(s) = failed(s)/total_failed / (passed(s)/total_passed + failed(s)/total_failed)` |
| **Công thức Ochiai** | `Suspiciousness(s) = failed(s) / sqrt(total_failed * (failed(s) + passed(s)))` |
| **Class chính** | `FaultLocalizer`, `TestCase`, `SuspiciousnessScore` |
| **Ánh xạ bài tập** | ✅ Định vị lỗi dựa trên phổ <br> ✅ Tarantula & Ochiai <br> ✅ Ma trận coverage |

**Cách sử dụng:**
```python
from fault_localization import FaultLocalizer
localizer = FaultLocalizer()
localizer.add_test_case("test1", (1, 2, 3), 3)
localizer.run_tests(buggy_function)
localizer.print_results()
```

---

### 5. HEISENBUG DEMO (Thử Thách Nâng Cao)

| **Khía Cạnh** | **Mô Tả** |
|---------------|-----------|
| **File** | `heisenbug_demo.py` |
| **Khái niệm** | Lỗi biến mất khi bạn cố quan sát nó |
| **Kịch bản** | Chuyển tiền tài khoản ngân hàng với race condition |
| **3 lần chạy** | 1. Thực thi bình thường (nhanh, lỗi có thể không xuất hiện) <br> 2. Thực thi có perturbation (inject delay buộc race condition) <br> 3. Thực thi an toàn (dùng lock ngăn lỗi) |
| **Class chính** | `BankAccount`, `Perturbator` |
| **Ánh xạ bài tập** | ✅ Demo Heisenbug <br> ✅ Race condition đa luồng <br> ✅ Perturbation với execution indexing |

**Kết quả mẫu:**
```
KỊCH BẢN 1: Thực Thi Bình Thường
Số dư cuối: $700 (Mong đợi: $700) ✓ ĐÚNG

KỊCH BẢN 2: Thực Thi Có Perturbation
Số dư cuối: $800 (Mong đợi: $700) ✗ SAI - Mất $100

KỊCH BẢN 3: Thực Thi An Toàn (Với Thread Locks)
Số dư cuối: $700 (Mong đợi: $700) ✓ ĐÚNG
```

---

### Cấu Trúc File Homework 3

```
homework3_dynamic_analysis/
├── tracer_engine.py       # Khái niệm 1: Tracing Core
├── execution_indexer.py   # Khái niệm 3: Execution Indexing
├── dynamic_slicer.py      # Khái niệm 2: Dynamic Slicing
├── fault_localization.py # Khái niệm 4: Fault Localization
├── heisenbug_demo.py     # Thử thách: Heisenbug
├── target_programs.py    # Các hàm test có lỗi
├── main_runner.py         # Chương trình chính
└── README.md              # Tài liệu
```

---

## 🔒 HWASanIO: MEMORY SAFETY VỚI MEMORY SHADING {#hwasanio}

### Tổng Quan

| **Thông Tin** | **Chi Tiết** |
|---------------|--------------|
| **Tên đầy đủ** | HWASanIO: Detecting C/C++ Intra-object Overflows with Memory Shading |
| **Nguồn gốc** | Mở rộng từ HWASan (Hardware-assisted AddressSanitizer) |
| **Kiến trúc** | Chỉ hỗ trợ ARMv8 (AArch64) với Top-Byte Ignore (TBI) |
| **Công cụ** | LLVM/Clang với compiler instrumentation |
| **Vấn đề giải quyết** | Phát hiện Intra-object Overflow (tràn bộ nhớ giữa các field trong struct) |

---

### Vấn Đề Cốt Lõi

| **Vấn đề** | **Mô Tả** |
|------------|-----------|
| **HWASan gốc** | Chỉ gắn tag cho toàn bộ object, không phân biệt các field bên trong |
| **Ví dụ** | `struct { char buf[10]; int secret; }` - ghi tràn từ `buf` sang `secret` không bị phát hiện |
| **Hậu quả** | Có thể gây ra hành vi sai lệch hoặc bị khai thác để chiếm quyền điều khiển |

---

### Giải Pháp: Memory Shading

| **Khái Niệm** | **Mô Tả** |
|---------------|-----------|
| **Memory Shading** | Mở rộng của Memory Tagging, chia metadata thành 2 phần |
| **Color (Màu)** | 4 bit cao - định danh đối tượng (giống tag cũ) |
| **Shade (Bóng)** | 4 bit thấp - định danh trường (field) bên trong object |
| **Cơ chế** | • Struct: Shade bắt đầu từ 1, tăng dần cho mỗi field <br> • Non-struct: Shade = 0 <br> • Nested struct: Reset shade về 1 cho struct con |

**Ví dụ:**
```
struct double_buffer {
    char buf1[16];  // Color: E, Shade: 1 → Tag: 0xE1
    char buf2[16];  // Color: E, Shade: 2 → Tag: 0xE2
}
```

---

### Cơ Chế Hoạt Động

| **Bước** | **Mô Tả** |
|----------|-----------|
| **1. Gán Tag & Shade** | Khi khởi tạo struct, mỗi field được gán Color và Shade riêng |
| **2. Truy cập bộ nhớ** | Con trỏ trỏ tới field mang tag (Color + Shade) của field đó |
| **3. Kiểm tra Runtime** | So sánh tag con trỏ với tag trong Shadow Memory |
| **4. Phát hiện lỗi** | Nếu tag không khớp → Báo lỗi `tag-mismatch` |

**Logic kiểm tra:**
```cpp
// So sánh Color
if (ptr_color != mem_color) → Inter-object overflow

// So sánh Shade (nếu Color khớp)
if (ptr_shade == 0 || mem_shade == 0) → Hợp lệ (non-struct)
else if (ptr_shade == mem_shade) → Hợp lệ
else → Intra-object overflow!
```

---

### So Sánh Với Các Phương Pháp Khác

| **Tiêu chí** | **ASan/HWASan** | **SoftBound/CETS** | **EffectiveSan** | **HWASanIO** |
|--------------|-----------------|-------------------|------------------|--------------|
| **Phát hiện inter-object overflow** | ✅ Có | ✅ Có | ✅ Có | ✅ Có |
| **Phát hiện intra-object overflow** | ❌ Không | ✅ Có (overhead cao) | ✅ Có (hạn chế) | ✅ Có |
| **Phát hiện use-after-free** | ✅ Có | ✅ Có | ❌ Không | ✅ Có |
| **Kiểu metadata** | Red-zone & shadow memory | Bounds + lock-key | Dynamic type info | Color + Shade |
| **Overhead bộ nhớ** | Trung bình | Rất cao | Cao | Trung bình |
| **Tương thích ABI** | Tốt | Kém | Tốt | Tốt (không dùng redzone) |

---

### Kết Quả Thực Nghiệm

| **Benchmark** | **Kết Quả** |
|---------------|-------------|
| **Juliet Test Suite** | 100% tỷ lệ phát hiện lỗi (vs 85.4% của HWASan gốc) |
| **SPEC CPU 2017** | Overhead trung bình: 29% (vs 18% của HWASan) |
| **Memory Overhead** | ~136% (do ánh xạ 1-to-1 thay vì 1-to-16) |

---

### Hạn Chế

| **Hạn chế** | **Mô Tả** |
|-------------|-----------|
| **Giới hạn 4-bit Shade** | Chỉ phân biệt được 15 field liền kề (modulo khi vượt quá) |
| **Padding** | Vùng padding giữa các field không có shade riêng → có thể bỏ sót lỗi |
| **Kiến trúc** | Chỉ hỗ trợ ARMv8 (cần TBI), x86_64 phải dùng UntagAddr thủ công |
| **Granularity** | Hoạt động dựa trên granule 16-byte, struct nhỏ có thể nằm chung granule |

---

### Kịch Bản Thực Nghiệm

#### Kịch Bản 1: KHÔNG phát hiện lỗi (`repro_issue.c`)

| **Thông tin** | **Chi tiết** |
|---------------|--------------|
| **Code** | `struct UserData { char name[10]; int secret_id; }` |
| **Lỗi** | Ghi 16 bytes vào `name` (tràn 6 bytes sang `secret_id`) |
| **Kết quả** | Exit code 0 - KHÔNG báo lỗi |
| **Nguyên nhân** | Padding giữa `name` và `secret_id` không có shade riêng, hoặc cả hai nằm chung granule 16-byte |

#### Kịch Bản 2: PHÁT HIỆN lỗi (`test-hwasanio.c`)

| **Thông tin** | **Chi tiết** |
|---------------|--------------|
| **Code** | `struct double_buffer { char buf1[16]; char buf2[16]; }` |
| **Lỗi** | Ghi 20 bytes vào `buf1` (tràn 4 bytes sang `buf2`) |
| **Kết quả** | CRASH với `tag-mismatch` |
| **Log** | `e1` (buf1) vs `e2` (buf2) - cùng Color E, khác Shade 1 vs 2 |

---

## 📊 SO SÁNH CÁC KỸ THUẬT {#so-sanh}

### Phân Tích Động vs Phân Tích Tĩnh

| **Tiêu chí** | **Phân Tích Động** | **Phân Tích Tĩnh** |
|--------------|-------------------|-------------------|
| **Thời điểm** | Runtime (khi chạy) | Compile-time (khi biên dịch) |
| **Input** | Cần test case cụ thể | Phân tích toàn bộ code |
| **Độ chính xác** | Cao (biết giá trị thực tế) | Có thể có false positive |
| **Overhead** | Cao (chậm hơn khi chạy) | Thấp (chỉ chậm khi biên dịch) |
| **Ví dụ** | HWASanIO, Homework 3 | Static analysis tools |

---

### Memory Safety Approaches

| **Phương pháp** | **Cơ chế** | **Ưu điểm** | **Nhược điểm** |
|----------------|------------|-------------|----------------|
| **ASan** | Red-zones + shadow memory | Phổ biến, dễ dùng | Tốn bộ nhớ, không bắt intra-object |
| **HWASan** | Memory tagging (hardware) | Nhanh, ít tốn bộ nhớ | Không bắt intra-object |
| **SoftBound** | Fat pointers (bounds) | Chính xác cao | Overhead cao, khó tương thích |
| **EffectiveSan** | Dynamic type info | Phát hiện type confusion | Không bắt intra-object cùng kiểu |
| **HWASanIO** | Memory shading (color+shade) | Bắt intra-object, tương thích ABI | Chỉ ARMv8, overhead bộ nhớ cao |

---

## 📖 KHÁI NIỆM LÝ THUYẾT {#ly-thuyet}

### Memory Safety

| **Loại** | **Mô Tả** | **Ví dụ lỗi** |
|----------|-----------|---------------|
| **Spatial Memory Safety** | Đảm bảo truy cập trong ranh giới hợp lệ | Buffer overflow, buffer underflow |
| **Temporal Memory Safety** | Đảm bảo truy cập trong vòng đời object | Use-after-free, double-free |

---

### Dynamic Analysis Techniques

| **Kỹ thuật** | **Mục đích** | **Công cụ** |
|--------------|-------------|-------------|
| **Tracing** | Thu thập lịch sử thực thi | `sys.settrace` (Python) |
| **Dynamic Slicing** | Tìm phụ thuộc ngược | Backward traversal algorithm |
| **Execution Indexing** | Định danh điểm thực thi | Context + Statement + Instance |
| **Fault Localization** | Tìm dòng code lỗi | Spectrum-based (Tarantula/Ochiai) |

---

### Memory Tagging vs Memory Shading

| **Khía cạnh** | **Memory Tagging** | **Memory Shading** |
|---------------|-------------------|-------------------|
| **Metadata** | 1 tag (8 bit) cho object | Color (4 bit) + Shade (4 bit) |
| **Phạm vi** | Phân biệt object | Phân biệt object + field |
| **Phát hiện** | Inter-object overflow | Inter + Intra-object overflow |
| **Ví dụ** | HWASan | HWASanIO |

---

## 🧪 KẾT QUẢ THỰC NGHIỆM {#ket-qua}

### Homework 3 - Test Coverage

| **Component** | **Trạng thái** | **Test Cases** |
|---------------|----------------|----------------|
| `tracer_engine.py` | ✅ Đã test | `loop_example` |
| `execution_indexer.py` | ✅ Đã test | Các vòng lặp |
| `dynamic_slicer.py` | ✅ Đã test | Chuỗi phụ thuộc |
| `fault_localization.py` | ✅ Đã test | `buggy_max` (7 test cases) |
| `heisenbug_demo.py` | ✅ Đã test | 3 kịch bản |

---

### HWASanIO - Thực Nghiệm

| **Kịch bản** | **Kết quả** | **Ghi chú** |
|--------------|-------------|-------------|
| **Test case chuẩn** | ✅ Phát hiện lỗi | `test-hwasanio.c` - struct 16-byte |
| **Test case thực tế** | ❌ Không phát hiện | `repro_issue.c` - struct nhỏ với padding |
| **Juliet Test Suite** | ✅ 100% detection | Theo bài báo gốc |
| **SPEC CPU 2017** | ⚠️ 29% overhead | Chấp nhận được cho testing |

---

## 🔑 ĐIỂM QUAN TRỌNG CẦN NHỚ

### Homework 3

1. ✅ **Tracing**: Sử dụng `sys.settrace` để chặn mọi dòng code
2. ✅ **Dynamic Slicing**: Backward traversal tìm phụ thuộc
3. ✅ **Execution Indexing**: Format `<Context, Line, Instance>`
4. ✅ **Fault Localization**: Tarantula và Ochiai formulas
5. ✅ **Heisenbug**: Race condition + perturbation

### HWASanIO

1. ✅ **Memory Shading**: Color (4 bit) + Shade (4 bit)
2. ✅ **Chỉ ARMv8**: Cần Top-Byte Ignore (TBI)
3. ✅ **1-to-1 mapping**: Shadow memory (vs 1-to-16 của HWASan)
4. ✅ **100% detection**: Trên Juliet Test Suite
5. ⚠️ **Hạn chế**: Padding, granule 16-byte, giới hạn 15 field

---

## 📚 TÀI LIỆU THAM KHẢO

### Bài Báo Chính
- **HWASanIO**: "HWASanIO: Detecting C/C++ Intra-object Overflows with Memory Shading" (SOAP '23)

### Tài Liệu Khác
- Memory Tagging and how it improves C/C++ memory safety
- SoftBound: Highly Compatible and Complete Spatial Memory Safety for C
- Tech-ASan: Two-stage check for Address Sanitizer
- EffectiveSan: Type and Memory Error Detection using Dynamically Typed C/C++
- SoK: Sanitizing for Security

### Python Documentation
- `sys.settrace`: https://docs.python.org/3/library/sys.html#sys.settrace

---

## 🎯 CÂU HỎI ÔN TẬP

### Câu Hỏi Về Homework 3

1. **Tracing hoạt động như thế nào?**
   - Sử dụng `sys.settrace` để chặn mọi dòng code, thu thập control flow, giá trị biến, và truy cập bộ nhớ.

2. **Dynamic Slicing khác gì với Static Slicing?**
   - Dynamic slicing dựa trên trace thực tế của một lần chạy cụ thể, còn static slicing phân tích toàn bộ code.

3. **Execution Indexing dùng để làm gì?**
   - Định danh duy nhất mỗi điểm thực thi bằng `<Context, Line, Instance>` để phân biệt các lần lặp của cùng một dòng.

4. **Công thức Tarantula tính như thế nào?**
   - `Suspiciousness = failed(s)/total_failed / (passed(s)/total_passed + failed(s)/total_failed)`

### Câu Hỏi Về HWASanIO

1. **Memory Shading là gì?**
   - Mở rộng của Memory Tagging, chia metadata thành Color (định danh object) và Shade (định danh field).

2. **Tại sao HWASanIO chỉ hỗ trợ ARMv8?**
   - Cần tính năng Top-Byte Ignore (TBI) để lưu tag trong các bit cao của con trỏ mà không ảnh hưởng đến địa chỉ.

3. **Tại sao kịch bản 1 không phát hiện lỗi?**
   - Do padding giữa các field không có shade riêng, hoặc cả struct nằm chung trong một granule 16-byte.

4. **HWASanIO khác HWASan ở điểm nào?**
   - HWASanIO thêm Shade để phân biệt field, dùng 1-to-1 mapping thay vì 1-to-16, và phát hiện được intra-object overflow.

---

**Chúc bạn ôn tập tốt! 🚀**

