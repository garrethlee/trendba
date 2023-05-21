FROM python
COPY . /app
WORKDIR /app
ENV GOOGLE_APPLICATION_CREDENTIALS="credentials/data-service-account.json"
RUN pip install -r requirements.txt
EXPOSE 8050
CMD ["python", "app.py"]