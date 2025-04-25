import glob
import os
import re
import sys

import pandas as pd
import matplotlib.pyplot as plt

# 1) Encontre todos os CSVs no padrão users{X}_inst{Y}_stats.csv
csv_pattern = os.path.join("locust", "results", "users*_inst*_stats.csv")
paths = glob.glob(csv_pattern)
if not paths:
    print(f"Nenhum CSV encontrado em locust/results com padrão {csv_pattern}")
    sys.exit(1)

records = []
for path in paths:
    filename = os.path.basename(path)
    m = re.match(r'users(\d+)_inst(\d+)_stats\.csv', filename)
    if not m:
        print(f"Ignorando arquivo com nome fora do padrão: {filename}")
        continue

    users = int(m.group(1))
    inst = int(m.group(2))

    df = pd.read_csv(path)
    if df.empty:
        print(f"CSV está vazio, ignorando: {filename}")
        continue

    last = df.iloc[-1]

    # 2) Encontre as colunas de forma flexível
    avg_col = next((c for c in df.columns if 'Average' in c and 'Response' in c), None)
    req_col = next((c for c in df.columns if 'Requests' in c and '/s' in c), None)

    if avg_col is None or req_col is None:
        print(f"Colunas esperadas não encontradas em {filename}:")
        print(" → colunas disponíveis:", df.columns.tolist())
        continue

    records.append({
        "users": users,
        "inst": inst,
        "avg_response": last[avg_col],
        "req_per_sec": last[req_col]
    })

if not records:
    print("Nenhum dado válido foi carregado. Verifique seus CSVs.")
    sys.exit(1)

data = pd.DataFrame(records)
data.sort_values(["inst", "users"], inplace=True)

# 3) Gráfico 1: Latência × Nº de usuários
plt.figure()
for inst_val in sorted(data["inst"].unique()):
    subset = data[data["inst"] == inst_val]
    plt.plot(
        subset["users"],
        subset["avg_response"],
        marker="o",
        label=f"{inst_val} instância(s)"
    )
plt.xlabel("Número de usuários")
plt.ylabel("Tempo médio de resposta (ms)")
plt.title("Latência x Número de usuários")
plt.legend()
plt.grid(True)
plt.savefig("resp_vs_usuarios.png")
print("Gerado: resp_vs_usuarios.png")

# 4) Gráfico 2: Throughput × Nº de instâncias
plt.figure()
for users_val in sorted(data["users"].unique()):
    subset = data[data["users"] == users_val]
    plt.plot(
        subset["inst"],
        subset["req_per_sec"],
        marker="o",
        label=f"{users_val} usuário(s)"
    )
plt.xlabel("Número de instâncias")
plt.ylabel("Requisições por segundo")
plt.title("Throughput x Nº de instâncias")
plt.legend()
plt.grid(True)
plt.savefig("reqs_vs_instancias.png")
print("Gerado: reqs_vs_instancias.png")
