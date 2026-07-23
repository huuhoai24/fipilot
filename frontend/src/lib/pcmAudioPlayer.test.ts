import { describe, expect, it, vi } from 'vitest'
import { PcmAudioPlayer } from '@/lib/pcmAudioPlayer'

class FakeBuffer {
  readonly duration: number
  readonly copyToChannel = vi.fn()

  constructor(length: number, sampleRate: number) {
    this.duration = length / sampleRate
  }
}

class FakeSource {
  buffer: FakeBuffer | null = null
  onended: (() => void) | null = null
  readonly connect = vi.fn()
  readonly disconnect = vi.fn()
  readonly stop = vi.fn()
  readonly start = vi.fn()

  finish() {
    this.onended?.()
  }
}

class FakeContext {
  state: AudioContextState = 'suspended'
  currentTime = 0
  destination = {}
  sources: FakeSource[] = []
  readonly resume = vi.fn(async () => {
    this.state = 'running'
  })
  readonly close = vi.fn(async () => {
    this.state = 'closed'
  })

  createBuffer(_channels: number, length: number, sampleRate: number) {
    return new FakeBuffer(length, sampleRate)
  }

  createBufferSource() {
    const source = new FakeSource()
    this.sources.push(source)
    return source
  }
}

describe('PcmAudioPlayer', () => {
  it('queues PCM chunks continuously and resolves after playback drains', async () => {
    const context = new FakeContext()
    const player = new PcmAudioPlayer(
      () => context as unknown as AudioContext
    )
    await player.prepare()
    player.beginStream()
    player.configure(24000, 'pcm')

    player.enqueue(new Int16Array([100, 200, 300, 400]).buffer)
    player.enqueue(new Int16Array([500, 600, 700, 800]).buffer)

    expect(context.sources).toHaveLength(2)
    expect(context.sources[0].start).toHaveBeenCalledWith(0)
    expect(context.sources[1].start).toHaveBeenCalledWith(4 / 24000)

    let completed = false
    const completion = player.markStreamComplete().then(() => {
      completed = true
    })
    context.sources[0].finish()
    await Promise.resolve()
    expect(completed).toBe(false)
    context.sources[1].finish()
    await completion
    expect(completed).toBe(true)

    await player.close()
    expect(context.close).toHaveBeenCalled()
  })

  it('stops queued sources during cleanup', async () => {
    const context = new FakeContext()
    const player = new PcmAudioPlayer(
      () => context as unknown as AudioContext
    )
    await player.prepare()
    player.beginStream()
    player.configure(24000, 'pcm')
    player.enqueue(new Int16Array([100, 200]).buffer)

    await player.close()

    expect(context.sources[0].stop).toHaveBeenCalled()
    expect(context.sources[0].disconnect).toHaveBeenCalled()
  })
})
