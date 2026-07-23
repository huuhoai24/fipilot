class PCM16CaptureProcessor extends AudioWorkletProcessor {
  constructor() {
    super()
    this.frameSize = 512
    this.buffer = new Int16Array(this.frameSize)
    this.offset = 0
  }

  process(inputs) {
    const input = inputs[0]?.[0]
    if (!input) return true

    for (let index = 0; index < input.length; index += 1) {
      const sample = Math.max(-1, Math.min(1, input[index]))
      this.buffer[this.offset] = sample < 0 ? sample * 32768 : sample * 32767
      this.offset += 1
      if (this.offset === this.frameSize) {
        const payload = this.buffer.buffer
        this.port.postMessage(payload, [payload])
        this.buffer = new Int16Array(this.frameSize)
        this.offset = 0
      }
    }
    return true
  }
}

registerProcessor('pcm16-capture', PCM16CaptureProcessor)
