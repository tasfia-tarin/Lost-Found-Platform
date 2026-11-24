import { useEffect, useState } from "react"

import {
  getAdminUsers,
  getAdminStats,
  banUser,
  unbanUser,
  updateUserRole,
  revokeUserSessions,
  getAuditLogs,
  getSecurityLogs,
  type AdminUser,
  type AdminStats,
} from "../../services/api"

export default function AdminDashboard() {
  const [users, setUsers] = useState<AdminUser[]>([])
  const [stats, setStats] = useState<AdminStats | null>(null)
  const [search, setSearch] = useState("")
  const [auditLogs, setAuditLogs] = useState<unknown[]>([])
  const [securityLogs, setSecurityLogs] = useState<unknown[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [message, setMessage] = useState("")

  async function loadDashboard() {
    setLoading(true)
    setError("")

    try {
      const [userData, statsData, auditData, securityData] =
        await Promise.all([
          getAdminUsers(search),
          getAdminStats(),
          getAuditLogs(),
          getSecurityLogs(),
        ])

      setUsers(userData.users)
      setStats(statsData)
      setAuditLogs(auditData)
      setSecurityLogs(securityData)
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to load admin dashboard"
      )
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadDashboard()
  }, [])

  async function handleSearch(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    await loadDashboard()
  }

  async function handleBan(user: AdminUser) {
    const reason = window.prompt(
      `Enter a ban reason for ${user.email}:`
    )

    if (!reason?.trim()) return

    try {
      await banUser(user.id, reason)
      setMessage("User banned successfully!")
      await loadDashboard()
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to ban user")
    }
  }

  async function handleUnban(user: AdminUser) {
    if (!window.confirm(`Unban ${user.email}?`)) return

    try {
      await unbanUser(user.id)
      setMessage("User unbanned successfully!")
      await loadDashboard()
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to unban user")
    }
  }

  async function handleRoleChange(user: AdminUser) {
    const newRole = user.role === "admin" ? "user" : "admin"

    if (!window.confirm(`Change ${user.email}'s role to ${newRole}?`)) {
      return
    }

    try {
      await updateUserRole(user.id, newRole)
      setMessage("User role updated successfully!")
      await loadDashboard()
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update role")
    }
  }

  async function handleRevokeSessions(user: AdminUser) {
    if (!window.confirm(`Revoke all sessions for ${user.email}?`)) {
      return
    }

    try {
      await revokeUserSessions(user.id)
      setMessage("User sessions revoked successfully!")
      await loadDashboard()
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to revoke sessions"
      )
    }
  }

  if (loading) {
    return <div className="admin-dashboard">Loading admin dashboard...</div>
  }

  return (
    <section className="admin-dashboard">
      <div className="admin-heading">
        <div>
          <h2>Admin Dashboard</h2>
          <p>Manage users and monitor platform activity.</p>
        </div>

        <button type="button" onClick={loadDashboard}>
          Refresh
        </button>
      </div>

      {error && <div className="error">{error}</div>}
      {message && <div className="notice">{message}</div>}

      <div className="admin-stats">
        <div className="stat-card">
          <h3>Total Users</h3>
          <strong>{stats?.total_users ?? 0}</strong>
        </div>

        <div className="stat-card">
          <h3>Administrators</h3>
          <strong>{stats?.total_admins ?? 0}</strong>
        </div>

        <div className="stat-card">
          <h3>Regular Users</h3>
          <strong>{stats?.total_regular_users ?? 0}</strong>
        </div>

        <div className="stat-card">
          <h3>Banned Users</h3>
          <strong>{stats?.banned_users ?? 0}</strong>
        </div>
      </div>

      <div className="admin-users">
        <h3>User Management</h3>

        <form className="admin-search" onSubmit={handleSearch}>
          <input
            type="text"
            placeholder="Search users by email..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />

          <button type="submit">Search</button>
        </form>

        <div className="admin-table-wrapper">
          <table className="admin-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Email</th>
                <th>Role</th>
                <th>Status</th>
                <th>Failed Logins</th>
                <th>Actions</th>
              </tr>
            </thead>

            <tbody>
              {users.map((user) => (
                <tr key={user.id}>
                  <td>{user.id}</td>
                  <td>{user.email}</td>
                  <td>{user.role}</td>
                  <td>
                    {user.is_banned ? "Banned" : "Active"}
                  </td>
                  <td>{user.failed_login_attempts ?? 0}</td>
                  <td>
                    <div className="admin-actions">
                      {user.role !== "admin" && (
                        <>
                          {user.is_banned ? (
                            <button
                              type="button"
                              onClick={() => handleUnban(user)}
                            >
                              Unban
                            </button>
                          ) : (
                            <button
                              type="button"
                              onClick={() => handleBan(user)}
                            >
                              Ban
                            </button>
                          )}

                          <button
                            type="button"
                            onClick={() => handleRoleChange(user)}
                          >
                            Make Admin
                          </button>
                        </>
                      )}

                      {user.role === "admin" && (
                        <button
                          type="button"
                          onClick={() => handleRoleChange(user)}
                        >
                          Make User
                        </button>
                      )}

                      <button
                        type="button"
                        onClick={() => handleRevokeSessions(user)}
                      >
                        Revoke Sessions
                      </button>
                    </div>
                  </td>
                </tr>
              ))}

              {users.length === 0 && (
                <tr>
                  <td colSpan={6}>No users found.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      <div className="admin-logs">
        <h3>Recent Audit Logs</h3>
        <pre>{JSON.stringify(auditLogs, null, 2)}</pre>

        <h3>Recent Security Logs</h3>
        <pre>{JSON.stringify(securityLogs, null, 2)}</pre>
      </div>
    </section>
  )
}