import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, roc_auc_score, mean_squared_error
from xgboost import XGBClassifier, XGBRegressor

# -----------------------
# 1. Load and Prep Data
# -----------------------
df = pd.read_csv("2022-games-week13.csv")

# Assume you have columns: season, week, results.homeTeam.score, results.awayTeam.score, spread, total
df["home_margin"] = df["results.homeTeam.score"] - df["results.awayTeam.score"]
df["total_points"] = df["results.homeTeam.score"] + df["results.awayTeam.score"]

df["favorite_cover"] = (df["home_margin"] > -df["odds.spread"]).astype(int)
df["over_hit"] = (df["total_points"] > df["odds.total"]).astype(int)

# Implied scores
df["implied_fav_score"] = (df["odds.total"] + df["odds.spread"]) / 2
df["implied_dog_score"] = (df["odds.total"] - df["odds.spread"]) / 2

features = ["odds.spread", "odds.total", "implied_fav_score", "implied_dog_score"]

# -----------------------
# 2. Season-Based CV
# -----------------------
seasons = sorted(df["season"].unique())
results = []

for i in range(5, len(seasons)):  # train on >=5 years, test on 1 year
    train_seasons = seasons[:i]
    test_season = seasons[i]
    
    train = df[df["season"].isin(train_seasons)]
    test = df[df["season"] == test_season]
    
    X_train, y_train_cover, y_train_over = train[features], train["favorite_cover"], train["over_hit"]
    X_test, y_test_cover, y_test_over = test[features], test["favorite_cover"], test["over_hit"]
    
    # -----------------------
    # 3. Models
    # -----------------------
    cover_model = XGBClassifier(
        n_estimators=200, max_depth=4, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, random_state=42
    )
    cover_model.fit(X_train, y_train_cover)
    
    over_model = XGBClassifier(
        n_estimators=200, max_depth=4, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, random_state=42
    )
    over_model.fit(X_train, y_train_over)
    
    margin_model = XGBRegressor(
        n_estimators=200, max_depth=4, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, random_state=42
    )
    margin_model.fit(X_train, train["home_margin"])
    
    total_model = XGBRegressor(
        n_estimators=200, max_depth=4, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, random_state=42
    )
    total_model.fit(X_train, train["total_points"])
    
    # -----------------------
    # 4. Evaluate
    # -----------------------
    cover_probs = cover_model.predict_proba(X_test)[:,1]
    over_probs = over_model.predict_proba(X_test)[:,1]
    
    cover_preds = (cover_probs >= 0.5).astype(int)
    over_preds = (over_probs >= 0.5).astype(int)
    
    margin_preds = margin_model.predict(X_test)
    total_preds = total_model.predict(X_test)
    
    results.append({
        "test_season": test_season,
        "cover_acc": accuracy_score(y_test_cover, cover_preds),
        "cover_auc": roc_auc_score(y_test_cover, cover_probs),
        "over_acc": accuracy_score(y_test_over, over_preds),
        "over_auc": roc_auc_score(y_test_over, over_probs),
        "margin_rmse": np.sqrt(mean_squared_error(test["home_margin"], margin_preds)),
        "total_rmse": np.sqrt(mean_squared_error(test["total_points"], total_preds))
    })

results_df = pd.DataFrame(results)
print(results_df)

# -----------------------
# 5. Edge Analysis
# -----------------------
# Example: only bet when model is very confident (>60%)
threshold = 0.60
confident_cover = results_df.copy()
# You could also store predictions per game and filter by probability
