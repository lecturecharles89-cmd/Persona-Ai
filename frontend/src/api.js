const API = import.meta.env.VITE_API_URL || ''

export async function sendMessage(message, personaId, history = []) {
  const res = await fetch(`${API}/api/chat`, { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({message, persona_id:personaId, history}) })
  if (!res.ok) throw new Error((await res.json().catch(()=>({}))).detail || 'Request failed')
  return res.json()
}

export async function getPersonas() {
  const res = await fetch(`${API}/api/personas`)
  if (!res.ok) throw new Error('Could not load personas')
  return res.json()
}

export async function createPersona(persona) {
  const res = await fetch(`${API}/api/personas`, { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(persona) })
  if (!res.ok) throw new Error('Could not create persona')
  return res.json()
}
