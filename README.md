# Open Data AI Analytics

Контейнеризований багатомодульний проєкт для завантаження, перевірки якості, дослідження та візуалізації відкритих даних у Docker Workspace.

## Quick Start
1. Переконайтеся, що Docker Desktop або Docker Engine запущено.
2. За потреби скопіюйте `.env.example` у `.env` і змініть порт або шляхи.
3. Запустіть стек однією командою:

```bash
docker compose up --build
```

4. Відкрийте веб-інтерфейс: `http://localhost:8000`

## What The Stack Does
| Сервіс | Призначення | Результат |
| --- | --- | --- |
| `data_load` | Зчитує CSV і завантажує дані в SQLite | `runtime_data/analytics.db` у Docker volume |
| `data_quality_analysis` | Рахує пропуски, дублікати та перевіряє числові поля | `data_quality_report.json` |
| `data_research` | Формує базові статистики та підсумкові метрики | `data_research_report.json` |
| `visualization` | Генерує два графіки | `income_distribution.png`, `wine_vs_meat_spending.png` |
| `web` | Показує таблицю, звіти та графіки в браузері | `http://localhost:8000` |

## Dataset
Набір даних: [Customer Personality Analysis](https://www.kaggle.com/datasets/imakash3011/customer-personality-analysis)

Використовується файл `data/raw/marketing_campaign.csv`.

## Project Structure
```text
.
├── common/                     # Спільна логіка роботи з CSV, SQLite, звітами та графіками
├── data/                       # Вхідні дані
├── data_load/                  # Сервіс завантаження CSV у SQLite
├── data_quality_analysis/      # Сервіс перевірки якості даних
├── data_research/              # Сервіс дослідження даних
├── visualization/              # Сервіс побудови графіків
├── web/                        # Flask веб-інтерфейс
├── src/                        # Попередні лабораторні модулі
├── compose.yaml                # Спільний запуск контейнерів
├── .env.example                # Приклад змінних середовища
└── LAB3_REPORT.md              # Звіт до лабораторної роботи №3
```

## Services And Data Flow
1. `data_load` читає CSV з `data/raw/marketing_campaign.csv` і створює таблицю `customers` в SQLite.
2. `data_quality_analysis`, `data_research` і `visualization` читають дані з тієї самої БД через спільний Docker volume.
3. Звіти JSON і PNG-графіки записуються у спільні volumes `reports_data` і `plots_data`.
4. `web` читає БД, JSON-звіти та графіки і показує їх у браузері.

## Ports And Volumes
| Ресурс | Значення |
| --- | --- |
| Веб-інтерфейс | `8000` |
| Docker network | `analytics_net` |
| Volume для БД | `runtime_data` |
| Volume для звітів | `reports_data` |
| Volume для графіків | `plots_data` |

## Configuration
Приклад змінних середовища:

```env
DATASET_PATH=/workspace/data/raw/marketing_campaign.csv
DB_PATH=/workspace/runtime/analytics.db
REPORTS_DIR=/workspace/reports
PLOTS_DIR=/workspace/plots
WEB_PORT=8000
```

## Main Files For The Lab
| File | Purpose |
| --- | --- |
| `compose.yaml` | Оркестрація всіх контейнерів |
| `data_load/Dockerfile` | Образ для імпорту CSV у SQLite |
| `data_quality_analysis/Dockerfile` | Образ для перевірки якості даних |
| `data_research/Dockerfile` | Образ для базового дослідження даних |
| `visualization/Dockerfile` | Образ для побудови графіків |
| `web/Dockerfile` | Образ для веб-інтерфейсу |
| `LAB3_REPORT.md` | Письмовий звіт до лабораторної |

## Lab Artifacts
Після запуску стеку:
1. JSON-звіти зберігаються у Docker volume `reports_data`.
2. Графіки зберігаються у Docker volume `plots_data`.
3. SQLite база даних зберігається у Docker volume `runtime_data`.

## Related
- [LAB3_REPORT.md](LAB3_REPORT.md) - Повний звіт з архітектурою, командами запуску та відповідями на контрольні питання.
- [REPORT.md](REPORT.md) - Звіт з лабораторної роботи №1.
- [Report2.md](Report2.md) - Звіт з лабораторної роботи №2.
