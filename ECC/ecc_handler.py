# Định nghĩa các hàm cần thiết (đã có trong mã trước)
def gf_add(a, b, p=31):
    return (a + b) % p

def gf_sub(a, b, p=31):
    return (a - b) % p

def gf_mult(a, b, p=31):
    return (a * b) % p

def gf_inverse(a, p=31):
    if a == 0:
        return 0
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    _, x, _ = extended_gcd(a, p)
    return x % p

class Point:
    def __init__(self, x, y, infinity=False):
        self.x = x
        self.y = y
        self.infinity = infinity

    def __str__(self):
        if self.infinity:
            return "Point(infinity)"
        return f"Point({self.x}, {self.y})"

a = 1
b = 1
p = 31

def is_on_curve(point):
    if point.infinity:
        return True
    left = gf_mult(point.y, point.y, p)
    right = gf_add(gf_add(gf_mult(point.x, gf_mult(point.x, point.x, p), p), gf_mult(a, point.x, p)), b, p)
    return left == right

def point_add(P, Q):
    if P.infinity:
        return Q
    if Q.infinity:
        return P
    if P.x == Q.x and P.y != Q.y:
        return Point(0, 0, True)
    if P.x == Q.x and P.y == Q.y:
        if P.y == 0:
            return Point(0, 0, True)
        lam = gf_mult(gf_add(gf_mult(3, gf_mult(P.x, P.x)), a), gf_inverse(gf_add(P.y, P.y)))
        x_r = gf_sub(gf_add(gf_mult(lam, lam), gf_mult(-2, P.x)), a)
        y_r = gf_sub(gf_mult(lam, gf_sub(P.x, x_r)), P.y)
    else:
        lam = gf_mult(gf_sub(Q.y, P.y), gf_inverse(gf_sub(Q.x, P.x)))
        x_r = gf_sub(gf_sub(gf_mult(lam, lam), P.x), Q.x)
        y_r = gf_sub(gf_mult(lam, gf_sub(P.x, x_r)), P.y)
    return Point(x_r, y_r)

def point_mult(k, P):
    result = Point(0, 0, True)
    temp = P
    while k > 0:
        if k & 1:
            result = point_add(result, temp)
        temp = point_add(temp, temp)
        k >>= 1
    return result

# Kiểm tra điểm (0, 1)
G = Point(0, 1)
print(f"Điểm cơ sở G: {G}")
print(f"Điểm (0, 1) có thuộc đường cong? {is_on_curve(G)}")

# Tính một vài bội số để kiểm tra bậc
for k in range(1, 10):
    kG = point_mult(k, G)
    print(f"{k}G = {kG}, thuộc đường cong? {is_on_curve(kG)}")