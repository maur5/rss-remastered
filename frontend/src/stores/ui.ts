import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface UIState {
  sidebarCollapsed: boolean
  contextPanelOpen: boolean
  theme: 'dark' | 'light' | 'system'
  toggleSidebar: () => void
  toggleContextPanel: () => void
  setTheme: (theme: 'dark' | 'light' | 'system') => void
}

export const useUIStore = create<UIState>()(
  persist(
    (set) => ({
      sidebarCollapsed: false,
      contextPanelOpen: true,
      theme: 'dark',
      toggleSidebar: () => set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),
      toggleContextPanel: () => set((state) => ({ contextPanelOpen: !state.contextPanelOpen })),
      setTheme: (theme) => set({ theme }),
    }),
    {
      name: 'rss-ui-storage',
    }
  )
)
