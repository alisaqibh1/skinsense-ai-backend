FROM python:3.10-slim

RUN useradd -m -u 1000 user

USER user

ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

COPY --chown=user requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install huggingface_hub

COPY --chown=user download_model.py .

RUN python download_model.py

COPY --chown=user . /app

EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
