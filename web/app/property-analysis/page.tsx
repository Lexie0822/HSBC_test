'use client'

import { useEffect, useState } from 'react'

interface Stats {
  count: number
  averagePrice: number
  minPrice: number
  maxPrice: number
}

export default function PropertyAnalysis() {
  const [stats, setStats] = useState<Stats | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchStats() {
      try {
        const res = await fetch('http://localhost:8080/statistics')
        if (!res.ok) throw new Error(`Failed: ${res.status}`)
        const data = await res.json()
        setStats(data)
      } catch (err: any) {
        setError(err.message ?? 'Unable to load statistics')
      } finally {
        setLoading(false)
      }
    }
    fetchStats()
  }, [])

  return (
    <section className="space-y-4">
      <h2 className="text-xl font-bold">Property Market Analysis</h2>
      {loading && <p>Loading statistics…</p>}
      {error && <p className="text-red-600">Error: {error}</p>}
      {stats && (
        <div className="grid grid-cols-2 gap-4">
          <div className="p-4 bg-white shadow rounded">
            <h3 className="font-semibold">Number of properties</h3>
            <p>{stats.count}</p>
          </div>
          <div className="p-4 bg-white shadow rounded">
            <h3 className="font-semibold">Average price</h3>
            <p>${stats.averagePrice.toLocaleString()}</p>
          </div>
          <div className="p-4 bg-white shadow rounded">
            <h3 className="font-semibold">Minimum price</h3>
            <p>${stats.minPrice.toLocaleString()}</p>
          </div>
          <div className="p-4 bg-white shadow rounded">
            <h3 className="font-semibold">Maximum price</h3>
            <p>${stats.maxPrice.toLocaleString()}</p>
          </div>
        </div>
      )}
    </section>
  )
}
