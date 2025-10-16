import math
import random
import time

def measure_runtime(func):
    """
    Một decorator để đo lường và in ra thời gian thực thi của một hàm.
    Nó sử dụng time.perf_counter() để có độ chính xác cao nhất.
    """
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        runtime = end_time - start_time
        print(f"---")
        print(f"Hàm '{func.__name__}' đã chạy trong: {runtime:.6f} giây.")
        print(f"---")
        return result
    return wrapper

# --- HÀM HỖ TRỢ TOÁN HỌC ---

def gcd(a, b):
    """Tính ước chung lớn nhất (GCD) bằng thuật toán Euclid."""
    while b:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    """Tính nghịch đảo modulo d = e^(-1) mod phi."""
    return pow(e, -1, phi)

# --- BƯỚC 1: TẠO MỘT CẶP KHÓA RSA NHỎ ĐỂ LÀM MỤC TIÊU ---

# Chọn hai số nguyên tố nhỏ (trong thực tế, chúng rất lớn)
p = 4093
q = 4091
print(f"--- 1. Tạo khóa RSA mục tiêu ---")
print(f"Số nguyên tố bí mật: p = {p}, q = {q}")

# Tính N và phi(N)
N = p * q
phi_N = (p - 1) * (q - 1)
print(f"Khóa công khai N = p * q = {N}")
print(f"Giá trị phi(N) = (p-1)*(q-1) = {phi_N}")

# Chọn khóa công khai e
e = 13 # e phải là số nguyên tố cùng nhau với phi_N
print(f"Khóa công khai e = {e}")

# Tính khóa bí mật d (Đây là thứ chúng ta sẽ cố gắng tìm)
d_original = mod_inverse(e, phi_N)
print(f"Khóa bí mật gốc d = {d_original}\n")


# --- BƯỚC 2: MÔ PHỎNG THUẬT TOÁN SHOR ĐỂ TÌM p VÀ q ---

@measure_runtime
def find_period_classically(a, N):
    """
    HÀM "GIẢ LẬP" LƯỢNG TỬ: Tìm chu kỳ r của a^x mod N.
    Đây là bước mà máy tính lượng tử thực hiện SIÊU NHANH bằng
    Biến đổi Fourier Lượng tử (QFT).
    Trên máy tính cổ điển, bước này rất chậm và là nút thắt cổ chai.
    """
    if gcd(a, N) != 1:
        return None # Không cần tìm chu kỳ nếu a không nguyên tố cùng nhau với N

    x = 1
    while True:
        # pow(a, x, N) là a^x mod N
        if pow(a, x, N) == 1:
            return x
        x += 1

@measure_runtime
def simulate_shors(N):
    """Mô phỏng logic của thuật toán Shor để phân tích N thành thừa số."""
    print("--- 2. Bắt đầu mô phỏng thuật toán Shor ---")
    
    while True:
        # Bước 1 (Cổ điển): Chọn một số ngẫu nhiên a < N
        a = random.randint(2, N - 1)
        print(f"\nChọn số ngẫu nhiên a = {a}")

        # Bước 2 (Cổ điển): Kiểm tra gcd(a, N). Nếu > 1, ta đã may mắn tìm được một thừa số.
        common_divisor = gcd(a, N)
        if common_divisor > 1:
            print(f"May mắn! gcd(a, N) = {common_divisor}, đã tìm thấy một thừa số.")
            p_found = common_divisor
            q_found = N // p_found
            return p_found, q_found

        # Bước 3 (LƯỢNG TỬ): Tìm chu kỳ 'r' của hàm f(x) = a^x mod N.
        # Đây là bước "ma thuật" mà chúng ta giả lập bằng hàm cổ điển.
        print("Bắt đầu bước 'lượng tử' (giả lập) để tìm chu kỳ r...")
        r = find_period_classically(a, N)
        print(f"Đã tìm thấy chu kỳ r = {r}")

        # Bước 4 (Cổ điển): Kiểm tra các điều kiện của r
        if r % 2 != 0:
            print(f"Chu kỳ r = {r} là số lẻ. Thử lại với a khác.")
            continue # Quay lại vòng lặp, chọn a khác

        x = pow(a, r // 2, N)
        if x == N - 1: # Tương đương x == -1 (mod N)
            print(f"a^(r/2) mod N = -1. Thử lại với a khác.")
            continue # Quay lại vòng lặp, chọn a khác
            
        # Bước 5 (Cổ điển): Tính các thừa số
        # p = gcd(a^(r/2) - 1, N)
        # q = gcd(a^(r/2) + 1, N)
        p_found = gcd(x - 1, N)
        q_found = gcd(x + 1, N)
        
        if p_found * q_found == N and p_found != 1 and q_found != 1:
            print("Phân tích thành công!")
            return p_found, q_found
        else:
            print("Tìm thấy thừa số không tầm thường. Thử lại với a khác.")
            # Đôi khi có thể tìm thấy p=1 hoặc q=1, cần thử lại.

# Chạy mô phỏng Shor
p_found, q_found = simulate_shors(N)
print(f"\nKết quả từ thuật toán Shor: p = {p_found}, q = {q_found}\n")

# --- BƯỚC 3: TÍNH KHÓA BÍ MẬT TỪ CÁC THỪA SỐ ĐÃ TÌM ĐƯỢC ---

print("--- 3. Phá vỡ RSA: Tính lại khóa bí mật d ---")
# Kẻ tấn công giờ đã có p và q. Họ có thể tính phi(N).
phi_N_cracked = (p_found - 1) * (q_found - 1)
print(f"Tính lại phi(N) từ p và q đã tìm được: phi_N = {phi_N_cracked}")

# Từ phi(N) và khóa công khai e, kẻ tấn công tính khóa bí mật d
d_cracked = mod_inverse(e, phi_N_cracked)
print(f"Tính lại khóa bí mật: d_cracked = {d_cracked}")


# --- KIỂM TRA KẾT QUẢ ---
print("\n--- SO SÁNH KẾT QUẢ ---")
print(f"Khóa bí mật gốc: {d_original}")
print(f"Khóa bí mật đã phá: {d_cracked}")

if d_original == d_cracked:
    print("\n✅ THÀNH CÔNG: Đã phá vỡ thành công khóa RSA bằng cách mô phỏng thuật toán Shor!")
else:
    print("\n❌ THẤT BẠI: Quá trình mô phỏng có lỗi.")
    