import type { Item } from "../types/item"
import ItemCard from "./ItemCard"

interface ItemListProps {
  items: Item[]
  loading: boolean
  onView: (id: number) => void
  onEdit: (item: Item) => void
  onDelete: (id: number) => void
}

export default function ItemList({
  items,
  loading,
  onView,
  onEdit,
  onDelete,
}: ItemListProps) {
  return (
    <section className="panel">
      <h2>Lost & Found Items</h2>

      {loading ? (
        <p className="loading">Loading items...</p>
      ) : items.length === 0 ? (
        <div className="empty-state">
          <p>No items have been reported yet.</p>
          <p>Be the first to report an item!</p>
        </div>
      ) : (
        <div className="item-grid">
          {items.map((item) => (
            <ItemCard
              key={item.id}
              item={item}
              onView={onView}
              onEdit={onEdit}
              onDelete={onDelete}
            />
          ))}
        </div>
      )}
    </section>
  )
}
