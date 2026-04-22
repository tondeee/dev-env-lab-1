# Звіт з виконання Лабораторної роботи №6

## Тема
Ознайомлення із практиками GitOps. Автоматизоване розгортання застосунку в Kubernetes за допомогою Argo CD.

## Мета
Ознайомитися з підходом GitOps і реалізувати автоматичне розгортання та оновлення застосунку в Kubernetes-середовищі на основі змін у GitHub-репозиторії.

## Коротко про GitOps
GitOps — це підхід, у якому Git-репозиторій є джерелом істини для бажаного стану системи. Зміни вносяться через `commit/push`, а агент у кластері (у цій роботі — Argo CD) автоматично синхронізує фактичний стан із декларативними YAML-описами в репозиторії.  
Rollback виконується поверненням Git-стану до попереднього коміту.

## Використане середовище
1. Azure Linux VM з попередньої лабораторної (`analyticslab-vm-lnrp0u`).
2. `k3s` як Kubernetes кластер (single-node).
3. Argo CD у namespace `argocd`.
4. GitHub репозиторій: `tondeee/dev-env-lab-1`.
5. Kubernetes manifests у каталозі `gitops/`.
6. Публічні endpoint-и:
   - Застосунок: `http://20.93.160.132:30080`
   - Argo CD: `https://20.93.160.132:31431`
   - Prometheus: `http://20.93.160.132:9090`
   - Grafana: `http://20.93.160.132:3000`

## Структура GitOps у репозиторії
```text
gitops/
  app/
    namespace.yaml
    deployment.yaml
    service.yaml
  argocd/
    application.yaml
```

## Основні YAML-файли

### `gitops/app/namespace.yaml`
Створює namespace `analytics-gitops` для застосунку.

### `gitops/app/deployment.yaml`
Описує Deployment `analytics-web`:
1. Docker image: `ghcr.io/tondeee/dev-env-lab-1-web:lab6-v1`
2. `replicas: 2` (на старті)
3. Порт контейнера `8000`
4. Labels/selectors для зв'язку з Service
5. `readinessProbe` і `livenessProbe` на `/health`

### `gitops/app/service.yaml`
Створює Service `analytics-web` типу `NodePort`:
1. `port: 8000`
2. `targetPort: 8000`
3. `nodePort: 30080` (доступ іззовні через IP VM)

### `gitops/argocd/application.yaml`
Argo CD Application `analytics-web-gitops`:
1. Репозиторій: `https://github.com/tondeee/dev-env-lab-1.git`
2. Гілка: `feature/docker-workspace-lab3`
3. Шлях до маніфестів: `gitops/app`
4. Namespace призначення: `analytics-gitops`
5. Автосинхронізація: `automated`, `prune`, `selfHeal`

## Покрокове виконання

### 1. Підготовка Kubernetes-середовища
На Azure VM встановлено `k3s`, перевірено вузол командою:
```bash
kubectl get nodes
```

### 2. Встановлення Argo CD
1. Створено namespace `argocd`.
2. Встановлено Argo CD з офіційного маніфесту.
3. Перевірено роботу pod-ів:
```bash
kubectl -n argocd get pods
```

### 3. Підключення GitHub до Argo CD
Створено `Application` через `gitops/argocd/application.yaml`, увімкнено автоматичну синхронізацію.

### 4. Перше розгортання
Після застосування `Application` Argo CD отримав стан `Synced`, а ресурси застосунку створені в `analytics-gitops`.

### 5. Демонстрація автоматичного оновлення
У GitHub змінено `replicas` у `deployment.yaml` (`2 -> 3`), виконано `commit` і `push`.  
Argo CD виконав синхронізацію без ручного `kubectl apply`.

### 6. Демонстрація rollback
Останню зміну скасовано через Git (`git revert <commit>`).  
Argo CD повернув кластер до попередньої конфігурації (`replicas: 2`).

Примітка: у цьому середовищі для пришвидшення виявлення нового Git-стану використовувалась анотація:
```bash
kubectl -n argocd annotate application analytics-web-gitops argocd.argoproj.io/refresh=hard --overwrite
```
Після виявлення змін синхронізація застосунку виконувалась Argo CD автоматично.

### 7. Сумісність із моніторингом
Після GitOps-оновлень перевірено:
1. Застосунок доступний.
2. Prometheus доступний і продовжує збір метрик.
3. Grafana доступна.
4. Дашборд із Lab 5 працює.

## Приклад commit, що викликав оновлення
```text
0a3c8bc chore(gitops): scale analytics-web replicas from 2 to 3 (autosync)
```

## Приклад rollback
```text
2ea5dea Revert "chore(gitops): scale analytics-web replicas from 2 to 3 (autosync)"
```

## Скріншоти (placeholder-и для вставки)

### Скріншот 1. `kubectl get nodes`
Файл для заміни: `lab6-01-kubectl-get-nodes.png`
![kubectl get nodes](lab6-01-kubectl-get-nodes.png)

Рис. 1. Активний вузол Kubernetes у k3s-кластері.

### Скріншот 2. Pod-и Argo CD
Файл для заміни: `lab6-02-argocd-pods.png`
![argocd pods](lab6-02-argocd-pods.png)

Рис. 2. Стан pod-ів Argo CD у namespace `argocd`.

### Скріншот 3. Інтерфейс Argo CD зі станом Synced
Файл для заміни: `lab6-03-argocd-synced.png`
![argocd synced](lab6-03-argocd-synced.png)

Рис. 3. Стан `Synced` для застосунку `analytics-web-gitops`.

### Скріншот 4. Застосунок у браузері
Файл для заміни: `lab6-04-app-browser.png`
![app browser](lab6-04-app-browser.png)

Рис. 4. Веб-застосунок, розгорнутий у Kubernetes і доступний через NodePort.

### Скріншот 5. Grafana dashboard
Файл для заміни: `lab6-05-grafana-dashboard.png`
![grafana dashboard](lab6-05-grafana-dashboard.png)

Рис. 5. Дашборд Grafana після GitOps-оновлення застосунку.

### Скріншот 6. Commit, що викликав автооновлення
Файл для заміни: `lab6-06-git-commit-update.png`
![git commit update](lab6-06-git-commit-update.png)

Рис. 6. Коміт у GitHub, після якого Argo CD автоматично синхронізував зміни.

### Скріншот 7. Rollback (Git revert + Argo CD sync)
Файл для заміни: `lab6-07-git-rollback.png`
![git rollback](lab6-07-git-rollback.png)

Рис. 7. Повернення до попереднього стану через Git revert і автоматичний rollback у кластері.

## Висновки
У лабораторній роботі реалізовано повний GitOps-сценарій на базі Azure VM + k3s + Argo CD.  
Декларативні конфігурації винесено в GitHub-репозиторій, перше розгортання виконано через Argo CD, підтверджено автоматичне оновлення після зміни в Git і rollback через `git revert`.  
Моніторинг (Prometheus + Grafana) залишився працездатним після GitOps-змін.
