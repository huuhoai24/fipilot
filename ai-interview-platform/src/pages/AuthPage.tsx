import React, { useState } from 'react'
import { Mic, Eye, EyeOff, AlertCircle } from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { Input, Label } from '@/components/ui/Input'
import { useAuthStore } from '@/store/useAuthStore'
import { cn } from '@/lib/utils'

type Mode = 'login' | 'register'

export function AuthPage() {
  const [mode, setMode] = useState<Mode>('login')

  return (
    <div className="flex min-h-screen items-center justify-center bg-bg px-4">
      <div className="w-full max-w-sm">
        {/* Brand */}
        <div className="mb-8 flex flex-col items-center gap-3">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-accent">
            <Mic className="h-6 w-6 text-white" />
          </div>
          <span className="font-display text-lg font-bold tracking-tight-display text-text-primary">
            Fi<span className="text-accent">Pilot</span>
          </span>
        </div>

        {/* Tabs */}
        <div className="mb-6 flex rounded-lg border border-border bg-surface-raised p-1">
          <TabButton active={mode === 'login'} onClick={() => setMode('login')}>
            Đăng nhập
          </TabButton>
          <TabButton active={mode === 'register'} onClick={() => setMode('register')}>
            Đăng ký
          </TabButton>
        </div>

        {mode === 'login' ? <LoginForm /> : <RegisterForm onSuccess={() => setMode('login')} />}
      </div>
    </div>
  )
}

function TabButton({
  active,
  onClick,
  children,
}: {
  active: boolean
  onClick: () => void
  children: React.ReactNode
}) {
  return (
    <button
      onClick={onClick}
      className={cn(
        'flex-1 rounded-md py-2 text-sm font-medium transition-colors duration-150',
        active ? 'bg-accent text-white' : 'text-text-muted hover:text-text-primary'
      )}
    >
      {children}
    </button>
  )
}

function ErrorBanner({ message }: { message: string }) {
  return (
    <div className="mb-4 flex items-start gap-2 rounded-lg border border-danger/30 bg-danger/10 px-3 py-2.5 text-xs text-danger animate-fade-in">
      <AlertCircle className="h-3.5 w-3.5 shrink-0 mt-0.5" />
      <span>{message}</span>
    </div>
  )
}

function LoginForm() {
  const login = useAuthStore((s) => s.login)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    setTimeout(() => {
      const result = login(email, password)
      setLoading(false)
      if (!result.ok) setError(result.error ?? 'Đăng nhập thất bại.')
    }, 400)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4 rounded-card border border-border bg-surface p-6">
      {error && <ErrorBanner message={error} />}
      <div>
        <Label>Email</Label>
        <Input
          type="email"
          placeholder="ban@example.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          autoComplete="email"
        />
      </div>
      <div>
        <Label>Mật khẩu</Label>
        <div className="relative">
          <Input
            type={showPassword ? 'text' : 'password'}
            placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            autoComplete="current-password"
            className="pr-10"
          />
          <button
            type="button"
            onClick={() => setShowPassword((v) => !v)}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-text-faint hover:text-text-muted transition-colors duration-150"
            tabIndex={-1}
          >
            {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
          </button>
        </div>
      </div>
      <Button type="submit" className="w-full" disabled={loading}>
        {loading ? 'Đang đăng nhập…' : 'Đăng nhập'}
      </Button>
      <p className="text-center text-xs text-text-faint">
        Demo admin: admin2026@gmail.com / 123456789
        <br />
        Demo user: minh.tran@example.com / 123456789
      </p>
    </form>
  )
}

function RegisterForm({ onSuccess }: { onSuccess: () => void }) {
  const register = useAuthStore((s) => s.register)
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    setTimeout(() => {
      const result = register(username, email, password)
      setLoading(false)
      if (!result.ok) {
        setError(result.error ?? 'Đăng ký thất bại.')
      }
      // Khi đăng ký thành công, register() đã tự đăng nhập (set currentUser),
      // nên không cần gọi onSuccess để chuyển tab — app sẽ tự vào Dashboard.
    }, 400)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4 rounded-card border border-border bg-surface p-6">
      {error && <ErrorBanner message={error} />}
      <div>
        <Label>Tên người dùng</Label>
        <Input
          placeholder="ten_cua_ban"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
          autoComplete="username"
        />
      </div>
      <div>
        <Label>Email</Label>
        <Input
          type="email"
          placeholder="ban@example.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          autoComplete="email"
        />
      </div>
      <div>
        <Label>Mật khẩu</Label>
        <div className="relative">
          <Input
            type={showPassword ? 'text' : 'password'}
            placeholder="Tối thiểu 8 ký tự"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            autoComplete="new-password"
            className="pr-10"
          />
          <button
            type="button"
            onClick={() => setShowPassword((v) => !v)}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-text-faint hover:text-text-muted transition-colors duration-150"
            tabIndex={-1}
          >
            {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
          </button>
        </div>
      </div>
      <Button type="submit" className="w-full" disabled={loading}>
        {loading ? 'Đang tạo tài khoản…' : 'Tạo tài khoản'}
      </Button>
    </form>
  )
}
