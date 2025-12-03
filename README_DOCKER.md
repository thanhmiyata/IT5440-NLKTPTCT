# Hướng dẫn chạy HWASanIO bằng Docker trên MacBook M3

Do HWASanIO yêu cầu môi trường Linux và kiến trúc ARMv8 (có TBI), việc chạy trực tiếp trên macOS là không khả thi. Docker là giải pháp tốt nhất để tận dụng phần cứng M3 của bạn.

## 1. Yêu cầu
*   Đã cài đặt **Docker Desktop** trên macOS.

## 2. Cách Build và Chạy

### Bước 1: Build Docker Image
Mở terminal tại thư mục chứa file `Dockerfile` và chạy lệnh sau:
```bash
docker build -t hwasanio-env .
```
*Lưu ý: Quá trình build LLVM sẽ mất khá nhiều thời gian (có thể từ 30-60 phút tùy vào tốc độ mạng và CPU).*

### Bước 2: Chạy Container
Sau khi build xong, khởi động container:
```bash
docker run -it --name hwasanio-container hwasanio-env
```
Lệnh này sẽ đưa bạn vào shell `bash` bên trong môi trường Linux đã cài đặt sẵn HWASanIO.

## 3. Chạy Thử Nghiệm (Bên trong Container)

Sau khi vào được container, bạn có thể thử chạy script ví dụ:

1.  **Kiểm tra Clang**:
    ```bash
    clang --version
    ```
    Bạn sẽ thấy phiên bản Clang do HWASanIO build (thường là version 14.x).

2.  **Chạy Example**:
    Trong thư mục `/workspace/hwasanio-llvm-project`, bạn có thể tạo một file test hoặc tìm script ví dụ (nếu có trong repo gốc, hoặc tự viết).

    Ví dụ tạo file `test.c`:
    ```c
    #include <stdio.h>
    #include <stdlib.h>

    struct Point {
        int x;
        int y;
    };

    int main() {
        struct Point *p = (struct Point*)malloc(sizeof(struct Point));
        // Truy cập hợp lệ
        p->x = 10;
        
        // Giả lập lỗi intra-object (cần code cụ thể để trigger logic của HWASanIO)
        // HWASanIO sẽ tự động chèn check khi biên dịch
        
        free(p);
        return 0;
    }
    ```

    Biên dịch với cờ HWASan:
    ```bash
    clang -fsanitize=hwaddress -g test.c -o test
    ./test
    ```

## 4. Lưu ý
*   Nếu bạn muốn chỉnh sửa code trên máy Mac và sync vào Docker, hãy dùng cờ `-v` khi run:
    ```bash
    docker run -it -v $(pwd):/workspace/mount --name hwasanio-container hwasanio-env
    ```
