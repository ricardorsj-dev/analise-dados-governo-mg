import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# LEITURA DOS ARQUIVOS
# =========================

df = pd.read_csv(
    "Dados governo Zema x Pimentel.csv",
    decimal=",",
    thousands="."
)
df_salario = pd.read_csv("salario_servidores.csv")

# Remover espaços extras dos nomes das colunas
df.columns = df.columns.str.strip()
df_salario.columns = df_salario.columns.str.strip()

print(df.head())
print(df.columns)

# =========================
# CONFIGURAÇÃO DOS GRÁFICOS
# =========================

sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams["figure.figsize"] = (12, 6)

# =========================
# TRATAMENTO DOS DADOS
# =========================

df.columns = (
    df.columns
    .str.strip()
    .str.replace(" ", "_")
)

# PIB
df["PIB_do_Estado"] = (
    df["PIB_do_Estado"]
    .str.replace("R$", "", regex=False)
    .str.replace("bi", "", regex=False)
    .str.strip()
)

df["PIB_do_Estado"] = pd.to_numeric(
    df["PIB_do_Estado"],
    errors="coerce"
)

# Dívida
df["Dívida_Consolidada_Liquida"] = (
    df["Dívida_Consolidada_Liquida"]
    .str.replace("R$", "", regex=False)
    .str.replace("bi", "", regex=False)
    .str.strip()
)

df["Dívida_Consolidada_Liquida"] = pd.to_numeric(
    df["Dívida_Consolidada_Liquida"],
    errors="coerce"
)

# Renda
df["Renda_Per_Capita_Mensal"] = (
    df["Renda_Per_Capita_Mensal"]
    .str.replace("R$", "", regex=False)
    .str.replace(".", "", regex=False)
    .str.strip()
)

df["Renda_Per_Capita_Mensal"] = pd.to_numeric(
    df["Renda_Per_Capita_Mensal"],
    errors="coerce"
)

# Saúde
df["Saude_Percentual_Aplicado"] = (
    df["Saude_Percentual_Aplicado"]
    .str.replace("%", "", regex=False)
)

df["Saude_Percentual_Aplicado"] = pd.to_numeric(
    df["Saude_Percentual_Aplicado"],
    errors="coerce"
)

# Segurança
df["Seguranca_Taxa_Homicidios_100k"] = pd.to_numeric(
    df["Seguranca_Taxa_Homicidios_100k"],
    errors="coerce"
)

# Conferência
print(df.dtypes)

print(df.head())

# PIB
# =========================

plt.figure(figsize=(12,6))

sns.lineplot(
    data=df,
    x='Ano',
    y='PIB_do_Estado',
    hue='Gestao',
    marker='o'
)

media_pib = df.groupby("Gestao")["PIB_do_Estado"].mean()

if media_pib["Zema"] > media_pib["Pimentel"]:
    insight = "Zema apresentou maior PIB médio."
else:
    insight = "Pimentel apresentou maior PIB médio."

plt.text(
    0.5,
    0.02,
    insight,
    fontsize=12,
    transform=plt.gca().transAxes,
    bbox=dict(facecolor='white', alpha=0.8)
)

plt.title("Comparação do PIB entre os governos")
plt.xlabel("Ano")
plt.ylabel("PIB do Estado")

plt.show()

# =========================
# DÍVIDA PÚBLICA
# =========================

plt.figure(figsize=(12,6))

sns.barplot(
    data=df,
    x="Ano",
    y="Dívida_Consolidada_Liquida",
    hue="Gestao"
)

media_divida = df.groupby("Gestao")["Dívida_Consolidada_Liquida"].mean()

if media_divida["Zema"] > media_divida["Pimentel"]:
    insight_divida = "Zema apresentou maior dívida média."
else:
    insight_divida = "Pimentel apresentou maior dívida média."

plt.text(
    0.5,
    0.02,
    insight_divida,
    fontsize=12,
    transform=plt.gca().transAxes,
    bbox=dict(facecolor='white', alpha=0.8)
)

plt.title("Dívida Consolidada Líquida")
plt.xlabel("Ano")
plt.ylabel("Valor da dívida")

plt.show()

# =========================
# RENDA PER CAPITA
# =========================

plt.figure(figsize=(12,6))

sns.lineplot(
    data=df,
    x="Ano",
    y="Renda_Per_Capita_Mensal",
    hue="Gestao",
    marker="o"
)

plt.title("Renda Per Capita Mensal")
plt.xlabel("Ano")
plt.ylabel("R$")

plt.show()

# =========================
# SAÚDE
# =========================

plt.figure(figsize=(12,6))

sns.barplot(
    data=df,
    x="Ano",
    y="Saude_Percentual_Aplicado",
    hue="Gestao"
)

plt.title("Percentual Aplicado em Saúde")
plt.xlabel("Ano")
plt.ylabel("% aplicado")

plt.show()

# =========================
# SEGURANÇA PÚBLICA
# =========================

plt.figure(figsize=(12,6))

sns.lineplot(
    data=df,
    x="Ano",
    y="Seguranca_Taxa_Homicidios_100k",
    hue="Gestao",
    marker="o"
)

plt.title("Taxa de Homicídios")
plt.xlabel("Ano")
plt.ylabel("Homicídios por 100 mil habitantes")

plt.show()

# =========================
# PAGAMENTO DOS SERVIDORES
# =========================

comparativo = df_salario.groupby("governo")[["dia_util_medio", "parcelas"]].mean().round(1)

fig, ax1 = plt.subplots(figsize=(10,6))

# Barras
barras = ax1.bar(
    comparativo.index,
    comparativo["dia_util_medio"],
    alpha=0.8
)

ax1.set_ylabel("Dia útil médio de pagamento")
ax1.set_xlabel("Governo")

# Valores nas barras
for barra in barras:
    altura = barra.get_height()

    ax1.text(
        barra.get_x() + barra.get_width()/2,
        altura + 0.2,
        f"{altura}",
        ha='center'
    )

# Linha
ax2 = ax1.twinx()

ax2.plot(
    comparativo.index,
    comparativo["parcelas"],
    marker='o',
    linewidth=3
)

ax2.set_ylabel("Número médio de parcelas")

plt.title(
    "Pagamento dos servidores públicos de MG\nComparação: Pimentel x Zema",
    fontsize=14
)

ax1.grid(axis='y', linestyle='--', alpha=0.4)

plt.show()

# =========================
# MERENDA ESCOLAR
# =========================

plt.figure(figsize=(12,6))

sns.countplot(
    data=df,
    y="Merenda_Escolar_Investimento",
    hue="Gestao"
)

plt.title("Situação da Merenda Escolar")

plt.tight_layout()

plt.show()