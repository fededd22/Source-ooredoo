# ============================================================
# OOREDOO CLI - power 6 terminal.py
# ============================================================
FROM python:3.11-slim

LABEL maintainer="moon" \
      description="Ooredoo CLI Activator - power 6 terminal" \
      version="1.0.0"

# ---------- متغيرات البيئة ----------
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    APP_HOME=/app \
    SESSION_FILE=/data/ooredoo_session.json

# ---------- حزم النظام ----------
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        tzdata \
    && rm -rf /var/lib/apt/lists/* \
    && ln -snf /usr/share/zoneinfo/Africa/Algiers /etc/localtime \
    && echo "Africa/Algiers" > /etc/timezone

WORKDIR ${APP_HOME}

# ---------- الاعتماديات ----------
RUN pip install --no-cache-dir requests urllib3

# ---------- نسخ السكربت (إعادة تسميته بدون مسافات) ----------
COPY ["power 6 terminal.py", "/app/power6_terminal.py"]

# ---------- مستخدم غير جذري + مجلد الجلسات ----------
RUN useradd -m -u 1000 -s /bin/bash ooredoo \
    && mkdir -p /data \
    && chown -R ooredoo:ooredoo ${APP_HOME} /data

USER ooredoo

VOLUME ["/data"]

# ---------- نقطة الدخول ----------
ENTRYPOINT ["python", "-u", "/app/power6_terminal.py"]
