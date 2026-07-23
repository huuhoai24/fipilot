# Speech inference boundary

This private FastAPI service owns Silero VAD, faster-whisper, and VieNeu-TTS
model dependencies. Deploy it with `Dockerfile.speech`; do not expose its
WebSocket publicly.

The internal WebSocket is `/internal/v1/inference` and requires
`Authorization: Bearer $SPEECH_SERVICE_TOKEN` in production. It accepts
bounded PCM16 frames for STT and streams PCM binary frames for TTS. Audio is
kept in memory and is never persisted or logged.

The public API gateway remains the owner of Firebase authentication, interview
session authorization, orchestration, and browser WebSocket contracts.
Set `SPEECH_SERVICE_URL` and the matching `SPEECH_SERVICE_TOKEN` on the API
service to route inference through this boundary. Leave `SPEECH_SERVICE_URL`
unset only for embedded local development.
