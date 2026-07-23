type AudioContextFactory = () => AudioContext

export class PcmAudioPlayer {
  private readonly contextFactory: AudioContextFactory
  private context: AudioContext | null = null
  private sampleRate: number | null = null
  private nextStartTime = 0
  private streamComplete = false
  private sources = new Set<AudioBufferSourceNode>()
  private completionResolvers: Array<() => void> = []

  constructor(contextFactory: AudioContextFactory = () => new AudioContext()) {
    this.contextFactory = contextFactory
  }

  async prepare(): Promise<void> {
    if (!this.context || this.context.state === 'closed') {
      this.context = this.contextFactory()
      this.nextStartTime = this.context.currentTime
    }
    if (this.context.state === 'suspended') {
      await this.context.resume()
    }
  }

  beginStream(): void {
    this.streamComplete = false
    this.sampleRate = null
    if (this.context) {
      this.nextStartTime = Math.max(
        this.context.currentTime,
        this.nextStartTime,
      )
    }
  }

  configure(sampleRate: number, format: string): void {
    if (!Number.isInteger(sampleRate) || sampleRate <= 0 || format !== 'pcm') {
      throw new Error('Unsupported TTS audio format.')
    }
    this.sampleRate = sampleRate
  }

  enqueue(payload: ArrayBuffer): void {
    const context = this.context
    const sampleRate = this.sampleRate
    if (!context || context.state === 'closed' || sampleRate === null) {
      throw new Error('TTS audio player is not ready.')
    }
    if (!payload.byteLength || payload.byteLength % 2 !== 0) {
      throw new Error('Invalid PCM16 audio frame.')
    }

    const view = new DataView(payload)
    const samples = new Float32Array(payload.byteLength / 2)
    for (let index = 0; index < samples.length; index += 1) {
      samples[index] = view.getInt16(index * 2, true) / 32768
    }

    const buffer = context.createBuffer(1, samples.length, sampleRate)
    buffer.copyToChannel(samples, 0)
    const source = context.createBufferSource()
    source.buffer = buffer
    source.connect(context.destination)

    const startTime = Math.max(context.currentTime, this.nextStartTime)
    this.nextStartTime = startTime + buffer.duration
    this.sources.add(source)
    source.onended = () => {
      source.disconnect()
      this.sources.delete(source)
      this.resolveCompletionIfReady()
    }
    source.start(startTime)
  }

  markStreamComplete(): Promise<void> {
    this.streamComplete = true
    if (this.sources.size === 0) return Promise.resolve()
    return new Promise((resolve) => {
      this.completionResolvers.push(resolve)
    })
  }

  async close(): Promise<void> {
    for (const source of this.sources) {
      source.onended = null
      try {
        source.stop()
      } catch {
        // The source may already have ended.
      }
      source.disconnect()
    }
    this.sources.clear()
    this.resolveAllCompletions()

    const context = this.context
    this.context = null
    this.sampleRate = null
    this.nextStartTime = 0
    this.streamComplete = false
    if (context && context.state !== 'closed') {
      await context.close()
    }
  }

  private resolveCompletionIfReady(): void {
    if (this.streamComplete && this.sources.size === 0) {
      this.resolveAllCompletions()
    }
  }

  private resolveAllCompletions(): void {
    const resolvers = this.completionResolvers.splice(0)
    resolvers.forEach((resolve) => resolve())
  }
}
