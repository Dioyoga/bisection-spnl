import streamlit as st
import sympy as sp

st.title("Solusi SPNL dengan Metode Bisection")
st.write("Metode Bisection digunakan untuk mencari akar dari fungsi nonlinear.")

# Input fungsi
f_input = st.text_input("Masukkan fungsi f(x):", "x**3 - 4*x + 1")

# Input interval
a = st.number_input("Batas bawah (a):", value=0.0)
b = st.number_input("Batas atas (b):", value=1.0)

# Input toleransi
tol = st.number_input("Toleransi error:", value=1e-6, format="%.10f")
max_iter = st.number_input("Maksimal iterasi:", value=50)

x = sp.symbols('x')

def bisection(f, a, b, tol, max_iter):
    fa = f.subs(x, a)
    fb = f.subs(x, b)
    
    if fa * fb > 0:
        return None, "Tidak ada perubahan tanda pada interval — metode tidak valid."

    for i in range(max_iter):
        c = (a + b) / 2
        fc = f.subs(x, c)
        
        if abs(fc) < tol or (b - a)/2 < tol:
            return float(c), f"Akar ditemukan pada iterasi ke-{i+1}"
        
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
    
    return float(c), "Maksimal iterasi tercapai."

if st.button("Hitung Akar"):
    f = sp.sympify(f_input)
    akar, info = bisection(f, a, b, tol, max_iter)

    if akar is None:
        st.error(info)
    else:
        st.success(f"Akar: {akar}")
        st.info(info)
