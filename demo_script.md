# Kịch Bản Demo Thực Nghiệm HWASanIO

Tài liệu này hướng dẫn chi tiết các bước thực hiện demo, giải thích cơ chế hoạt động và chuẩn bị câu trả lời cho các câu hỏi phản biện từ giáo viên.

## 1. Chuẩn bị Môi trường

Trước khi bắt đầu demo, hãy đảm bảo Docker container đã chạy.

**Lệnh kiểm tra:**
```bash
docker ps
```
*Nếu container `hwasanio-runner` chưa chạy, hãy khởi động lại nó (xem file `README_DOCKER.md`).*

---

## 2. Kịch bản 1: Trường hợp KHÔNG phát hiện lỗi (`repro_issue.c`)

Đây là kịch bản mô phỏng lỗi thực tế thường gặp (tràn bộ đệm nhỏ trong struct), nhưng công cụ **không** bắt được.

### Bước 1: Show code
Mở file `repro_issue.c` và giải thích:
*   Chúng ta có `struct UserData` với `char name[10]` và `int secret_id`.
*   Mục tiêu: Ghi tràn từ `name` sang `secret_id`.
*   Code ghi 16 byte vào `name` (tràn 6 byte).

### Bước 2: Biên dịch và Chạy
Chạy lệnh sau trong terminal:
```bash
# Biên dịch
docker exec hwasanio-runner clang -fsanitize=hwaddress -fuse-ld=lld -g /workspace/mount/repro_issue.c -o /workspace/repro_issue

# Chạy
docker exec hwasanio-runner /workspace/repro_issue
```

### Bước 3: Kết quả & Giải thích
*   **Hiện tượng:** Chương trình chạy xong, in ra `Overwritten Secret ID: ...` và **Exit Code 0** (Không crash).
*   **Giải thích (Cho thầy giáo):**
    *   **Vấn đề Granularity (Độ mịn):** HWASan hoạt động dựa trên việc gắn tag cho mỗi **16 byte** bộ nhớ (granule).
    *   **Memory Layout:** Struct `UserData` có kích thước nhỏ (`name` 10 byte + padding + `secret_id` 4 byte ≈ 16 byte).
    *   **Nguyên nhân:** Do `name` và `secret_id` nằm chung trong một granule 16-byte (hoặc vùng padding giữa chúng không đủ lớn để tách sang granule mới), chúng buộc phải chia sẻ cùng một Tag. Khi ghi tràn từ `name` sang `secret_id`, tag vẫn khớp nên HWASanIO không phát hiện ra sự vi phạm.
    *   **Kết luận:** Đây là hạn chế phần cứng của kỹ thuật Memory Tagging hiện tại.

---

## 3. Kịch bản 2: Trường hợp PHÁT HIỆN lỗi (`test-hwasanio.c`)

Đây là kịch bản lý tưởng ("Happy Path") mà HWASanIO được thiết kế để xử lý.

### Bước 1: Show code
Mở file `hwasanio_repo/example/test-hwasanio.c` (hoặc file bạn đã copy ra):
*   Struct `double_buffer` gồm 2 mảng `buf1[16]` và `buf2[16]`.
*   Kích thước 16 byte là "con số vàng" vì nó khớp hoàn hảo với kích thước granule của HWASan.

### Bước 2: Biên dịch và Chạy
```bash
# Biên dịch
docker exec hwasanio-runner clang -fsanitize=hwaddress -fuse-ld=lld -g /workspace/mount/hwasanio_repo/example/test-hwasanio.c -o /workspace/test-hwasanio

# Chạy (tham số 0 để chọn test case intra-object overflow)
docker exec hwasanio-runner /workspace/test-hwasanio 0
```

### Bước 3: Kết quả & Giải thích
*   **Hiện tượng:** Chương trình **CRASH** ngay lập tức.
*   **Log:** Xuất hiện thông báo đỏ lòm:
    ```text
    ERROR: HWAddressSanitizer: tag-mismatch on address ...
    ...
    Intra-Object Violation
    ```
*   **Giải thích (Cho thầy giáo):**
    *   **Cơ chế Memory Shading:** Ở đây, `buf1` chiếm trọn 1 granule (16 byte) và `buf2` chiếm trọn granule tiếp theo.
    *   **Gán Tag:** HWASanIO đã gán cho `buf1` một **Shade** (ví dụ: 1) và `buf2` một **Shade** khác (ví dụ: 2).
    *   **Phát hiện:** Khi vòng lặp ghi vượt quá `buf1[15]` sang `buf2[0]`, con trỏ vẫn mang tag của `buf1` (Shade 1) nhưng lại truy cập vào vùng nhớ của `buf2` (Shade 2). Sự lệch pha này (`tag-mismatch`) kích hoạt báo lỗi.

---

## 4. Ứng dụng Thực tế Chuyên Sâu

Bài toán này giải quyết vấn đề cốt lõi trong bảo mật phần mềm hệ thống viết bằng C/C++, nơi mà **90% biến phức tạp là struct/class**.

1.  **Xử lý Đa phương tiện (Multimedia Parsing):**
    *   Các thư viện xử lý ảnh/video (như `libjpeg`, `ffmpeg`) sử dụng dày đặc các `struct` để định nghĩa header file, frame data.
    *   **Nguy cơ:** Hacker có thể chèn file ảnh độc hại gây tràn bộ nhớ từ trường `width` sang trường `buffer_pointer` trong cùng một struct, điều hướng con trỏ ghi đè lên vùng nhớ thực thi mã (RCE). HWASanIO ngăn chặn điều này bằng cách gán Shade khác nhau cho `width` và `buffer_pointer`.

2.  **Giao thức Mạng (Network Protocol Stacks):**
    *   Trong kernel hoặc các thư viện mạng (như `OpenSSL`, `lwIP`), các gói tin (packet) thường được map vào các `struct` phức tạp.
    *   **Nguy cơ:** Lỗ hổng Heartbleed là ví dụ điển hình của việc đọc quá giới hạn. Với intra-object overflow, kẻ tấn công có thể ghi đè các cờ trạng thái (flags) hoặc độ dài (length) nằm kề nhau trong struct quản lý session, dẫn đến leo thang đặc quyền hoặc rò rỉ dữ liệu.

3.  **Trình duyệt Web (Web Browsers):**
    *   DOM tree trong Chrome/Firefox được biểu diễn bằng hàng triệu object C++ liên kết với nhau.
    *   **Nguy cơ:** Use-after-free và overflow trong các object này là vector tấn công phổ biến nhất. HWASanIO giúp phát hiện sớm các lỗi memory corruption tinh vi trong quá trình fuzzing engine render (Blink/Gecko).

---

## 5. Tối ưu hóa & Hướng Phát triển Tương lai (Research Directions)

Dựa trên phân tích từ bài báo gốc (Section 8.2), hệ thống hiện tại có thể được tối ưu hóa theo các hướng sau:

### a. Tối ưu Hiệu năng (Performance Optimization)
*   **Vấn đề:** HWASanIO chậm hơn HWASan gốc khoảng 10% (trung bình hình học) nhưng có thể chậm hơn tới 90% trong các trường hợp đặc biệt (như benchmark `511.povray`). Nguyên nhân là do việc gọi hàm shading liên tục cho từng field mỗi khi cấp phát một struct lớn (ví dụ struct có 26 field).
*   **Giải pháp Đề xuất:** **"Static Shading Layout Pre-calculation"** (Tính toán trước bố cục Shading tĩnh).
    *   Thay vì tính toán và gán shade động cho từng field lúc runtime (chạy chương trình), trình biên dịch có thể tính toán trước toàn bộ "bản đồ shade" cho struct đó ngay lúc compile.
    *   Khi cấp phát struct, chỉ cần `memcpy` (copy nhanh) bản đồ shade này vào Shadow Memory một lần duy nhất. Điều này sẽ giảm thiểu đáng kể overhead cho các struct phức tạp.

### b. Tối ưu Bộ nhớ (Memory Optimization)
*   **Vấn đề:** Overhead bộ nhớ của HWASanIO rất cao (~136%) do sử dụng ánh xạ 1-to-1 (1 byte metadata cho 1 byte dữ liệu).
*   **Giải pháp Đề xuất:** Nghiên cứu các cơ chế **"Adaptive Mapping"** (Ánh xạ thích ứng).
    *   Chỉ sử dụng ánh xạ 1-to-1 cho các vùng nhớ chứa struct (nơi cần shading).
    *   Giữ nguyên ánh xạ 1-to-16 (tiết kiệm hơn) cho các mảng lớn (arrays) hoặc vùng nhớ không định kiểu (void*), nơi mà shading không thực sự cần thiết hoặc hiệu quả thấp. Điều này đòi hỏi sự hỗ trợ phức tạp hơn từ phần cứng hoặc OS để quản lý các vùng nhớ hỗn hợp.

### c. Mở rộng Kiến trúc (Architecture Support)
*   **Hướng đi:** Hiện tại chỉ hỗ trợ ARMv8 với TBI (Top Byte Ignore).
*   **Tương lai:** Porting sang **RISC-V** (với tính năng Pointer Masking sắp tới) hoặc **Intel x86_64** (sử dụng Linear Address Masking - LAM). Việc hỗ trợ đa nền tảng sẽ mở rộng khả năng ứng dụng thực tế của công cụ.

---

## 6. Q&A Chuyên Sâu (Code & Hướng Nghiên cứu)

**Q1: Tại sao HWASanIO lại chuyển từ ánh xạ 1-to-16 (của HWASan gốc) sang ánh xạ 1-to-1?**
*   **A:** Hãy tưởng tượng bộ nhớ như một cuốn vở ô ly.
    *   **HWASan gốc (1-to-16):** Dùng 1 cái nhãn dán cho cả một dòng 16 ô. Nếu bạn chỉ viết 10 chữ cái, 6 ô còn lại bị bỏ trống (lãng phí) nhưng vẫn phải dán chung nhãn đó. Điều này giống như bắt buộc mọi từ phải dài đúng 16 chữ cái, rất cứng nhắc.
    *   **HWASanIO (1-to-1):** Dùng 1 cái nhãn nhỏ cho **từng ô một**. Bạn viết đến đâu dán nhãn đến đó. Điều này giúp tiết kiệm chỗ trống (không cần padding) và giữ nguyên cách viết văn bản gốc (tương thích ABI), không bắt buộc phải cách dòng hay chừa chỗ trống vô lý.

**Q2: Việc loại bỏ "Granule Byte" ảnh hưởng thế nào đến thuật toán kiểm tra?**
*   **A:**
    *   Trong HWASan cũ, vì nhãn dán cho cả dòng 16 ô, nên cần một ký hiệu đặc biệt (Granule Byte) ở cuối để biết chính xác chữ dừng lại ở ô thứ mấy. Việc kiểm tra ký hiệu này giống như phải đếm thủ công từng ô mỗi khi đọc, rất rắc rối.
    *   Với HWASanIO, vì mỗi ô đã có nhãn riêng (Shade), ta biết ngay ô nào thuộc về từ nào. Không cần ký hiệu đặc biệt nữa. Việc kiểm tra trở nên đơn giản hơn: "Nhìn nhãn là biết ngay", giúp máy tính xử lý nhanh hơn (ít lệnh assembly hơn).

**Q3: Làm thế nào Compiler biết khi nào cần gán Shade cho một con trỏ? (Instrumentation Detail)**
*   **A:** Trình biên dịch giống như một người biên tập viên kỹ tính.
    *   Nó sẽ soi từng dòng code, đặc biệt là các lệnh tính toán địa chỉ (như `GEP` - GetElementPtr).
    *   Khi thấy bạn định truy cập vào một "trường con" (field) trong một struct (ví dụ: `user->name`), nó sẽ tự động chèn thêm một lệnh ngầm: "Lấy cái thẻ ID của `user` (Color), rồi đóng thêm dấu mộc phụ (Shade) tương ứng với trường `name` vào". Kết quả là con trỏ mới sẽ mang cả ID của cha và dấu mộc của con.

**Q4: Shadow Memory được tính toán như thế nào trong HWASanIO?**
*   **A:** Shadow Memory giống như một "bản sao song song" của bộ nhớ chính.
    *   Để tìm bản sao của một địa chỉ, HWASanIO dùng một mẹo cực nhanh: **Lật ngược bit đầu tiên** (MSB).
    *   Ví dụ: Nếu nhà bạn ở địa chỉ `0x0...` (Khu A), thì hồ sơ quản lý nhà bạn sẽ nằm chính xác ở địa chỉ `0x8...` (Khu B). Máy tính chỉ cần đổi chữ số đầu tiên là tìm ra ngay hồ sơ quản lý (Shadow Memory) mà không cần tra cứu danh bạ phức tạp.

**Q5: Hạn chế lớn nhất của phương pháp "Memory Shading" này là gì? (Về mặt lý thuyết)**
*   **A:** Đó là vấn đề **"Hết màu để tô"** trong các cấu trúc lồng nhau quá sâu (Nested Structs).
*   Vì "dấu mộc phụ" (Shade) chỉ có 4 bit (tức là chỉ có 16 kiểu dấu khác nhau). Khi đi vào một struct con nằm trong struct mẹ, ta phải reset lại bộ đếm dấu từ 1.
*   Nếu cấu trúc quá phức tạp (Mẹ chứa Con, Con chứa Cháu...), có thể xảy ra tình huống: Chú của Cháu (nằm cạnh Cháu) và Cháu vô tình có cùng ID và cùng dấu mộc. Lúc này nếu Cháu lấn đất sang nhà Chú, công cụ sẽ không phát hiện được vì thấy "giấy tờ hợp lệ". Đây là giới hạn toán học không thể tránh khỏi khi số lượng bit trong con trỏ có hạn.
