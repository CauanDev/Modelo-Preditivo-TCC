import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from scipy.stats import randint
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report
from tensorboardX import SummaryWriter
import os
import joblib

# ====== Configurações ======
engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost/db_tcc")

model_file = "random_forest_model.pkl"
scaler_file = "scaler.pkl"
columns_file = "model_columns.pkl"

# ====== 1. Carregar dados ======
df_mortos = pd.read_sql("SELECT * FROM obitos_infantil", engine)
df_mortos["label"] = 1

df_sobreviventes = pd.read_sql("SELECT * FROM sobreviventes", engine)
df_sobreviventes["label"] = 0

df = pd.concat([df_mortos, df_sobreviventes], ignore_index=True)

# ====== 2. Preparar dados ======
colunas_excluir = ["contador", "nome"]
X = df.drop(columns=[c for c in colunas_excluir if c in df.columns] + ["label"])
y = df["label"]
X = pd.get_dummies(X, drop_first=True)

# ====== 3. Treino / teste ======
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ====== 4. Hiperparâmetros ======
param_dist = {
    "n_estimators": randint(100, 500),
    "max_depth": randint(3, 30),
    "min_samples_split": randint(2, 20),
    "min_samples_leaf": randint(1, 20),
    "max_features": ["sqrt", "log2", None],
}

rf = RandomForestClassifier(random_state=42)

search = RandomizedSearchCV(
    rf,
    param_distributions=param_dist,
    n_iter=20,
    cv=3,
    scoring=["roc_auc", "accuracy"],
    refit="roc_auc",
    n_jobs=-1,
    random_state=42
)

search.fit(X_train_scaled, y_train)
model = search.best_estimator_

print("✅ Melhores parâmetros encontrados:", search.best_params_)

# ====== 5. Avaliação ======
y_pred = model.predict(X_test_scaled)
y_proba = model.predict_proba(X_test_scaled)[:, 1]

print("\n📊 Relatório de classificação:")
print(classification_report(y_test, y_pred))
print("Acurácia:", accuracy_score(y_test, y_pred))
print("ROC AUC:", roc_auc_score(y_test, y_proba))

# ====== 6. Salvar modelo, scaler e colunas ======
joblib.dump(model, model_file)
joblib.dump(scaler, scaler_file)
joblib.dump(X.columns.tolist(), columns_file)
print(f"\n💾 Modelo salvo em: {model_file}")
print(f"💾 Scaler salvo em: {scaler_file}")
print(f"💾 Colunas salvas em: {columns_file}")

# ====== 7. TensorBoard ======
log_dir = os.path.join(os.getcwd(), "logs", "random_forest")
os.makedirs(log_dir, exist_ok=True)
writer = SummaryWriter(log_dir)

results = search.cv_results_
for i in range(len(results['params'])):
    mean_roc = results['mean_test_roc_auc'][i]
    params_str = ", ".join([f"{k}:{v}" for k, v in results['params'][i].items()])
    writer.add_scalar("RandomizedSearch/ROC_AUC", mean_roc, i)
    writer.add_text("RandomizedSearch/Parameters", params_str, i)

writer.close()
print(f"📈 Logs do TensorBoard em: {log_dir}")
