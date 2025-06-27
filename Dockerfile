FROM apache/airflow:3.0.2

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt

# Копируем папки внутрь контейнера
COPY dags/ /opt/airflow/dags/
COPY plugins/ /opt/airflow/plugins/
COPY config/ /opt/airflow/config/