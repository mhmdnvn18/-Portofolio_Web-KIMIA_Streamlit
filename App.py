import streamlit as st
import pandas as pd
import requests
import json

# =============================================================================
# Konfigurasi Halaman dan Data
# =============================================================================

# Mengatur konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Tabel Periodik Pro",
    page_icon="⚛️",
    layout="wide"
)

# Data lengkap elemen-elemen periodik
# Data ini sama dengan versi JavaScript, sekarang dalam format Python
ELEMENTS_DATA = [
    {'symbol': 'H', 'name': 'Hidrogen', 'atomicNumber': 1, 'atomicMass': 1.008, 'category': 'reactive-nonmetal', 'row': 1, 'col': 1, 'electronConfiguration': '1s¹', 'electronegativity': 2.20, 'meltingPoint': '13.83 K', 'boilingPoint': '20.27 K'},
    {'symbol': 'He', 'name': 'Helium', 'atomicNumber': 2, 'atomicMass': 4.0026, 'category': 'noble-gas', 'row': 1, 'col': 18, 'electronConfiguration': '1s²', 'electronegativity': None, 'meltingPoint': '0.95 K', 'boilingPoint': '4.22 K'},
    {'symbol': 'Li', 'name': 'Litium', 'atomicNumber': 3, 'atomicMass': 6.94, 'category': 'alkali-metal', 'row': 2, 'col': 1, 'electronConfiguration': '[He] 2s¹', 'electronegativity': 0.98, 'meltingPoint': '453.65 K', 'boilingPoint': '1615 K'},
    {'symbol': 'Be', 'name': 'Berilium', 'atomicNumber': 4, 'atomicMass': 9.0122, 'category': 'alkaline-earth-metal', 'row': 2, 'col': 2, 'electronConfiguration': '[He] 2s²', 'electronegativity': 1.57, 'meltingPoint': '1560 K', 'boilingPoint': '2742 K'},
    {'symbol': 'B', 'name': 'Boron', 'atomicNumber': 5, 'atomicMass': 10.81, 'category': 'metalloid', 'row': 2, 'col': 13, 'electronConfiguration': '[He] 2s² 2p¹', 'electronegativity': 2.04, 'meltingPoint': '2349 K', 'boilingPoint': '4200 K'},
    {'symbol': 'C', 'name': 'Karbon', 'atomicNumber': 6, 'atomicMass': 12.011, 'category': 'reactive-nonmetal', 'row': 2, 'col': 14, 'electronConfiguration': '[He] 2s² 2p²', 'electronegativity': 2.55, 'meltingPoint': '3800 K', 'boilingPoint': '5100 K'},
    {'symbol': 'N', 'name': 'Nitrogen', 'atomicNumber': 7, 'atomicMass': 14.007, 'category': 'reactive-nonmetal', 'row': 2, 'col': 15, 'electronConfiguration': '[He] 2s² 2p³', 'electronegativity': 3.04, 'meltingPoint': '63.15 K', 'boilingPoint': '77.36 K'},
    {'symbol': 'O', 'name': 'Oksigen', 'atomicNumber': 8, 'atomicMass': 15.999, 'category': 'reactive-nonmetal', 'row': 2, 'col': 16, 'electronConfiguration': '[He] 2s² 2p⁴', 'electronegativity': 3.44, 'meltingPoint': '54.36 K', 'boilingPoint': '90.18 K'},
    {'symbol': 'F', 'name': 'Fluorin', 'atomicNumber': 9, 'atomicMass': 18.998, 'category': 'reactive-nonmetal', 'row': 2, 'col': 17, 'electronConfiguration': '[He] 2s² 2p⁵', 'electronegativity': 3.98, 'meltingPoint': '53.48 K', 'boilingPoint': '85.03 K'},
    {'symbol': 'Ne', 'name': 'Neon', 'atomicNumber': 10, 'atomicMass': 20.180, 'category': 'noble-gas', 'row': 2, 'col': 18, 'electronConfiguration': '[He] 2s² 2p⁶', 'electronegativity': None, 'meltingPoint': '24.56 K', 'boilingPoint': '27.07 K'},
    {'symbol': 'Na', 'name': 'Natrium', 'atomicNumber': 11, 'atomicMass': 22.990, 'category': 'alkali-metal', 'row': 3, 'col': 1, 'electronConfiguration': '[Ne] 3s¹', 'electronegativity': 0.93, 'meltingPoint': '370.94 K', 'boilingPoint': '1156 K'},
    {'symbol': 'Mg', 'name': 'Magnesium', 'atomicNumber': 12, 'atomicMass': 24.305, 'category': 'alkaline-earth-metal', 'row': 3, 'col': 2, 'electronConfiguration': '[Ne] 3s²', 'electronegativity': 1.31, 'meltingPoint': '923 K', 'boilingPoint': '1363 K'},
    {'symbol': 'Al', 'name': 'Aluminium', 'atomicNumber': 13, 'atomicMass': 26.982, 'category': 'post-transition-metal', 'row': 3, 'col': 13, 'electronConfiguration': '[Ne] 3s² 3p¹', 'electronegativity': 1.61, 'meltingPoint': '933.47 K', 'boilingPoint': '2792 K'},
    {'symbol': 'Si', 'name': 'Silikon', 'atomicNumber': 14, 'atomicMass': 28.085, 'category': 'metalloid', 'row': 3, 'col': 14, 'electronConfiguration': '[Ne] 3s² 3p²', 'electronegativity': 1.90, 'meltingPoint': '1687 K', 'boilingPoint': '3538 K'},
    {'symbol': 'P', 'name': 'Fosfor', 'atomicNumber': 15, 'atomicMass': 30.974, 'category': 'reactive-nonmetal', 'row': 3, 'col': 15, 'electronConfiguration': '[Ne] 3s² 3p³', 'electronegativity': 2.19, 'meltingPoint': '317.3 K', 'boilingPoint': '553.7 K'},
    {'symbol': 'S', 'name': 'Belerang', 'atomicNumber': 16, 'atomicMass': 32.06, 'category': 'reactive-nonmetal', 'row': 3, 'col': 16, 'electronConfiguration': '[Ne] 3s² 3p⁴', 'electronegativity': 2.58, 'meltingPoint': '388.36 K', 'boilingPoint': '717.8 K'},
    {'symbol': 'Cl', 'name': 'Klorin', 'atomicNumber': 17, 'atomicMass': 35.45, 'category': 'reactive-nonmetal', 'row': 3, 'col': 17, 'electronConfiguration': '[Ne] 3s² 3p⁵', 'electronegativity': 3.16, 'meltingPoint': '171.6 K', 'boilingPoint': '239.11 K'},
    {'symbol': 'Ar', 'name': 'Argon', 'atomicNumber': 18, 'atomicMass': 39.948, 'category': 'noble-gas', 'row': 3, 'col': 18, 'electronConfiguration': '[Ne] 3s² 3p⁶', 'electronegativity': None, 'meltingPoint': '83.81 K', 'boilingPoint': '87.30 K'},
    {'symbol': 'K', 'name': 'Kalium', 'atomicNumber': 19, 'atomicMass': 39.098, 'category': 'alkali-metal', 'row': 4, 'col': 1, 'electronConfiguration': '[Ar] 4s¹', 'electronegativity': 0.82, 'meltingPoint': '336.53 K', 'boilingPoint': '1032 K'},
    {'symbol': 'Ca', 'name': 'Kalsium', 'atomicNumber': 20, 'atomicMass': 40.078, 'category': 'alkaline-earth-metal', 'row': 4, 'col': 2, 'electronConfiguration': '[Ar] 4s²', 'electronegativity': 1.00, 'meltingPoint': '1115 K', 'boilingPoint': '1757 K'},
    {'symbol': 'Sc', 'name': 'Skandium', 'atomicNumber': 21, 'atomicMass': 44.956, 'category': 'transition-metal', 'row': 4, 'col': 3, 'electronConfiguration': '[Ar] 3d¹ 4s²', 'electronegativity': 1.36, 'meltingPoint': '1814 K', 'boilingPoint': '3109 K'},
    {'symbol': 'Ti', 'name': 'Titanium', 'atomicNumber': 22, 'atomicMass': 47.867, 'category': 'transition-metal', 'row': 4, 'col': 4, 'electronConfiguration': '[Ar] 3d² 4s²', 'electronegativity': 1.54, 'meltingPoint': '1941 K', 'boilingPoint': '3560 K'},
    {'symbol': 'V', 'name': 'Vanadium', 'atomicNumber': 23, 'atomicMass': 50.942, 'category': 'transition-metal', 'row': 4, 'col': 5, 'electronConfiguration': '[Ar] 3d³ 4s²', 'electronegativity': 1.63, 'meltingPoint': '2183 K', 'boilingPoint': '3680 K'},
    {'symbol': 'Cr', 'name': 'Kromium', 'atomicNumber': 24, 'atomicMass': 51.996, 'category': 'transition-metal', 'row': 4, 'col': 6, 'electronConfiguration': '[Ar] 3d⁵ 4s¹', 'electronegativity': 1.66, 'meltingPoint': '2180 K', 'boilingPoint': '2944 K'},
    {'symbol': 'Mn', 'name': 'Mangan', 'atomicNumber': 25, 'atomicMass': 54.938, 'category': 'transition-metal', 'row': 4, 'col': 7, 'electronConfiguration': '[Ar] 3d⁵ 4s²', 'electronegativity': 1.55, 'meltingPoint': '1519 K', 'boilingPoint': '2334 K'},
    {'symbol': 'Fe', 'name': 'Besi', 'atomicNumber': 26, 'atomicMass': 55.845, 'category': 'transition-metal', 'row': 4, 'col': 8, 'electronConfiguration': '[Ar] 3d⁶ 4s²', 'electronegativity': 1.83, 'meltingPoint': '1811 K', 'boilingPoint': '3134 K'},
    {'symbol': 'Co', 'name': 'Kobalt', 'atomicNumber': 27, 'atomicMass': 58.933, 'category': 'transition-metal', 'row': 4, 'col': 9, 'electronConfiguration': '[Ar] 3d⁷ 4s²', 'electronegativity': 1.88, 'meltingPoint': '1768 K', 'boilingPoint': '3200 K'},
    {'symbol': 'Ni', 'name': 'Nikel', 'atomicNumber': 28, 'atomicMass': 58.693, 'category': 'transition-metal', 'row': 4, 'col': 10, 'electronConfiguration': '[Ar] 3d⁸ 4s²', 'electronegativity': 1.91, 'meltingPoint': '1728 K', 'boilingPoint': '3186 K'},
    {'symbol': 'Cu', 'name': 'Tembaga', 'atomicNumber': 29, 'atomicMass': 63.546, 'category': 'transition-metal', 'row': 4, 'col': 11, 'electronConfiguration': '[Ar] 3d¹⁰ 4s¹', 'electronegativity': 1.90, 'meltingPoint': '1357.77 K', 'boilingPoint': '2835 K'},
    {'symbol': 'Zn', 'name': 'Seng', 'atomicNumber': 30, 'atomicMass': 65.38, 'category': 'transition-metal', 'row': 4, 'col': 12, 'electronConfiguration': '[Ar] 3d¹⁰ 4s²', 'electronegativity': 1.65, 'meltingPoint': '692.68 K', 'boilingPoint': '1180 K'},
    {'symbol': 'Ga', 'name': 'Galium', 'atomicNumber': 31, 'atomicMass': 69.723, 'category': 'post-transition-metal', 'row': 4, 'col': 13, 'electronConfiguration': '[Ar] 3d¹⁰ 4s² 4p¹', 'electronegativity': 1.81, 'meltingPoint': '302.91 K', 'boilingPoint': '2477 K'},
    {'symbol': 'Ge', 'name': 'Germanium', 'atomicNumber': 32, 'atomicMass': 72.630, 'category': 'metalloid', 'row': 4, 'col': 14, 'electronConfiguration': '[Ar] 3d¹⁰ 4s² 4p²', 'electronegativity': 2.01, 'meltingPoint': '1211.40 K', 'boilingPoint': '3106 K'},
    {'symbol': 'As', 'name': 'Arsen', 'atomicNumber': 33, 'atomicMass': 74.922, 'category': 'metalloid', 'row': 4, 'col': 15, 'electronConfiguration': '[Ar] 3d¹⁰ 4s² 4p³', 'electronegativity': 2.18, 'meltingPoint': '1090 K', 'boilingPoint': '887 K'},
    {'symbol': 'Se', 'name': 'Selenium', 'atomicNumber': 34, 'atomicMass': 78.971, 'category': 'reactive-nonmetal', 'row': 4, 'col': 16, 'electronConfiguration': '[Ar] 3d¹⁰ 4s² 4p⁴', 'electronegativity': 2.55, 'meltingPoint': '494 K', 'boilingPoint': '958 K'},
    {'symbol': 'Br', 'name': 'Bromin', 'atomicNumber': 35, 'atomicMass': 79.904, 'category': 'reactive-nonmetal', 'row': 4, 'col': 17, 'electronConfiguration': '[Ar] 3d¹⁰ 4s² 4p⁵', 'electronegativity': 2.96, 'meltingPoint': '265.8 K', 'boilingPoint': '332.0 K'},
    {'symbol': 'Kr', 'name': 'Kripton', 'atomicNumber': 36, 'atomicMass': 83.798, 'category': 'noble-gas', 'row': 4, 'col': 18, 'electronConfiguration': '[Ar] 3d¹⁰ 4s² 4p⁶', 'electronegativity': 3.00, 'meltingPoint': '115.79 K', 'boilingPoint': '119.93 K'},
    {'symbol': 'Rb', 'name': 'Rubidium', 'atomicNumber': 37, 'atomicMass': 85.468, 'category': 'alkali-metal', 'row': 5, 'col': 1, 'electronConfiguration': '[Kr] 5s¹', 'electronegativity': 0.82, 'meltingPoint': '312.46 K', 'boilingPoint': '961 K'},
    {'symbol': 'Sr', 'name': 'Stronsium', 'atomicNumber': 38, 'atomicMass': 87.62, 'category': 'alkaline-earth-metal', 'row': 5, 'col': 2, 'electronConfiguration': '[Kr] 5s²', 'electronegativity': 0.95, 'meltingPoint': '1050 K', 'boilingPoint': '1655 K'},
    {'symbol': 'Y', 'name': 'Itrium', 'atomicNumber': 39, 'atomicMass': 88.906, 'category': 'transition-metal', 'row': 5, 'col': 3, 'electronConfiguration': '[Kr] 4d¹ 5s²', 'electronegativity': 1.22, 'meltingPoint': '1799 K', 'boilingPoint': '3609 K'},
    {'symbol': 'Zr', 'name': 'Zirkonium', 'atomicNumber': 40, 'atomicMass': 91.224, 'category': 'transition-metal', 'row': 5, 'col': 4, 'electronConfiguration': '[Kr] 4d² 5s²', 'electronegativity': 1.33, 'meltingPoint': '2128 K', 'boilingPoint': '4682 K'},
    {'symbol': 'Nb', 'name': 'Niobium', 'atomicNumber': 41, 'atomicMass': 92.906, 'category': 'transition-metal', 'row': 5, 'col': 5, 'electronConfiguration': '[Kr] 4d⁴ 5s¹', 'electronegativity': 1.6, 'meltingPoint': '2750 K', 'boilingPoint': '5017 K'},
    {'symbol': 'Mo', 'name': 'Molibdenum', 'atomicNumber': 42, 'atomicMass': 95.95, 'category': 'transition-metal', 'row': 5, 'col': 6, 'electronConfiguration': '[Kr] 4d⁵ 5s¹', 'electronegativity': 2.16, 'meltingPoint': '2896 K', 'boilingPoint': '4912 K'},
    {'symbol': 'Tc', 'name': 'Teknesium', 'atomicNumber': 43, 'atomicMass': 98, 'category': 'transition-metal', 'row': 5, 'col': 7, 'electronConfiguration': '[Kr] 4d⁵ 5s²', 'electronegativity': 1.9, 'meltingPoint': '2430 K', 'boilingPoint': '4538 K'},
    {'symbol': 'Ru', 'name': 'Rutenium', 'atomicNumber': 44, 'atomicMass': 101.07, 'category': 'transition-metal', 'row': 5, 'col': 8, 'electronConfiguration': '[Kr] 4d⁷ 5s¹', 'electronegativity': 2.2, 'meltingPoint': '2607 K', 'boilingPoint': '4423 K'},
    {'symbol': 'Rh', 'name': 'Rodium', 'atomicNumber': 45, 'atomicMass': 102.91, 'category': 'transition-metal', 'row': 5, 'col': 9, 'electronConfiguration': '[Kr] 4d⁸ 5s¹', 'electronegativity': 2.28, 'meltingPoint': '2237 K', 'boilingPoint': '3968 K'},
    {'symbol': 'Pd', 'name': 'Paladium', 'atomicNumber': 46, 'atomicMass': 106.42, 'category': 'transition-metal', 'row': 5, 'col': 10, 'electronConfiguration': '[Kr] 4d¹⁰', 'electronegativity': 2.20, 'meltingPoint': '1828.05 K', 'boilingPoint': '3236 K'},
    {'symbol': 'Ag', 'name': 'Perak', 'atomicNumber': 47, 'atomicMass': 107.87, 'category': 'transition-metal', 'row': 5, 'col': 11, 'electronConfiguration': '[Kr] 4d¹⁰ 5s¹', 'electronegativity': 1.93, 'meltingPoint': '1234.93 K', 'boilingPoint': '2435 K'},
    {'symbol': 'Cd', 'name': 'Kadmium', 'atomicNumber': 48, 'atomicMass': 112.41, 'category': 'transition-metal', 'row': 5, 'col': 12, 'electronConfiguration': '[Kr] 4d¹⁰ 5s²', 'electronegativity': 1.69, 'meltingPoint': '594.22 K', 'boilingPoint': '1040 K'},
    {'symbol': 'In', 'name': 'Indium', 'atomicNumber': 49, 'atomicMass': 114.82, 'category': 'post-transition-metal', 'row': 5, 'col': 13, 'electronConfiguration': '[Kr] 4d¹⁰ 5s² 5p¹', 'electronegativity': 1.78, 'meltingPoint': '429.75 K', 'boilingPoint': '2345 K'},
    {'symbol': 'Sn', 'name': 'Timah', 'atomicNumber': 50, 'atomicMass': 118.71, 'category': 'post-transition-metal', 'row': 5, 'col': 14, 'electronConfiguration': '[Kr] 4d¹⁰ 5s² 5p²', 'electronegativity': 1.96, 'meltingPoint': '505.08 K', 'boilingPoint': '2875 K'},
    {'symbol': 'Sb', 'name': 'Antimon', 'atomicNumber': 51, 'atomicMass': 121.76, 'category': 'metalloid', 'row': 5, 'col': 15, 'electronConfiguration': '[Kr] 4d¹⁰ 5s² 5p³', 'electronegativity': 2.05, 'meltingPoint': '903.78 K', 'boilingPoint': '1860 K'},
    {'symbol': 'Te', 'name': 'Telurium', 'atomicNumber': 52, 'atomicMass': 127.60, 'category': 'metalloid', 'row': 5, 'col': 16, 'electronConfiguration': '[Kr] 4d¹⁰ 5s² 5p⁴', 'electronegativity': 2.1, 'meltingPoint': '722.66 K', 'boilingPoint': '1261 K'},
    {'symbol': 'I', 'name': 'Iodin', 'atomicNumber': 53, 'atomicMass': 126.90, 'category': 'reactive-nonmetal', 'row': 5, 'col': 17, 'electronConfiguration': '[Kr] 4d¹⁰ 5s² 5p⁵', 'electronegativity': 2.66, 'meltingPoint': '386.85 K', 'boilingPoint': '457.4 K'},
    {'symbol': 'Xe', 'name': 'Xenon', 'atomicNumber': 54, 'atomicMass': 131.29, 'category': 'noble-gas', 'row': 5, 'col': 18, 'electronConfiguration': '[Kr] 4d¹⁰ 5s² 5p⁶', 'electronegativity': 2.6, 'meltingPoint': '161.4 K', 'boilingPoint': '165.1 K'},
    {'symbol': 'Cs', 'name': 'Sesium', 'atomicNumber': 55, 'atomicMass': 132.91, 'category': 'alkali-metal', 'row': 6, 'col': 1, 'electronConfiguration': '[Xe] 6s¹', 'electronegativity': 0.79, 'meltingPoint': '301.59 K', 'boilingPoint': '944 K'},
    {'symbol': 'Ba', 'name': 'Barium', 'atomicNumber': 56, 'atomicMass': 137.33, 'category': 'alkaline-earth-metal', 'row': 6, 'col': 2, 'electronConfiguration': '[Xe] 6s²', 'electronegativity': 0.89, 'meltingPoint': '1000 K', 'boilingPoint': '2170 K'},
    {'symbol': 'La', 'name': 'Lantanum', 'atomicNumber': 57, 'atomicMass': 138.91, 'category': 'lanthanide', 'row': 9, 'col': 3, 'electronConfiguration': '[Xe] 5d¹ 6s²', 'electronegativity': 1.10, 'meltingPoint': '1193 K', 'boilingPoint': '3737 K'},
    {'symbol': 'Ce', 'name': 'Serium', 'atomicNumber': 58, 'atomicMass': 140.12, 'category': 'lanthanide', 'row': 9, 'col': 4, 'electronConfiguration': '[Xe] 4f¹ 5d¹ 6s²', 'electronegativity': 1.12, 'meltingPoint': '1068 K', 'boilingPoint': '3716 K'},
    {'symbol': 'Pr', 'name': 'Praseodimium', 'atomicNumber': 59, 'atomicMass': 140.91, 'category': 'lanthanide', 'row': 9, 'col': 5, 'electronConfiguration': '[Xe] 4f³ 6s²', 'electronegativity': 1.13, 'meltingPoint': '1208 K', 'boilingPoint': '3793 K'},
    {'symbol': 'Nd', 'name': 'Neodimium', 'atomicNumber': 60, 'atomicMass': 144.24, 'category': 'lanthanide', 'row': 9, 'col': 6, 'electronConfiguration': '[Xe] 4f⁴ 6s²', 'electronegativity': 1.14, 'meltingPoint': '1297 K', 'boilingPoint': '3347 K'},
    {'symbol': 'Pm', 'name': 'Prometium', 'atomicNumber': 61, 'atomicMass': 145, 'category': 'lanthanide', 'row': 9, 'col': 7, 'electronConfiguration': '[Xe] 4f⁵ 6s²', 'electronegativity': 1.13, 'meltingPoint': '1315 K', 'boilingPoint': '3273 K'},
    {'symbol': 'Sm', 'name': 'Samarium', 'atomicNumber': 62, 'atomicMass': 150.36, 'category': 'lanthanide', 'row': 9, 'col': 8, 'electronConfiguration': '[Xe] 4f⁶ 6s²', 'electronegativity': 1.17, 'meltingPoint': '1345 K', 'boilingPoint': '2067 K'},
    {'symbol': 'Eu', 'name': 'Europium', 'atomicNumber': 63, 'atomicMass': 151.96, 'category': 'lanthanide', 'row': 9, 'col': 9, 'electronConfiguration': '[Xe] 4f⁷ 6s²', 'electronegativity': 1.2, 'meltingPoint': '1099 K', 'boilingPoint': '1802 K'},
    {'symbol': 'Gd', 'name': 'Gadolinium', 'atomicNumber': 64, 'atomicMass': 157.25, 'category': 'lanthanide', 'row': 9, 'col': 10, 'electronConfiguration': '[Xe] 4f⁷ 5d¹ 6s²', 'electronegativity': 1.2, 'meltingPoint': '1585 K', 'boilingPoint': '3546 K'},
    {'symbol': 'Tb', 'name': 'Terbium', 'atomicNumber': 65, 'atomicMass': 158.93, 'category': 'lanthanide', 'row': 9, 'col': 11, 'electronConfiguration': '[Xe] 4f⁹ 6s²', 'electronegativity': 1.2, 'meltingPoint': '1629 K', 'boilingPoint': '3503 K'},
    {'symbol': 'Dy', 'name': 'Disprosium', 'atomicNumber': 66, 'atomicMass': 162.50, 'category': 'lanthanide', 'row': 9, 'col': 12, 'electronConfiguration': '[Xe] 4f¹⁰ 6s²', 'electronegativity': 1.22, 'meltingPoint': '1680 K', 'boilingPoint': '2840 K'},
    {'symbol': 'Ho', 'name': 'Holmium', 'atomicNumber': 67, 'atomicMass': 164.93, 'category': 'lanthanide', 'row': 9, 'col': 13, 'electronConfiguration': '[Xe] 4f¹¹ 6s²', 'electronegativity': 1.23, 'meltingPoint': '1734 K', 'boilingPoint': '2993 K'},
    {'symbol': 'Er', 'name': 'Erbium', 'atomicNumber': 68, 'atomicMass': 167.26, 'category': 'lanthanide', 'row': 9, 'col': 14, 'electronConfiguration': '[Xe] 4f¹² 6s²', 'electronegativity': 1.24, 'meltingPoint': '1802 K', 'boilingPoint': '3141 K'},
    {'symbol': 'Tm', 'name': 'Tulium', 'atomicNumber': 69, 'atomicMass': 168.93, 'category': 'lanthanide', 'row': 9, 'col': 15, 'electronConfiguration': '[Xe] 4f¹³ 6s²', 'electronegativity': 1.25, 'meltingPoint': '1818 K', 'boilingPoint': '2223 K'},
    {'symbol': 'Yb', 'name': 'Iterbium', 'atomicNumber': 70, 'atomicMass': 173.05, 'category': 'lanthanide', 'row': 9, 'col': 16, 'electronConfiguration': '[Xe] 4f¹⁴ 6s²', 'electronegativity': 1.1, 'meltingPoint': '1097 K', 'boilingPoint': '1469 K'},
    {'symbol': 'Lu', 'name': 'Lutetium', 'atomicNumber': 71, 'atomicMass': 174.97, 'category': 'lanthanide', 'row': 9, 'col': 17, 'electronConfiguration': '[Xe] 4f¹⁴ 5d¹ 6s²', 'electronegativity': 1.27, 'meltingPoint': '1925 K', 'boilingPoint': '3675 K'},
    {'symbol': 'Hf', 'name': 'Hafnium', 'atomicNumber': 72, 'atomicMass': 178.49, 'category': 'transition-metal', 'row': 6, 'col': 4, 'electronConfiguration': '[Xe] 4f¹⁴ 5d² 6s²', 'electronegativity': 1.3, 'meltingPoint': '2506 K', 'boilingPoint': '4876 K'},
    {'symbol': 'Ta', 'name': 'Tantalum', 'atomicNumber': 73, 'atomicMass': 180.95, 'category': 'transition-metal', 'row': 6, 'col': 5, 'electronConfiguration': '[Xe] 4f¹⁴ 5d³ 6s²', 'electronegativity': 1.5, 'meltingPoint': '3290 K', 'boilingPoint': '5731 K'},
    {'symbol': 'W', 'name': 'Tungsten', 'atomicNumber': 74, 'atomicMass': 183.84, 'category': 'transition-metal', 'row': 6, 'col': 6, 'electronConfiguration': '[Xe] 4f¹⁴ 5d⁴ 6s²', 'electronegativity': 2.36, 'meltingPoint': '3695 K', 'boilingPoint': '5828 K'},
    {'symbol': 'Re', 'name': 'Renium', 'atomicNumber': 75, 'atomicMass': 186.21, 'category': 'transition-metal', 'row': 6, 'col': 7, 'electronConfiguration': '[Xe] 4f¹⁴ 5d⁵ 6s²', 'electronegativity': 1.9, 'meltingPoint': '3459 K', 'boilingPoint': '5869 K'},
    {'symbol': 'Os', 'name': 'Osmium', 'atomicNumber': 76, 'atomicMass': 190.23, 'category': 'transition-metal', 'row': 6, 'col': 8, 'electronConfiguration': '[Xe] 4f¹⁴ 5d⁶ 6s²', 'electronegativity': 2.2, 'meltingPoint': '3306 K', 'boilingPoint': '5285 K'},
    {'symbol': 'Ir', 'name': 'Iridium', 'atomicNumber': 77, 'atomicMass': 192.22, 'category': 'transition-metal', 'row': 6, 'col': 9, 'electronConfiguration': '[Xe] 4f¹⁴ 5d⁷ 6s²', 'electronegativity': 2.20, 'meltingPoint': '2719 K', 'boilingPoint': '4701 K'},
    {'symbol': 'Pt', 'name': 'Platina', 'atomicNumber': 78, 'atomicMass': 195.08, 'category': 'transition-metal', 'row': 6, 'col': 10, 'electronConfiguration': '[Xe] 4f¹⁴ 5d⁹ 6s¹', 'electronegativity': 2.28, 'meltingPoint': '2041.4 K', 'boilingPoint': '4098 K'},
    {'symbol': 'Au', 'name': 'Emas', 'atomicNumber': 79, 'atomicMass': 196.97, 'category': 'transition-metal', 'row': 6, 'col': 11, 'electronConfiguration': '[Xe] 4f¹⁴ 5d¹⁰ 6s¹', 'electronegativity': 2.54, 'meltingPoint': '1337.33 K', 'boilingPoint': '3129 K'},
    {'symbol': 'Hg', 'name': 'Raksa', 'atomicNumber': 80, 'atomicMass': 200.59, 'category': 'transition-metal', 'row': 6, 'col': 12, 'electronConfiguration': '[Xe] 4f¹⁴ 5d¹⁰ 6s²', 'electronegativity': 2.00, 'meltingPoint': '234.32 K', 'boilingPoint': '629.88 K'},
    {'symbol': 'Tl', 'name': 'Talium', 'atomicNumber': 81, 'atomicMass': 204.38, 'category': 'post-transition-metal', 'row': 6, 'col': 13, 'electronConfiguration': '[Xe] 4f¹⁴ 5d¹⁰ 6s² 6p¹', 'electronegativity': 1.62, 'meltingPoint': '577 K', 'boilingPoint': '1746 K'},
    {'symbol': 'Pb', 'name': 'Timbal', 'atomicNumber': 82, 'atomicMass': 207.2, 'category': 'post-transition-metal', 'row': 6, 'col': 14, 'electronConfiguration': '[Xe] 4f¹⁴ 5d¹⁰ 6s² 6p²', 'electronegativity': 1.87, 'meltingPoint': '600.61 K', 'boilingPoint': '2022 K'},
    {'symbol': 'Bi', 'name': 'Bismut', 'atomicNumber': 83, 'atomicMass': 208.98, 'category': 'post-transition-metal', 'row': 6, 'col': 15, 'electronConfiguration': '[Xe] 4f¹⁴ 5d¹⁰ 6s² 6p³', 'electronegativity': 2.02, 'meltingPoint': '544.7 K', 'boilingPoint': '1837 K'},
    {'symbol': 'Po', 'name': 'Polonium', 'atomicNumber': 84, 'atomicMass': 209, 'category': 'post-transition-metal', 'row': 6, 'col': 16, 'electronConfiguration': '[Xe] 4f¹⁴ 5d¹⁰ 6s² 6p⁴', 'electronegativity': 2.0, 'meltingPoint': '527 K', 'boilingPoint': '1235 K'},
    {'symbol': 'At', 'name': 'Astatin', 'atomicNumber': 85, 'atomicMass': 210, 'category': 'metalloid', 'row': 6, 'col': 17, 'electronConfiguration': '[Xe] 4f¹⁴ 5d¹⁰ 6s² 6p⁵', 'electronegativity': 2.2, 'meltingPoint': '575 K', 'boilingPoint': '610 K'},
    {'symbol': 'Rn', 'name': 'Radon', 'atomicNumber': 86, 'atomicMass': 222, 'category': 'noble-gas', 'row': 6, 'col': 18, 'electronConfiguration': '[Xe] 4f¹⁴ 5d¹⁰ 6s² 6p⁶', 'electronegativity': 2.2, 'meltingPoint': '202 K', 'boilingPoint': '211.3 K'},
    {'symbol': 'Fr', 'name': 'Fransium', 'atomicNumber': 87, 'atomicMass': 223, 'category': 'alkali-metal', 'row': 7, 'col': 1, 'electronConfiguration': '[Rn] 7s¹', 'electronegativity': 0.7, 'meltingPoint': '295 K', 'boilingPoint': '950 K'},
    {'symbol': 'Ra', 'name': 'Radium', 'atomicNumber': 88, 'atomicMass': 226, 'category': 'alkaline-earth-metal', 'row': 7, 'col': 2, 'electronConfiguration': '[Rn] 7s²', 'electronegativity': 0.9, 'meltingPoint': '973 K', 'boilingPoint': '2010 K'},
    {'symbol': 'Ac', 'name': 'Aktinium', 'atomicNumber': 89, 'atomicMass': 227, 'category': 'actinide', 'row': 10, 'col': 3, 'electronConfiguration': '[Rn] 6d¹ 7s²', 'electronegativity': 1.1, 'meltingPoint': '1323 K', 'boilingPoint': '3471 K'},
    {'symbol': 'Th', 'name': 'Torium', 'atomicNumber': 90, 'atomicMass': 232.04, 'category': 'actinide', 'row': 10, 'col': 4, 'electronConfiguration': '[Rn] 6d² 7s²', 'electronegativity': 1.3, 'meltingPoint': '2115 K', 'boilingPoint': '5061 K'},
    {'symbol': 'Pa', 'name': 'Protaktinium', 'atomicNumber': 91, 'atomicMass': 231.04, 'category': 'actinide', 'row': 10, 'col': 5, 'electronConfiguration': '[Rn] 5f² 6d¹ 7s²', 'electronegativity': 1.5, 'meltingPoint': '1841 K', 'boilingPoint': '4300 K'},
    {'symbol': 'U', 'name': 'Uranium', 'atomicNumber': 92, 'atomicMass': 238.03, 'category': 'actinide', 'row': 10, 'col': 6, 'electronConfiguration': '[Rn] 5f³ 6d¹ 7s²', 'electronegativity': 1.38, 'meltingPoint': '1405.3 K', 'boilingPoint': '4404 K'},
    {'symbol': 'Np', 'name': 'Neptunium', 'atomicNumber': 93, 'atomicMass': 237, 'category': 'actinide', 'row': 10, 'col': 7, 'electronConfiguration': '[Rn] 5f⁴ 6d¹ 7s²', 'electronegativity': 1.36, 'meltingPoint': '917 K', 'boilingPoint': '4273 K'},
    {'symbol': 'Pu', 'name': 'Plutonium', 'atomicNumber': 94, 'atomicMass': 244, 'category': 'actinide', 'row': 10, 'col': 8, 'electronConfiguration': '[Rn] 5f⁶ 7s²', 'electronegativity': 1.28, 'meltingPoint': '912.5 K', 'boilingPoint': '3501 K'},
    {'symbol': 'Am', 'name': 'Amerisium', 'atomicNumber': 95, 'atomicMass': 243, 'category': 'actinide', 'row': 10, 'col': 9, 'electronConfiguration': '[Rn] 5f⁷ 7s²', 'electronegativity': 1.13, 'meltingPoint': '1449 K', 'boilingPoint': '2880 K'},
    {'symbol': 'Cm', 'name': 'Kurium', 'atomicNumber': 96, 'atomicMass': 247, 'category': 'actinide', 'row': 10, 'col': 10, 'electronConfiguration': '[Rn] 5f⁷ 6d¹ 7s²', 'electronegativity': 1.28, 'meltingPoint': '1613 K', 'boilingPoint': '3383 K'},
    {'symbol': 'Bk', 'name': 'Berkelium', 'atomicNumber': 97, 'atomicMass': 247, 'category': 'actinide', 'row': 10, 'col': 11, 'electronConfiguration': '[Rn] 5f⁹ 7s²', 'electronegativity': 1.3, 'meltingPoint': '1259 K', 'boilingPoint': '2900 K'},
    {'symbol': 'Cf', 'name': 'Kalifornium', 'atomicNumber': 98, 'atomicMass': 251, 'category': 'actinide', 'row': 10, 'col': 12, 'electronConfiguration': '[Rn] 5f¹⁰ 7s²', 'electronegativity': 1.3, 'meltingPoint': '1173 K', 'boilingPoint': '1743 K'},
    {'symbol': 'Es', 'name': 'Einsteinium', 'atomicNumber': 99, 'atomicMass': 252, 'category': 'actinide', 'row': 10, 'col': 13, 'electronConfiguration': '[Rn] 5f¹¹ 7s²', 'electronegativity': 1.3, 'meltingPoint': '1133 K', 'boilingPoint': '1269 K'},
    {'symbol': 'Fm', 'name': 'Fermium', 'atomicNumber': 100, 'atomicMass': 257, 'category': 'actinide', 'row': 10, 'col': 14, 'electronConfiguration': '[Rn] 5f¹² 7s²', 'electronegativity': 1.3, 'meltingPoint': '1800 K', 'boilingPoint': None},
    {'symbol': 'Md', 'name': 'Mendelevium', 'atomicNumber': 101, 'atomicMass': 258, 'category': 'actinide', 'row': 10, 'col': 15, 'electronConfiguration': '[Rn] 5f¹³ 7s²', 'electronegativity': 1.3, 'meltingPoint': '1100 K', 'boilingPoint': None},
    {'symbol': 'No', 'name': 'Nobelium', 'atomicNumber': 102, 'atomicMass': 259, 'category': 'actinide', 'row': 10, 'col': 16, 'electronConfiguration': '[Rn] 5f¹⁴ 7s²', 'electronegativity': 1.3, 'meltingPoint': '1100 K', 'boilingPoint': None},
    {'symbol': 'Lr', 'name': 'Lawrensium', 'atomicNumber': 103, 'atomicMass': 262, 'category': 'actinide', 'row': 10, 'col': 17, 'electronConfiguration': '[Rn] 5f¹⁴ 7s² 7p¹', 'electronegativity': 1.3, 'meltingPoint': '1900 K', 'boilingPoint': None},
    {'symbol': 'Rf', 'name': 'Rutherfordium', 'atomicNumber': 104, 'atomicMass': 267, 'category': 'transition-metal', 'row': 7, 'col': 4, 'electronConfiguration': '[Rn] 5f¹⁴ 6d² 7s²', 'electronegativity': None, 'meltingPoint': None, 'boilingPoint': None},
    {'symbol': 'Db', 'name': 'Dubnium', 'atomicNumber': 105, 'atomicMass': 268, 'category': 'transition-metal', 'row': 7, 'col': 5, 'electronConfiguration': '[Rn] 5f¹⁴ 6d³ 7s²', 'electronegativity': None, 'meltingPoint': None, 'boilingPoint': None},
    {'symbol': 'Sg', 'name': 'Seaborgium', 'atomicNumber': 106, 'atomicMass': 271, 'category': 'transition-metal', 'row': 7, 'col': 6, 'electronConfiguration': '[Rn] 5f¹⁴ 6d⁴ 7s²', 'electronegativity': None, 'meltingPoint': None, 'boilingPoint': None},
    {'symbol': 'Bh', 'name': 'Bohrium', 'atomicNumber': 107, 'atomicMass': 272, 'category': 'transition-metal', 'row': 7, 'col': 7, 'electronConfiguration': '[Rn] 5f¹⁴ 6d⁵ 7s²', 'electronegativity': None, 'meltingPoint': None, 'boilingPoint': None},
    {'symbol': 'Hs', 'name': 'Hassium', 'atomicNumber': 108, 'atomicMass': 270, 'category': 'transition-metal', 'row': 7, 'col': 8, 'electronConfiguration': '[Rn] 5f¹⁴ 6d⁶ 7s²', 'electronegativity': None, 'meltingPoint': None, 'boilingPoint': None},
    {'symbol': 'Mt', 'name': 'Meitnerium', 'atomicNumber': 109, 'atomicMass': 278, 'category': 'unknown', 'row': 7, 'col': 9, 'electronConfiguration': '[Rn] 5f¹⁴ 6d⁷ 7s²', 'electronegativity': None, 'meltingPoint': None, 'boilingPoint': None},
    {'symbol': 'Ds', 'name': 'Darmstadtium', 'atomicNumber': 110, 'atomicMass': 281, 'category': 'unknown', 'row': 7, 'col': 10, 'electronConfiguration': '[Rn] 5f¹⁴ 6d⁸ 7s²', 'electronegativity': None, 'meltingPoint': None, 'boilingPoint': None},
    {'symbol': 'Rg', 'name': 'Roentgenium', 'atomicNumber': 111, 'atomicMass': 282, 'category': 'unknown', 'row': 7, 'col': 11, 'electronConfiguration': '[Rn] 5f¹⁴ 6d⁹ 7s²', 'electronegativity': None, 'meltingPoint': None, 'boilingPoint': None},
    {'symbol': 'Cn', 'name': 'Kopernisium', 'atomicNumber': 112, 'atomicMass': 285, 'category': 'transition-metal', 'row': 7, 'col': 12, 'electronConfiguration': '[Rn] 5f¹⁴ 6d¹⁰ 7s²', 'electronegativity': None, 'meltingPoint': None, 'boilingPoint': '357 K'},
    {'symbol': 'Nh', 'name': 'Nihonium', 'atomicNumber': 113, 'atomicMass': 286, 'category': 'unknown', 'row': 7, 'col': 13, 'electronConfiguration': '[Rn] 5f¹⁴ 6d¹⁰ 7s² 7p¹', 'electronegativity': None, 'meltingPoint': None, 'boilingPoint': None},
    {'symbol': 'Fl', 'name': 'Flerovium', 'atomicNumber': 114, 'atomicMass': 289, 'category': 'post-transition-metal', 'row': 7, 'col': 14, 'electronConfiguration': '[Rn] 5f¹⁴ 6d¹⁰ 7s² 7p²', 'electronegativity': None, 'meltingPoint': None, 'boilingPoint': None},
    {'symbol': 'Mc', 'name': 'Moskovium', 'atomicNumber': 115, 'atomicMass': 290, 'category': 'unknown', 'row': 7, 'col': 15, 'electronConfiguration': '[Rn] 5f¹⁴ 6d¹⁰ 7s² 7p³', 'electronegativity': None, 'meltingPoint': None, 'boilingPoint': None},
    {'symbol': 'Lv', 'name': 'Livermorium', 'atomicNumber': 116, 'atomicMass': 293, 'category': 'unknown', 'row': 7, 'col': 16, 'electronConfiguration': '[Rn] 5f¹⁴ 6d¹⁰ 7s² 7p⁴', 'electronegativity': None, 'meltingPoint': None, 'boilingPoint': None},
    {'symbol': 'Ts', 'name': 'Tennessin', 'atomicNumber': 117, 'atomicMass': 294, 'category': 'unknown', 'row': 7, 'col': 17, 'electronConfiguration': '[Rn] 5f¹⁴ 6d¹⁰ 7s² 7p⁵', 'electronegativity': None, 'meltingPoint': None, 'boilingPoint': None},
    {'symbol': 'Og', 'name': 'Oganesson', 'atomicNumber': 118, 'atomicMass': 294, 'category': 'unknown', 'row': 7, 'col': 18, 'electronConfiguration': '[Rn] 5f¹⁴ 6d¹⁰ 7s² 7p⁶', 'electronegativity': None, 'meltingPoint': None, 'boilingPoint': None}
]

# Konversi ke DataFrame dan Map untuk akses cepat
elements_df = pd.DataFrame(ELEMENTS_DATA)
elements_by_symbol = {el['symbol']: el for el in ELEMENTS_DATA}

# Warna untuk kategori (digunakan dalam CSS)
CATEGORY_COLORS = {
    "alkali-metal": "#fca5a5",
    "alkaline-earth-metal": "#fdba74",
    "lanthanide": "#fde68a",
    "actinide": "#fde047",
    "transition-metal": "#a5b4fc",
    "post-transition-metal": "#93c5fd",
    "metalloid": "#6ee7b7",
    "reactive-nonmetal": "#86efac",
    "noble-gas": "#a78bfa",
    "unknown": "#d1d5db",
}

# Inisialisasi session state
if 'selected_element' not in st.session_state:
    st.session_state.selected_element = None
if 'gemini_content' not in st.session_state:
    st.session_state.gemini_content = ""
if 'gemini_loading' not in st.session_state:
    st.session_state.gemini_loading = False


# =============================================================================
# Fungsi Bantuan
# =============================================================================

def get_gemini_content(element_name, mode):
    """
    Fungsi untuk mengambil konten dari Google Gemini API.
    """
    st.session_state.gemini_loading = True
    st.session_state.gemini_content = "" # Hapus konten lama
    
    prompt = ""
    if mode == 'fact':
        prompt = f"Berikan satu fakta yang menarik dan mengejutkan tentang elemen kimia \"{element_name}\" dalam bahasa Indonesia. Buatlah agar mudah dipahami oleh siswa sekolah menengah."
    elif mode == 'uses':
        prompt = f"Jelaskan kegunaan umum dari elemen kimia \"{element_name}\" dalam kehidupan sehari-hari atau industri. Jelaskan dalam 2-3 kalimat sederhana dalam bahasa Indonesia."

    try:
        # Dapatkan API Key dari Streamlit secrets
        api_key = st.secrets.get("GEMINI_API_KEY", "") 
        if not api_key:
            # Fallback jika tidak ada di secrets, bisa diganti dengan input manual atau env var
            api_key = "" # Disediakan oleh environment Canvas

        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "role": "user",
                "parts": [{"text": prompt}]
            }]
        }
        
        response = requests.post(api_url, json=payload, headers={'Content-Type': 'application/json'})
        response.raise_for_status() # Akan error jika status bukan 2xx
        
        result = response.json()
        
        if (result.get('candidates') and 
            result['candidates'][0].get('content') and 
            result['candidates'][0]['content'].get('parts')):
            text = result['candidates'][0]['content']['parts'][0]['text']
            st.session_state.gemini_content = text
        else:
            st.session_state.gemini_content = "Respon dari AI tidak valid atau kosong."

    except requests.exceptions.RequestException as e:
        st.session_state.gemini_content = f"Gagal menghubungi API: {e}"
    except Exception as e:
        st.session_state.gemini_content = f"Terjadi kesalahan: {e}"
    finally:
        st.session_state.gemini_loading = False


def parse_formula(formula: str) -> float:
    """
    Fungsi untuk mem-parsing rumus kimia dan menghitung massa molar.
    Logika ini diadaptasi dari versi JavaScript.
    """
    import re
    # Regex untuk tokenisasi: Elemen, Angka, Kurung Buka, Kurung Tutup + Angka
    tokens = re.findall(r"([A-Z][a-z]*)(\d*)|(\()|(\))(\d*)", formula)
    if not tokens:
        raise ValueError("Format rumus tidak valid.")

    # Stack untuk menangani grup dalam kurung
    stack = [{}]  # Setiap item adalah dict {simbol: jumlah}

    for symbol, count, l_paren, r_paren, multiplier in tokens:
        if l_paren: # Jika token adalah '('
            stack.append({})
        elif r_paren: # Jika token adalah ')'
            if len(stack) < 2:
                raise ValueError("Kurung tidak cocok.")
            
            multiplier_val = int(multiplier) if multiplier else 1
            top_group = stack.pop()
            prev_group = stack[-1]

            for s, c in top_group.items():
                prev_group[s] = prev_group.get(s, 0) + c * multiplier_val
        else: # Jika token adalah elemen
            if symbol not in elements_by_symbol:
                raise ValueError(f"Elemen tidak valid: {symbol}")
            
            count_val = int(count) if count else 1
            current_group = stack[-1]
            current_group[symbol] = current_group.get(symbol, 0) + count_val

    if len(stack) != 1:
        raise ValueError("Kurung tidak cocok atau formula tidak valid.")

    # Hitung massa total dari dict elemen final
    total_mass = 0
    final_counts = stack[0]
    for symbol, count in final_counts.items():
        total_mass += elements_by_symbol[symbol]['atomicMass'] * count
    
    return total_mass


# =============================================================================
# Tampilan (UI)
# =============================================================================

# Judul Aplikasi
st.title("⚛️ Tabel Periodik Pro")
st.markdown("Visualisasi Data Atom Interaktif dengan Bantuan AI Gemini")

# --- CSS Kustom untuk Tampilan Tabel ---
st.markdown("""
<style>
    /* Style untuk kotak elemen */
    .element-tile {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 5px;
        margin: 2px;
        text-align: center;
        transition: transform 0.2s, box-shadow 0.2s;
        height: 90px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        font-size: 12px;
        color: #333;
    }
    .element-tile:hover {
        transform: scale(1.1);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        z-index: 10;
    }
    .element-tile strong {
        font-size: 16px;
        display: block;
    }
    .element-tile small {
        font-size: 10px;
        display: block;
    }
    .dimmed {
        opacity: 0.2;
        pointer-events: none;
    }
    /* Style untuk kartu info */
    .info-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .info-card h3 {
        margin-top: 0;
    }
</style>
""", unsafe_allow_html=True)


# --- Layout Utama ---
col1, col2 = st.columns([2.5, 1.5])

with col1:
    # --- Fitur Pencarian ---
    search_query = st.text_input(
        "Cari elemen berdasarkan nama, simbol, atau nomor atom...",
        key="search_query"
    ).lower().strip()

    # --- Tampilan Tabel Periodik ---
    st.subheader("Tabel Periodik Unsur")
    
    # Membuat grid 18 kolom
    grid_cols = st.columns(18)
    
    # Filter elemen berdasarkan pencarian
    if search_query:
        filtered_symbols = {
            el['symbol'] for el in ELEMENTS_DATA if
            search_query in el['name'].lower() or
            search_query == el['symbol'].lower() or
            search_query == str(el['atomicNumber'])
        }
    else:
        filtered_symbols = set(elements_by_symbol.keys())

    # Menempatkan setiap elemen di grid
    for el in ELEMENTS_DATA:
        # Hanya tampilkan elemen utama di grid utama
        if el['row'] <= 7:
            col_index = el['col'] - 1
            with grid_cols[col_index]:
                is_dimmed = el['symbol'] not in filtered_symbols
                dimmed_class = "dimmed" if is_dimmed else ""
                
                # Membuat konten HTML untuk setiap tile
                tile_html = f"""
                <div class="element-tile {dimmed_class}" style="background-color: {CATEGORY_COLORS.get(el['category'], '#ccc')};">
                    <small>{el['atomicNumber']}</small>
                    <strong>{el['symbol']}</strong>
                    <span>{el['name']}</span>
                </div>
                """
                # Tombol dibuat dengan st.markdown untuk handling klik
                if st.button(f"{el['symbol']}", key=f"btn_{el['symbol']}"):
                    st.session_state.selected_element = el
                    st.session_state.gemini_content = "" # Reset konten Gemini saat elemen baru dipilih
                
                # Menggunakan trik untuk menempatkan HTML di atas tombol transparan
                st.markdown(tile_html, unsafe_allow_html=True)

    # Menambahkan placeholder untuk Lantanida dan Aktinida
    with grid_cols[2]:
        st.markdown(f"""
        <div class="element-tile" style="background-color: {CATEGORY_COLORS['lanthanide']};">
            <small>57-71</small><strong>*</strong><span>Lantanida</span>
        </div>""", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="element-tile" style="background-color: {CATEGORY_COLORS['actinide']};">
            <small>89-103</small><strong>**</strong><span>Aktinida</span>
        </div>""", unsafe_allow_html=True)


    # --- Baris Lantanida dan Aktinida ---
    st.write("") # Spasi
    st.write("---")
    
    # Lantanida
    st.write("*Lantanida")
    lanthanide_cols = st.columns(15)
    lanthanides = [el for el in ELEMENTS_DATA if el['category'] == 'lanthanide']
    for i, el in enumerate(lanthanides):
        with lanthanide_cols[i]:
            is_dimmed = el['symbol'] not in filtered_symbols
            dimmed_class = "dimmed" if is_dimmed else ""
            tile_html = f"""<div class="element-tile {dimmed_class}" style="background-color: {CATEGORY_COLORS['lanthanide']};"><small>{el['atomicNumber']}</small><strong>{el['symbol']}</strong><span>{el['name']}</span></div>"""
            if st.button(f"{el['symbol']}", key=f"btn_{el['symbol']}"):
                st.session_state.selected_element = el
                st.session_state.gemini_content = ""
            st.markdown(tile_html, unsafe_allow_html=True)

    # Aktinida
    st.write("**Aktinida")
    actinide_cols = st.columns(15)
    actinides = [el for el in ELEMENTS_DATA if el['category'] == 'actinide']
    for i, el in enumerate(actinides):
        with actinide_cols[i]:
            is_dimmed = el['symbol'] not in filtered_symbols
            dimmed_class = "dimmed" if is_dimmed else ""
            tile_html = f"""<div class="element-tile {dimmed_class}" style="background-color: {CATEGORY_COLORS['actinide']};"><small>{el['atomicNumber']}</small><strong>{el['symbol']}</strong><span>{el['name']}</span></div>"""
            if st.button(f"{el['symbol']}", key=f"btn_{el['symbol']}"):
                st.session_state.selected_element = el
                st.session_state.gemini_content = ""
            st.markdown(tile_html, unsafe_allow_html=True)


with col2:
    # --- Panel Informasi Elemen ---
    st.subheader("Detail Elemen")
    if st.session_state.selected_element:
        el = st.session_state.selected_element
        
        with st.container(border=True):
            st.header(f"{el['name']} ({el['symbol']})")
            
            # Tampilkan gambar (placeholder)
            st.image(f"https://placehold.co/400x200/{CATEGORY_COLORS.get(el['category'], '#ccc').lstrip('#')}/333?text={el['symbol']}", caption=f"Representasi visual untuk {el['name']}")
            
            st.markdown(f"""
            - **Nomor Atom:** `{el['atomicNumber']}`
            - **Massa Atom:** `{el['atomicMass']:.3f} u`
            - **Kategori:** `{el['category'].replace('-', ' ').title()}`
            - **Konfigurasi Elektron:** `{el['electronConfiguration'] or 'N/A'}`
            - **Elektronegativitas:** `{el['electronegativity'] or 'N/A'}`
            - **Titik Leleh:** `{el['meltingPoint'] or 'N/A'}`
            - **Titik Didih:** `{el['boilingPoint'] or 'N/A'}`
            """)

            # --- Fitur Gemini ---
            st.markdown("---")
            st.subheader("✨ Didukung oleh AI Gemini")
            
            gemini_col1, gemini_col2 = st.columns(2)
            if gemini_col1.button("Fakta Menarik", key=f"fact_{el['symbol']}", use_container_width=True):
                get_gemini_content(el['name'], 'fact')
            
            if gemini_col2.button("Kegunaan Umum", key=f"uses_{el['symbol']}", use_container_width=True):
                get_gemini_content(el['name'], 'uses')

            if st.session_state.gemini_loading:
                st.info("Meminta data dari AI Gemini...")
            elif st.session_state.gemini_content:
                st.success(st.session_state.gemini_content)

    else:
        st.info("Klik sebuah elemen pada tabel untuk melihat detailnya di sini.")

    st.write("---")

    # --- Kalkulator Massa Molar ---
    st.subheader("Kalkulator Massa Molar")
    with st.container(border=True):
        formula = st.text_input("Masukkan Rumus Kimia", placeholder="Contoh: Al2(SO4)3")
        if st.button("Hitung Massa Molar"):
            if formula:
                try:
                    mass = parse_formula(formula.strip())
                    st.success(f"**Total Massa Molar:** `{mass:.4f} g/mol`")
                except ValueError as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Silakan masukkan rumus kimia terlebih dahulu.")
