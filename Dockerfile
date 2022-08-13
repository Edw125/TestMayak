FROM python:3.9-slim
LABEL author='Edward' version=1.0 description="Mayak"

ENV TELEGRAM_TOKEN="Your token sequence"
WORKDIR /app
COPY requirements.txt .
COPY . .
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir
CMD ["python", "bot.py"]