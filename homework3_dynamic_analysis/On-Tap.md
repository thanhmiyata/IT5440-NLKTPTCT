### 1. Module: Tracing Engine (`tracer_engine.py`)
*Mục tiêu: Ghi lại lịch sử thực thi chương trình một cách trung thực (Lossless).*

*   **Kỹ thuật cốt lõi:**
    *   Sử dụng Hook: `sys.settrace(trace_callback)`.
    *   Hàm callback chặn 3 loại sự kiện chính: `'call'` (vào hàm), `'line'` (thực thi dòng), `'return'` (thoát hàm).
*   **Chi tiết triển khai (Slide 4):**
    1.  **Control Flow Tracing:** Ghi lại số dòng (`frame.f_lineno`) và tên file/hàm. Đây là xương sống để tái hiện đường đi.
    2.  **Value Tracing:** Tại mỗi dòng, snapshot lại giá trị biến cục bộ bằng `frame.f_locals.copy()`. Điều này cho biết trạng thái bộ nhớ tại thời điểm đó.
    3.  **Memory Access (Giả lập):** So sánh `f_locals` trước và sau khi thực thi dòng lệnh. Nếu biến `x` thay đổi giá trị -> Ghi nhận sự kiện **WRITE**. Nếu biến `y` được dùng trong biểu thức -> Ghi nhận sự kiện **READ**.
*   **Câu hỏi có thể gặp:** *Tại sao tracing lại làm chậm chương trình?*
    *   **Trả lời:** Vì `sys.settrace` là một hàm callback đồng bộ, nó can thiệp vào từng dòng lệnh bytecode của Python, làm tăng overhead xử lý lên rất nhiều lần.

### 2. Module: Dynamic Slicing (`dynamic_slicer.py`)
*Mục tiêu: Tìm tập hợp lệnh ảnh hưởng đến một biến mục tiêu (Slicing Criterion).*

*   **Kỹ thuật cốt lõi:** Backward Traversal (Duyệt ngược) trên Execution Trace.
*   **Chi tiết triển khai (Slide 84, 86):**
    1.  **Input:** Một Trace đầy đủ + Tiêu chí cắt `<Dòng, Biến>`.
    2.  **Thuật toán:**
        *   Đi ngược từ cuối trace lên đầu.
        *   **Data Dependence:** Nếu dòng hiện tại (L_curr) ghi đè lên biến mục tiêu -> Giữ lại dòng đó -> Thêm các biến vế phải của L_curr vào danh sách "biến cần theo dõi tiếp".
        *   **Control Dependence:** Nếu dòng hiện tại nằm trong một khối `if/while` (scope), thì điều kiện của `if/while` đó cũng được thêm vào Slice.
    3.  **Kết quả:** Một danh sách các dòng lệnh nhỏ hơn nhiều so với chương trình gốc, nhưng đủ để tái tạo giá trị biến mục tiêu.
*   **Điểm nhấn:** Dynamic Slice chính xác hơn Static Slice vì nó loại bỏ các nhánh `if/else` không bao giờ được thực thi với input cụ thể đó (Slide 79).

### 3. Module: Execution Indexing (`execution_indexer.py`)
*Mục tiêu: Định danh duy nhất một điểm thực thi để so sánh giữa các lần chạy.*

*   **Kỹ thuật cốt lõi:** Bộ ba định danh (The Triple) - Slide 101.
*   **Chi tiết triển khai:**
    *   Cấu trúc Index ID: `<Calling Context, Statement, Instance>`.
    *   **Calling Context:** Một Stack lưu chuỗi gọi hàm (VD: `[main, calculate_tax, get_rate]`).
    *   **Statement:** Số dòng lệnh (`line_no`).
    *   **Instance:** Bộ đếm tần suất. Một Dictionary `counts[(context, line)]` được dùng để đếm xem dòng lệnh đó đã chạy lần thứ mấy trong context đó (quan trọng cho vòng lặp).
*   **Ứng dụng:** Giúp phân biệt lần lặp thứ 1 (`i=0`) và lần lặp thứ 100 (`i=99`) của cùng một dòng code. Đây là nền tảng để thực hiện Heisenbug Demo.

### 4. Module: Fault Localization (`fault_localization.py`)
*Mục tiêu: Khoanh vùng lỗi tự động dựa trên thống kê.*

*   **Kỹ thuật cốt lõi:** Spectrum-based Fault Localization (SBFL).
*   **Chi tiết triển khai (Slide 142):**
    1.  **Program Spectra:** Ma trận nhị phân (Test cases x Lines). Ô `[i][j] = 1` nếu Test `i` chạy qua dòng `j`.
    2.  **Labeling:** Đánh dấu mỗi Test Case là PASS hoặc FAIL.
    3.  **Công thức (Tarantula/Ochiai):** Tính điểm nghi ngờ (Suspiciousness Score) cho từng dòng lệnh.
        *   Logic: Dòng nào xuất hiện nhiều trong các ca FAIL và ít trong các ca PASS sẽ có điểm cao.
    4.  **Ranking:** Sắp xếp giảm dần theo điểm. Dòng code đầu bảng là "thủ phạm" tiềm năng nhất.

### 5. Module: Challenge Three - Heisenbug (`heisenbug_demo.py`)
*Mục tiêu: Tái tạo lỗi Race Condition khó nắm bắt.*

*   **Mô tả kịch bản:**
    *   Bài toán chuyển tiền/tính toán với biến chia sẻ (Shared Variable) giữa 2 luồng (Threads) mà không có Lock.
    *   Lỗi chỉ xảy ra khi Thread 1 đọc giá trị, Thread 2 xen vào ghi đè, rồi Thread 1 mới ghi (Lost Update).
*   **Kỹ thuật "Bẫy" lỗi:**
    1.  **Normal Run:** Lỗi không hiện ra do CPU chạy quá nhanh hoặc Scheduler ưu tiên Thread 1 chạy xong mới đến Thread 2.
    2.  **Perturbed Run (Nhiễu loạn):**
        *   Dùng **Execution Indexing** để xác định đúng thời điểm nhạy cảm (VD: Dòng 50, lần chạy thứ 1).
        *   Chèn `time.sleep(0.1)` (Perturbation) vào đúng Index đó.
        *   Kết quả: Buộc Scheduler phải chuyển ngữ cảnh (Context Switch), tạo điều kiện cho Race Condition xảy ra -> Crash/Bug xuất hiện.
*   **Lưu ý kỹ thuật:** Trong Python, để trace đa luồng, cần dùng `threading.settrace()`, không chỉ `sys.settrace()`.

---

### Mẹo trả lời vấn đáp (Defense Tips)

1.  **Câu hỏi 1:** *"Làm sao em biết dòng code nào phụ thuộc dữ liệu vào dòng nào trong Python?"*
    *   **Trả lời:** "Do hạn chế của `sys.settrace` chỉ báo dòng lệnh, nhóm em thực hiện phân tích bằng cách so sánh `locals()` (biến cục bộ) trước và sau dòng lệnh. Nếu biến `A` thay đổi, nghĩa là dòng đó ghi vào `A`. Tuy nhiên, để chính xác tuyệt đối như lý thuyết compiler, cần phân tích AST (Abstract Syntax Tree) kết hợp, nhưng cách `locals()` là đủ cho mục đích minh họa Dynamic Analysis."

2.  **Câu hỏi 2:** *"Tại sao Heisenbug lại biến mất khi dùng Debugger?"*
    *   **Trả lời:** "Vì Debugger làm thay đổi thời gian thực thi (timing) của các luồng. Heisenbug (thường là Race Condition) phụ thuộc chặt chẽ vào thứ tự xen kẽ (interleaving) của các chỉ thị máy. Việc dừng debug hoặc chạy chậm lại làm thay đổi thứ tự này, khiến lỗi không tái hiện được. Phương pháp của nhóm em dùng Indexing để chèn nhiễu (sleep) chính xác mà không cần dừng thủ công."

3.  **Câu hỏi 3:** *"Indexing <Context, Line, Instance> giải quyết vấn đề gì?"*
    *   **Trả lời:** "Nó giải quyết vấn đề nhập nhằng (ambiguity). Nếu chỉ dùng số dòng, ta không biết đang ở vòng lặp thứ mấy hay được gọi từ hàm nào. Indexing giúp định vị tọa độ chính xác tuyệt đối của một trạng thái thực thi."

### Câu 1: Về Tracing & Performance (Hiệu năng)
**Hỏi:** *"Em sử dụng `sys.settrace` để ghi lại mọi thứ (Lossless Tracing). Vậy nếu chương trình của tôi chạy trong 1 tiếng đồng hồ hoặc có vòng lặp 1 triệu lần, giải pháp của em sẽ gặp vấn đề gì và hướng giải quyết ra sao?"*

*   **Mục đích:** Kiểm tra kiến thức về Overhead (chi phí) và Scalability (khả năng mở rộng) - Slide 14, 15.
*   **Gợi ý trả lời:**
    *   **Vấn đề:** File log sẽ cực kỳ lớn (Gigabytes/Terabytes) và chương trình chạy rất chậm (slowdown 10x-100x). Bộ nhớ RAM có thể bị tràn nếu lưu trace trong list.
    *   **Hướng giải quyết (dựa trên slide):**
        1.  **Ghi file stream:** Ghi trực tiếp xuống đĩa thay vì lưu trong RAM.
        2.  **Sampling (Lấy mẫu):** Chỉ trace một phần (như Slide 23).
        3.  **Coarse-grained Tracing:** Chỉ trace mức hàm (Function level) thay vì mức dòng lệnh (Line level) (Slide 16).
        4.  **Compression:** Nén trace log ngay lúc ghi (dùng thuật toán như Zlib - Slide 17).

### Câu 2: Về Dynamic Slicing (Độ chính xác)
**Hỏi:** *"Trong thuật toán Slicing, làm sao em xác định được 'Control Dependence' (Phụ thuộc điều khiển)? Ví dụ: Làm sao biết dòng lệnh `z = x + 1` thực thi là do `if x > 0` đúng hay sai?"*

*   **Mục đích:** Kiểm tra hiểu biết về logic thuật toán cắt lát - Slide 76, 84.
*   **Gợi ý trả lời:**
    *   Trong Python, nhóm em dựa vào **cấu trúc khối (indentation/block structure)**.
    *   Khi trace đi vào một khối lệnh mới (tăng indentation) ngay sau một lệnh rẽ nhánh (`if`, `while`), em ghi nhận lệnh rẽ nhánh đó là cha (parent) của các lệnh bên trong.
    *   Nếu code phức tạp hơn (như `goto` trong C), ta phải dùng khái niệm **Post-dominator** (như Slide 102 đề cập trong phần Indexing) để xác định phạm vi ảnh hưởng của câu lệnh điều kiện.

### Câu 3: Về Fault Localization (Tình huống sai)
**Hỏi:** *"Phương pháp Tarantula dựa trên phổ (Spectrum) có nhược điểm gì? Có trường hợp nào dòng lệnh bị lỗi (Buggy line) được thực thi nhưng Test Case vẫn PASS không (Coincidental Correctness)?"*

*   **Mục đích:** Kiểm tra hiểu biết về bản chất thống kê của Fault Localization - Slide 140, 141.
*   **Gợi ý trả lời:**
    *   **Có.** Hiện tượng này gọi là **Coincidental Correctness** (Đúng ngẫu nhiên).
    *   **Ví dụ:** Câu lệnh lỗi là `x = x * 2` (đáng lẽ là `x = x + 2`). Nếu tại đó `x = 2`, thì cả hai đều ra `4`. Test case vẫn PASS dù chạy qua dòng lỗi.
    *   **Hậu quả:** Tarantula sẽ đánh giá dòng lỗi đó ít nghi ngờ hơn (vì nó xuất hiện trong case PASS), dẫn đến việc xếp hạng (ranking) bị sai lệch.

### Câu 4: Về Execution Indexing (Đệ quy & Đa luồng)
**Hỏi:** *"Bộ ba `<Context, Line, Instance>` của em xử lý thế nào với trường hợp Đệ quy (Recursion)? Context Stack sẽ trông như thế nào?"*

*   **Mục đích:** Kiểm tra tính đúng đắn của giải thuật Indexing - Slide 101.
*   **Gợi ý trả lời:**
    *   Khi đệ quy, `Context` sẽ phát triển dài ra theo độ sâu của ngăn xếp.
    *   Ví dụ hàm `fib(n)` gọi `fib(n-1)`.
    *   Index 1: `<[main, fib], line 5, instance 1>`
    *   Index 2: `<[main, fib, fib], line 5, instance 1>`
    *   Index 3: `<[main, fib, fib, fib], line 5, instance 1>`
    *   Nhờ `Context` lưu trữ chuỗi gọi hàm, Indexing vẫn phân biệt được chính xác ta đang ở tầng đệ quy nào, không bị nhầm lẫn.

### Câu 5: Về Heisenbug (Challenge Three)
**Hỏi:** *"Tại sao em lại khẳng định phương pháp chèn nhiễu (Perturbation) của em là hiệu quả? Nếu chèn `sleep` sai chỗ hoặc sai thời điểm thì sao?"*

*   **Mục đích:** Hỏi xoáy vào giải pháp cho bài toán điểm thưởng - Slide 120.
*   **Gợi ý trả lời:**
    *   Phương pháp của em là **Targeted Perturbation** (Nhiễu có chủ đích), không phải Random.
    *   Em dùng **Slicing** để tìm ra các biến chia sẻ (Shared Variables) gây ra lỗi (Critical Section).
    *   Em dùng **Indexing** để đảm bảo em chèn `sleep` vào đúng **lần thực thi (Instance)** đó của dòng lệnh.
    *   Nếu chèn sai, lỗi có thể không tái hiện. Do đó, chiến lược là chạy lặp lại (Search strategy) xung quanh các điểm Index nghi ngờ (đã tìm ra từ Slicing) cho đến khi khớp đúng mẫu hình lỗi (failure pattern).

---

**Mẹo nhỏ:** Khi trả lời, hãy cố gắng nhắc đến số Slide hoặc từ khóa tiếng Anh trong Slide (như "Post-dominator", "Coincidental Correctness", "Lossless") để thầy thấy bạn bám sát bài giảng rất kỹ.