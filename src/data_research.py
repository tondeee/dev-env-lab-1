import pandas as pd


def analyze_income_spending(file_path):
    print("Analyzing income vs spending...")
    try:
        df = pd.read_csv(file_path, sep="\t")
        print(df[["Income", "MntWines", "MntMeatProducts"]].describe())
    except Exception as e:
        print("Analysis error:", e)


if __name__ == "__main__":
    analyze_income_spending("../data/raw/marketing_campaign.csv")
