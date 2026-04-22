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

## Azure Lab 4 Quick Start
Лабораторна робота №4 винесена в `infra/terraform/` і розрахована на запуск з Azure Cloud Shell без локального Terraform.

1. В Azure Portal відкрийте `Cloud Shell`.
2. Клонуйте репозиторій у Cloud Shell:

```bash
git clone https://github.com/tondeee/dev-env-lab-1.git
cd dev-env-lab-1/infra/terraform
```

3. Підготуйте змінні Terraform:

```bash
cp terraform.tfvars.example terraform.tfvars
nano terraform.tfvars
```

Потрібно вказати:
- `subscription_id` - ідентифікатор Azure subscription.
- `admin_ssh_public_key` - ваш SSH public key для входу на VM.

4. Створіть інфраструктуру:

```bash
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply
```

5. Візьміть `application_url` з outputs і перевірте веб-інтерфейс:

```bash
curl $(terraform output -raw application_url)
```

6. Після демонстрації видаліть ресурси:

```bash
terraform destroy
```

## Azure Lab 5 Quick Start (Prometheus + Grafana)
Лабораторна робота №5 додає моніторинг до вже розгорнутого стеку в Azure.

1. Підготуйте Terraform змінні:

```bash
cd infra/terraform
cp terraform.tfvars.example terraform.tfvars
nano terraform.tfvars
```

2. Переконайтеся, що задані порти моніторингу:
- `grafana_port = 3000`
- `prometheus_port = 9090`

3. Оновіть інфраструктуру:

```bash
terraform init
terraform plan
terraform apply
```

4. Після застосування відкрийте:
- Grafana: `terraform output -raw grafana_url`
- Prometheus: `terraform output -raw prometheus_url`
- Web app: `terraform output -raw application_url`

5. Перевірте, що моніторингові контейнери працюють:

```bash
ssh azureuser@PUBLIC_IP
cd /opt/analyticslab
docker compose -f compose.yaml -f monitoring/docker-compose.monitoring.yml ps
```

6. У Grafana використовується попередньо налаштований Prometheus data source та автозавантажений дашборд `Lab 5 Monitoring Overview`.

## Azure Lab 6 Quick Start (GitOps with Argo CD)
Лабораторна робота №6 переносить розгортання веб-застосунку в Kubernetes (`k3s`) та керує ним через GitOps (`Argo CD`).

1. Переконайтеся, що Azure VM з Lab 5 активна.
2. На VM встановіть `k3s` і `kubectl` контекст:

```bash
curl -sfL https://get.k3s.io | sh -
sudo kubectl get nodes
```

3. Встановіть Argo CD:

```bash
sudo kubectl create namespace argocd
sudo kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
sudo kubectl -n argocd get pods
```

4. Застосуйте Argo CD Application з репозиторію:

```bash
sudo kubectl apply -f gitops/argocd/application.yaml
```

5. Перевірте стан синхронізації та ресурси застосунку:

```bash
sudo kubectl get applications.argoproj.io -n argocd
sudo kubectl get all -n analytics-gitops
```

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
| `infra/terraform/main.tf` | Створення Azure інфраструктури для лаби 4 |
| `infra/terraform/cloud-init.tftpl` | Автоматичне налаштування VM та запуск Docker Compose |
| `monitoring/docker-compose.monitoring.yml` | Сервіси Prometheus, Grafana, Node Exporter, cAdvisor |
| `monitoring/prometheus/prometheus.yml` | `scrape_configs` для VM, контейнерів і web |
| `monitoring/grafana/provisioning/*` | Автододавання data source і dashboard у Grafana |
| `gitops/app/*.yaml` | Kubernetes маніфести застосунку для GitOps |
| `gitops/argocd/application.yaml` | Argo CD Application для автосинхронізації з GitHub |
| `LAB3_REPORT.md` | Письмовий звіт до лабораторної |
| `LAB4_REPORT.md` | Письмовий звіт до лабораторної №4 |
| `LAB5_REPORT.md` | Письмовий звіт до лабораторної №5 |
| `LAB6_REPORT.md` | Письмовий звіт до лабораторної №6 (GitOps) |

## Lab 4 Azure Infrastructure
Terraform створює такі ресурси Azure:

| Ресурс | Призначення |
| --- | --- |
| `azurerm_resource_group` | Логічний контейнер для всіх ресурсів лаби |
| `azurerm_virtual_network` | Приватна мережа VM |
| `azurerm_subnet` | Підмережа для мережевого інтерфейсу |
| `azurerm_public_ip` | Публічна IP-адреса для браузерного доступу |
| `azurerm_network_security_group` | Правила доступу для `22` і `8000` |
| `azurerm_network_interface` | Мережевий інтерфейс віртуальної машини |
| `azurerm_linux_virtual_machine` | Ubuntu VM для запуску контейнерів |

`cloud-init` у файлі `infra/terraform/cloud-init.tftpl` виконує такі кроки:
1. Оновлює пакети і встановлює `git`, Docker Engine та Docker Compose plugin.
2. Клонує репозиторій у `/opt/analyticslab`.
3. Генерує `.env` з портом веб-інтерфейсу.
4. Запускає `docker compose` з двома файлами: застосунок + моніторинг.

Для Lab 5 NSG додатково відкриває порти:
- `3000/tcp` для Grafana.
- `9090/tcp` для Prometheus.

Примітка: для повністю автоматичного `git clone` репозиторій має бути публічним або VM має отримати окремий deploy key / PAT. Якщо репозиторій приватний, `cloud-init` не зможе клонувати його без додаткової автентифікації.

## Lab Artifacts
Після запуску стеку:
1. JSON-звіти зберігаються у Docker volume `reports_data`.
2. Графіки зберігаються у Docker volume `plots_data`.
3. SQLite база даних зберігається у Docker volume `runtime_data`.

## Related
- [LAB3_REPORT.md](LAB3_REPORT.md) - Повний звіт з архітектурою, командами запуску та відповідями на контрольні питання.
- [LAB4_REPORT.md](LAB4_REPORT.md) - Звіт з Azure Terraform + cloud-init розгортання.
- [LAB5_REPORT.md](LAB5_REPORT.md) - Звіт з Prometheus + Grafana моніторингу в Azure.
- [LAB6_REPORT.md](LAB6_REPORT.md) - Звіт з GitOps-розгортання в k3s через Argo CD.
- [REPORT.md](REPORT.md) - Звіт з лабораторної роботи №1.
- [Report2.md](Report2.md) - Звіт з лабораторної роботи №2.
