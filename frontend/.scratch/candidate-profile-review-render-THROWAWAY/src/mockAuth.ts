// THROWAWAY deterministic auth boundary for rendering the production layout.
export function useAuth() {
  return {
    user: {
      displayName: 'Nguyễn Minh Anh',
      email: 'minh.anh@example.com',
    },
    loading: false,
    logout: async () => undefined,
  }
}
