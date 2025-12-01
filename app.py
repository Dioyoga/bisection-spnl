# app.py
import streamlit as st
import sympy as sp
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

st.set_page_config(page_title="Solusi SPNL - Metode Bisection", layout="centered")

st.title("Solusi Persamaan Non-Linear (Metode Bisection)")
st.write("Masukkan fungsi f(x) dan interval [a,b] dimana f(a) dan f(b) berbeda tanda.")

# Input
f_input = st.text_input("Masukkan fungsi f(x) (contoh: x**3 - 4*x + 1):", value="x**3 - 4*x + 1")
col1, col2 = st.columns(2)
with col1:
    a = st.number_input("Batas bawah a", value=0.0, format="%.6f")
with col2:
    b = st.number_input("Batas atas b", value=1.0, format="%.6f")
tol = st.number_input("Toleransi (epsilon)", value=1e-6, format="%.10f")
max_iter = st.number_input("Max iterasi", min_value=1, value=50, step=1)

# Parse fungsi dengan sympy
x = sp.symbols('x')
try:
    expr = sp.sympify(f_input)
    f_lamb = sp.lambdify(x, expr, 'numpy')
    func_ok = True
except Exception as e:
    st.error(f"Error parsing fungsi: {e}")
    func_ok = False

def bisection(f, a, b, tol=1e-6, max_iter=50):
    fa = f(a)
    fb = f(b)
    if math.isnan(fa) or math.isnan(fb):
        return {"error": "f(a) atau f(b) bukan angka (NaN). Periksa domain fungsi."}
    if fa * fb > 0:
        return {"error": "f(a) dan f(b) harus memiliki tanda berlawanan."}
    rows = []
    for i in range(1, max_iter+1):
        c = (a + b) / 2.0
        fc = f(c)
        rows.append({"iter": i, "a": a, "b": b, "c": c, "f(a)": fa, "f(b)": fb, "f(c)": fc, "interval_length": b - a})
        if abs(fc) < tol or (b-a)/2 < tol:
            return {"result": c, "f(c)": fc, "iterations": i, "table": pd.DataFrame(rows)}
        # update interval
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
    # jika mencapai batas iterasi
    return {"result": (a+b)/2, "f(c)": f((a+b)/2), "iterations": max_iter, "table": pd.DataFrame(rows), "warning": "Max iter reached"}

if st.button("Jalankan Bisection") and func_ok:
    with st.spinner("Menjalankan metode..."):
        try:
            res = bisection(f_lamb, float(a), float(b), tol=float(tol), max_iter=int(max_iter))
        except Exception as e:
            st.error(f"Terjadi error saat menjalankan metode: {e}")
            st.stop()

    if "error" in res:
        st.error(res["error"])
    else:
        st.success(f"Akar aproksimasi: {res['result']:.10f}")
        st.write(f"f(akar) ≈ {res['f(c)']:.4e}")
        st.write(f"Iterasi: {res['iterations']}")
        if res.get("warning"):
            st.warning(res["warning"])

        # show table
        df = res["table"]
        st.subheader("Tabel Iterasi")
        st.dataframe(df.style.format({"a":"{:.8f}","b":"{:.8f}","c":"{:.8f}","f(a)":"{:.6e}","f(b)":"{:.6e}","f(c)":"{:.6e}","interval_length":"{:.8e}"}))

        # plot konvergensi c vs iter
        fig, ax = plt.subplots()
        ax.plot(df["iter"], df["c"], marker='o')
        ax.set_xlabel("Iterasi")
        ax.set_ylabel("Nilai c (aproks)")
        ax.set_title("Konvergensi akar terhadap iterasi")
        ax.grid(True)
        st.pyplot(fig)

        # plot interval length vs iter (log scale)
        fig2, ax2 = plt.subplots()
        ax2.semilogy(df["iter"], df["interval_length"], marker='o')
        ax2.set_xlabel("Iterasi")
        ax2.set_ylabel("Panjang interval (log scale)")
        ax2.set_title("Panjang interval vs Iterasi")
        ax2.grid(True, which='both')
        st.pyplot(fig2)

# Footer: tips
st.markdown("---")
st.write("Tips: Pastikan f(a) dan f(b) memiliki tanda berlawanan. Untuk fungsi dengan domain terbatas (log, sqrt), pilih interval yang valid.")

