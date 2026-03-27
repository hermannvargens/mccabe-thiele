import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Configuração da Página
st.set_page_config(page_title="McCabe-Thiele Pro", layout="wide")

st.title("Projeto de Destilação: McCabe-Thiele Avançado")

# --- BARRA LATERAL (INPUTS) ---
st.sidebar.header("Parâmetros de Entrada")
xD = st.sidebar.number_input("Fração Destilado ($x_D$)", 0.5, 0.99, 0.95, 0.01)
xB = st.sidebar.number_input("Fração Resíduo ($x_B$)", 0.01, 0.5, 0.05, 0.01)
zF = st.sidebar.slider("Fração de Alimentação ($z_F$)", float(xB + 0.01), float(xD - 0.01), 0.50)

st.sidebar.divider()

R = st.sidebar.number_input("Razão de Refluxo Operacional ($R$)", 0.1, 50.0, 3.0, 0.1)
q = st.sidebar.number_input("Fator de Carga ($q$)", -1.0, 2.0, 1.0, 0.1)
alpha = st.sidebar.number_input("Volatilidade Relativa ($\\alpha$)", 1.1, 10.0, 2.5, 0.1)

# --- CÁLCULOS TÉCNICOS ---

# 1. Número Mínimo de Estágios (Equação de Fenske - Refluxo Total)
# Nmin = log([xD/(1-xD)] * [(1-xB)/xB]) / log(alpha)
n_min = np.log((xD / (1 - xD)) * ((1 - xB) / xB)) / np.log(alpha)

# 2. Razão de Refluxo Mínima (Rmin)
# Encontrar a interseção da linha-q com a curva de equilíbrio (Pinch Point)
if q == 1:
    xi_min = zF
    yi_min = (alpha * xi_min) / (1 + (alpha - 1) * xi_min)
else:
    # Resolvendo a quadrática: mq*x + bq = (alpha*x)/(1+(alpha-1)x)
    mq = q / (q - 1)
    bq = -zF / (q - 1)
    
    A = mq * (alpha - 1)
    B = mq + bq * (alpha - 1) - alpha
    C = bq
    
    # Bhaskara para encontrar a interseção correta
    delta = B**2 - 4*A*C
    roots = [(-B + np.sqrt(delta)) / (2*A), (-B - np.sqrt(delta)) / (2*A)]
    # Selecionamos a raiz que faz sentido físico (entre xB e xD)
    xi_min = [r for r in roots if xB < r < xD][0]
    yi_min = (alpha * xi_min) / (1 + (alpha - 1) * xi_min)

# Inclinação da LOR mínima (m_min) ligando (xD, xD) ao Pinch Point (xi_min, yi_min)
m_min = (xD - yi_min) / (xD - xi_min)
r_min = m_min / (1 - m_min)

# --- LÓGICA DE PLOTAGEM ---
fig, ax = plt.subplots(figsize=(10, 10))
x_curva = np.linspace(0, 1, 100)
y_curva = (alpha * x_curva) / (1 + (alpha - 1) * x_curva)

ax.plot(x_curva, y_curva, 'b', label='Equilíbrio', linewidth=2)
ax.plot([0, 1], [0, 1], 'k--', alpha=0.5, label='Refluxo Total ($N_{min}$)')

# Cálculos da Interseção Operacional (R real)
a_lor = R / (R + 1)
b_lor = xD / (R + 1)

if q == 1:
    xi, yi = zF, a_lor * zF + b_lor
else:
    a_q, b_q = q / (q - 1), -zF / (q - 1)
    xi = (b_q - b_lor) / (a_lor - a_q)
    yi = a_lor * xi + b_lor

# Plotagem das Linhas Operacionais
ax.plot([xD, xi], [xD, yi], 'r', linewidth=2, label='LOR (Operacional)')
ax.plot([zF, xi], [zF, yi], 'g', linewidth=2, label='Linha-q')
ax.plot([xB, xi], [xB, yi], 'm', linewidth=2, label='LOE (Operacional)')

# Degraus do McCabe-Thiele (Operacional)
x_atual, y_atual = xD, xD
estagios = 0
while x_atual > xB and estagios < 100:
    estagios += 1
    y_ant = y_atual
    x_eq_ponto = y_atual / (alpha - y_atual * (alpha - 1))
    ax.plot([x_atual, x_eq_ponto], [y_atual, y_atual], 'k', linewidth=0.8)
    x_atual = x_eq_ponto
    
    if x_atual > xi:
        y_atual = a_lor * x_atual + b_lor
    else:
        a_loe = (yi - xB) / (xi - xB)
        b_loe = xB - a_loe * xB
        y_atual = a_loe * x_atual + b_loe
    ax.plot([x_atual, x_atual], [y_ant, y_atual], 'k', linewidth=0.8)

# Estética do Gráfico
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.grid(True, alpha=0.2)
ax.legend()

# --- EXIBIÇÃO ---
col1, col2 = st.columns([3, 1])

with col1:
    st.pyplot(fig)

with col2:
    st.subheader("Limites de Projeto")
    st.metric("Refluxo Mínimo ($R_{min}$)", f"{r_min:.3f}")
    st.metric("Estágios Mínimos ($N_{min}$)", f"{n_min:.2f}")
    
    st.divider()
    
    st.subheader("Operação Atual")
    st.metric("Estágios Teóricos ($N$)", estagios)
    
    # Alerta de viabilidade
    if R < r_min:
        st.error(f"Atenção: R ({R}) é menor que Rmin ({r_min:.2f}). A separação é impossível nesta condição.")
    else:
        st.success("Operação dentro da região factível.")
