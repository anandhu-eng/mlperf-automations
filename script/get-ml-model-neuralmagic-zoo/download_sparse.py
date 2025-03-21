from sparsezoo import Model
import os

model_stub = os.environ.get('MLC_MODEL_ZOO_STUB', '')
print(f"Downloading model {model_stub}")
stub = f"{model_stub}"
model = Model(stub)

with open('tmp-run-env.out', 'w') as f:
    f.write(f"MLC_ML_MODEL_FILE_WITH_PATH={model.path}")
