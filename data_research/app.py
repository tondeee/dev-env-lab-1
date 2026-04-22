from common.pipeline import TABLE_NAME, build_research_report


def main() -> None:
    report = build_research_report(TABLE_NAME)
    print(
        "Generated research report with "
        f"average income {report['income_mean']} and response rate {report['response_rate']}"
    )


if __name__ == "__main__":
    main()
