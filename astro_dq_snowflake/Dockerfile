FROM quay.io/astronomer/astro-runtime:12.7.1

RUN python -m venv soda_venv && source soda_venv/bin/activate && \
    pip install --no-cache-dir soda-core-snowflake &&\
    pip install --no-cache-dir soda-core-scientific && deactivate