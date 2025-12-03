#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Định nghĩa struct có 2 trường nằm cạnh nhau
struct UserData {
    char name[10];
    int secret_id;
};

int main() {
    printf("=== HWASanIO Reproduction Demo ===\n");
    
    // Cấp phát bộ nhớ cho struct
    struct UserData *user = (struct UserData*)malloc(sizeof(struct UserData));
    
    if (!user) {
        perror("Malloc failed");
        return 1;
    }

    // Gán giá trị ban đầu
    user->secret_id = 12345;
    printf("Original Secret ID: %d\n", user->secret_id);

    // LỖI: Ghi tràn từ trường 'name' (10 bytes) sang 'secret_id'
    // HWASan thường (không có IO) sẽ KHÔNG bắt được lỗi này vì nó vẫn nằm trong vùng nhớ của struct UserData.
    // HWASanIO sẽ bắt được nhờ Memory Shading (name và secret_id có Shade khác nhau).
    printf("Attempting intra-object overflow...\n");
    
    // Ghi 16 bytes vào name (tràn 6 bytes sang secret_id)
    // Dùng pointer arithmetic để giả lập việc truy cập mảng không an toàn
    char *ptr = user->name;
    for (int i = 0; i < 16; i++) {
        ptr[i] = 'A'; 
    }
    
    printf("Overwritten Secret ID: %d\n", user->secret_id);
    
    free(user);
    return 0;
}
