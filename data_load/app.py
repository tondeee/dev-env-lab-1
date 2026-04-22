from common.pipeline import TABLE_NAME, dataset_path, load_csv_into_sqlite


def main() -> None:
    database_path, row_count = load_csv_into_sqlite(TABLE_NAME)
    print(f"Loaded {row_count} rows from {dataset_path()} into {database_path}")


if __name__ == "__main__":
    main()
