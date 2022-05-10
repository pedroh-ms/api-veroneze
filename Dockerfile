FROM python:3.9-bullseye

WORKDIR /api_veroneze

ENV DATABASE=postgresql

COPY . .

RUN pip install -e .

EXPOSE 5000

CMD ["python", "src/api_veroneze/server.py"]