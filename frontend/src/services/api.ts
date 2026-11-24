import type { Item, ItemForm } from "../types/item"

const API_BASE_URL = ""

export interface AuthUser {
  id: number
  email: string
  role: string
  is_banned?: boolean
}

interface AuthResponse {
  access_token: string
  token_type: string
  user: AuthUser
}

interface RefreshResponse {
  access_token: string
  token_type: string
}

let accessToken: string | null = null

let refreshPromise: Promise<boolean> | null = null

// Store access token in memory
export function setAccessToken(token: string | null): void {
  accessToken = token
}

export function getAccessToken(): string | null {
  return accessToken
}

// Read API response safely
async function readResponse<T>(response: Response): Promise<T> {
  const data = await response.json().catch(() => ({}))

  if (!response.ok) {
    throw new Error(data.detail || "Something went wrong")
  }

  return data as T
}

// SIGNUP
export async function signup(
  email: string,
  password: string
): Promise<AuthResponse> {
  const response = await fetch(`${API_BASE_URL}/api/auth/signup`, {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  })

  const data = await readResponse<AuthResponse>(response)

  setAccessToken(data.access_token)

  return data
}

// LOGIN
export async function login(
  email: string,
  password: string
): Promise<AuthResponse> {
  const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  })

  const data = await readResponse<AuthResponse>(response)

  setAccessToken(data.access_token)

  return data
}

// REFRESH ACCESS TOKEN
export async function refreshAccessToken(): Promise<boolean> {
  if (refreshPromise) {
    return refreshPromise
  }

  refreshPromise = (async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/refresh`, {
        method: "POST",
        credentials: "include",
      })

      if (!response.ok) {
        setAccessToken(null)
        return false
      }

      const data = await response.json() as RefreshResponse

      setAccessToken(data.access_token)

      return true
    } catch {
      setAccessToken(null)
      return false
    } finally {
      refreshPromise = null
    }
  })()

  return refreshPromise
}

// LOGOUT
export async function logout(): Promise<void> {
  try {
    await fetch(`${API_BASE_URL}/api/auth/logout`, {
      method: "POST",
      credentials: "include",
    })
  } finally {
    setAccessToken(null)
  }
}

// COMMON AUTHENTICATED API REQUEST
async function apiRequest(
  url: string,
  options: RequestInit = {},
  retry = true
): Promise<Response> {
  const headers = new Headers(options.headers)

  if (accessToken) {
    headers.set("Authorization", `Bearer ${accessToken}`)
  }

  const response = await fetch(`${API_BASE_URL}${url}`, {
    ...options,
    headers,
    credentials: "include",
  })

  if (response.status === 401 && retry) {
    const refreshed = await refreshAccessToken()

    if (refreshed) {
      return apiRequest(url, options, false)
    }

    setAccessToken(null)
  }

  return response
}

// GET ALL ITEMS
export async function getItems(): Promise<Item[]> {
  const response = await apiRequest("/api/items")

  const data = await readResponse<{ items: Item[] }>(response)

  return data.items
}

// GET SINGLE ITEM
export async function getItem(id: number): Promise<Item> {
  const response = await apiRequest(`/api/items/${id}`)

  const data = await readResponse<{ item: Item }>(response)

  return data.item
}

// CREATE ITEM
export async function createItem(form: ItemForm): Promise<void> {
  const response = await apiRequest("/api/items", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(form),
  })

  await readResponse(response)
}

// UPDATE ITEM
export async function updateItem(
  id: number,
  form: ItemForm
): Promise<void> {
  const response = await apiRequest(`/api/items/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(form),
  })

  await readResponse(response)
}

// DELETE ITEM
export async function deleteItem(id: number): Promise<void> {
  const response = await apiRequest(`/api/items/${id}`, {
    method: "DELETE",
  })

  await readResponse(response)
}


export async function getCurrentUser(): Promise<AuthUser> {
  const response = await apiRequest("/api/auth/me")

  const data = await readResponse<{ user: AuthUser }>(response)

  return data.user
}


// ===============================
// ADMIN API FUNCTIONS
// ===============================

export interface AdminUser {
  id: number
  email: string
  role: string
  is_banned: boolean
  failed_login_attempts?: number
  locked_until?: string | null
  created_at?: string
  updated_at?: string
}

export interface AdminStats {
  [key: string]: number
}

export interface AdminUsersResponse {
  total: number
  limit: number
  offset: number
  users: AdminUser[]
}

export async function getAdminUsers(
  search = "",
  limit = 20,
  offset = 0
): Promise<AdminUsersResponse> {
  const params = new URLSearchParams({
    search,
    limit: String(limit),
    offset: String(offset),
  })

  const response = await apiRequest(`/api/admin/users?${params}`)
  return readResponse<AdminUsersResponse>(response)
}

export async function getAdminStats(): Promise<AdminStats> {
  const response = await apiRequest("/api/admin/stats")
  return readResponse<AdminStats>(response)
}

export async function banUser(
  userId: number,
  reason: string
): Promise<void> {
  const response = await apiRequest(
    `/api/admin/users/${userId}/ban`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ reason }),
    }
  )

  await readResponse(response)
}

export async function unbanUser(userId: number): Promise<void> {
  const response = await apiRequest(
    `/api/admin/users/${userId}/unban`,
    { method: "POST" }
  )

  await readResponse(response)
}

export async function updateUserRole(
  userId: number,
  role: "admin" | "user"
): Promise<void> {
  const response = await apiRequest(
    `/api/admin/users/${userId}/role`,
    {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ role }),
    }
  )

  await readResponse(response)
}

export async function revokeUserSessions(
  userId: number
): Promise<void> {
  const response = await apiRequest(
    `/api/admin/users/${userId}/revoke-sessions`,
    { method: "POST" }
  )

  await readResponse(response)
}

export async function getAuditLogs(): Promise<unknown[]> {
  const response = await apiRequest("/api/admin/audit-logs")
  const data = await readResponse<{ logs: unknown[] }>(response)
  return data.logs
}

export async function getSecurityLogs(): Promise<unknown[]> {
  const response = await apiRequest("/api/admin/security-logs")
  const data = await readResponse<{ logs: unknown[] }>(response)
  return data.logs
}