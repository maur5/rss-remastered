import { useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { useUIStore } from '@/stores/ui'

function App() {
  const theme = useUIStore((state) => state.theme)

  // Apply dark theme to document root
  useEffect(() => {
    const root = document.documentElement
    root.classList.remove('light', 'dark')

    if (theme === 'system') {
      const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
      root.classList.add(systemTheme)
    } else {
      root.classList.add(theme)
    }
  }, [theme])

  return (
    <div className="min-h-screen bg-background text-foreground flex items-center justify-center p-8">
      <div className="max-w-2xl mx-auto text-center space-y-6">
        <h1 className="text-4xl font-bold">RSS Remastered</h1>
        <p className="text-muted-foreground">
          Frontend project structure initialized successfully!
        </p>
        <div className="space-y-4">
          <p className="text-sm">
            React 19.x + Vite 6.x + Tailwind CSS 4.x + shadcn/ui
          </p>
          <Button>Test Button Component</Button>
        </div>
        <p className="text-xs text-muted-foreground mt-8">
          Story 1-2: Initialize Frontend Project Structure - Complete
        </p>
      </div>
    </div>
  )
}

export default App
