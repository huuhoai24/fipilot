import { create } from 'zustand'

export interface Account {
  username: string
  email: string
  password: string
  role: 'admin' | 'user'
}

export interface CurrentUser {
  username: string
  email: string
  role: 'admin' | 'user'
}

interface AuthState {
  accounts: Account[]
  currentUser: CurrentUser | null
  login: (email: string, password: string) => { ok: boolean; error?: string }
  register: (username: string, email: string, password: string) => { ok: boolean; error?: string }
  logout: () => void
}

// Seed accounts: admin có sẵn + 1 user thường để demo phân quyền Templates/History.
const seedAccounts: Account[] = [
  {
    username: 'admin',
    email: 'admin2026@gmail.com',
    password: '123456789',
    role: 'admin',
  },
  {
    username: 'minh.tran',
    email: 'minh.tran@example.com',
    password: '123456789',
    role: 'user',
  },
]

export const useAuthStore = create<AuthState>((set, get) => ({
  accounts: seedAccounts,
  currentUser: null,

  login: (email, password) => {
    const account = get().accounts.find(
      (a) => a.email.toLowerCase() === email.trim().toLowerCase()
    )
    if (!account) {
      return { ok: false, error: 'Email chưa được đăng ký.' }
    }
    if (account.password !== password) {
      return { ok: false, error: 'Mật khẩu không đúng.' }
    }
    set({ currentUser: { username: account.username, email: account.email, role: account.role } })
    return { ok: true }
  },

  register: (username, email, password) => {
    const normalizedEmail = email.trim().toLowerCase()
    if (!username.trim() || !email.trim() || !password) {
      return { ok: false, error: 'Vui lòng điền đầy đủ thông tin.' }
    }
    const exists = get().accounts.some((a) => a.email.toLowerCase() === normalizedEmail)
    if (exists) {
      return { ok: false, error: 'Email này đã được đăng ký.' }
    }
    const newAccount: Account = { username: username.trim(), email: email.trim(), password, role: 'user' }
    set((s) => ({
      accounts: [...s.accounts, newAccount],
      currentUser: { username: newAccount.username, email: newAccount.email, role: newAccount.role },
    }))
    return { ok: true }
  },

  logout: () => set({ currentUser: null }),
}))
