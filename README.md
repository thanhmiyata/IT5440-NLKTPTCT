# IT5440 - Nguyên lý và Kỹ thuật Phân tích Chương trình - Nhóm 5

Dự án này chứa các báo cáo, mã nguồn thực nghiệm và bài tập cho môn học IT5440.

## Cấu trúc Dự án

*   **Report IT5440 - Group 5.md**: Báo cáo chính của nhóm về chủ đề HWASanIO.
*   **hwasanio_repo/**: Thư mục chứa mã nguồn thực nghiệm (reproduction code) và các script cài đặt.
*   **homework3_dynamic_analysis/**: Bài tập về nhà số 3 (Phân tích động).
*   **README_DOCKER.md**: Hướng dẫn cài đặt và sử dụng môi trường Docker.

## Mã nguồn HWASanIO

Dự án sử dụng phiên bản tùy chỉnh của LLVM/Clang để thực hiện kỹ thuật HWASanIO. Do kích thước mã nguồn quá lớn, chúng tôi không lưu trữ trực tiếp trong repository này.

Để tải mã nguồn đầy đủ, vui lòng clone từ repository gốc hoặc sử dụng script `setup.sh` trong thư mục `hwasanio_repo`:

```bash
git clone https://github.com/Fraunhofer-AISEC/hwasanio-llvm-project.git hwasanio-llvm-project
```

Hoặc chạy:
```bash
cd hwasanio_repo
./setup.sh
```

## Hướng dẫn chạy thực nghiệm

Vui lòng tham khảo Chương 3 trong báo cáo `Report IT5440 - Group 5.md` để biết chi tiết các bước thiết lập môi trường và chạy kịch bản kiểm thử.
