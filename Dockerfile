FROM apache/airflow:3.0.2

COPY requirements.txt ./
RUN pip install --no-cache-dir -r ./requirements.txt

COPY dags /opt/airflow/dags
COPY plugins /opt/airflow/plugins
COPY config /opt/airflow/config