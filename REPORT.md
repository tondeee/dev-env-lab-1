# Звіт з виконання Лабораторної роботи №1

## Мета
Ознайомитись із системою контролю версій Git, відпрацювати базові команди: створення гілок, об'єднання (merging), вирішення конфліктів при злитті, а також оформлення репозиторію.

## Виконані кроки:
1. **Ініціалізація та налаштування:**
   - Створено локальний репозиторій.
   - Створено та налаштовано файл `.gitignore` для ігнорування кешу, середовищ та сирих даних (`__pycache__/`, `.venv/`, `data/raw/` тощо).
   - Створено базову структуру директорій: `data/`, `notebooks/`, `src/`, `reports/figures/`.
   
2. **Оформлення README:**
   - Додано `README.md` з описом мети проєкту, посиланням на відкриті дані (Customer Personality Analysis) та трьома гіпотезами для подальшого аналізу.

3. **Розробка в гілках (Branching & Merging):**
   - У гілці `feature/data_load` створено bash-скрипт (`data_load.sh`) для завантаження набору даних з Kaggle, злито в `main`.
   - У гілках `feature/data_quality_analysis` та `feature/data_research` створено скрипти для перевірки якості даних та аналізу, після чого виконано злиття обох гілок у `main`.
   
4. **Вирішення конфліктів:**
   - Створено дві нові гілки від `main`: `feature/update-readme-1` та `feature/update-readme-2`.
   - В обох гілках змінено секцію структури репозиторію у `README.md`.
   - При спробі злиття другої гілки виник конфлікт, який було успішно вирішено (залишено комбінований покращений варіант опису).
   
5. **Фінальні кроки:**
   - Додано код візуалізації у гілці `feature/visualization` та злито в `main`.
   - Створено `CHANGELOG.md` з описом змін.
   - Створено тег `v0.1.0`.

## Git Log (Історія комітів)

```bash
* 696a94e (HEAD -> main, tag: v0.1.0) docs: Add CHANGELOG.md
*   f07cf68 Merge branch 'feature/visualization': added script for data visualization
|\  
| * a64f024 (feature/visualization) feat: Add visualization script
|/  
*   6bd2c23 Merge branch 'feature/update-readme-2' into main, resolve conflict in README
|\  
| * 311f3b0 (feature/update-readme-2) docs: Modify README directory structure in branch 2
* | 3e59ff1 (feature/update-readme-1) docs: Update README structure description in branch 1
|/  
*   35c337d Merge branch 'feature/data_research': added code for data analysis and models
|\  
| * 2989526 (feature/data_research) feat: Add data research script for hypothesis analysis
|/  
*   30eb3e2 Merge branch 'feature/data_quality_analysis': added script to check data quality
|\  
| * b5c422a (feature/data_quality_analysis) feat: Add data quality analysis script
|/  
* 38ee35a (feature/data_load) feat: Add data load script
* 20c9d3c docs: Add project info, dataset link, and hypotheses to README
* bda6ac3 Initial commit with project structure and .gitignore
```
