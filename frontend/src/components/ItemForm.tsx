import type { FormEvent } from "react"
import type { ItemForm as ItemFormType } from "../types/item"

interface ItemFormProps {
  form: ItemFormType
  editingId: number | null
  saving: boolean
  onFieldChange: (field: keyof ItemFormType, value: string) => void
  onSubmit: (e: FormEvent<HTMLFormElement>) => void
  onCancel: () => void
}

export default function ItemForm({
  form,
  editingId,
  saving,
  onFieldChange,
  onSubmit,
  onCancel,
}: ItemFormProps) {
  return (
    <section className="panel">
      <h2>
        {editingId !== null ? "Edit Item" : "Report an Item"}
      </h2>

      <form onSubmit={onSubmit}>
        <div className="form-grid">
          <div className="field">
            <label>Item Title *</label>
            <input
              type="text"
              value={form.title}
              onChange={(e) => onFieldChange("title", e.target.value)}
              placeholder="Example: Black Wallet"
              required
            />
          </div>

          <div className="field">
            <label>Category</label>
            <input
              type="text"
              value={form.category}
              onChange={(e) => onFieldChange("category", e.target.value)}
              placeholder="Example: Accessories"
            />
          </div>

          <div className="field">
            <label>Status *</label>
            <select
              value={form.status}
              onChange={(e) => onFieldChange("status", e.target.value)}
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
              onChange={(e) => onFieldChange("location", e.target.value)}
              placeholder="Where was it lost or found?"
            />
          </div>

          <div className="field">
            <label>Description</label>
            <textarea
              value={form.description}
              onChange={(e) => onFieldChange("description", e.target.value)}
              placeholder="Describe the item..."
              rows={4}
            />
          </div>

          <div className="field">
            <label>Contact Information</label>
            <input
              type="text"
              value={form.contact_info}
              onChange={(e) => onFieldChange("contact_info", e.target.value)}
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
            onClick={onCancel}
          >
            Cancel Edit
          </button>
        )}
      </form>
    </section>
  )
}
