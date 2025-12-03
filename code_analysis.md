# Phân Tích Mã Nguồn HWASanIO (Static Analysis)

Do hạn chế về môi trường build (yêu cầu Linux/ARMv8 và compiler-rt), tôi đã tiến hành phân tích tĩnh mã nguồn để làm rõ cơ chế hoạt động.

## 1. Cơ chế Memory Shading trong Code

### Cấu trúc Metadata
Dựa trên `hwasan_checks.h`, metadata (tag) 8-bit được chia làm 2 phần:
```cpp
tag_t ptr_tag = metadata & 0xf0;   // Color (4 bit cao) - Định danh đối tượng
tag_t ptr_shade = metadata & 0x0f; // Shade (4 bit thấp) - Định danh trường (field)
```

### Logic Kiểm tra (Runtime Check)
Hàm `PossiblyShortTagShadeMatches` trong `hwasan_checks.h` thực hiện kiểm tra như sau:
1.  **So sánh Color**: `ptr_tag == mem_tag`. Nếu sai -> Lỗi Inter-object overflow (tràn sang đối tượng khác).
2.  **So sánh Shade**: Nếu Color đúng, kiểm tra tiếp Shade:
    *   `ptr_shade == 0x0`: Con trỏ không có shade (ví dụ: con trỏ `void*` hoặc trỏ tới object thường). Hợp lệ.
    *   `mem_shade == 0x0`: Bộ nhớ không có shade (object thường). Hợp lệ.
    *   `ptr_shade == mem_shade`: Shade khớp. Hợp lệ.
    *   Ngược lại -> **Lỗi Intra-object overflow**.

### Instrumentation (Chèn mã)
Trong `HWAddressSanitizer.cpp`:
*   **Gán Shade**: Hàm `memToShade` và `shadeAlloca` chịu trách nhiệm tính toán và gán shade cho các biến.
*   **Xoay vòng Shade**: `shade = shade % (maxShadeSize)` (với `maxShadeSize = 15`). Điều này xác nhận việc tái sử dụng giá trị shade nếu struct có nhiều hơn 15 trường.
*   **Reshade**: Hàm `reshadePointer` cập nhật tag của con trỏ khi nó trỏ vào một trường cụ thể của struct.

## 2. Đánh giá & Ý tưởng Cải tiến

### Điểm mạnh
*   **Tương thích**: Logic kiểm tra `0x0` cho phép HWASanIO hoạt động chung với mã không được instrument (uninstrumented code) hoặc các object không phải struct mà không gây báo lỗi giả (false positive).
*   **Hiệu quả**: Sử dụng phép toán bit (`&`, `==`) rất nhanh, giảm thiểu overhead.

### Điểm yếu & Thách thức
*   **Giới hạn 4-bit**: Chỉ phân biệt được 15 trường liền kề. Nếu struct lớn và có các trường cùng kiểu nằm xa nhau nhưng trùng shade (do modulo), lỗi tràn có thể bị bỏ qua (False Negative).
*   **x86_64 Support**: Code có hỗ trợ `__x86_64__` nhưng phải dùng `UntagAddr(ptr)` để gỡ tag thủ công trước khi truy cập bộ nhớ (do x86_64 chưa có TBI phần cứng như ARMv8). Điều này làm tăng overhead đáng kể trên PC thường.

### Đề xuất Cải tiến (Improvements)
1.  **Dynamic Shade Allocation**: Thay vì gán shade tĩnh (1, 2, 3...), có thể dùng thuật toán tô màu đồ thị (graph coloring) lúc biên dịch để gán shade sao cho các trường *có khả năng bị tràn sang nhau* sẽ luôn có shade khác nhau, giảm thiểu rủi ro trùng lặp do modulo.
2.  **Hybrid Analysis**: Kết hợp Static Analysis để loại bỏ check ở những nơi chứng minh được là an toàn (ví dụ: truy cập qua index hằng số trong vòng lặp giới hạn).
3.  **Fuzzing Integration**: Tích hợp với **AFL++** hoặc **LibFuzzer**. Sử dụng chế độ `fork` server của fuzzer để tăng tốc độ test trên HWASanIO. Fuzzer sẽ sinh input dị biệt để cố gắng kích hoạt các đường dẫn code truy cập vào ranh giới các trường của struct.
