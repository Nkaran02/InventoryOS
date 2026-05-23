'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'

type WarehouseStock = {
  warehouse_id: number
  available_stock: number
}

type Product = {
  id: number
  name: string
  warehouses: WarehouseStock[]
}

export default function HomePage() {
  const [products, setProducts] = useState<Product[]>([])
  const [error, setError] = useState('')
  const router = useRouter()

  useEffect(() => {
    fetch('https://inventoryos.onrender.com/api/products')
      .then((res) => res.json())
      .then((data) => setProducts(data))
  }, [])

  const reserveStock = async (
    productId: number,
    warehouseId: number
  ) => {
    try {
      setError('')

      const res = await fetch(
        'https://inventoryos.onrender.com/api/reservations',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            product_id: productId,
            warehouse_id: warehouseId,
            quantity: 1,
          }),
        }
      )

      if (res.status === 409) {
        setError('Not enough stock available')
        return
      }

      const data = await res.json()

      localStorage.setItem(
        'reservation',
        JSON.stringify(data)
      )

      router.push('/reservation')
    } catch {
      setError('Reservation failed')
    }
  }

  return (
    <div className="container">
      <h1 className="title">InventoryOS</h1>

      {error && <p className="error">{error}</p>}

      <div className="grid">
        {products.map((product) => (
          <div className="card" key={product.id}>
            <h2>{product.name}</h2>

            {product.warehouses.map((warehouse) => (
              <div
                className="stock"
                key={warehouse.warehouse_id}
              >
                <p>
                  Warehouse: {warehouse.warehouse_id}
                </p>

                <p>
                  Available Stock:{' '}
                  {warehouse.available_stock}
                </p>

                <button
                  onClick={() =>
                    reserveStock(
                      product.id,
                      warehouse.warehouse_id
                    )
                  }
                >
                  Reserve
                </button>
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  )
}