import pandas as pd


def check_data_quality(file_path):
    print(f"Loading data from {file_path}")
    try:
        df = pd.read_csv(file_path, sep="\t")
        print("Data shape:", df.shape)
        print("Missing values per column:\n", df.isnull().sum())
        print("Data types:\n", df.dtypes)
    except Exception as e:
        print("Error loading data:", e)


if __name__ == "__main__":
    check_data_quality("../data/raw/marketing_campaign.csv")
