# ⚡ Consumo de Energia Elétrica no Brasil

**Projeto G2 — Tema 14** | Análise e Visualização de Dados (2015–2024)

---

## 📋 Descrição

Este projeto analisa o consumo de energia elétrica no Brasil entre 2015 e 2024,
investigando padrões regionais, setoriais, sazonalidade e eficiência energética.
O dashboard interativo foi desenvolvido com **Python + Streamlit + Plotly**.

---

## 🗂️ Estrutura do Projeto

```
projeto-consumo-energia/
│
├── app.py                    # Dashboard Streamlit principal
├── requirements.txt          # Dependências Python
├── README.md                 # Documentação do projeto
├── index.html                # Página GitHub Pages
├── dados/
│   └── simulacao_consumo_energia_brasil.csv
├── notebooks/
│   └── analise_consumo_energia.ipynb
├── database/                 # (opcional) SQLite
└── imagens/                  # Screenshots do dashboard
```

---

## 🚀 Como Executar Localmente

### 1. Clone o repositório
```bash
git clone https://github.com/SEU_USUARIO/projeto-consumo-energia.git
cd projeto-consumo-energia
```

### 2. Crie e ative o ambiente virtual
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Execute o dashboard
```bash
streamlit run app.py
```

O app abrirá automaticamente em `http://localhost:8501`.

---

## 📊 Funcionalidades do Dashboard

| Seção | Descrição |
|---|---|
| **KPIs** | Consumo total, estado líder, setor líder, demanda média, tarifa e CO₂ |
| **Linha temporal** | Evolução mensal do consumo |
| **Ranking por estado** | Comparação horizontal entre UFs |
| **Comparação setorial** | Residencial, Industrial, Comercial, Rural, Público |
| **Dispersão temp × consumo** | Correlação com temperatura média |
| **Heatmap mensal** | Sazonalidade por ano |
| **Comparação regional** | Evolução de cada região ao longo do tempo |
| **Eficiência energética** | Índice por região e setor |
| **Tabela dinâmica** | Exploração dos dados brutos filtrados |
| **Conclusão executiva** | Insights automáticos baseados nos filtros aplicados |

---

## 🎛️ Filtros Disponíveis

- Ano (2015–2024)
- Mês (Jan–Dez)
- Região (Norte, Nordeste, Centro-Oeste, Sudeste, Sul)
- Estado (UF)
- Setor de Consumo
- Nível de Demanda (Baixo, Médio, Alto, Crítico)

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.11+**
- **Pandas** — manipulação de dados
- **Plotly** — visualizações interativas
- **Streamlit** — dashboard web
- **NumPy** — operações numéricas

---

## 📦 Base de Dados

O dataset `simulacao_consumo_energia_brasil.csv` contém **4.440 registros** com as seguintes colunas:

| Coluna | Descrição |
|---|---|
| ano / mes / data | Período de referência |
| regiao / uf | Localização geográfica |
| setor_consumo | Residencial, Industrial, Comercial, Rural, Público |
| consumo_mwh | Consumo em megawatts-hora |
| demanda_pico | Demanda máxima registrada |
| temperatura_media | Temperatura média do período |
| tarifa_media | Tarifa média (R$/kWh) |
| populacao | População estimada |
| eficiencia_energetica | Índice de 0 a 100 |
| emissao_co2 | Emissão estimada de CO₂ |
| nivel_demanda | Baixo / Médio / Alto / Crítico |

---

## 🌐 Links

| Plataforma | Link |
|---|---|
| GitHub | `https://github.com/SEU_USUARIO/projeto-consumo-energia` |
| GitHub Pages | `https://SEU_USUARIO.github.io/projeto-consumo-energia` |
| Streamlit Cloud | `https://SEU_USUARIO-projeto-consumo-energia.streamlit.app` |

---

## 👤 Autor

Projeto desenvolvido para a disciplina de **Análise e Visualização de Dados**.

---

*⚡ Dados simulados para fins acadêmicos.*
