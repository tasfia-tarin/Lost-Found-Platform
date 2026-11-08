import type { Item } from "../types/item"

interface ItemCardProps {
  item: Item
  onView: (id: number) => void
  onEdit: (item: Item) => void
  onDelete: (id: number) => void
}

export default function ItemCard({
  item,
  onView,
  onEdit,
  onDelete,
}: ItemCardProps) {
  return (
    <article className="item-card">
      <span
        className={`status ${
          item.status === "found" ? "found" : ""
        }`}
      >
        {item.status.toUpperCase()}
      </span>

      <h3>{item.title}</h3>

      <p>
        <strong>Category:</strong>{" "}
        {item.category || "Not specified"}
      </p>

      <p>
        <strong>Location:</strong>{" "}
        {item.location || "Not specified"}
      </p>

      <div className="card-actions">
        <button
          className="secondary-btn"
          onClick={() => onView(item.id)}
        >
          View
        </button>

        <button
          className="secondary-btn"
          onClick={() => onEdit(item)}
        >
          Edit
        </button>

        <button
          className="delete-btn"
          onClick={() => onDelete(item.id)}
        >
          Delete
        </button>
      </div>
    </article>
  )
}
