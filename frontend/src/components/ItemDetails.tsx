import type { Item } from "../types/item"

interface ItemDetailsProps {
  item: Item
  onClose: () => void
}

export default function ItemDetails({
  item,
  onClose,
}: ItemDetailsProps) {
  return (
    <section className="panel details-panel">
      <h2>Item Details</h2>

      <h3>{item.title}</h3>

      <p>
        <strong>Description:</strong>{" "}
        {item.description || "Not provided"}
      </p>

      <p>
        <strong>Category:</strong>{" "}
        {item.category || "Not specified"}
      </p>

      <p>
        <strong>Status:</strong> {item.status}
      </p>

      <p>
        <strong>Location:</strong>{" "}
        {item.location || "Not specified"}
      </p>

      <p>
        <strong>Contact:</strong>{" "}
        {item.contact_info || "Not provided"}
      </p>

      <p>
        <strong>Reported on:</strong>{" "}
        {new Date(item.created_at).toLocaleString()}
      </p>

      <button className="secondary-btn" onClick={onClose}>
        Close Details
      </button>
    </section>
  )
}
