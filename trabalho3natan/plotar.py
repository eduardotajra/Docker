import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

arq = Path("locust/resultados/teste_stats_history.csv")
df = pd.read_csv(arq)

# normaliza cabeçalhos
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
print(df.columns.tolist())

# filtra linhas agregadas
df_agg = df[df["name"] == "Aggregated"]

# converte ms → s usando a coluna padronizada
df_agg["avg_s"] = df_agg["total_average_response_time"] / 1000

# plota
plt.figure()
plt.plot(df_agg["timestamp"], df_agg["avg_s"])
plt.title("Tempo médio de resposta – stack WordPress (Locust)")
plt.xlabel("Instante do teste (s)")
plt.ylabel("Tempo médio (s)")
plt.grid(True)
plt.tight_layout()
plt.savefig("grafico_tempo_medio.png", dpi=300)
plt.show()
