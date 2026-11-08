import type { Item, ItemForm } from "../types/item"

const API_BASE_URL = ""

export async function getItems(): Promise<Item[]> {
  const response = await fetch(`${API_BASE_URL}/api/items`)

  if (!response.ok) {
    throw new Error("Failed to load items")
  }

  const data: { items: Item[] } = await response.json()
  return data.items
}

export async function getItem(id: number): Promise<Item> {
  const response = await fetch(`${API_BASE_URL}/api/items/${id}`)
  const data: { item: Item; detail?: string } = await response.json()

  if (!response.ok) {
    throw new Error(data.detail || "Failed to load item")
  }

  return data.item
}

export async function createItem(form: ItemForm): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/items`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(form),
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.detail || "Failed to save item")
  }
}

export async function updateItem(
  id: number,
  form: ItemForm
): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/items/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(form),
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.detail || "Failed to update item")
  }
}

export async function deleteItem(id: number): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/items/${id}`, {
    method: "DELETE",
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.detail || "Failed to delete item")
  }
}
