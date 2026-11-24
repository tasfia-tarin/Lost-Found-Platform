import { type FormEvent, useEffect, useState } from "react"

import {
  createItem,
  deleteItem as deleteItemService,
  getItem,
  getItems,
  updateItem,
  refreshAccessToken,
  getCurrentUser,
  logout,
  type AuthUser,
} from "./services/api"

import {
  emptyForm,
  type Item,
  type ItemForm,
} from "./types/item"

import ItemFormComponent from "./components/ItemForm"
import ItemList from "./components/ItemList"
import ItemDetails from "./components/ItemDetails"
import Login from "./components/auth/Login"
import Signup from "./components/auth/Signup"
import AdminDashboard from "./components/admin/AdminDashboard"

export default function App() {
  const [currentUser, setCurrentUser] = useState<AuthUser | null>(null)
  const [authLoading, setAuthLoading] = useState(true)
  const [authPage, setAuthPage] = useState<"login" | "signup">("login")

  const [items, setItems] = useState<Item[]>([])
  const [form, setForm] = useState<ItemForm>(emptyForm)
  const [editingId, setEditingId] = useState<number | null>(null)
  const [selectedItem, setSelectedItem] = useState<Item | null>(null)

  const [loading, setLoading] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState("")
  const [message, setMessage] = useState("")

  // Restore login session after page refresh
  useEffect(() => {
    async function restoreSession() {
      try {
        const refreshed = await refreshAccessToken()

        if (refreshed) {
          const user = await getCurrentUser()
          setCurrentUser(user)
        }
      } catch {
        setCurrentUser(null)
      } finally {
        setAuthLoading(false)
      }
    }

    restoreSession()
  }, [])

  // Load items after successful login
  useEffect(() => {
    if (currentUser) {
      loadItems()
    }
  }, [currentUser])

  // Read all items
  async function loadItems() {
    setLoading(true)
    setError("")

    try {
      const data = await getItems()
      setItems(data)
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Something went wrong"
      )
    } finally {
      setLoading(false)
    }
  }

  // Handle form field changes
  function handleFieldChange(
    field: keyof ItemForm,
    value: string
  ) {
    setForm((current) => ({
      ...current,
      [field]: value,
    }))
  }

  // Handle successful login or signup
  function handleAuthSuccess(user: AuthUser) {
    setCurrentUser(user)
    setError("")
    setMessage("Welcome to Lost & Found!")
  }

  // Logout
  async function handleLogout() {
    try {
      await logout()
    } finally {
      setCurrentUser(null)
      setItems([])
      setForm(emptyForm)
      setEditingId(null)
      setSelectedItem(null)
      setMessage("")
      setError("")
      setAuthPage("login")
    }
  }

  // Create or Update item
  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault()

    setError("")
    setMessage("")
    setSaving(true)

    try {
      if (editingId !== null) {
        await updateItem(editingId, form)
        setMessage("Item updated successfully!")
      } else {
        await createItem(form)
        setMessage("Item added successfully!")
      }

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
      const item = await getItem(id)
      setSelectedItem(item)
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
      await deleteItemService(id)

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

  // Show session loading screen
  if (authLoading) {
    return (
      <div className="app-shell">
        <div className="loading">Checking your login session...</div>
      </div>
    )
  }

  // Show Login or Signup page
  if (!currentUser) {
    return authPage === "login" ? (
      <Login
        onLogin={handleAuthSuccess}
        onSwitchToSignup={() => {
          setError("")
          setAuthPage("signup")
        }}
      />
    ) : (
      <Signup
        onSignup={handleAuthSuccess}
        onSwitchToLogin={() => {
          setError("")
          setAuthPage("login")
        }}
      />
    )
  }

  // Main application after login
  return (
    <div className="app-shell">

      <header className="topbar">
        <div className="brand">
          <span>🔎</span>
          <span>Lost & Found</span>
        </div>

        <div className="user-section">
          <span>{currentUser.email}</span>
          <span className="user-role">{currentUser.role}</span>

          <button
            type="button"
            className="secondary-btn"
            onClick={handleLogout}
          >
            Logout
          </button>
        </div>
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

      {/* Admin Dashboard - Only visible to admins */}
      {currentUser.role === "admin" && (
        <AdminDashboard />
      )}

      {/* Item Management */}
      <div className="content-grid">

        <ItemFormComponent
          form={form}
          editingId={editingId}
          saving={saving}
          onFieldChange={handleFieldChange}
          onSubmit={handleSubmit}
          onCancel={cancelEdit}
        />

        <ItemList
          items={items}
          loading={loading}
          onView={viewItem}
          onEdit={editItem}
          onDelete={deleteItem}
        />

      </div>

      {selectedItem && (
        <ItemDetails
          item={selectedItem}
          onClose={() => setSelectedItem(null)}
        />
      )}

      <footer>
        <p>Lost & Found Platform | CSE Project 2026</p>
      </footer>

    </div>
  )
}