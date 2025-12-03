# **Chương III. Thực nghiệm** {#chương-iii.-thực-nghiệm}

## **3.1. Thiết lập** {#3.1.-thiết-lập}

### 3.1.1. Cấu hình thiết bị {#3.1.1.-cấu-hình-thiết-bị}

| Thành phần | Cấu hình được sử dụng trong tài liệu | Cấu hình thực tế nhóm sử dụng |
| :--- | :--- | :--- |
| **Thiết bị** | Google Pixel 4 | MacBook Pro (Apple Silicon M3 Pro) |
| **CPU** | Qualcomm Snapdragon 855 (ARM64) | Apple M3 Pro (ARM64) |
| **Hệ điều hành** | Android 13 | macOS Sonoma (Host) / Ubuntu 22.04 (Docker) |
| **Kiến trúc** | AArch64 (ARMv8) | AArch64 (ARMv8) |

Link bài báo gốc: https://dl.acm.org/doi/pdf/10.1145/3589250.3596139

Do HWASanIO yêu cầu kiến trúc AArch64 (ARMv8) và tính năng Top-Byte Ignore (TBI) đặc thù của phần cứng ARM, việc sử dụng MacBook M3 (dựa trên ARM) là phù hợp. Tuy nhiên, để đảm bảo tương thích với các công cụ hệ thống Linux mà dự án yêu cầu, nhóm sử dụng Docker để tạo môi trường Linux.

### 3.1.2. Môi trường phần mềm {#3.1.2.-môi-trường-phần-mềm}

Chúng tôi xây dựng một Docker image dựa trên `ubuntu:22.04` để biên dịch và chạy HWASanIO. Các thành phần chính bao gồm:

*   **Hệ điều hành:** Ubuntu 22.04 LTS (AArch64).
*   **Trình biên dịch:** Clang/LLVM 14.0.6 (phiên bản tùy chỉnh của HWASanIO).
*   **Công cụ build:** CMake, Ninja.
*   **Linker:** LLD (LLVM Linker).

### 3.1.3. Kịch bản kiểm thử {#3.1.3.-kịch-bản-kiểm-thử}

Để đánh giá toàn diện, nhóm thực hiện hai kịch bản kiểm thử khác nhau:

1.  **Kịch bản 1 (Tự xây dựng):**
    *   Mô tả: Sử dụng một `struct` đơn giản với các biến liền kề, cố tình ghi tràn từ biến này sang biến kia.
    *   Mục tiêu: Kiểm tra khả năng phát hiện lỗi trên mã nguồn thông thường chưa được tinh chỉnh.

2.  **Kịch bản 2 (Test case chuẩn):**
    *   Mô tả: Sử dụng file `test-hwasanio.c` từ repository gốc của dự án.
    *   Cấu trúc: `struct double_buffer` chứa hai mảng `buf1[16]` và `buf2[16]` được thiết kế để nằm sát nhau trong bộ nhớ.
    *   Mục tiêu: Xác minh khả năng hoạt động của công cụ trong điều kiện lý tưởng.

## **3.2. Kết quả và đánh giá** {#3.2.-kết-quả-và-đánh-giá}

### 3.2.1. Kết quả thực thi {#3.2.1.-kết-quả-thực-thi}

**Kết quả Kịch bản 1:**
Chương trình thực thi xong mà **không báo lỗi** (Exit code 0).
*   *Phân tích:* Việc này không đồng nghĩa công cụ hỏng. Nguyên nhân khả dĩ là do cơ chế **Padding** của trình biên dịch. Khi biên dịch một struct ngẫu nhiên, trình biên dịch thường chèn các byte trống (padding) giữa các biến để tối ưu hóa truy cập bộ nhớ. Nếu hành vi ghi tràn chỉ chạm vào vùng padding này (vốn không được HWASanIO gắn tag hoặc kiểm soát chặt), lỗi sẽ không bị phát hiện.

**Kết quả Kịch bản 2:**
Công cụ phát hiện lỗi chính xác và dừng chương trình ngay lập tức.
*   **Log báo lỗi:**
    ```text
    SUMMARY: HWAddressSanitizer: tag-mismatch (/workspace/mount/test-hwasanio+0x53e20) in __hwasan_store1_shade_dbg
    Exit code: 99
    ```
*   **Phân tích bộ nhớ:** Log cho thấy sự xung đột tag rõ ràng:
    *   Con trỏ đang ghi mang tag `e1` (của `buf1`).
    *   Vùng nhớ bị ghi đè mang tag `e2` (của `buf2`).
    *   Lỗi `tag-mismatch` được kích hoạt ngay khi con trỏ `e1` chạm vào vùng nhớ `e2`.

### 3.2.2. Đánh giá hiệu quả {#3.2.2.-đánh-giá-hiệu-quả}

Từ hai kết quả trái ngược trên, chúng tôi rút ra các nhận định quan trọng về HWASanIO:

1.  **Hiệu quả cao trong điều kiện chuẩn:** Với Kịch bản 2, công cụ chứng minh được khả năng cốt lõi là phát hiện lỗi tràn bộ nhớ nội đối tượng (intra-object) nhờ cơ chế Memory Shading (4 bit Color + 4 bit Shade), điều mà các công cụ cũ thường bỏ qua.
2.  **Độ nhạy với Layout bộ nhớ:** Sự thất bại của Kịch bản 1 cho thấy HWASanIO (phiên bản prototype này) khá nhạy cảm với cách bố trí bộ nhớ. Để công cụ hoạt động hiệu quả nhất, các đối tượng cần được căn chỉnh (align) sao cho không có padding "vô chủ" xen giữa, hoặc vùng padding cũng cần được gắn tag phù hợp.
3.  **Tiềm năng và Hạn chế:** Công cụ rất hứa hẹn cho việc bảo mật các cấu trúc dữ liệu quan trọng, nhưng việc áp dụng đại trà cho mọi mã nguồn C/C++ tự phát có thể gặp khó khăn do sự can thiệp của trình biên dịch (padding, optimization) làm thay đổi hành vi bộ nhớ dự kiến.

# **Chương IV. Kết luận** {#chương-iv.-kết-luận}

Báo cáo đã trình bày về HWASanIO, một kỹ thuật mới mở rộng từ HWASan nhằm phát hiện các lỗi tràn bộ nhớ nội đối tượng (intra-object overflows) - một lớp lỗi nguy hiểm mà các công cụ truyền thống thường bỏ qua. Bằng cách sử dụng cơ chế Memory Shading, kết hợp 4 bit tag màu sắc (Color) và 4 bit tag sắc thái (Shade), HWASanIO cho phép kiểm soát quyền truy cập ở mức độ mịn hơn, phân biệt được các trường dữ liệu liền kề trong cùng một cấu trúc.

Kết quả thực nghiệm cho thấy HWASanIO hoạt động chính xác trên các bộ test case chuẩn, phát hiện thành công các lỗi ghi đè giữa các biến thành viên. Tuy nhiên, thực nghiệm cũng chỉ ra thách thức trong việc áp dụng trên các mã nguồn tùy ý, nơi cơ chế padding và alignment của trình biên dịch có thể tạo ra các vùng nhớ "vô chủ", làm giảm khả năng phát hiện lỗi nếu không có sự can thiệp sâu vào quá trình biên dịch.

Tóm lại, HWASanIO là một bước tiến quan trọng trong bảo mật bộ nhớ, đặc biệt hữu ích cho các hệ thống nhúng sử dụng kiến trúc AArch64. Để công cụ trở nên phổ biến hơn, cần có những cải tiến để tự động hóa việc xử lý layout bộ nhớ, giảm thiểu yêu cầu tinh chỉnh thủ công từ phía lập trình viên.

# **Danh mục tài liệu tham khảo** {#danh-mục-tài-liệu-tham-khảo}

\[1\]	Benjamin Steenhoek, Hongyang Gao and Wei Le, “Dataflow Analysis-Inspired Deep Learning for Efficient Vulnerability Detection"

\[2\]	Zhonghao Jiang,  Weifeng Sun,  Xiaoyan Gu,  Jiaxin Wu,  Tao Wen,  Haibo Hu and  Meng Yan, "DFEPT: Data Flow Embedding for Enhancing Pre-Trained Model Based Vulnerability Detection"

\[3\]	David Hin,  Andrey Kan, Huaming Chen and  M. Ali Babar, "LineVD: Statement-level Vulnerability Detection using Graph Neural Networks"

\[4\]	Adriana Sejfia,  Satyaki Das,  Saad Shafiq and  Nenad Medvidović, "Toward Improved Deep Learning-based Vulnerability Detection"

\[5\]	Avishree Khare,  Saikat Dutta,  Ziyang Li, Alaia Solko-Breslin,  Rajeev Alur and  Mayur Naik, "Understanding the Effectiveness of Large Language Models in Detecting Security Vulnerabilities"

\[6\]	Xin-Cheng Wen , Yupan Chen , Cuiyun Gao , Hongyu Zhang, Jie M. Zhang and Qing Liao, "Vulnerability Detection with Graph Simplification and Enhanced Graph Representation Learning"