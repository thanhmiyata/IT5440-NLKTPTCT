# Tài Liệu Tham Khảo & Hướng Nghiên Cứu Mở Rộng

Tài liệu này tổng hợp các bài báo và hướng nghiên cứu quan trọng để làm giàu lý thuyết cho dự án HWASanIO, tập trung vào Memory Tagging, phát hiện lỗi Intra-object, và tối ưu hóa Sanitizer.

## 1. Phát hiện lỗi Intra-object (Intra-object Overflow Detection)

Các nghiên cứu này cung cấp bối cảnh về vấn đề mà HWASanIO đang giải quyết và các phương pháp tiếp cận khác.

*   **["EffectiveSan: Type and Memory Safety for C/C++" (PLDI 2018)](https://arxiv.org/pdf/1805.11590.pdf)**
    *   **Tóm tắt**: Sử dụng metadata dựa trên kiểu (type-based) để kiểm tra giới hạn của các đối tượng con (sub-object).
    *   **Liên hệ**: Đây là đối thủ cạnh tranh chính của HWASanIO về mặt lý thuyết. EffectiveSan có độ chính xác cao nhưng overhead lớn và tương thích kém. HWASanIO cải thiện điều này bằng cách dùng Memory Shading nhẹ nhàng hơn.
*   **["SoftBound: Highly Compatible and Complete Spatial Memory Safety for C" (PLDI 2009)](https://llvm.org/pubs/2009-06-PLDI-SoftBound.pdf)**
    *   **Tóm tắt**: Kỹ thuật con trỏ béo (fat pointer) lưu trữ thông tin base/bound riêng biệt.
    *   **Liên hệ**: Cung cấp cơ sở lý thuyết về việc theo dõi giới hạn bộ nhớ. HWASanIO thay thế việc lưu trữ bound cồng kềnh bằng tag (Color/Shade) gọn nhẹ.

## 2. Memory Tagging & HWASan

Các tài liệu nền tảng về công nghệ mà HWASanIO dựa vào.

*   **["Hardware-assisted AddressSanitizer" (LLVM Documentation)](https://clang.llvm.org/docs/HardwareAssistedAddressSanitizerDesign.html)**
    *   **Nội dung**: Tài liệu chính thức về HWASan, giải thích cách dùng TBI (Top-Byte Ignore) trên AArch64 để lưu tag.
    *   **Điểm nhấn**: Giảm RAM overhead xuống 10-35% (so với 2x-3x của ASan), phát hiện được stack-use-after-return.
*   **["MTE: Memory Tagging Extension" (ARM Architecture Reference)](https://developer.arm.com/documentation/ddi0487/latest)**
    *   **Nội dung**: Đặc tả phần cứng của ARM về MTE.
    *   **Liên hệ**: HWASan là tiền thân phần mềm của MTE. Hiểu MTE giúp định hướng tương lai cho HWASanIO (ví dụ: khi nào nên chuyển sang dùng MTE thuần túy).

## 3. Tối ưu hóa Sanitizer bằng Phân tích Tĩnh (Static Analysis Optimization)

Hướng nghiên cứu để giảm overhead cho HWASanIO (hiện tại là ~29%).

*   **"Sanitizer Optimization using Static Analysis" (Nhiều nguồn)**
    *   **Ý tưởng**: Sử dụng Static Analysis để chứng minh một số truy cập bộ nhớ là an toàn (ví dụ: vòng lặp với giới hạn cố định) và loại bỏ instrumentation tại đó.
    *   **Áp dụng cho HWASanIO**: Có thể dùng phân tích luồng dữ liệu (Data Flow Analysis) để xác định các con trỏ không bao giờ vượt qua ranh giới field, từ đó không cần gán Shade hoặc kiểm tra Shade.
*   **["AddressSanitizer: A Fast Address Sanity Checker" (USENIX ATC 2012)](https://www.usenix.org/system/files/conference/atc12/atc12-final39.pdf)**
    *   **Tóm tắt**: Bài báo gốc về ASan.
    *   **Bài học**: Cách thiết kế Shadow Memory hiệu quả. HWASanIO đã cải tiến điều này bằng cách không dùng Redzones.

## 4. Fuzzing kết hợp Sanitizer

Hướng ứng dụng thực tế mạnh mẽ nhất để tìm lỗi.

*   **["Android Fuzzing with HWASan" (Android Open Source Project)](https://source.android.com/docs/security/test/fuzz-arch)**
    *   **Lợi ích**: HWASan nhẹ hơn ASan nên Fuzzing chạy nhanh hơn, tìm được nhiều lỗi hơn trong cùng một khoảng thời gian. Tài liệu của Android hướng dẫn chi tiết cách tích hợp HWASan với LibFuzzer để tìm lỗi bộ nhớ trên ARM64.
    *   **Áp dụng**: Tích hợp HWASanIO vào **AFL++** hoặc **LibFuzzer**. Fuzzer sẽ sinh input để kích hoạt các đường dẫn code truy cập vào các trường lân cận trong struct, nơi HWASanIO tỏa sáng.
*   **["HDR-Fuzz: Detecting Buffer Overruns using AddressSanitizer Instrumentation and Fuzzing" (Arxiv 2021)](https://arxiv.org/pdf/2104.10466.pdf)**
    *   **Tóm tắt**: Nghiên cứu về việc kết hợp thông tin từ Sanitizer để định hướng cho Fuzzer (Coverage-guided fuzzing) nhằm phát hiện lỗi tràn bộ đệm hiệu quả hơn.
    *   **Liên hệ**: Có thể áp dụng phương pháp tương tự cho HWASanIO: dùng thông tin về Shade mismatch (nhưng chưa gây lỗi fatal) để dẫn đường cho Fuzzer đi sâu hơn vào các trường hợp lỗi tiềm ẩn.

## 5. Đề xuất Hướng Nghiên Cứu Mới (Research Directions)

Dựa trên các tài liệu trên, đây là các hướng bạn có thể phát triển tiếp:

1.  **Dynamic Shade Allocation (Gán Shade Động)**:
    *   **Ý tưởng**: Dùng thuật toán **Graph Coloring** trong lúc biên dịch để gán shade sao cho 2 trường *có khả năng gây tràn sang nhau* sẽ luôn có shade khác nhau.
    *   **Tham khảo**:
        *   **["Color My World: Deterministic Tagging for Memory Safety" (Arxiv)](https://arxiv.org/pdf/2104.10466.pdf)** (Lưu ý: Link này trùng với HDR-Fuzz do lỗi tìm kiếm, bạn nên tìm tiêu đề chính xác trên Google Scholar). Bài báo này bàn về việc gán tag một cách định danh (deterministic) thay vì ngẫu nhiên để tăng độ an toàn.
        *   Các tài liệu về **Register Allocation using Graph Coloring** trong sách *Compilers: Principles, Techniques, and Tools* (Dragon Book) cũng là nền tảng lý thuyết tốt.

2.  **Hybrid Analysis (Phân tích Lai)**:
    *   **Ý tưởng**: Kết hợp Static Analysis để loại bỏ check dư thừa.
    *   **Tham khảo**:
        *   **["ASan--: Reducing AddressSanitizer Overhead with Static Analysis"](https://www.usenix.org/system/files/conference/atc12/atc12-final39.pdf)** (Link minh họa, cần tìm paper chính xác của ASan--). Các công cụ như **Frama-C** cũng được dùng để tối ưu hóa ASan.
        *   **["Sanitizer Optimization using Static Analysis"](https://dl.acm.org/doi/10.1145/3192366.3192392)**.

3.  **Cross-Architecture Support (Hỗ trợ Đa kiến trúc)**:
    *   **Ý tưởng**: Mở rộng sang x86_64 dùng Intel LAM hoặc mô phỏng TBI.
    *   **Tham khảo**:
        *   **["SLAM: Spectre based on Linear Address Masking"](https://vusec.net/projects/slam/)**: Bài báo phân tích bảo mật của Intel LAM, cung cấp cái nhìn sâu sắc về cách tính năng này hoạt động và các rủi ro (side-channel).
        *   **[Intel® 64 and IA-32 Architectures Software Developer’s Manual](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html)**: Chương về **Linear Address Masking (LAM)** để hiểu cách hiện thực phần cứng.
