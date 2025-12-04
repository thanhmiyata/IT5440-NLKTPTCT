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

## 5. Q&A Chuyên Sâu (Code & Hướng Nghiên cứu)

**Q1: Tại sao HWASanIO lại chuyển từ ánh xạ 1-to-16 (của HWASan gốc) sang ánh xạ 1-to-1?**
*   **A:** HWASan gốc dùng 1 byte metadata cho 16 byte bộ nhớ (1-to-16) để tiết kiệm RAM. Tuy nhiên, điều này buộc các object phải được căn chỉnh (align) theo bội số 16 byte, gây lãng phí bộ nhớ padding và **phá vỡ ABI** (Application Binary Interface) khi tương tác với thư viện bên ngoài không được instrument.
*   **HWASanIO dùng 1-to-1** (1 byte metadata cho 1 byte bộ nhớ) để:
    1.  Đạt độ chính xác tuyệt đối cho từng byte, cho phép shading từng field nhỏ nhất.
    2.  Loại bỏ yêu cầu padding bắt buộc, giữ nguyên layout bộ nhớ gốc -> **Bảo toàn ABI**, tương thích tốt hơn với mã nguồn cũ (legacy code).

**Q2: Việc loại bỏ "Granule Byte" ảnh hưởng thế nào đến thuật toán kiểm tra?**
*   **A:** Trong HWASan gốc, byte cuối cùng của vùng nhớ 16-byte được gọi là "Granule Byte" để đánh dấu địa chỉ kết thúc chính xác. Logic kiểm tra phải xử lý riêng trường hợp này (rất phức tạp).
*   Do HWASanIO dùng ánh xạ 1-to-1, mỗi byte bộ nhớ đều có metadata riêng. Vì vậy, khái niệm "Granule Byte" trở nên thừa thãi và đã bị **loại bỏ hoàn toàn**. Điều này giúp đơn giản hóa logic kiểm tra trong assembly (ít lệnh hơn), bù đắp phần nào chi phí hiệu năng do việc kiểm tra thêm Shade.

**Q3: Làm thế nào Compiler biết khi nào cần gán Shade cho một con trỏ? (Instrumentation Detail)**
*   **A:** Trình biên dịch (LLVM Pass) được sửa đổi để theo dõi các lệnh **GEP (GetElementPtr)** - lệnh tính toán địa chỉ các thành phần trong struct.
*   Khi gặp lệnh GEP trỏ vào một field của struct, compiler sẽ chèn thêm code để:
    1.  Lấy Tag hiện tại của con trỏ gốc (Color).
    2.  Tính toán Shade mới dựa trên chỉ số (index) của field đó.
    3.  Gộp Color + Shade mới vào 8 bit cao của con trỏ kết quả.

**Q4: Shadow Memory được tính toán như thế nào trong HWASanIO?**
*   **A:** Địa chỉ Shadow Memory được tính bằng công thức đơn giản: `ShadowAddr = MemAddr | Mask`.
*   Cụ thể, HWASanIO sử dụng kỹ thuật **đảo bit MSB** (Most Significant Bit) của địa chỉ ảo. Ví dụ: nếu địa chỉ bộ nhớ là `0x0000...`, địa chỉ shadow tương ứng sẽ là `0x8000...` (hoặc một vùng cố định khác tùy OS). Việc này giúp chuyển đổi địa chỉ cực nhanh chỉ bằng một lệnh bitwise.

**Q5: Hạn chế lớn nhất của phương pháp "Memory Shading" này là gì? (Về mặt lý thuyết)**
*   **A:** Đó là vấn đề **Shade Collision (Xung đột Shade)** trong các **Nested Structs** (Struct lồng nhau).
*   Vì Shade chỉ có 4 bit (giá trị 0-15), thuật toán phải reset Shade về 1 khi đi vào một struct con. Nếu cấu trúc lồng nhau phức tạp (ví dụ: `struct A` chứa `struct B` chứa `char x`), có thể xảy ra trường hợp hai field nằm cạnh nhau vô tình có cùng Color và cùng Shade (do reset), khiến công cụ không phát hiện được tràn bộ nhớ giữa chúng. Đây là giới hạn toán học của việc dùng số bit ít ỏi trong con trỏ.
