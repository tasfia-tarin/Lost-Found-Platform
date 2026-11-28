import { useEffect, useState } from "react"

import {
  createGroup,
  getGroups,
  deleteGroup,
  type Group,
} from "../services/api"

export default function GroupManagement() {
  const [groups, setGroups] = useState<Group[]>([])
  const [name, setName] = useState("")
  const [description, setDescription] = useState("")
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState("")
  const [message, setMessage] = useState("")

  async function loadGroups() {
    setLoading(true)
    setError("")

    try {
      const data = await getGroups()
      setGroups(data)
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to load groups"
      )
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadGroups()
  }, [])

  async function handleCreateGroup(
    e: React.FormEvent<HTMLFormElement>
  ) {
    e.preventDefault()

    if (!name.trim()) {
      setError("Group name is required")
      return
    }

    setSaving(true)
    setError("")
    setMessage("")

    try {
      await createGroup(name, description)

      setName("")
      setDescription("")
      setMessage("Group created successfully!")

      await loadGroups()
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to create group"
      )
    } finally {
      setSaving(false)
    }
  }

  async function handleDeleteGroup(groupId: number) {
    const confirmed = window.confirm(
      "Are you sure you want to delete this group?"
    )

    if (!confirmed) return

    setError("")
    setMessage("")

    try {
      await deleteGroup(groupId)

      setMessage("Group deleted successfully!")
      await loadGroups()
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to delete group"
      )
    }
  }

  return (
    <section className="group-management">

      <div className="panel">
        <h2>👥 Group Management</h2>

        <p>
          Create groups and collaborate with other users.
        </p>

        {message && (
          <div className="notice">{message}</div>
        )}

        {error && (
          <div className="error">{error}</div>
        )}

        <form
          className="form-grid"
          onSubmit={handleCreateGroup}
        >
          <div className="field">
            <label>Group Name</label>

            <input
              type="text"
              placeholder="Enter group name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>

          <div className="field">
            <label>Description</label>

            <textarea
              placeholder="Enter group description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </div>

          <button
            type="submit"
            className="primary-btn"
            disabled={saving}
          >
            {saving ? "Creating..." : "Create Group"}
          </button>
        </form>
      </div>

      <div className="panel group-list-panel">
        <h2>My Groups</h2>

        {loading ? (
          <p className="loading">Loading groups...</p>
        ) : groups.length === 0 ? (
          <div className="empty-state">
            You haven't created or joined any groups yet.
          </div>
        ) : (
          <div className="group-grid">
            {groups.map((group) => (
              <div className="group-card" key={group.id}>
                <h3>{group.name}</h3>

                <p>
                  {group.description || "No description provided"}
                </p>

                <span className="user-role">
                  {group.member_role}
                </span>

                <p>
                  Group ID: {group.id}
                </p>

                <button
                  type="button"
                  className="delete-btn"
                  onClick={() => handleDeleteGroup(group.id)}
                >
                  Delete Group
                </button>
              </div>
            ))}
          </div>
        )}

        <button
          type="button"
          className="secondary-btn"
          onClick={loadGroups}
          disabled={loading}
          style={{ marginTop: "18px" }}
        >
          Refresh Groups
        </button>
      </div>

    </section>
  )
}