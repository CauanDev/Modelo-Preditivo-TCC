import pandas as pd
from sqlalchemy import create_engine
import joblib

# ====== Configurações ======
engine = create_engine("postgresql+psycopg2://postgres:postgres@192.168.100.18:5432/db_tcc")

model_file = "random_forest_model.pkl"
scaler_file = "scaler.pkl"
columns_file = "model_columns.pkl"

# ====== 1. Carregar modelo e pré-processamento ======
model = joblib.load(model_file)
scaler = joblib.load(scaler_file)
cols = joblib.load(columns_file)

print("✅ Modelo carregado com sucesso.")

# ====== 2. Carregar novos pacientes ======
novos = pd.read_sql("SELECT * FROM novos_pacientes", engine)
nomes = novos["nome"].fillna("Sem Nome")

# Preprocessar dados
colunas_excluir = ["contador", "nome"]
novos = novos.drop(columns=[c for c in colunas_excluir if c in novos.columns])
novos = pd.get_dummies(novos, drop_first=True)
novos = novos.reindex(columns=cols, fill_value=0)

# ====== 3. Fazer previsões ======
novos_scaled = scaler.transform(novos)
probs = model.predict_proba(novos_scaled)[:, 1]

print("\n📊 Probabilidade de óbito para novos pacientes:")
for nome, prob in zip(nomes, probs):
    print(f"Paciente: {nome} | Risco de óbito: {prob:.2%}")
