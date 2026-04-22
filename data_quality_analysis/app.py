from common.pipeline import TABLE_NAME, build_quality_report


def main() -> None:
    report = build_quality_report(TABLE_NAME)
    print(
        "Generated quality report with "
        f"{report['row_count']} rows and {report['duplicate_rows']} duplicate rows"
    )


if __name__ == "__main__":
    main()
