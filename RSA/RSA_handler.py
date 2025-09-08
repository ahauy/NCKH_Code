import random
# import base64

# chọn 2 số nguyên tố p và q
p = 11
q = 53

# thông điệp muốn mã hoá
mes = 'hello guy !!!'

# thuật toán tìm ước chung lớn nhất
def gcd(a, b): # 6, 8
  return gcd(b, a % b) if b else a
'''
8, 6
6, 2
2, 0
-> 2
'''

# thuật toán tìm bội chung nhỏ nhất
def lcm(a, b):
  return a * b // gcd(a, b)

# chương trình tìm số nghịch đảo
def modInverse(a, m): # a^-1 mod m
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    b = m
    while b > 0:
        q = a // b
        r = a % b
        x = x0 - x1 * q
        y = y0 - y1 * q
        a, b = b, r
        x0, x1 = x1, x
        y0, y1 = y1, y
    if a != 1:
        return None  # không tồn tại nghịch đảo
    return x0 % m

# chương trình tính số mũ - thuật toán bình phương và nhân
# có thể dùng hàm pow trong python luôn
def binhPhuong(x, n, m): # x^n mod m
  if n == 0:
    return 1
  p = binhPhuong(x, n // 2, m) # n // 2: chia lấy phần nguyên
  if n % 2 == 0:
    return (p * p) % m
  else:
    return (p * p * x) % m
'''
2^11 mod 7
-> 11 = 1011
p = binhPhuong(2, 5, 7)
p = binhPhuong(2, 2, 7)
p = binhPhuong(2, 1, 7)
p = binhPhuong(2, 0, 7)
-> binhPhuong(2, 0, 7) = 1
binhPhuong(2, 1, 7) = (1 * 1 * 2) mod 7 = 2
binhPhuong(2, 2, 7) = (2 * 2) mod 7 = 4
p = binhPhuong(2, 5, 7) = (4 * 4 * 2) mod 7 = 4
'''

# thuật toán sinh một số ngẫu nhiên trong đoạn [a, b]
def randomNumber(a, b):
  return random.randint(a, b)

# thuật toán chuyển 1 chuỗi văn bản thành dạng số
def mesToInt(mes: str) -> int: # (mes) thôi cũng được nhưng có sẽ giúp code tường minh hơn
  return int.from_bytes(mes.encode(), 'big')

# chuyển số về chuỗi
def intToMes(num: int) -> str:
  length = (num.bit_length() + 7) // 8
  return num.to_bytes(length, 'big').decode(errors='ignore')

# thuật toán sinh khoá
def generateKey():
  n = p * q
  phiCarmichael_n = lcm(p - 1, q - 1) # có thể dùng hàm phi_euler
  phiEuler_n = (p - 1) * (q - 1)
  # Sinh ngẫu nhiên e, sao cho: gcd(e, phiCarmichael_n) = 1
  e = randomNumber(2, phiCarmichael_n - 1)
  while True:
    if gcd(e, phiCarmichael_n) == 1:
      break
    else:
      e = randomNumber(2, phiCarmichael_n - 1)
  # tính khoá bí mật d = e^-1 mod phiCarmichael_n
  d = modInverse(e, phiCarmichael_n)
  return (e, n), (d, n)

# Mã hóa
def encrypt(publicKey, plaintext: str):
    e, n = publicKey
    blocks = [pow(ord(ch), e, n) for ch in plaintext]
    '''
    blocks = [pow(ord(ch), e, n) for ch in plaintext] 
    tương tự như:
    blocks = []
    for ch in plaintext:
      blocks.append(pow(ord(ch), e, n))
    '''
    return blocks

# Giải mã
def decrypt(privateKey, ciphertext: list[int]):
    d, n = privateKey
    chars = [chr(pow(c, d, n)) for c in ciphertext] # chr() giúp chuyển số thành chứ: 104 = h
    return ''.join(chars)

# --- Demo ---
publicKey, privateKey = generateKey()
cipher = encrypt(publicKey, mes)
plain = decrypt(privateKey, cipher)

print(f"Công khai (e, n): {publicKey}")
print(f"Bí mật (d, n): {privateKey}")
print(f"Mã hóa: {cipher}")
print(f"Giải mã: {plain}")
