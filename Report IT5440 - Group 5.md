**ĐẠI HỌC BÁCH KHOA HÀ NỘI**

**TRƯỜNG CÔNG NGHỆ THÔNG TIN VÀ TRUYỀN THÔNG**

**\---o0o---**

![Ảnh có chứa văn bản, áp phích, Phông chữ, biểu tượngMô tả được tạo tự động][image1]

**HWASanIO: Detecting C/C++ Intra-object Over-ows with Memory Shading**

Môn học: IT5440 \- Nguyên lý và kỹ thuật phân tích chương trình

GVHD: PGS.TS. Huỳnh Quyết Thắng

Nhóm học viên: Nhóm 5

| STT | Mã SV | Họ Tên |
| :---: | :---: | :---: |
| 1 | 20242123M | Lưu Thị Hạnh |
| 2 | 20242422M | Phạm Tiến Thành |
| 3 | 20242036M | Vương Thị Giang |
| 4 | 20251184M | Phan Thị Thanh Hương |
| 5 | 20242179M | Nguyễn Dương Kỳ Anh |

**Hà Nội, 12/2025**

# **Lời cảm ơn** {#lời-cảm-ơn}

Kính gửi PGS.TS. Huỳnh Quyết Thắng,

Chúng em là các học viên Nhóm 5, thực hiện báo cáo tiểu luận với đề tài "HWASanIO: Detecting C/C++ Intra-object Over-ows with Memory Shading". Báo cáo này được xây dựng dựa trên sự hướng dẫn tận tình của Thầy, sự nỗ lực của toàn bộ thành viên nhóm, cùng với việc tham khảo các tài liệu khoa học và nguồn thông tin uy tín.

Trước tiên, nhóm xin bày tỏ lòng biết ơn sâu sắc đến Thầy, người đã tận tình hướng dẫn, hỗ trợ và cung cấp những gợi ý quý báu trong suốt quá trình học tập, nghiên cứu và hoàn thiện bài báo cáo này.

Nhằm đảm bảo tính khoa học, đạo đức trong học thuật, chúng em xin cam kết rằng:

* Báo cáo này là kết quả của sự nghiên cứu và làm việc nghiêm túc của tất cả thành viên trong nhóm.  
* Mọi nội dung trong báo cáo đều trung thực, không sao chép hoặc vi phạm bản quyền của bất kỳ cá nhân hay tổ chức nào.  
* Các tài liệu tham khảo đều được trích dẫn chính xác và đầy đủ theo quy định.  
* Nhóm cam kết chịu hoàn toàn trách nhiệm nếu có bất kỳ hành vi vi phạm nào liên quan đến tính trung thực của báo cáo này.

Chúng em hy vọng báo cáo này sẽ đạt được những tiêu chuẩn cần thiết, góp phần bổ sung kiến thức hữu ích và đáp ứng kỳ vọng của Thầy trong quá trình đánh giá.

Trân trọng cảm ơn Thầy\!

*Hà Nội, ngày 02 tháng 12 năm 2025*

# 

# **Mục lục** {#mục-lục}

[Lời cảm ơn	1](#lời-cảm-ơn)

[Mục lục	2](#mục-lục)

[Danh mục hình ảnh	5](#danh-mục-hình-ảnh)

[Danh mục bảng biểu	6](#danh-mục-bảng-biểu)

[Danh mục từ viết tắt	7](#danh-mục-từ-viết-tắt)

[Giới thiệu	8](#giới-thiệu)

[Chương I. Phương pháp nghiên cứu	10](#chương-i.-phương-pháp-nghiên-cứu)

[1.1. Nghiên cứu tài liệu tham khảo chính	10](#1.1.-nghiên-cứu-tài-liệu-tham-khảo-chính)

[1.2. Xác định từ khóa chính cho nghiên cứu	10](#1.2.-xác-định-từ-khóa-chính-cho-nghiên-cứu)

[1.3. Tìm kiếm, nghiên cứu các tài liệu tham khảo khác	10](#1.3.-tìm-kiếm,-nghiên-cứu-các-tài-liệu-tham-khảo-khác)

[1.4. Xây dựng và chạy thử nghiệm	12](#1.4.-xây-dựng-và-chạy-thử-nghiệm)

[1.5. Đánh giá hiệu quả mô hình	12](#1.5.-đánh-giá-hiệu-quả)

[Chương II. Tổng quan lý thuyết	13](#chương-ii.-tổng-quan-lý-thuyết)

[2.1. Semantics/Dataflow Patterns và Loop Invariants	13](#2.1.-memory-safety)

[2.1.1. Semantics và Dataflow Patterns	13](#heading=h.dv4sdnmuyzxo)

[2.1.2. Loop Invariants	13](#heading=h.gvj1abq51yj2)

[2.2. Graph Learning trong Control Flow Graph (CFG)	14](#heading=h.pcqtyrr2sxe7)

[2.2.1. Control Flow Graph (CFG)	14](#heading=h.sjzax3lgncwm)

[2.2.2. Graph Learning và ứng dụng trong CFG	15](#heading=h.wof9ar2kwscr)

[2.3. Dataflow Analysis \- DFA	15](#2.3.-memory-tagging-và-hwasan)

[2.3.1. Vai trò của DFA trong phát hiện lỗ hổng chương trình	15](#heading=h.6fvy2age2xnp)

[2.3.2. Sự tương tự giữa DFA và Graph Learning	16](#heading=h.md8dc7srmwnz)

[2.4. Abstract Dataflow Embedding	17](#2.4.-memory-shading)

[2.4.1. Xây dựng từ điển cho các thuộc tính	18](#heading=h.tkfsplvm029)

[2.4.2. Trích xuất thuộc tính	18](#heading=h.d7ib9ndvjm9b)

[2.4.3. Tạo ra nhúng luồng dữ liệu	18](#heading=h.hjdnveo654rn)

[2.5. Deep Learning	19](#2.5.-state-of-the-art-memory-safety-approaches)

[2.6. DeepDFA Framework	20](#heading=h.5eoxu12ke12p)

[2.6.1. Trích xuất luồng dữ liệu qua CFG (Control Flow Graph)	21](#heading=h.g43eda23kmrv)

[2.6.2. Ánh xạ dữ liệu bằng Abstract Dataflow Embedding	21](#heading=h.bfp3vonv2y7q)

[2.6.3. Truyền và phân tích thông tin luồng dữ liệu qua GNNs	21](#heading=h.tweed9ewzdex)

[2.6.4. Tối ưu hóa hiệu suất và tài nguyên	21](#heading=h.n3jw9dpzom5u)

[2.7. State-of-the-art Vulnerability Detection	22](#heading=h.fdkomodaf57)

[2.7.1. Một số phương pháp phổ biến	22](#2.5.1.-một-số-phương-pháp-phổ-biến)

[2.7.2. So sánh	23](#2.5.2.-so-sánh)

[2.7.3. Đánh giá hiệu suất của các phương pháp trên bộ dữ liệu chuẩn	24](#heading=h.1zza4w3ej80e)

[2.7.4. Những hạn chế	24](#heading=h.t021e3t73fcd)

[Chương III. Thực nghiệm	25](#chương-iii.-thực-nghiệm)

[3.1. Thiết lập	25](#3.1.-thiết-lập)

[3.1.1. Cấu hình thiết bị	25](#3.1.1.-cấu-hình-thiết-bị)

[3.1.2. Tập dữ liệu	25](#3.1.2.-môi-trường-phần-mềm)

[3.2. Kết quả và đánh giá	25](#3.2.-kết-quả-và-đánh-giá)

[3.2.1. Hiệu quả của mô hình	25](#3.2.1.-kết-quả-thực-thi)

[3.2.2. Hiệu quả tài nguyên tính toán	28](#3.2.2.-đánh-giá-hiệu-quả)

[3.2.3. Hiệu quả trên các tập dữ liệu huấn luyện	30](#heading=h.i1myfce589dy)

[Chương IV. Kết luận	32](#chương-iv.-kết-luận)

[Danh mục tài liệu tham khảo	33](#danh-mục-tài-liệu-tham-khảo)

# **Danh mục hình ảnh** {#danh-mục-hình-ảnh}

| Hình 2.1. Một số ví dụ trực quan về CFG | 14 |
| ----- | ----- |
| Hình 2.2. Sự tương tự của việc truyền bá thông tin trong DFA và Graph Learning | 17 |
| Hình 2.3. Tổng quan quy trình Abstract Dataflow Embedding | 17 |
| Hình 2.4. Ví dụ về mạng Neuron trong Deep Learning | 19 |
| Hình 2.5. Tổng quan cách DeepDFA hoạt động | 20 |
|  |  |
|  |  |
|  |  |

# **Danh mục bảng biểu** {#danh-mục-bảng-biểu}

| Bảng 2.1. So sánh các phương pháp phát hiện lỗ hổng | 23 |
| :---- | ----: |
| Bảng 3.1. Cấu hình sử dụng để thí nghiệm các mô hình | 25 |
| Bảng 3.2. So sánh DeepDFA với các model non-transformer | 26 |
| Bảng 3.3. So sánh DeepDFA với các model transformer | 27 |
| Bảng 3.4. Tiêu tốn tài nguyên khi train các mô hình | 29 |
| Bảng 3.5. Hiệu quả các mô hình trên tập dữ liệu giới hạn | 30 |
|  |  |
|  |  |

# **Danh mục từ viết tắt** {#danh-mục-từ-viết-tắt}

**DFA** – Dataflow Analysis: Phân tích luồng dữ liệu

**GNNs** – Graph Neural Networks: Mạng nơ-ron đồ thị

**CFG** – Control Flow Graph: Đồ thị luồng điều khiển

**API** – Application Programming Interface: Giao diện lập trình ứng dụng

**CVE** – Common Vulnerability Enumeration: Phân loại lỗ hổng bảo mật phổ biến

**DeepDFA** – Deep Learning-based Dataflow Analysis: Phân tích luồng dữ liệu dựa trên học sâu

# **Giới thiệu** {#giới-thiệu}

Các lỗ hổng bộ nhớ trong C/C++ đang là một trong những mối đe dọa bảo mật nghiêm trọng nhất, gây ảnh hưởng trực tiếp đến an toàn của phần mềm và hệ thống nền tảng. Theo danh sách MITRE CWE Top 25 năm 2022\[1\], các lỗi liên quan đến thao tác bộ nhớ như *out-of-bounds write/read* hay *use-after-free* nằm ở các vị trí hàng đầu trong những dạng lỗi nguy hiểm nhất, là nguồn gốc của nhiều khai thác bảo mật nghiêm trọng trong thực tế. Điều này đặc biệt đáng lo ngại khi C/C++ vẫn là lựa chọn chủ đạo cho các hệ thống hiệu năng cao, bao gồm trình duyệt, hệ điều hành và thư viện phần mềm lõi.

Các phương pháp phát hiện lỗi bộ nhớ truyền thống dựa trên static hoặc dynamic analysis đã mang lại hiệu quả nhất định, nhưng vẫn tồn tại hạn chế trong việc xử lý các vi phạm tinh vi xảy ra bên trong đối tượng. Các kỹ thuật tiên tiến như AddressSanitizer hoặc HWASan sử dụng memory tagging để phát hiện sai phạm truy cập bộ nhớ giữa các đối tượng, tuy nhiên vẫn không thể phát hiện các lỗi intra-object overflow hoặc sub-object overflow, tức là tràn bộ nhớ giữa các field của cùng một struct hoặc class — vốn là loại lỗi có khả năng gây ra các hành vi chạy sai hoặc bị khai thác để chiếm quyền điều khiển.

Để khắc phục những hạn chế trên, nghiên cứu này đã đề xuất HWASanIO, một công cụ dựa trên HWASan, áp dụng khái niệm tạo bóng bộ nhớ (memory shading) cho cơ chế gắn thẻ bộ nhớ (memory tagging) — một cải tiến của memory tagging — cho phép phân biệt không chỉ giữa các đối tượng khác nhau, mà còn giữa từng trường dữ liệu bên trong một đối tượng. Bằng việc gắn thêm “shade” vào metadata để nhận diện sub-object, công nghệ này nâng cao đáng kể khả năng phát hiện các vi phạm bộ nhớ tinh vi mà các phương pháp truyền thống bỏ sót. Việc triển khai prototype HWASanIO đã cho thấy hiệu quả vượt trội, đạt mức phát hiện lỗi 100% trong bộ kiểm thử Juliet Test Suite, đồng thời vẫn duy trì khả năng tương thích cao với code C/C++ hiện hành mà không phá vỡ ABI của hệ thống.

Phần tiếp theo của báo cáo sẽ đi sâu vào từng nội dung, nhằm làm rõ các lý thuyết được sử dụng trong báo cáo, các bước trong quy trình phân tích đề tài, triển khai kiểm thử và đánh giá kết quả, bao gồm:

1. Chương 1: Phương pháp nghiên cứu  
2. Chương 2: Tổng quan lý thuyết  
3. Chương 3: Thực nghiệm  
4. Chương 4: Kết luận

Nghiên cứu này đóng góp một số kết quả thực nghiệm của các giải pháp phát hiện lỗ hổng bảo mật tiên tiến và tạo tiền đề cho các nghiên cứu mới về việc kết hợp các kỹ thuật phân tích truyền thống với học sâu để xử lý các vấn đề phức tạp trong lập trình.

# **Chương I. Phương pháp nghiên cứu** {#chương-i.-phương-pháp-nghiên-cứu}

## **1.1. Nghiên cứu tài liệu tham khảo chính** {#1.1.-nghiên-cứu-tài-liệu-tham-khảo-chính}

Tài liệu tham khảo chính của báo cáo này là “HWASanIO: Detecting C/C++ Intra-object Overows with Memory Shading”. Tổng quan, tài liệu tập trung giới thiệu cách tiếp cận cải tiến trong việc đảm bảo an toàn bộ nhớ thông qua kỹ thuật memory tagging và cơ chế memory shading, nhằm mở rộng khả năng phát hiện các lỗi truy cập bộ nhớ phức tạp trong C/C++. Báo cáo trình bày HWASanIO, một bộ công cụ phân tích động được tích hợp ở mức compiler instrumentation, cho phép phân biệt không chỉ giữa các đối tượng trong bộ nhớ mà còn giữa các trường dữ liệu bên trong một đối tượng. Cơ chế này hỗ trợ phát hiện các lỗi intra-object overflow vốn bị bỏ sót bởi các sanitizer truyền thống như HWASan hay AddressSanitizer. HWASanIO đạt hiệu quả phát hiện lỗi hoàn chỉnh trên bộ kiểm thử Juliet Test Suite, đồng thời duy trì khả năng tương thích với mã C/C++ hiện có mà không phá vỡ ABI, mở ra tiềm năng ứng dụng rộng rãi trong quy trình phát triển phần mềm yêu cầu độ tin cậy cao về bộ nhớ.

## **1.2. Xác định từ khóa chính cho nghiên cứu** {#1.2.-xác-định-từ-khóa-chính-cho-nghiên-cứu}

Để định hướng nghiên cứu và thu thập tài liệu phù hợp, các từ khóa liên quan được xác định bao gồm:

* Memory Safety

* Memory Tagging/Memory Coloring

* Intra-Object Overflows 

* Sub-Object Overflows 

* Dynamic Analysis

Những từ khóa này đóng vai trò làm nền tảng để thu thập dữ liệu từ các bài báo khoa học, tài liệu tham khảo và các công cụ mã nguồn mở.

## **1.3. Tìm kiếm, nghiên cứu các tài liệu tham khảo khác** {#1.3.-tìm-kiếm,-nghiên-cứu-các-tài-liệu-tham-khảo-khác}

Ngoài các tài liệu tham khảo trong tài liệu tham khảo chính, nhóm tập trung tìm hiểu thêm về các nghiên cứu gần đây mà nội dung có liên quan đến Memory Safety, Memory Tagging, Intra-Object Overflows và Sub-Object Overflows. Bao gồm:

1. Memory Tagging and how it improves C/C++ memory safety

   Nghiên cứu này trình bày kỹ thuật Memory Tagging, gán nhãn cho vùng nhớ và con trỏ để phát hiện lỗi truy cập bộ nhớ sai. Hai cơ chế SPARC ADI (hoàn toàn phần cứng) và AArch64 HWASAN (phần cứng hỗ trợ compiler) được đánh giá về hiệu quả và chi phí. Memory Tagging giúp phát hiện tốt hơn lỗi use-after-free và overflow trong môi trường thực tế với chi phí thấp, đặc biệt có thể sử dụng luôn trong sản phẩm (production) thay vì chỉ giai đoạn test..

2. SoftBound: Highly Compatible and CompleteSpatial Memory Safety for C

   Bài báo giới thiệu SoftBound, một cơ chế đảm bảo an toàn bộ nhớ không gian bằng cách gắn metadata (bounds) cho từng con trỏ trong C, giúp phát hiện và ngăn chặn lỗi tràn bộ đệm và truy cập ngoài vùng nhớ. SoftBound duy trì tính tương thích cao với mã hiện có, không thay đổi ABI hoặc layout bộ nhớ, và có thể áp dụng cho phần mềm legacy mà không cần sửa mã nguồn. HWASanIO thay thế việc lưu trữ bound cồng kềnh bằng tag (Color/Shade) gọn nhẹ.

3. Tech-ASan: Two-stage check for Address Sanitizer

   Nghiên cứu này giới thiệu Tech-ASan, một cơ chế kiểm tra hai giai đoạn cho Address Sanitizer nhằm giảm chi phí runtime trong phát hiện lỗi bộ nhớ. Tech-ASan dùng so sánh magic value để lọc nhanh các truy cập hợp lệ và chỉ kiểm tra shadow memory khi cần thiết. Đồng thời, công cụ tích hợp một bộ tối ưu loại bỏ kiểm tra dư thừa, đặc biệt trong các vòng lặp, giúp tăng tốc mà vẫn duy trì khả năng phát hiện lỗi.

4. EffectiveSan: Type and Memory Error Detection using Dynamically Typed C/C++

   Nghiên cứu này giới thiệu EffectiveSan, một cơ chế biến C/C++ thành ngôn ngữ kiểu động bằng cách gắn type meta-data vào mỗi object và kiểm tra type khi dereference. Nó phát hiện nhiều loại lỗi bộ nhớ như type confusion, sub-object overflows và use-after-free, vượt trội hơn các sanitizer chuyên biệt nhờ sử dụng dynamic type và low-fat pointers, đồng thời không thay đổi ABI và vẫn tương thích tốt với code đa luồng..

5. SoK: Sanitizing for Security

   Bài báo này hệ thống hóa toàn bộ các bộ công cụ sanitizer trong C/C++, phân loại theo loại lỗi bảo mật mà chúng phát hiện, cách thức hoạt động, chi phí runtime và mức độ tương thích. Nó trình bày sự khác biệt giữa exploit mitigation và sanitizer, phân tích ưu–nhược điểm của các mô hình như shadow memory, bounds checking, lock-and-key, pointer tagging… và đưa ra định hướng nghiên cứu tương lai cho việc cải thiện độ chính xác và hiệu suất của sanitizer.

## **1.4. Xây dựng và chạy thử nghiệm** {#1.4.-xây-dựng-và-chạy-thử-nghiệm}

Quá trình xây dựng và chạy thử nghiệm được thực hiện dựa trên môi trường giả lập và các kịch bản kiểm thử cụ thể:

*   **Cài đặt môi trường:** Do yêu cầu đặc thù về kiến trúc AArch64 (ARMv8) và tính năng Top-Byte Ignore (TBI), nhóm sử dụng Docker trên nền tảng MacBook Pro (Apple Silicon M3 Pro) để tạo môi trường Ubuntu 22.04 tương thích.
*   **Xây dựng kịch bản kiểm thử:** Nhóm thực hiện hai kịch bản chính:
    *   *Kịch bản 1 (Tự xây dựng):* Sử dụng struct đơn giản để kiểm tra khả năng phát hiện lỗi trên mã nguồn thông thường.
    *   *Kịch bản 2 (Test case chuẩn):* Sử dụng file `test-hwasanio.c` từ repository gốc để xác minh hoạt động trong điều kiện lý tưởng.
*   **Thực thi và thu thập log:** Chạy các chương trình đã biên dịch với HWASanIO và phân tích log báo lỗi (nếu có) để xác định nguyên nhân và cơ chế phát hiện.

## **1.5. Đánh giá hiệu quả**  {#1.5.-đánh-giá-hiệu-quả}

Dựa trên kết quả thực nghiệm, nhóm đánh giá hiệu quả của HWASanIO trên các khía cạnh sau:

*   **Khả năng phát hiện lỗi:** Phân tích khả năng phát hiện lỗi tràn bộ nhớ nội bộ đối tượng (intra-object overflow) thông qua việc so sánh kết quả giữa hai kịch bản kiểm thử.
*   **Độ chính xác của cảnh báo:** Đánh giá thông qua việc phân tích log `tag-mismatch` và các thông tin bộ nhớ (memory tags) được công cụ trích xuất khi xảy ra lỗi.
*   **Tính ổn định và hạn chế:** Xem xét các yếu tố ảnh hưởng đến khả năng phát hiện lỗi trong thực tế, chẳng hạn như cơ chế padding của trình biên dịch và cách bố trí bộ nhớ (memory layout).

# **Chương II. Tổng quan lý thuyết** {#chương-ii.-tổng-quan-lý-thuyết}

## **2.1. Memory Safety** {#2.1.-memory-safety}

Memory Safety (An toàn bộ nhớ) là một khái niệm trong lập trình và bảo mật phần mềm, đảm bảo rằng chương trình chỉ truy cập và thao tác trên vùng bộ nhớ hợp lệ — tránh việc đọc/ghi ngoài phạm vi được cấp phát hoặc trên các vùng bộ nhớ không còn hợp lệ. Có hai loại chính là An toàn bộ nhớ Không gian(Spatial Memory Safety) và An toàn bộ nhớ Thời gian(Temporal Memory Safety)

### 2.1.1. Spatial Memory Safety

An toàn bộ nhớ Không gian(Spatial Memory Safety) đảm bảo rằng mọi truy cập bộ nhớ đều nằm trong ranh giới hợp lệ (in-bounds) của đối tượng được cấp phát. Nó đảm bảo rằng các truy cập bộ nhớ (đọc hoặc ghi) được giới hạn trong phạm vi bộ nhớ đã được cấp phát cho một đối tượng cụ thể.

Vi phạm Spatial Memory Safety bao gồm các lỗi tràn vượt bộ đệm (buffer overflow) và tràn ngược bộ đệm (buffer underflow), nơi chương trình cố gắng truy cập dữ liệu bên ngoài vùng bộ nhớ được cấp cho đối tượng, ví dụ như truy cập vào bộ nhớ của một đối tượng lân cận hoặc vùng bộ nhớ không xác định.

### 2.1.2. Temporal Memory Safety

An toàn bộ nhớ Thời gian(Temporal Memory Safety) đảm bảo rằng các truy cập bộ nhớ chỉ được phép trong suốt vòng đời của đối tượng. Nó đảm bảo rằng một đối tượng chỉ được truy cập sau khi được cấp phát và trước khi nó bị hủy (free).

Vi phạm Temporal Memory Safety bao gồm các lỗi Sử dụng sau khi Giải phóng (Use After Free \- UAF), nơi chương trình vẫn giữ và cố gắng sử dụng một con trỏ trỏ đến một vùng bộ nhớ đã được giải phóng (và có thể đã được cấp phát lại cho một mục đích khác).

Các phương pháp đảm bảo an toàn bộ nhớ hiện nay như guard pages, red-zones, bounds tracking, fat-pointer hay memory tagging (HWASan, MTE) đã cải thiện đáng kể khả năng phát hiện vi phạm bộ nhớ ở mức đối tượng. Tuy nhiên, các cách tiếp cận này đều xem đối tượng như một khối bộ nhớ duy nhất mà không phân biệt các trường dữ liệu bên trong struct/class, dẫn đến việc không thể phát hiện các lỗi tràn bộ nhớ nội bộ đối tượng xảy ra giữa các field.

Mặc dù các kỹ thuật hiện tại xử lý tốt spatial memory safety và temporal memory safety, chúng vẫn chưa giải quyết hiệu quả các vi phạm bên trong một đối tượng. Điều này đặc biệt quan trọng trong C/C++ — nơi intrafield overflow có thể gây ra các hành vi sai lệch tinh vi hoặc được kẻ tấn công lợi dụng để thao túng dữ liệu hoặc chiếm quyền điều khiển hệ thống.

## **2.2. Intra-object Memory Violations**

Intra-object memory violation (vi phạm bộ nhớ nội bộ đối tượng) xảy ra khi việc truy cập bộ nhớ vượt khỏi phạm vi của một trường (field) nhưng vẫn nằm trong phạm vi của cùng một object. Nói cách khác, chương trình ghi đè từ field này sang field khác bên trong cùng struct/class, thay vì sang object khác.Một phân tích mã nguồn của các chương trình trong bộ benchmark SPEC CPU 2017 cho thấy khoảng 90% biến tổng hợp là struct/class với nhiều trường dữ liệu, làm tăng đáng kể khả năng xảy ra vi phạm nội bộ đối tượng. Tuy nhiên, các sanitizer như HWASan không thể phát hiện lỗi này vì chúng coi toàn bộ struct là một khối bộ nhớ duy nhất mà không phân biệt từng trường bên trong.

![][image2]

Hình 2.1. Tràn bộ nhớ nội bộ đối tượng trong test case Juliet CWE-121

	Hình 2.1 minh họa một đoạn mã trong bộ kiểm thử Juliet, nơi sizeof được áp dụng cho toàn bộ struct thay vì buffer 16 byte, khiến memcpy ghi vượt phạm vi bộ nhớ. Điều này gây tràn bộ nhớ nội bộ đối tượng và ghi đè các trường dữ liệu kế cận, có thể dẫn đến thao túng dữ liệu hoặc chiếm quyền điều khiển nếu các field chứa con trỏ.

## **2.3. Memory Tagging và HWASan** {#2.3.-memory-tagging-và-hwasan}

Memory tagging (hay memory coloring) là một cơ chế được sử dụng để đảm bảo an toàn bộ nhớ bằng cách thêm các lệnh nhằm theo dõi một tag được gán cho mỗi đối tượng cả trong địa chỉ con trỏ lẫn trong metadata bộ nhớ. Hình 2.2 mô tả khái niệm cơ bản này. Trong quá trình cấp phát, biến buffer được gán một tag ngẫu nhiên khác với đối tượng bộ nhớ liền trước và liền sau nó. Tag này được gán trong vùng shadow memory tương ứng với địa chỉ bộ nhớ của buffer, đồng thời cũng được lưu trong các bit trên cùng của con trỏ.

![][image3]

Hình 2.2. Tag bộ nhớ xác định truy cập hợp lệ/không hợp lệ

Mỗi lần dereference một con trỏ, hệ thống sẽ so sánh tag chứa trong con trỏ với tag lưu trong metadata của đối tượng nhằm xác định truy cập có hợp lệ hay không. HWASan sử dụng ánh xạ 16:1, tức 16 byte bộ nhớ ứng dụng được gắn với 1 byte metadata trong shadow memory. Nhờ đó, việc kiểm soát truy cập diễn ra hiệu quả nhưng vẫn tiết kiệm bộ nhớ.

Để xác định byte cuối cùng hợp lệ trong phạm vi 16 byte này, HWASan thêm một granule byte vào metadata của đối tượng. Tag của con trỏ được lưu trong 8 bit cao nhất của địa chỉ, và nhờ cơ chế Top Byte Ignore (TBI) trên ARM, các bit này không ảnh hưởng đến quá trình thao tác bộ nhớ.

Từ góc nhìn ứng dụng, việc sử dụng con trỏ diễn ra trong suốt và bình thường. Tuy nhiên, ở tầng compiler, các lệnh kiểm tra tag được tự động chèn vào trước mỗi thao tác load/store để tải metadata từ shadow memory và so sánh với tag của con trỏ. Nếu trùng khớp, truy cập tiếp tục bình thường; nếu không, một ngoại lệ được sinh ra để ngăn chặn truy cập vượt phạm vi.

Ngoài ra, memory tagging còn giúp phát hiện các vi phạm bộ nhớ theo thời gian, bởi metadata trong shadow memory của đối tượng đã bị giải phóng sẽ được đặt về tag bằng 0, khiến mọi con trỏ trỏ đến nó trở nên không hợp lệ. Nhờ đó ngăn chặn các lỗi như use-after-free.

## **2.4. Memory Shading** {#2.4.-memory-shading}

Nhóm tác giả đề xuất khái niệm memory shading như một mở rộng của memory tagging nhằm khắc phục hạn chế trong việc phát hiện vi phạm bộ nhớ nội bộ đối tượng (intra-object). Thay vì chỉ sử dụng một tag duy nhất cho toàn bộ object, giải pháp này phân tách metadata thành hai phần: color để xác định biên đối tượng và shade để phân biệt các trường dữ liệu bên trong object. Cách tiếp cận này cho phép hệ thống nhận biết truy cập giữa các field trong cùng một struct hoặc class, vốn không được phát hiện bởi các phương pháp tagging truyền thống. Trong giải thích của nhóm tác giả, cấu trúc minh họa chủ yếu sử dụng struct, nhưng cơ chế shading áp dụng đầy đủ cho cả struct và class trong C/C++.

**Color**. Color được định nghĩa bởi một nửa trên của metadata. Nó được sử dụng theo cùng cách như tag được mô tả trong Mục 2.3. Khi đối tượng được cấp phát, color được gán một giá trị ngẫu nhiên khác 0 và khác với các đối tượng liền kề nhằm tránh va chạm. Giá trị này được áp dụng xuyên suốt toàn bộ vùng shadow memory của object và được sử dụng trong mọi thao tác kiểm tra truy cập bộ nhớ (load/store).

**Shade**. Các bit còn lại trong metadata được sử dụng làm shade của đối tượng. Giá trị shade khác nhau giữa các trường dữ liệu lân cận, cho phép phát hiện tràn bộ nhớ nội bộ đối tượng.

* Với các đối tượng không phải struct, shade được đặt bằng 0, vì bất kỳ con trỏ nào trỏ tới đối tượng đều có thể truy cập hợp lệ vào toàn bộ vùng nhớ của nó.  
  * Với struct, shade bắt đầu từ giá trị 1 và tăng dần cho mỗi trường không phải struct tiếp theo, và quay vòng về 1 khi đạt giá trị tối đa.  
  * Với struct lồng nhau (layered struct), nơi một trường là một struct khác, thuật toán shading sẽ bắt đầu lại từ 1 cho struct con. Điều này giúp duy trì tính đồng nhất của shading bất kể độ sâu của cấu trúc.

![][image4]

Hình 2.3. Memory shading: phân biệt object và field bằng color–shade..

Hình 2.3 minh họa layout bộ nhớ tại runtime của hai biến trong hệ thống sử dụng memory shading. Struct kiểu foo\_t chứa một biến kiểu char và một buffer kiểu char. Metadata của nó bao gồm một color dùng chung cho toàn bộ đối tượng và một shade riêng biệt cho từng trường. Ngoài ra, một biến char và một biến buffer khác được cấp phát, và vì chúng không phải struct nên shade của chúng bằng 0, tức không có phân biệt sub-object. Trong ví dụ này, việc tràn bộ nhớ sang đối tượng khác bị ngăn chặn bởi color trong metadata.

## **2.5. State-of-the-art Memory Safety Approaches** {#2.5.-state-of-the-art-memory-safety-approaches}

State-of-the-art Memory Safety tập trung vào các cơ chế bảo vệ bộ nhớ ở mức runtime được tích hợp vào trình biên dịch hoặc phần cứng, nhằm phát hiện và ngăn chặn các vi phạm bộ nhớ trong C/C++. Các phương pháp hiện đại như ASan, HWASan, EffectiveSan hay Softbound/CETS sử dụng các kỹ thuật như red-zones, memory tagging, bounds metadata và dynamic type checking để đảm bảo an toàn bộ nhớ không gian (spatial) và thời gian (temporal). Tuy nhiên, đa số các phương pháp này vẫn xem đối tượng như một đơn vị bộ nhớ nguyên khối và do đó chưa thể xử lý hiệu quả các lỗi vi phạm nội bộ đối tượng (intra-object overflow). Do đó, phương pháp tiên tiến như HWASanIO đề xuất cơ chế memory shading, cho phép phân biệt các trường bên trong cấu trúc dữ liệu bằng cặp metadata color–shade, mở rộng phạm vi bảo vệ xuống cấp độ sub-object, từ đó phát hiện các vi phạm bộ nhớ mà các phương pháp state-of-the-art trước đây bỏ sót.

### 2.5.1. Một số phương pháp phổ biến {#2.5.1.-một-số-phương-pháp-phổ-biến}

#### 2.5.1.1. Tagging-based Approaches (ASan, HWASan)

Phương pháp gắn thẻ bộ nhớ, còn được gọi là tô màu bộ nhớ, sử dụng siêu dữ liệu gắn với con trỏ để thực hiện kiểm tra an toàn bộ nhớ.

* Cơ chế: Gán một thẻ (tag) cho cả con trỏ và vùng bộ nhớ đối tượng tương ứng. Mỗi lần truy cập bộ nhớ, thẻ trong con trỏ được so sánh với thẻ lưu trong bộ nhớ bóng (shadow memory).  
* Mục tiêu: Đạt được An toàn Bộ nhớ Không gian và Thời gian.  
* Ưu điểm: Chi phí bộ nhớ thấp và giảm độ phức tạp của logic kiểm tra so với các phương pháp dựa trên metadata phức tạp hơn. HWASan (Hardware-assisted AddressSanitizer): Sử dụng các bit trên của con trỏ để lưu thẻ, tận dụng tính năng ARM Top Byte Ignore (TBI).  
* Hạn chế:  
  * Va chạm (Collisions): Do kích thước thẻ hạn chế, có thể xảy ra va chạm metadata, cho phép con trỏ truy cập nhầm đối tượng khác có cùng thẻ.  
  * Intra-object: Không thể phát hiện các vi phạm bộ nhớ nội bộ đối tượng (intra-object violations) vì chúng coi đối tượng là một đơn vị duy nhất.

#### 2.5.1.2. Bounds-based Approaches (Softbound/CETS)

Phương pháp này đảm bảo an toàn bộ nhớ bằng cách theo dõi địa chỉ bắt đầu và kết thúc của đối tượng.

* Cơ chế:  
  * Theo dõi địa chỉ bắt đầu (start address) và kết thúc (end address) của các đối tượng.  
  * Các phép toán con trỏ được instrument để đảm bảo luôn nằm trong phạm vi bộ nhớ đã cấp phát.  
  * Softbound/CETS: Giữ thông tin giới hạn trong vùng nhớ riêng và đạt An toàn Bộ nhớ Thời gian bằng cơ chế khóa–chìa (lock–key metadata).  
* Mục tiêu: Đảm bảo An toàn Bộ nhớ Không gian.  
* Ưu điểm: Cung cấp độ chính xác cao khi sử dụng metadata theo từng con trỏ (fat-pointers).  
* Hạn chế:  
  * Logic kiểm tra khá phức tạp do phải so sánh con trỏ với địa chỉ bắt đầu và kết thúc.  
  * Việc truy vết giới hạn của đối tượng con (sub-object bounds) là có thể nhưng đánh đổi bằng overhead tăng đáng kể

#### 2.5.1.3. Type-based Approaches (EffectiveSan)

Phương pháp này sử dụng thông tin kiểu dữ liệu động để tăng cường khả năng phát hiện lỗi không gian.

* Cơ chế: Sử dụng thông tin kiểu động (dynamic type information) bổ sung để phát hiện các vi phạm không gian.  
* Mục tiêu: Phát hiện vi phạm không gian, bao gồm cả lỗi tràn nội bộ đối tượng.  
* Hạn chế:  
  * Intra-object: Không thể phát hiện lỗi tràn nội bộ đối tượng giữa các trường có cùng kiểu dữ liệu (ví dụ: hai mảng char bên trong một struct).  
  * Theo đánh giá, nó không thể phát hiện nhiều lỗ hổng trong các danh mục tràn vì các trường hợp kiểm thử sử dụng bộ đệm cùng loại.

#### 2.5.1.4. Memory Shading (HWASanIO) 

Tạo bóng bộ nhớ là một phương pháp mới được đề xuất để mở rộng khả năng của gắn thẻ bộ nhớ, giải quyết trực tiếp vấn đề vi phạm nội bộ đối tượng.

* Cơ chế: Thay đổi thiết kế metadata từ chỉ dựa trên màu (color-based) sang dựa trên màu (color) và bóng (shade).  
  * Color (Màu): Chỉ ranh giới đối tượng, giống như thẻ truyền thống.  
  * Shade (Bóng): Phân biệt giữa các trường (fields) và thành viên (members) bên trong cùng một đối tượng.  
* Mục tiêu: Mở rộng khả năng phát hiện vi phạm nội bộ đối tượng (intra-object violations).  
* Triển khai (HWASanIO):  
  * Sử dụng 1-đổi-1 mapping cho bộ nhớ bóng, đảm bảo độ chính xác từng byte và không phá vỡ ABI.  
  * Logic kiểm tra so sánh cả màu và bóng.  
* Ưu điểm: HWASanIO là sanitizer dựa trên trình biên dịch đầu tiên có khả năng gắn thẻ bộ nhớ để phát hiện đầy đủ các lỗi intra-object.

### 2.5.2. So sánh {#2.5.2.-so-sánh}

Bảng 2.1. So sánh các phương pháp an toàn bộ nhớ

| Tiêu chí | Phương pháp  ASan /HWASan | Phương pháp Softbound/CETS | Phương pháp EffectiveSan | Phương pháp HWASanIO |
| :---: | :---: | :---: | :---: | :---: |
| Phát hiện tràn bộ nhớ (inter-object) | Có | Có | Có | Có |
| Phát hiện intra-object overflow (giữa các field trong struct) | Không | Có nhưng overhead cao | Có nhưng hạn chế | Có |
| Phát hiện use-after-free | Có | Có | Không | Có |
| Phát hiện vi phạm thời gian sống object (temporal) | Không | Có | Không | Có |
| Kiểu metadata | Red-zone & shadow memory | Bounds \+ lock–key | Dynamic type info | Color \+ Shade |
| Overhead bộ nhớ | Trung bình | Rất cao | Cao | Trung bình |

# **Chương III. Thực nghiệm** {#chương-iii.-thực-nghiệm}

## **3.1. Thiết lập môi trường** {#3.1.-thiết-lập-môi-trường}

### 3.1.1. Cấu hình phần cứng
Do HWASanIO yêu cầu kiến trúc AArch64 (ARMv8) và tính năng Top-Byte Ignore (TBI), nhóm sử dụng thiết bị MacBook Pro với chip Apple Silicon (M3 Pro) để đáp ứng yêu cầu phần cứng.

| Thành phần | Cấu hình thực tế nhóm sử dụng |
| :--- | :--- |
| **Thiết bị** | MacBook Pro (Apple Silicon M3 Pro) |
| **CPU** | Apple M3 Pro (ARM64) |
| **Hệ điều hành Host** | macOS Sonoma |
| **Môi trường Guest** | Docker (Ubuntu 22.04 LTS) |

### 3.1.2. Chuẩn bị môi trường Docker
Để đảm bảo tính tương thích với các công cụ hệ thống Linux (như LLVM, Clang, GDB), nhóm sử dụng Docker để tạo môi trường Ubuntu 22.04 biệt lập.

**Bước 1: Tải Docker Image**
```bash
docker pull ubuntu:22.04
```

**Bước 2: Khởi chạy Container**
Chúng tôi gắn (mount) thư mục mã nguồn vào container để tiện chỉnh sửa trên Host và biên dịch trên Guest.
```bash
docker run -it --name hwasanio_env \
  -v $(pwd)/hwasanio_repo:/workspace \
  ubuntu:22.04 /bin/bash
```

**Bước 3: Cài đặt các gói phụ thuộc**
Trong container, tiến hành cập nhật và cài đặt các công cụ cần thiết để build LLVM:
```bash
apt-get update
apt-get install -y git cmake ninja-build build-essential python3
```

## **3.2. Cài đặt HWASanIO** {#3.2.-cài-đặt-hwasanio}

### 3.2.1. Tải mã nguồn
Mã nguồn của dự án được tải về từ repository (hoặc giải nén từ archive được cung cấp):
```bash
# Giả sử mã nguồn đã được mount vào /workspace
cd /workspace
```

### 3.2.2. Xây dựng (Build)
HWASanIO cung cấp script tự động để tải và patch LLVM 14. Quá trình build sẽ tạo ra một phiên bản Clang tùy chỉnh có tích hợp HWASanIO instrumentation.

```bash
# Script setup.sh thực tế được sử dụng
# 1. Clone dự án LLVM đã được patch
git clone https://github.com/Fraunhofer-AISEC/hwasanio-llvm-project.git hwasanio-llvm-project

# 2. Tạo thư mục build và cấu hình CMake
BUILD_DIR="hwasanio-llvm-project/build"
mkdir -p "$BUILD_DIR"
cd $BUILD_DIR

cmake ../llvm/ -G Ninja \
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_CXX_COMPILER=clang++ \
    -DCMAKE_BUILD_TYPE=Release \
    -DLLVM_ENABLE_LLD=ON \
    -DLLVM_TARGETS_TO_BUILD='AArch64' \
    -DLLVM_ENABLE_PROJECTS='clang;lld;compiler-rt'

# 3. Tiến hành biên dịch
cmake --build .
```
*Lưu ý: Quá trình này có thể mất từ 30-60 phút tùy thuộc vào cấu hình máy.*

Sau khi build thành công, trình biên dịch `clang` mới sẽ nằm trong thư mục `llvm-project/build/bin`.

## **3.3. Kịch bản kiểm thử và Kết quả** {#3.3.-kịch-bản-kiểm-thử-và-kết-quả}

### 3.3.1. Kịch bản 1: Kiểm thử với Struct đơn giản (Tự xây dựng)
**Mục tiêu:** Kiểm tra xem HWASanIO có phát hiện được lỗi tràn bộ nhớ giữa các biến đơn giản trong struct hay không.

**Mã nguồn (`repro_issue.c`):**
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct UserData {
    char name[10];
    int secret_id;
};

int main() {
    struct UserData *user = (struct UserData*)malloc(sizeof(struct UserData));
    user->secret_id = 12345;

    // LỖI: Ghi tràn từ trường 'name' (10 bytes) sang 'secret_id'
    // Ghi 16 bytes vào name (tràn 6 bytes sang secret_id)
    char *ptr = user->name;
    for (int i = 0; i < 16; i++) {
        ptr[i] = 'A'; 
    }
    
    printf("Overwritten Secret ID: %d\n", user->secret_id);
    free(user);
    return 0;
}
```

**Thực thi:**
```bash
# Biên dịch với cờ -fsanitize=hwaddress và sử dụng lld linker
docker run --rm hwasanio-temp \
bash -c "cd /workspace && ./hwasanio-llvm-project/build/bin/clang -fsanitize=hwaddress -fuse-ld=lld -g repro_issue.c -o repro_issue && ./repro_issue"
```

**Kết quả:** Chương trình chạy thành công (Exit code 0) và **không báo lỗi**.
**Phân tích:** Như đã đề cập ở phần 1.4, trình biên dịch thường chèn padding giữa các biến để căn chỉnh bộ nhớ. Việc ghi tràn 6 byte từ `name[10]` có thể chỉ ghi vào vùng padding này (thường là 2-6 byte tùy alignment). Do vùng padding không được gán Shade riêng biệt, HWASanIO không phát hiện ra vi phạm.

### 3.3.2. Kịch bản 2: Kiểm thử với Test Case chuẩn (test-hwasanio.c)
**Mục tiêu:** Xác minh khả năng hoạt động của công cụ trên mã nguồn được thiết kế để loại bỏ padding (hoặc padding đã được xử lý).

**Mã nguồn (`hwasanio_repo/example/test-hwasanio.c`):**
```c
typedef struct double_buffer_t {
    char buf1[16];
    char buf2[16];
} double_buffer;

void test_intra_object_overflow() {
    double_buffer db = { .buf1 = { 0 }, .buf2 = { 0 } };
    for (int i = 0; i < 20; i++) {
        db.buf1[i] = 'a'; // Ghi tràn 4 byte sang buf2
    };
}
// ... (các hàm test khác)
```

**Thực thi:**
Nhóm sử dụng lệnh biên dịch thực tế từ `example.sh`:
```bash
../hwasanio-llvm-project/build/bin/clang -fsanitize=hwaddress -fuse-ld=lld test-hwasanio.c -o build/test-hwasanio
./build/test-hwasanio 0
```

**Kết quả:** Công cụ phát hiện lỗi và dừng chương trình.
```text
SUMMARY: HWAddressSanitizer: tag-mismatch ... in __hwasan_store1_shade_dbg
Exit code: 99
```

**Phân tích Log:**
*   **Tag Mismatch:** Log chỉ ra rằng con trỏ đang truy cập có tag `e1` (tương ứng với `buf1`), nhưng vùng nhớ đích lại có tag `e2` (tương ứng với `buf2`).
*   **Cơ chế:** Điều này chứng minh HWASanIO đã gán các Shade khác nhau (1 và 2) cho hai trường `buf1` và `buf2` trong cùng một struct, và phát hiện thành công việc truy cập chéo.

## **3.4. Đánh giá tổng quan** {#3.4.-đánh-giá-tổng-quan}

Từ quá trình thực nghiệm chi tiết trên, nhóm rút ra các kết luận sau:

1.  **Tính khả thi trên ARM64:** HWASanIO hoạt động tốt trên kiến trúc Apple Silicon (thông qua Docker Linux), tận dụng hiệu quả tính năng TBI của phần cứng.
2.  **Hiệu quả phát hiện lỗi:** Công cụ phát hiện chính xác lỗi intra-object overflow khi các điều kiện về memory layout được thỏa mãn (như trong Kịch bản 2).
3.  **Hạn chế thực tế:** Sự phụ thuộc vào memory layout (padding, alignment) là một rào cản lớn. Trong các ứng dụng thực tế (như Kịch bản 1), các lỗi tinh vi có thể bị bỏ qua nếu chúng chỉ ảnh hưởng đến vùng padding. Cần có cơ chế "Shade" cho cả vùng padding để đạt độ phủ lỗi 100%.

# 

# **Chương IV. Kết luận** {#chương-iv.-kết-luận}

Báo cáo đã trình bày về HWASanIO, một kỹ thuật mới mở rộng từ HWASan nhằm phát hiện các lỗi tràn bộ nhớ nội đối tượng (intra-object overflows) \- một lớp lỗi nguy hiểm mà các công cụ truyền thống thường bỏ qua. Bằng cách sử dụng cơ chế Memory Shading, kết hợp 4 bit tag màu sắc (Color) và 4 bit tag sắc thái (Shade), HWASanIO cho phép kiểm soát quyền truy cập ở mức độ mịn hơn, phân biệt được các trường dữ liệu liền kề trong cùng một cấu trúc.

Kết quả thực nghiệm cho thấy HWASanIO hoạt động chính xác trên các bộ test case chuẩn, phát hiện thành công các lỗi ghi đè giữa các biến thành viên. Tuy nhiên, thực nghiệm cũng chỉ ra thách thức trong việc áp dụng trên các mã nguồn tùy ý, nơi cơ chế padding và alignment của trình biên dịch có thể tạo ra các vùng nhớ "vô chủ", làm giảm khả năng phát hiện lỗi nếu không có sự can thiệp sâu vào quá trình biên dịch.

Tóm lại, HWASanIO là một bước tiến quan trọng trong bảo mật bộ nhớ, đặc biệt hữu ích cho các hệ thống nhúng sử dụng kiến trúc AArch64. Để công cụ trở nên phổ biến hơn, cần có những cải tiến để tự động hóa việc xử lý layout bộ nhớ, giảm thiểu yêu cầu tinh chỉnh thủ công từ phía lập trình viên.

# **Danh mục tài liệu tham khảo** {#danh-mục-tài-liệu-tham-khảo}

\[1\]	Benjamin Steenhoek, Hongyang Gao and Wei Le, “Dataflow Analysis-Inspired Deep Learning for Efficient Vulnerability Detection"

\[2\]	Zhonghao Jiang,  Weifeng Sun,  Xiaoyan Gu,  Jiaxin Wu,  Tao Wen,  Haibo Hu and  Meng Yan, "DFEPT: Data Flow Embedding for Enhancing Pre-Trained Model Based Vulnerability Detection"

\[3\]	David Hin,  Andrey Kan, Huaming Chen and  M. Ali Babar, "LineVD: Statement-level Vulnerability Detection using Graph Neural Networks"

\[4\]	Adriana Sejfia,  Satyaki Das,  Saad Shafiq and  Nenad Medvidović, "Toward Improved Deep Learning-based Vulnerability Detection"

\[5\]	Avishree Khare,  Saikat Dutta,  Ziyang Li, Alaia Solko-Breslin,  Rajeev Alur and  Mayur Naik, "Understanding the Effectiveness of Large Language Models in Detecting Security Vulnerabilities"

\[6\]	Xin-Cheng Wen , Yupan Chen , Cuiyun Gao , Hongyu Zhang, Jie M. Zhang and Qing Liao, "Vulnerability Detection with Graph Simplification and Enhanced Graph Representation Learning"

 