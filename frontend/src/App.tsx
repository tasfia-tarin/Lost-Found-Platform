import { type FormEvent, useEffect, useState } from "react"

const API_BASE_URL = "http://127.0.0.1:8000"

interface Item {
  id: number
  title: string
  description: string | null
  category: string | null
  status: string
  location: string | null
  contact_info: string | null
  created_at: string
}

interface ItemForm {
  title: string
  description: string
  category: string
  status: string
  location: string
  contact_info: string
}

const emptyForm: ItemForm = {
  title: "",
  description: "",
  category: "",
  status: "lost",
  location: "",
  contact_info: "",
}

export default function App() {
  const [items, setItems] = useState<Item[]>([])
  const [form, setForm] = useState<ItemForm>(emptyForm)
  const [editingId, setEditingId] = useState<number | null>(null)
  const [selectedItem, setSelectedItem] = useState<Item | null>(null)

  const [loading, setLoading] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState("")
  const [message, setMessage] = useState("")

  // Read all items
  async function loadItems() {
    setLoading(true)
    setError("")

    try {
      const response = await fetch(`${API_BASE_URL}/api/items`)

      if (!response.ok) {
        throw new Error("Failed to load items")
      }

      const data: { items: Item[] } = await response.json()
      setItems(data.items)
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Something went wrong"
      )
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadItems()
  }, [])

  // Create or Update item
  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault()

    setError("")
    setMessage("")
    setSaving(true)

    try {
      const url =
        editingId !== null
          ? `${API_BASE_URL}/api/items/${editingId}`
          : `${API_BASE_URL}/api/items`

      const response = await fetch(url, {
        method: editingId !== null ? "PUT" : "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || "Failed to save item")
      }

      setMessage(
        editingId !== null
          ? "Item updated successfully!"
          : "Item added successfully!"
      )

      setForm(emptyForm)
      setEditingId(null)
      setSelectedItem(null)

      await loadItems()
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Something went wrong"
      )
    } finally {
      setSaving(false)
    }
  }

  // View single item
  async function viewItem(id: number) {
    setError("")

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/items/${id}`
      )

      const data: { item: Item; detail?: string } =
        await response.json()

      if (!response.ok) {
        throw new Error(data.detail || "Failed to load item")
      }

      setSelectedItem(data.item)
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Something went wrong"
      )
    }
  }

  // Edit item
  function editItem(item: Item) {
    setEditingId(item.id)

    setForm({
      title: item.title,
      description: item.description || "",
      category: item.category || "",
      status: item.status,
      location: item.location || "",
      contact_info: item.contact_info || "",
    })

    setSelectedItem(null)
    setMessage("")
    setError("")

    window.scrollTo({ top: 0, behavior: "smooth" })
  }

  // Delete item
  async function deleteItem(id: number) {
    const confirmed = window.confirm(
      "Are you sure you want to delete this item?"
    )

    if (!confirmed) return

    setError("")
    setMessage("")

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/items/${id}`,
        {
          method: "DELETE",
        }
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || "Failed to delete item")
      }

      setMessage("Item deleted successfully!")

      if (selectedItem?.id === id) {
        setSelectedItem(null)
      }

      if (editingId === id) {
        cancelEdit()
      }

      await loadItems()
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Something went wrong"
      )
    }
  }

  // Reset form
  function cancelEdit() {
    setForm(emptyForm)
    setEditingId(null)
    setError("")
    setMessage("")
  }

  return (
    <div className="app-shell">

      <header className="topbar">
        <div className="brand">
          <span>🔎</span>
          <span>Lost & Found</span>
        </div>
        <span>Find what matters.</span>
      </header>

      <section className="hero">
        <h1>Lost Something? Found Something?</h1>
        <p>
          Help your community reconnect with lost belongings.
          Report lost and found items here.
        </p>
      </section>

      {message && (
        <div className="notice">
          {message}
        </div>
      )}

      {error && (
        <div className="error">
          {error}
        </div>
      )}

      <div className="content-grid">

        {/* Item Form */}

        <section className="panel">
          <h2>
            {editingId !== null ? "Edit Item" : "Report an Item"}
          </h2>

          <form onSubmit={handleSubmit}>

            <div className="form-grid">

              <div className="field">
                <label>Item Title *</label>
                <input
                  type="text"
                  value={form.title}
                  onChange={(e) =>
                    setForm({ ...form, title: e.target.value })
                  }
                  placeholder="Example: Black Wallet"
                  required
                />
              </div>

              <div className="field">
                <label>Category</label>
                <input
                  type="text"
                  value={form.category}
                  onChange={(e) =>
                    setForm({ ...form, category: e.target.value })
                  }
                  placeholder="Example: Accessories"
                />
              </div>

              <div className="field">
                <label>Status *</label>
                <select
                  value={form.status}
                  onChange={(e) =>
                    setForm({ ...form, status: e.target.value })
                  }
                >
                  <option value="lost">Lost</option>
                  <option value="found">Found</option>
                </select>
              </div>

              <div className="field">
                <label>Location</label>
                <input
                  type="text"
                  value={form.location}
                  onChange={(e) =>
                    setForm({ ...form, location: e.target.value })
                  }
                  placeholder="Where was it lost or found?"
                />
              </div>

              <div className="field">
                <label>Description</label>
                <textarea
                  value={form.description}
                  onChange={(e) =>
                    setForm({ ...form, description: e.target.value })
                  }
                  placeholder="Describe the item..."
                  rows={4}
                />
              </div>

              <div className="field">
                <label>Contact Information</label>
                <input
                  type="text"
                  value={form.contact_info}
                  onChange={(e) =>
                    setForm({ ...form, contact_info: e.target.value })
                  }
                  placeholder="Phone number or email"
                />
              </div>

            </div>

            <button
              type="submit"
              className="primary-btn"
              disabled={saving}
            >
              {saving
                ? "Saving..."
                : editingId !== null
                  ? "Update Item"
                  : "Add Item"}
            </button>

            {editingId !== null && (
              <button
                type="button"
                className="secondary-btn"
                onClick={cancelEdit}
              >
                Cancel Edit
              </button>
            )}

          </form>
        </section>

        {/* Items List */}

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
                <article className="item-card" key={item.id}>

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
                      onClick={() => viewItem(item.id)}
                    >
                      View
                    </button>

                    <button
                      className="secondary-btn"
                      onClick={() => editItem(item)}
                    >
                      Edit
                    </button>

                    <button
                      className="delete-btn"
                      onClick={() => deleteItem(item.id)}
                    >
                      Delete
                    </button>

                  </div>

                </article>
              ))}

            </div>
          )}
        </section>

      </div>

      {/* Selected Item Details */}

      {selectedItem && (
        <section className="panel details-panel">

          <h2>Item Details</h2>

          <h3>{selectedItem.title}</h3>

          <p>
            <strong>Description:</strong>{" "}
            {selectedItem.description || "Not provided"}
          </p>

          <p>
            <strong>Category:</strong>{" "}
            {selectedItem.category || "Not specified"}
          </p>

          <p>
            <strong>Status:</strong> {selectedItem.status}
          </p>

          <p>
            <strong>Location:</strong>{" "}
            {selectedItem.location || "Not specified"}
          </p>

          <p>
            <strong>Contact:</strong>{" "}
            {selectedItem.contact_info || "Not provided"}
          </p>

          <p>
            <strong>Reported on:</strong>{" "}
            {new Date(selectedItem.created_at).toLocaleString()}
          </p>

          <button
            className="secondary-btn"
            onClick={() => setSelectedItem(null)}
          >
            Close Details
          </button>

        </section>
      )}

      <footer>
        <p>Lost & Found Platform | CSE Project 2026</p>
      </footer>

    </div>
  )
}