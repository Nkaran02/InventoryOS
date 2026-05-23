import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'InventoryOS',
  description: 'Inventory Reservation System',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}