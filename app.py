import streamlit as st

import matplotlib.pyplot as plt

import numpy as np


# Configuração da Página

st.set_page_config(page_title="Simulador McCabe-Thiele", layout="wide")


st.title("Simulador de Coluna de Destilação: Método de McCabe-Thiele")

st.markdown("""

Esta aplicação calcula o número de estágios teóricos e o prato de alimentação para uma mistura binária. 

Ajuste os parâmetros na barra lateral para ver a atualização em tempo real.

""")


# --- BARRA LATERAL (INPUTS) ---

st.sidebar.header("Parâmetros do Processo")


col_a, col_b = st.sidebar.columns(2)

xD = col_a.number_input("Fração Destilado ($x_D$)", 0.5, 1.0, 0.95, 0.01)

xB = col_b.number_input("Fração Resíduo ($x_B$)", 0.0, 0.5, 0.05, 0.01)

zF = st.sidebar.slider("Fração de Alimentação ($z_F$)", float(xB + 0.01), float(xD - 0.01), 0.50)


st.sidebar.divider()


R = st.sidebar.number_input("Razão de Refluxo ($R$)", 0.1, 50.0, 3.0, 0.1)

q = st.sidebar.number_input("Fator de Carga ($q$)", -30.0, 30.0, 0.3, 0.1)

alpha = st.sidebar.number_input("Volatilidade Relativa ($\\alpha$)", 1.1, 10.0, 2.5, 0.1)


# --- LÓGICA DE CÁLCULO E PLOTAGEM ---


# 1. Curva de Equilíbrio e Diagonal

x_curva = np.linspace(0, 1, 100)

y_curva = (alpha * x_curva) / (1 + (alpha - 1) * x_curva)


fig, ax = plt.subplots(figsize=(6,6))

ax.plot(x_curva, y_curva, 'b', label='Equilíbrio', linewidth=2)

ax.plot([0, 1], [0, 1], 'k--', alpha=0.5, label='x = y')


# 2. Cálculos da Interseção (Ponto de Encontro xi, yi)

a_lor = R / (R + 1)

b_lor = xD / (R + 1)


if q == 1:

    xi, yi = zF, a_lor * zF + b_lor

else:

    a_q, b_q = q / (q - 1), -zF / (q - 1)

    xi = (b_q - b_lor) / (a_lor - a_q)

    yi = a_lor * xi + b_lor

# --- LINHAS VERTICAIS INDICATIVAS (MARCADORES NO EIXO X) ---

# Linha para xD (Vermelha)
ax.plot([xD, xD], [0, xD], color='red', linestyle=':', linewidth=1, alpha=0.7)

# Linha para zF (Verde)
ax.plot([zF, zF], [0, zF], color='green', linestyle=':', linewidth=1, alpha=0.7)

# Linha para xB (Magenta)
ax.plot([xB, xB], [0, xB], color='m', linestyle=':', linewidth=1, alpha=0.7)

#Anotações

ax.text(xD, -0.02, '$x_D$', color='red', ha='center', fontsize=10)
ax.text(zF, -0.02, '$z_F$', color='green', ha='center', fontsize=10)
ax.text(xB, -0.02, '$x_B$', color='m', ha='center', fontsize=10)




# 3. Plotando as Linhas de Operação

ax.plot([xD, xi], [xD, yi], 'r', linewidth=2, label='LOR (Retificação)')

ax.plot([zF, xi], [zF, yi], 'g', linewidth=2, label='Reta q (Alimentação)')

ax.plot([xB, xi], [xB, yi], 'm', linewidth=2, label='LOE (Esgotamento)')


# 4. Construção dos Degraus

x_atual, y_atual = xD, xD

estagios = 0

prato_alimentacao = 0

ja_alimentou = False


while x_atual > xB and estagios < 100: # Trava de segurança para evitar loops infinitos

    estagios += 1

    y_anterior = y_atual


    # Passo Horizontal (Equilíbrio)

    x_equilibrio = y_atual / (alpha - y_atual * (alpha - 1))

    ax.plot([x_atual, x_equilibrio], [y_atual, y_atual], 'k', linewidth=1)

    x_atual = x_equilibrio


    # Identificação da Alimentação

    if x_atual <= xi and not ja_alimentou:

        prato_alimentacao = estagios

        ja_alimentou = True

        ax.plot(x_atual, y_atual, 'go', markersize=8, label='Prato de Carga')


    # Passo Vertical (Linha de Operação)

    if x_atual > xi:

        y_atual = a_lor * x_atual + b_lor

    else:

        a_loe = (yi - xB) / (xi - xB)

        b_loe = xB - a_loe * xB

        y_atual = a_loe * x_atual + b_loe


    ax.plot([x_atual, x_atual], [y_anterior, y_atual], 'k', linewidth=1)


# 5. Finalização do Gráfico

ax.plot([xD, zF, xB], [0, 0, 0], 'ko', markersize=5)

ax.set_xlim(0, 1)

ax.set_ylim(0, 1)

ax.set_title('Diagrama de McCabe-Thiele', fontsize=14)

ax.set_xlabel('Fração molar no líquido (x)')

ax.set_ylabel('Fração molar no vapor (y)')

ax.grid(True, alpha=0.2)

ax.legend(loc='upper left')


# --- EXIBIÇÃO NO STREAMLIT ---

col1, col2 = st.columns([1, 1])


with col1:

    st.pyplot(fig, use_container_width=False)


with col2:

    st.subheader("Resultados")

    st.metric("Total de Estágios", estagios)

    st.metric("Prato de Alimentação", prato_alimentacao)

    

    st.info(f"""

    **Resumo Técnico:**

    - Razão L/V: {a_lor:.3f}

    - Intercepto LOR: {b_lor:.3f}

    - Ponto de Interseção: ({xi:.3f}, {yi:.3f})

    """)


if estagios >= 100:

    st.error("ERRO: O número de estágios excedeu 100. Verifique se a Razão de Refluxo é superior à mínima.")



