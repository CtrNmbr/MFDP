FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt


COPY requirements_after_torch.txt .

RUN pip install torch==2.6.0 --extra-index-url https://download.pytorch.org/whl/cpu 

RUN pip install torch-scatter torch-sparse torch-cluster torch-geometric \
  -f https://data.pyg.org/whl/torch-2.6.0+cpu.html 

RUN pip install --upgrade pip && pip install -r requirements_after_torch.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/:/app"

EXPOSE 8080

ENTRYPOINT ["python", "src/api.py"]