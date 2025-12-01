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

