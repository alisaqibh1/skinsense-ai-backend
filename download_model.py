import os
import shutil
from huggingface_hub import hf_hub_download

token = os.environ.get('HF_TOKEN')
files = ['pytorch_model.bin', 'config.json', 'preprocessor_config.json']

for f in files:
    print(f'Downloading {f}...')
    path = hf_hub_download(
        repo_id='alisaqib14/skin-disease-model',
        filename=f,
        repo_type='model',
        token=token
    )
    shutil.copy(path, f'./{f}')
    print(f'Downloaded: {f}')

print('All files downloaded!')
