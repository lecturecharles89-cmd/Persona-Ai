import { useEffect, useMemo, useState } from 'react'
import { Menu, Plus, Send, Sparkles, Volume2, Mic, Settings2, Brain, ChevronDown } from 'lucide-react'
import { createPersona, getPersonas, sendMessage } from './api'

const fallback = [{id:'aria',name:'Aria',description:'Warm, intelligent and playful AI companion.',traits:['warm','playful','empathetic'],current_mood:{emotion:'calm',intensity:50}}]
const icons = {happy:'😊',sad:'😢',playful:'😜',angry:'😤',calm:'😌',surprised:'😮',curious:'🤔',neutral:'✨'}

export default function App(){
  const [personas,setPersonas]=useState(fallback),[active,setActive]=useState(fallback[0]),[messages,setMessages]=useState([]),[input,setInput]=useState(''),[loading,setLoading]=useState(false),[mobile,setMobile]=useState(false),[showCreate,setShowCreate]=useState(false),[error,setError]=useState('')
  useEffect(()=>{getPersonas().then(x=>{if(x.length){setPersonas(x);setActive(x[0])}}).catch(()=>{})},[])
  const emotion=active.current_mood?.emotion||'calm'
  const submit=async e=>{e?.preventDefault(); if(!input.trim()||loading)return; const text=input.trim(); setInput('');setError('');const next=[...messages,{role:'user',content:text}];setMessages(next);setLoading(true);try{const r=await sendMessage(text,active.id,next);setMessages([...next,{role:'assistant',content:r.text,emotion:r.emotion}]);setActive(p=>({...p,current_mood:r.emotion}))}catch(err){setError(err.message);setMessages(next)}finally{setLoading(false)}}
  const selectPersona=p=>{setActive(p);setMessages([]);setMobile(false)}
  return <div className="app">
    <aside className={`sidebar ${mobile?'open':''}`}>
      <div className="brand"><div className="logo"><Sparkles size={17}/></div><b>AI Persona</b></div>
      <button className="new" onClick={()=>setShowCreate(true)}><Plus size={17}/> New persona</button>
      <div className="label">PERSONAS</div>
      <div className="persona-list">{personas.map(p=><button className={`persona-item ${p.id===active.id?'active':''}`} key={p.id} onClick={()=>selectPersona(p)}><div className="avatar">{(p.name||'A')[0]}</div><div><b>{p.name}</b><span>{p.description}</span></div></button>)}</div>
      <div className="sidebar-bottom"><button><Brain size={17}/> Memory</button><button><Settings2 size={17}/> Settings</button></div>
    </aside>
    <main className="main">
      <header className="topbar"><button className="icon mobile-menu" onClick={()=>setMobile(!mobile)}><Menu/></button><div className="persona-title"><div className="avatar large">{active.name[0]}</div><div><b>{active.name}</b><span><i/> Online · {emotion}</span></div></div><button className="icon"><Settings2 size={18}/></button></header>
      <section className="chat">
        {messages.length===0&&<div className="welcome"><div className="hero-avatar">{active.name[0]}</div><h1>Meet {active.name}</h1><p>{active.description}</p><div className="chips">{(active.traits||['warm','creative','curious']).slice(0,4).map(t=><span key={t}>#{t}</span>)}</div></div>}
        {messages.map((m,i)=><div className={`message ${m.role}`} key={i}><div className="message-avatar">{m.role==='assistant'?active.name[0]:'You'}</div><div className="bubble"><div className="meta">{m.role==='assistant'?active.name:'You'}</div><div>{m.content}</div>{m.role==='assistant'&&<div className="message-tools"><button title="Play"><Volume2 size={15}/></button>{m.emotion&&<span>{icons[m.emotion.emotion]||'✨'} {m.emotion.emotion}</span>}</div>}</div></div>)}
        {loading&&<div className="message assistant"><div className="message-avatar">{active.name[0]}</div><div className="bubble"><div className="typing"><i/><i/><i/></div></div></div>}
        {error&&<div className="error">{error}</div>}
      </section>
      <form className="composer" onSubmit={submit}><div className="input-wrap"><button type="button" className="input-icon"><Plus size={19}/></button><input value={input} onChange={e=>setInput(e.target.value)} placeholder={`Message ${active.name}...`}/><button type="button" className="input-icon"><Mic size={18}/></button><button className="send" disabled={!input.trim()||loading}><Send size={18}/></button></div><small>{active.name} can remember details and express emotion. AI can make mistakes.</small></form>
    </main>
    {showCreate&&<CreateModal close={()=>setShowCreate(false)} onCreate={async p=>{const n=await createPersona(p).catch(()=>({...p,id:p.name.toLowerCase().replace(/\s+/g,'-')}));setPersonas(x=>[...x,n]);setActive(n);setShowCreate(false)}}/>}
  </div>
}

function CreateModal({close,onCreate}){const [name,setName]=useState('');const [desc,setDesc]=useState('');const [tone,setTone]=useState('natural');return <div className="modal-backdrop" onMouseDown={close}><div className="modal" onMouseDown={e=>e.stopPropagation()}><div className="modal-head"><h2>Create your persona</h2><button onClick={close}>×</button></div><label>Name<input value={name} onChange={e=>setName(e.target.value)} placeholder="Aria"/></label><label>Who are they?<textarea value={desc} onChange={e=>setDesc(e.target.value)} placeholder="Warm, intelligent, mysterious..."/></label><label>Speaking style<select value={tone} onChange={e=>setTone(e.target.value)}><option>natural</option><option>playful</option><option>professional</option><option>poetic</option><option>mysterious</option></select></label><button className="create" disabled={!name.trim()} onClick={()=>onCreate({name,description:desc,personality:{warmth:80,humor:70,empathy:80},speaking_style:{tone},traits:['warm','curious'],current_mood:{emotion:'calm',intensity:50}})}>Create Persona</button></div></div>}
