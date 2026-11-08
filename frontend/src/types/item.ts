export interface Item {
  id: number
  title: string
  description: string | null
  category: string | null
  status: string
  location: string | null
  contact_info: string | null
  created_at: string
}

export interface ItemForm {
  title: string
  description: string
  category: string
  status: string
  location: string
  contact_info: string
}

export const emptyForm: ItemForm = {
  title: "",
  description: "",
  category: "",
  status: "lost",
  location: "",
  contact_info: "",
}
