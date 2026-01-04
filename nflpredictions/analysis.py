import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import accuracy_score, mean_squared_error, roc_auc_score

# -----------------------
# 1. Load your dataset
# -----------------------
df = pd.read_csv("2022-games-week13.csv")

# Compute outcomes
df["total_points"] = df["results.homeTeam.score"] + df["results.awayTeam.score"]

df["homeFavored"] = (df["odds.spread"] <= 0).astype(int)
df["favoriteScore"] = np.where(df["homeFavored"] == 1, df["results.homeTeam.score"], df["results.awayTeam.score"])
df["dogScore"] = np.where(df["homeFavored"] == 1, df["results.awayTeam.score"], df["results.homeTeam.score"])
df["spreadMultiplier"] = np.where(df["homeFavored"] == 1, -1, 1)
df["favorite_margin"] = df["favoriteScore"] - df["dogScore"]

# Favorite implied by spread
df["favorite_cover"] = (df["favorite_margin"] > (df["odds.spread"] * df["spreadMultiplier"])).astype(int)  # 1 if favorite covered
df["over_hit"] = (df["total_points"] > df["odds.total"]).astype(int)        # 1 if game went over

# -----------------------
# 2. Feature Engineering
# -----------------------

# Implied scores from spread + total
df["implied_fav_score"] = (df["odds.total"] + df["odds.spread"]) / 2
df["implied_dog_score"] = (df["odds.total"] - df["odds.spread"]) / 2

# Residuals (market bias)
df["margin_residual"] = df["favoriteScore"] - ((df["odds.spread"] * df["spreadMultiplier"]))
df["total_residual"] = df["total_points"] - df["odds.total"]

features = ["odds.spread", "odds.total", "implied_fav_score", "implied_dog_score"]

# -----------------------
# 3. Train/Test Split
# -----------------------
X = df[features]
y_cover = df["favorite_cover"]
y_over = df["over_hit"]
X_train, X_test, y_train_cover, y_test_cover = train_test_split(X, y_cover, test_size=0.2, shuffle=False)
_, _, y_train_over, y_test_over = train_test_split(X, y_over, test_size=0.2, shuffle=False)

print(X_train, y_train_cover)
print(X_train, y_train_over)

# -----------------------
# 4. Modeling
# -----------------------
# Logistic regression for classification (cover/over)
cover_model = LogisticRegression(max_iter=1000)
cover_model.fit(X_train, y_train_cover)

over_model = LogisticRegression(max_iter=1000)
over_model.fit(X_train, y_train_over)

# Linear regression for regression (predict margin, total points)
margin_model = LinearRegression()
margin_model.fit(X_train, df.loc[y_train_cover.index, "favorite_margin"])

total_model = LinearRegression()
total_model.fit(X_train, df.loc[y_train_over.index, "total_points"])

# -----------------------
# 5. Evaluation
# -----------------------
cover_preds = cover_model.predict(X_test)
over_preds = over_model.predict(X_test)

print("Cover Accuracy:", accuracy_score(y_test_cover, cover_preds))
print("Over Accuracy:", accuracy_score(y_test_over, over_preds))

# Regression RMSE
margin_preds = margin_model.predict(X_test)
total_preds = total_model.predict(X_test)

print("Margin RMSE:", np.sqrt(mean_squared_error(df.loc[y_test_cover.index, "favorite_margin"], margin_preds)))
print("Total RMSE:", np.sqrt(mean_squared_error(df.loc[y_test_over.index, "total_points"], total_preds)))

# -----------------------
# 6. Backtesting / Edges
# -----------------------
# Example: probability predictions
cover_probs = cover_model.predict_proba(X_test)[:,1]
over_probs = over_model.predict_proba(X_test)[:,1]

# Compare to 52.38% threshold (break-even at -110 odds)
bets_cover = (cover_probs > 0.55).astype(int)
bets_over = (over_probs > 0.55).astype(int)

print("Potential edge (cover bets):", accuracy_score(y_test_cover[bets_cover==1], cover_preds[bets_cover==1]))
print("Potential edge (over bets):", accuracy_score(y_test_over[bets_over==1], over_preds[bets_over==1]))
