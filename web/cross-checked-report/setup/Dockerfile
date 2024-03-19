FROM python:3-slim
COPY app .
WORKDIR /app
RUN pip install -r requirements.txt
RUN playwright install-deps
RUN playwright install
EXPOSE 5000
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host", "0.0.0.0"]
