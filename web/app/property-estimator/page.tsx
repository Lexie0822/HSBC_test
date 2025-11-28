'use client'

import { useState } from 'react'

interface FormData {
  square_footage: number
  bedrooms: number
  bathrooms: number
  year_built: number
  lot_size: number
  distance_to_city_center: number
  school_rating: number
}

export default function PropertyEstimator() {
  const [form, setForm] = useState<FormData>({
    square_footage: 1500,
    bedrooms: 3,
    bathrooms: 2,
    year_built: 2000,
    lot_size: 5000,
    distance_to_city_center: 5,
    school_rating: 7
  })
  const [prediction, setPrediction] = useState<number | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const { name, value } = e.target
    setForm(prev => ({ ...prev, [name]: Number(value) }))
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setError(null)
    try {
      const res = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form)
      })
      if (!res.ok) {
        throw new Error(`Request failed with status ${res.status}`)
      }
      const data = await res.json()
      if (Array.isArray(data.predictions) && data.predictions.length > 0) {
        setPrediction(data.predictions[0])
      }
    } catch (err: any) {
      setError(err.message ?? 'An unexpected error occurred')
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="space-y-4">
      <h2 className="text-xl font-bold">Property Value Estimator</h2>
      <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
        <label className="flex flex-col">
          <span>Square Footage</span>
          <input
            type="number"
            name="square_footage"
            value={form.square_footage}
            onChange={handleChange}
            className="border p-1 rounded"
            required
          />
        </label>
        <label className="flex flex-col">
          <span>Bedrooms</span>
          <input
            type="number"
            name="bedrooms"
            value={form.bedrooms}
            onChange={handleChange}
            className="border p-1 rounded"
            required
          />
        </label>
        <label className="flex flex-col">
          <span>Bathrooms</span>
          <input
            type="number"
            step="0.5"
            name="bathrooms"
            value={form.bathrooms}
            onChange={handleChange}
            className="border p-1 rounded"
            required
          />
        </label>
        <label className="flex flex-col">
          <span>Year Built</span>
          <input
            type="number"
            name="year_built"
            value={form.year_built}
            onChange={handleChange}
            className="border p-1 rounded"
            required
          />
        </label>
        <label className="flex flex-col">
          <span>Lot Size (sq ft)</span>
          <input
            type="number"
            name="lot_size"
            value={form.lot_size}
            onChange={handleChange}
            className="border p-1 rounded"
            required
          />
        </label>
        <label className="flex flex-col">
          <span>Distance to City Center (miles)</span>
          <input
            type="number"
            step="0.1"
            name="distance_to_city_center"
            value={form.distance_to_city_center}
            onChange={handleChange}
            className="border p-1 rounded"
            required
          />
        </label>
        <label className="flex flex-col">
          <span>School Rating (0–10)</span>
          <input
            type="number"
            step="0.1"
            name="school_rating"
            value={form.school_rating}
            onChange={handleChange}
            min={0}
            max={10}
            className="border p-1 rounded"
            required
          />
        </label>
        <button
          type="submit"
          className="col-span-2 py-2 px-4 bg-blue-600 text-white rounded hover:bg-blue-700"
          disabled={loading}
        >
          {loading ? 'Predicting…' : 'Get Estimate'}
        </button>
      </form>
      {prediction !== null && (
        <p className="mt-4">Estimated price: <strong>${prediction.toLocaleString()}</strong></p>
      )}
      {error && <p className="text-red-600 mt-2">Error: {error}</p>}
    </section>
  )
}
