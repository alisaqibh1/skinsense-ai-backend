FROM python:3.10-slim

RUN useradd -m -u 1000 user

USER user

ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

COPY --chown=user requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install huggingface_hub

RUN python -c "import os\nfrom huggingface_hub import hf_hub_download\nimport shutil\ntoken = os.environ.get('HF_TOKEN')\nfiles = ['pytorch_model.bin', 'config.json', 'preprocessor_config.json']\nfor f in files:\n    path = hf_hub_download(repo_id='alisaqib14/skin-disease-model', filename=f, repo_type='model', token=token)\n    shutil.copy(path, f'./{f}')\n    print(f'Downloaded: {f}')"

COPY --chown=user . /app

EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
