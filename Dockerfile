FROM python:3.11-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99


RUN apt-get update && apt-get install -y \
    chromium chromium-driver xvfb \
    wget unzip curl gnupg ca-certificates fonts-liberation \
    libnss3 libatk-bridge2.0-0 libxss1 libgtk-3-0 \
    libgconf-2-4 libdbus-glib-1-2 libasound2 libpangocairo-1.0-0 libx11-xcb1 \
    build-essential python3-dev libffi-dev libssl-dev \
    && rm -rf /var/lib/apt/lists/*



WORKDIR /my_test


COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt


COPY . .

ENV PYTHONPATH=/my_test
CMD ["pytest","-v", "--headless"]