'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'

export default function ReservationPage() {
  const [reservation, setReservation] = useState<any>(null)
  const [message, setMessage] = useState('')
  const [timeLeft, setTimeLeft] = useState(0)

  const router = useRouter()

  useEffect(() => {
    const stored = localStorage.getItem('reservation')

    if (!stored) {
      router.push('/')
      return
    }

    const data = JSON.parse(stored)
    setReservation(data)

    const expiry = new Date(data.expires_at).getTime()

    const interval = setInterval(() => {
      const now = Date.now()
      const diff = Math.floor((expiry - now) / 1000)

      if (diff <= 0) {
        clearInterval(interval)
        setTimeLeft(0)
      } else {
        setTimeLeft(diff)
      }
    }, 1000)

    return () => clearInterval(interval)
  }, [router])

  const confirmReservation = async () => {
    const res = await fetch(
      `https://inventoryos.onrender.com/api/reservations/${reservation.id}/confirm`,
      {
        method: 'POST',
      }
    )

    if (res.status === 410) {
      setMessage('Reservation expired')
      return
    }

    setMessage('Reservation confirmed')
  }

  const cancelReservation = async () => {
    await fetch(
      `https://inventoryos.onrender.com/api/reservations/${reservation.id}/release`,
      {
        method: 'POST',
      }
    )

    setMessage('Reservation cancelled')
  }

  if (!reservation) return null

  return (
    <div className="container">
      <h1 className="title">Reservation</h1>

      <div className="card">
        <p>
          Product ID: {reservation.product_id}
        </p>

        <p>
          Warehouse ID:{' '}
          {reservation.warehouse_id}
        </p>

        <p>Quantity: {reservation.quantity}</p>

        <p>Status: {reservation.status}</p>

        <p>
          Time Left: {timeLeft} seconds
        </p>

        <button onClick={confirmReservation}>
          Confirm Purchase
        </button>

        <button
          onClick={cancelReservation}
          style={{ marginLeft: '10px' }}
        >
          Cancel
        </button>

        {message && (
          <p className="success">{message}</p>
        )}
      </div>
    </div>
  )
}