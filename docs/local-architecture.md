# Local Architecture

The local environment preserves the production service boundaries and API
contracts.

## Text Interview

```text
                         Browser
                            |
                            v
                 React localhost:5173
                            |
                  HTTPS-style bearer flow
                            |
                            v
                FastAPI localhost:8000
                            |
          +-----------------+-----------------+
          |                 |                 |
          v                 v                 v
   Firebase Auth        Firestore       Vertex Gemini
   token verify         persistence     ADC credentials
```

The browser signs in through Firebase, obtains an ID token, and sends it as a
Bearer token. FastAPI verifies identity and ownership before agents or
repositories are invoked.

## Speech Interview

```text
                Browser microphone and playback
                            |
                  WebSocket voice session
                            |
                            v
                FastAPI localhost:8000
                            |
              Internal speech WebSocket
                            |
                            v
            Speech Service localhost:9000
                            |
          +-----------------+-----------------+
          |                 |                 |
          v                 v                 v
     Silero VAD       faster-whisper      VieNeu-TTS
     endpointing      partial/final STT   PCM streaming
```

Audio chunks remain in bounded memory queues. They are not written to Firestore
or the filesystem and are not logged. Final transcripts enter the existing
Interview Orchestrator as normal answers.

## Local Ports

| Port | Process | External protocol |
| --- | --- | --- |
| `5173` | Vite | HTTP |
| `8000` | FastAPI gateway | HTTP and WebSocket |
| `9000` | Speech inference | HTTP health and internal WebSocket |

When Docker Compose is used, the browser still accesses the three localhost
ports. Backend-to-speech traffic uses the Compose DNS name
`speech-service:9000`.

## Trust Boundaries

- Browser-to-backend requests require Firebase ID tokens.
- Voice WebSockets validate Firebase identity, origin, and session ownership.
- Backend-to-speech communication stays behind the service boundary.
- Google Cloud calls use user ADC locally.
- CORS and WebSocket origins allow only `http://localhost:5173`.
- No wildcard origin or local authentication bypass is enabled.
