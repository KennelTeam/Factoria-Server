FROM python

WORKDIR /app

COPY . .

EXPOSE 10001

CMD ["python", "main.py"]
