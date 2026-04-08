# Projeto de Destilação Binária: Implementação e Análise pelo Método de McCabe-Thiele

Este repositório apresenta um conjunto de ferramentas computacionais voltadas ao ensino e à simulação de colunas de destilação binária utilizando o método clássico de McCabe-Thiele. O conteúdo abrange desde os fundamentos da linguagem Python aplicada à engenharia até a disponibilização de uma interface interativa para análise de sensibilidade paramétrica.

## Conteúdo do Repositório

### 1. Fundamentos de Programação para Engenharia Química
Este módulo consiste em uma introdução técnica à linguagem Python, com foco em manipulação de variáveis, estruturas de dados (NumPy arrays) e lógica de programação voltada à resolução de problemas de balanço de massa e energia.
* **Acesso ao Notebook:** [Introdução ao Python via Google Colab](https://github.com/hermannvargens/mccabe-thiele/blob/main/Introdu%C3%A7%C3%A3o.ipynb)

### 2. Implementação do Diagrama de McCabe-Thiele
Desenvolvimento passo a passo do algoritmo para construção das curvas de equilíbrio, retas de operação (Retificação, Esgotamento e Linha-q) e a contagem iterativa de estágios teóricos.
* **Acesso ao Notebook:** [Construção do Diagrama via Google Colab](https://github.com/hermannvargens/mccabe-thiele/blob/cccb593b17fdc04a9386f07c5e82b82f2fd75ed7/Diagrama_McCabe_Thiele.ipynb)

### 3. Simulador Interativo 
Interface desenvolvida em Streamlit para visualização dinâmica do impacto de variáveis de processo — como razão de refluxo, condição térmica da carga e volatilidade relativa — sobre o número de estágios teóricos e a localização do prato de alimentação.
* **Acesso à Aplicação:** [Simulador McCabe-Thiele](https://mccabe-thiele-t5xsmi3ft82p6klj5npgzs.streamlit.app/)

### 4. Atividades Práticas e Exercícios de Análise
Conjunto de estudos de caso propostos para que o estudante analise as consequências de alterações nos parâmetros de entrada, focando nos limites operacionais como refluxo mínimo e número mínimo de estágios .
* **Acesso aos Exercícios:** [Lista de Exercícios](https://forms.office.com/r/X6DFCKkjib)

## Requisitos Técnicos

Para execução local dos scripts, recomenda-se a instalação das seguintes bibliotecas:
* NumPy
* Matplotlib
* Streamlit

O desenvolvimento foi projetado para total compatibilidade com o ambiente Google Colaboratory, dispensando configurações locais complexas para finalidades didáticas.
