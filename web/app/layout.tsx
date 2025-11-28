import Link from 'next/link'
import './globals.css'

export const metadata = {
  title: 'Property Portal',
  description: 'Unified portal for property valuation and market analysis'
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50 text-gray-900">
        <header className="bg-white shadow">
          <div className="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
            <h1 className="text-2xl font-semibold">Property Portal</h1>
            <nav className="space-x-4">
              <Link href="/">Home</Link>
              <Link href="/property-estimator">Estimator</Link>
              <Link href="/property-analysis">Analysis</Link>
            </nav>
          </div>
        </header>
        <main className="max-w-5xl mx-auto p-4">
          {children}
        </main>
      </body>
    </html>
  )
}
