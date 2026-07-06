import { create } from 'zustand'

export interface RunningSessionMeta {
  sessionId: string
  candidateName: string
  startedAt: number // epoch ms, chỉ dùng để sắp xếp/hiển thị, không phục vụ tính giờ UI
  paused: boolean
}

interface ActiveSessionsState {
  /** Các phòng phỏng vấn đang mở, key theo sessionId. Nhiều phiên có thể chạy song song. */
  sessions: Record<string, RunningSessionMeta>

  /** Đánh dấu một phiên đang mở — gọi khi vào phòng phỏng vấn (Interview Flow hoặc Dashboard). */
  startSession: (params: { sessionId: string; candidateName: string }) => void
  setPaused: (sessionId: string, paused: boolean) => void
  /** Gỡ một phiên khỏi danh sách "đang mở" — gọi khi kết thúc phỏng vấn. */
  endSession: (sessionId: string) => void
}

export const useActiveSessionStore = create<ActiveSessionsState>((set) => ({
  sessions: {},

  startSession: ({ sessionId, candidateName }) =>
    set((s) => ({
      sessions: {
        ...s.sessions,
        [sessionId]: {
          sessionId,
          candidateName,
          startedAt: Date.now(),
          paused: false,
        },
      },
    })),

  setPaused: (sessionId, paused) =>
    set((s) => {
      const session = s.sessions[sessionId]
      if (!session) return s
      return { sessions: { ...s.sessions, [sessionId]: { ...session, paused } } }
    }),

  endSession: (sessionId) =>
    set((s) => {
      const { [sessionId]: _removed, ...rest } = s.sessions
      return { sessions: rest }
    }),
}))
