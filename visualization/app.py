from common.pipeline import TABLE_NAME, build_visualizations


def main() -> None:
    generated_files = build_visualizations(TABLE_NAME)
    print(f"Generated visualizations: {', '.join(generated_files)}")


if __name__ == "__main__":
    main()
