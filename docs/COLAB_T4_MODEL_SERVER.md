# Colab T4 Local Model Server

This guide runs all three models on Google Colab T4 and exposes them to the local backend through one HTTP URL.

Model stack:

- STT: `qbsmlabs/PhoWhisper-small`
- TTS: `vieneu`
- LLM: `Qwen/Qwen2.5-1.5B-Instruct` through Hugging Face Transformers

Recommended light demo stack:

- STT: `qbsmlabs/PhoWhisper-small`
- LLM: `Qwen/Qwen2.5-1.5B-Instruct`
- TTS: `vieneu`

Use `qbsmlabs/PhoWhisper-large` only when you want higher STT quality and can accept more VRAM/disk use.

Colab is useful for demos, but it is not stable production hosting. Sessions can stop, public URLs change, and the free T4 allocation is not guaranteed.

## 1. Use The Notebook

Import and run:

```text
docs/colab_t4_model_server1.ipynb
```

In Colab:

1. Runtime -> Change runtime type -> T4 GPU.
2. Run the install cell.
3. Run the config cell. It does not mount Google Drive.
4. Run the server and warmup cells.
5. Copy the printed `REMOTE_MODEL_URL` and `REMOTE_MODEL_TOKEN` into `backend/.env`.

If you previously ran the Gemma4-in-Colab or PhoWhisper-large version, restart the Colab runtime before running the new cells. Otherwise the old Python state can still be alive.

## Temporary Runtime Cache

The notebook stores downloaded models in the current Colab runtime:

```python
MODEL_CACHE_DIR = "/content/ai-interview-model-cache"
os.environ["HF_HOME"] = "/content/ai-interview-model-cache/huggingface"
os.environ["HF_HUB_CACHE"] = "/content/ai-interview-model-cache/huggingface/hub"
```

First run:

- Qwen2.5, PhoWhisper-small, and VieNeu download files into the runtime `huggingface` folder.

Next Colab runtime:

- Run install/config again because the VM and cache are temporary.
- Models may download again after a runtime reset.

If Colab is missing packages, run this install cell again:

```python
!pip -q install fastapi uvicorn pyngrok python-multipart nest_asyncio requests
!pip -q install faster-whisper soundfile static-ffmpeg vieneu
!pip -q install transformers accelerate sentencepiece
```

## 2. Expected Health

The local health cell should show something like:

```python
{
    "ok": True,
    "stt_model": "qbsmlabs/PhoWhisper-small",
    "stt_compute_type": "int8_float16",
    "tts": "vieneu",
    "tts_device": "cpu",
    "llm_backend": "huggingface",
    "llm_model": "Qwen/Qwen2.5-1.5B-Instruct",
    "gpu": "Tesla T4",
}
```

If it still says `qbsmlabs/PhoWhisper-large`, you are running the old notebook state or an old copy of the notebook.

## 3. Backend `.env`

Set the backend to use only the remote local model server:

```env
REMOTE_MODEL_URL=https://your-current-tunnel.trycloudflare.com
REMOTE_MODEL_TOKEN=demo-secret-change-me

STT_PROVIDER=remote
TTS_PROVIDER=remote
LLM_PROVIDER=remote
EVALUATOR_PROVIDER=remote
ALLOW_API_FALLBACK=false
REMOTE_LLM_MODEL=
CV_LLM_PROVIDER=remote

PHOWHISPER_ENABLED=false
LOCAL_STT_MODEL=qbsmlabs/PhoWhisper-small
LOCAL_STT_COMPUTE_TYPE=int8_float16
```

Restart the backend after changing `.env`.

The tunnel URL changes whenever Colab or the tunnel restarts. If `/health` fails with DNS errors like `NameResolutionError`, copy the newest printed URL from Colab into `REMOTE_MODEL_URL`, then restart the backend.

## 4. Tunnel Notes

Ngrok requires an auth token. The notebook uses Cloudflare quick tunnel when no ngrok token is set.

Quick tunnel can take 30-90 seconds before DNS works. If the first public health checks fail, wait a bit and run the test cell again. If it keeps failing, restart only the tunnel cell and copy the new URL.

## 5. Model Notes

Light T4 profile:

```bash
STT_MODEL_ID = "qbsmlabs/PhoWhisper-small"
STT_COMPUTE_TYPE = "int8_float16"
STT_BEAM_SIZE = 1
LLM_BACKEND = "huggingface"
HF_LLM_MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"
LLM_MAX_INPUT_CHARS = 16000
TTS_DEVICE = "cuda"
```

Colab `/llm` uses the Hugging Face Qwen2.5 1.5B model by default. Keep `REMOTE_LLM_MODEL` blank if you do not want to override it.

Backend task LLM settings for full Colab demo mode:

```env
REMOTE_LLM_MODEL=
LLM_PROVIDER=remote
EVALUATOR_PROVIDER=remote
CV_LLM_PROVIDER=remote
```

For Vietnamese STT on a T4 demo, start with `qbsmlabs/PhoWhisper-small`. If audio is noisy or accuracy is not enough, switch back to `qbsmlabs/PhoWhisper-large`.

The T4 has 15 GB VRAM. This profile uses GPU for STT, TTS, and LLM. If VRAM errors happen, change `TTS_DEVICE` back to `cpu` first.

Realtime behavior:

- Session creation uses a fast contextual question plan immediately.
- Hugging Face Qwen2.5 on Colab refines the adaptive plan in the background.
- STT uses `beam_size=1` for speed. Increase to `3` or `5` only if accuracy is more important than latency.
