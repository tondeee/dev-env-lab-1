import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def visualize_data(file_path):
    print("Generating visualizations...")
    try:
        df = pd.read_csv(file_path, sep="\t")

        plt.figure(figsize=(10, 6))
        sns.histplot(df["Income"], bins=50, kde=True)
        plt.title("Income Distribution")
        plt.savefig("../reports/figures/income_distribution.png")
        print("Visualization saved to reports/figures/income_distribution.png")

    except Exception as e:
        print("Visualization error:", e)


if __name__ == "__main__":
    visualize_data("../data/raw/marketing_campaign.csv")
