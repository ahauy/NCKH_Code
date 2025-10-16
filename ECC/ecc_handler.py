# thiết lập các tham số cho đường cong Weierstras:
p = 31
a = 0
b = 7

# khai báo điểm cơ sở đã được tính toán từ trước:
G = (15, 13)

# các hàm toán học 

# n^-1 (mod mod)
def mod_inverse(n, mod):
  return pow(n, -1, mod)

# cộng điểm
def add_point(P, Q):
  # None đại diện cho điểm vô cực
  if P is None:
    return Q
  if Q is None:
    return P

  xp, yp = P
  xq, yq = Q

  if xp == xq and yp != yq:
    return None

  # cộng 2 điểm
  if P == Q: # nhân đôi điểm
    numerator = (3 * xp**2 + a) % p #tử số
    denominator = (2 * yp) % p #mẫu số
  else:
    numerator = (yp - yq) % p
    denominator = (xp - xq) % p
  
  inv_denominator = mod_inverse(denominator, p);

  m = (numerator * inv_denominator) % p

  xr = (m**2 - xp - xq) % p
  yr = (m*(xp - xr) - yp) % p 

  return (xr, yr)

def scalar_multiply(k, P):
    """Thực hiện phép nhân vô hướng k * P bằng thuật toán Double-and-Add."""
    result = None  # Điểm vô cực
    current = P
    
    # Chuyển k sang dạng nhị phân
    binary_k = bin(k)[2:]
    
    # Lặp từ phải qua trái của chuỗi nhị phân
    for bit in reversed(binary_k):
        if bit == '1':
          result = add_point(result, current)
        current = add_point(current, current) # Nhân đôi điểm
        
    return result

# --- 3. QUÁ TRÌNH MÃ HÓA VÀ GIẢI MÃ ---

# --- Phía Alice: Tạo khóa ---
priv_key_A = 7  # Alice chọn khóa bí mật (một số nguyên)
pub_key_A = scalar_multiply(priv_key_A, G)

print("--- Quá trình tạo khóa của Alice ---")
print(f"Khóa bí mật của Alice: {priv_key_A}")
print(f"Khóa công khai của Alice (priv_key * G): {pub_key_A}\n")

# --- Phía Bob: Mã hóa tin nhắn ---
# Giả sử tin nhắn M là một điểm trên đường cong
# (20^3 + 2*20 + 3) mod 31 = 4. Và 2^2 mod 31 = 4
M = (20, 2)
k = 6 # Bob chọn một số ngẫu nhiên k

# Tính toán bản mã (C1, C2)
C1 = scalar_multiply(k, G)
C2 = add_point(M, scalar_multiply(k, pub_key_A))
ciphertext = (C1, C2)

print("--- Quá trình mã hóa của Bob ---")
print(f"Tin nhắn gốc M (là một điểm): {M}")
print(f"Bob chọn số ngẫu nhiên k = {k}")
print(f"Tính C1 = k * G = {C1}")
print(f"Tính C2 = M + k * pub_key_A = {C2}")
print(f"Bản mã được gửi đi: {ciphertext}\n")


# --- Phía Alice: Giải mã tin nhắn ---
# Alice nhận được bản mã (C1, C2)

# 1. Tính điểm S = priv_key_A * C1
S = scalar_multiply(priv_key_A, C1)

# 2. Để lấy lại M, tính M = C2 - S
# C2 - S tương đương với C2 + (-S)
# Nếu S = (x, y) thì -S = (x, p - y)
S_neg = (S[0], p - S[1])

# Giải mã tin nhắn
decrypted_M = add_point(C2, S_neg)

print("--- Quá trình giải mã của Alice ---")
print(f"Alice nhận được bản mã: {ciphertext}")
print(f"Alice tính S = priv_key_A * C1 = {S}")
print(f"Alice tính điểm đối của S: -S = {S_neg}")
print(f"Alice giải mã: Decrypted_M = C2 + (-S) = {decrypted_M}\n")


# --- 4. KIỂM TRA KẾT QUẢ ---
print("--- Kết quả cuối cùng ---")
print(f"Tin nhắn gốc:   {M}")
print(f"Tin nhắn giải mã: {decrypted_M}")

if M == decrypted_M:
    print("✅ THÀNH CÔNG: Tin nhắn giải mã trùng khớp với tin nhắn gốc.")
else:
    print("❌ THẤT BẠI: Có lỗi trong quá trình giải mã.")