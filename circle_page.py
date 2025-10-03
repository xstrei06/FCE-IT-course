import io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.backends.backend_pdf import PdfPages
import streamlit as st

st.set_page_config(page_title="Bod(y) na kružnici", layout="wide")

st.title("Bod(y) na kružnici — webová aplikace")

# INPUTS
with st.sidebar:
    st.header("Parametry úlohy")
    cx = st.number_input("Střed - x", value=0.0, format="%.3f")
    cy = st.number_input("Střed - y", value=0.0, format="%.3f")
    radius = st.number_input("Poloměr (r)", min_value=0.0, value=5.0, format="%.3f")
    n_points = st.number_input("Počet bodů", min_value=1, step=1, value=12)
    color = st.color_picker("Barva bodů", value="#1f77b4")
    unit = st.text_input("Jednotka os (např. m)", value="m")
    show_labels = st.checkbox("Zobrazit čísla u bodů (popisky)", value=True)
    angle_offset_deg = st.number_input("Úhel posunu (°) - 0 znamená bod 1 napravo", value=0.0)
    st.markdown("---")
    st.header("Export do PDF")
    author_name = "Jaroslav Streit"
    author_contact = "Jaroslav.Streit@vut.cz"
    author_github = "github.com/xstrei06"
    st.markdown(f"**Autor:** {author_name}")
    st.markdown(f"**Kontakt:** {author_contact}")
    st.markdown(f"**GitHub:** [{author_github}](https://www.github.com/xstrei06)")
    include_parameters = st.checkbox("Zahrnout parametry úlohy do PDF", value=True)

with st.sidebar.expander("O aplikaci a použitých technologiích", expanded=False):
    st.write("Tato aplikace generuje body rovnoměrně rozmístěné na kružnici a umožňuje export výsledku do PDF.")
    st.write("Použité technologie:")
    st.markdown("- Python 3.x\n- Streamlit (web UI)\n- NumPy (výpočty)\n- Matplotlib (vykreslení)\n- Pandas (tabulka / export)")
    st.write("Autor:")
    st.markdown(f"**{author_name}** — kontakt: {author_contact}")
    st.markdown("<p style='font-size:12px; color:gray;'>Při tvorbě aplikace byl využit model GPT-5 Thinking mini</p>", unsafe_allow_html=True)


col1, col2 = st.columns([2,1])

angles = np.linspace(0, 2*np.pi, int(n_points), endpoint=False) + np.deg2rad(angle_offset_deg)
xs = cx + radius * np.cos(angles)
ys = cy + radius * np.sin(angles)

df = pd.DataFrame({
    'index': np.arange(1, int(n_points)+1),
    'x': xs,
    'y': ys
})

pd.set_option('display.precision', 4)

with col1:
    st.subheader("Grafická vizualizace")

    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_aspect('equal', 'box')
    ax.scatter(xs, ys, c=[color], s=80, edgecolors='k')

    theta = np.linspace(0, 2*np.pi, 512)
    ax.plot(cx + radius*np.cos(theta), cy + radius*np.sin(theta), linestyle='--', alpha=0.6)

    if show_labels:
        for i, (x, y) in enumerate(zip(xs, ys), start=1):
            ax.text(x, y, str(i), fontsize=9, ha='left', va='bottom')

    def label_with_unit(x, pos):
        return f"{x:g} {unit}"

    ax.xaxis.set_major_formatter(FuncFormatter(label_with_unit))
    ax.yaxis.set_major_formatter(FuncFormatter(label_with_unit))

    ax.grid(True, linestyle=':', alpha=0.7)
    ax.set_xlabel(f"x [{unit}]")
    ax.set_ylabel(f"y [{unit}]")
    ax.set_title(f"Bodů: {int(n_points)}  — poloměr {radius} {unit} — střed ({cx}, {cy})")

    st.pyplot(fig)

with col2:
    st.subheader("Souřadnice bodů")
    df_display = df.copy()
    df_display['x'] = df_display['x'].map(lambda v: f"{v:.4f} {unit}")
    df_display['y'] = df_display['y'].map(lambda v: f"{v:.4f} {unit}")
    df_display = df_display.set_index('index')
    st.dataframe(df_display)

    st.markdown("---")
    st.write("Stáhnout výsledky")

    csv = df.to_csv(index=False)
    st.download_button("Stáhnout CSV souřadnic", data=csv, file_name="coordinates.csv", mime="text/csv")

    def create_pdf_bytes():
        buffer = io.BytesIO()
        with PdfPages(buffer) as pdf:

            fig_text = plt.figure(figsize=(8.27, 11.69))  # A4 v palcích
            fig_text.clf()
            txt = []
            txt.append("Úloha: body na kružnici")
            txt.append("")
            if include_parameters:
                txt.append(f"Střed (x, y): {cx:.4f}, {cy:.4f} {unit}")
                txt.append(f"Poloměr: {radius:.4f} {unit}")
                txt.append(f"Počet bodů: {int(n_points)}")
                txt.append(f"Barva bodů: {color}")
                txt.append(f"Úhel posunu: {angle_offset_deg}°")
                txt.append(f"Jednotka: {unit}")
                txt.append("")
            txt.append(f"Vytvořeno: {author_name}")
            txt.append(f"Kontakt: {author_contact}")
            full_txt = "\n".join(txt)
            fig_text.text(0.02, 0.98, full_txt, va='top', fontsize=12, family='monospace')
            plt.axis('off')
            pdf.savefig(fig_text)
            plt.close(fig_text)

            fig2, ax2 = plt.subplots(figsize=(8,8))
            ax2.set_aspect('equal', 'box')
            ax2.scatter(xs, ys, c=[color], s=80, edgecolors='k')
            ax2.plot(cx + radius*np.cos(theta), cy + radius*np.sin(theta), linestyle='--', alpha=0.6)
            if show_labels:
                for i, (x, y) in enumerate(zip(xs, ys), start=1):
                    ax2.text(x, y, str(i), fontsize=9, ha='left', va='bottom')
            ax2.xaxis.set_major_formatter(FuncFormatter(label_with_unit))
            ax2.yaxis.set_major_formatter(FuncFormatter(label_with_unit))
            ax2.grid(True, linestyle=':', alpha=0.7)
            ax2.set_xlabel(f"x [{unit}]")
            ax2.set_ylabel(f"y [{unit}]")
            ax2.set_title(f"Bodů: {int(n_points)}  — poloměr {radius} {unit} — střed ({cx}, {cy})")
            pdf.savefig(fig2)
            plt.close(fig2)

        buffer.seek(0)
        return buffer.read()

    pdf_bytes = None
    if st.button("Vytvořit PDF (stáhnout)"):
        with st.spinner("Generuji PDF…"):
            pdf_bytes = create_pdf_bytes()
            st.success("PDF připraveno")
            st.download_button("Stáhnout PDF", data=pdf_bytes, file_name="circle_points_report.pdf", mime="application/pdf")

st.markdown("---")
st.caption("Tip: použijte export do PDF pro tisk.")
