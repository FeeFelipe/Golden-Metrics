FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py /app/
COPY start.sh /app/
RUN chmod +x /app/start.sh
EXPOSE 8080
CMD ["/app/start.sh"]
