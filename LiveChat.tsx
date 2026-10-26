"use client";

import { useEffect, useRef, useState } from "react";

type ChatMessage = { id: number; sender_label: string; body: string; is_staff_reply: boolean; created_at: string };
const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function LiveChat() {
  const [open, setOpen] = useState(false);
  const [conversationId, setConversationId] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [firstMessage, setFirstMessage] = useState("");
  const [draft, setDraft] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open || !conversationId) return;
    let active = true;
    const poll = async () => {
      try {
        const res = await fetch(`${API}/api/chat/${conversationId}/messages/`, { cache: "no-store" });
        if (!res.ok) return;
        const data = await res.json();
        if (active) setMessages(data.messages || []);
      } catch { /* Backend may be offline while developing. */ }
    };
    void poll();
    const timer = window.setInterval(poll, 4000);
    return () => { active = false; window.clearInterval(timer); };
  }, [open, conversationId]);

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages, open]);

  async function start(e: React.FormEvent) {
    e.preventDefault(); setBusy(true); setError("");
    try {
      const res = await fetch(`${API}/api/chat/start/`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, subject: "Website support", message: firstMessage })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "চ্যাট শুরু করা যায়নি। আবার চেষ্টা করুন।");
      setConversationId(data.conversation_id); setFirstMessage("");
    } catch (err) { setError(err instanceof Error ? err.message : "সার্ভারের সঙ্গে সংযোগ হচ্ছে না।"); }
    finally { setBusy(false); }
  }

  async function send(e: React.FormEvent) {
    e.preventDefault(); if (!draft.trim() || !conversationId) return;
    const body = draft.trim(); setDraft(""); setBusy(true); setError("");
    try {
      const res = await fetch(`${API}/api/chat/${conversationId}/messages/`, {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ body })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "মেসেজ পাঠানো যায়নি।");
      setMessages(old => [...old, data]);
    } catch (err) { setDraft(body); setError(err instanceof Error ? err.message : "মেসেজ পাঠানো যায়নি।"); }
    finally { setBusy(false); }
  }

  return <>
    <button className="chat-launcher" onClick={() => setOpen(v => !v)} aria-label={open ? "চ্যাট বন্ধ করুন" : "লাইভ চ্যাট খুলুন"}>
      {open ? "×" : "✦"} <span>{open ? "বন্ধ করুন" : "লাইভ চ্যাট"}</span>
    </button>
    {open && <section className="chat-panel" aria-label="NOVAMART লাইভ চ্যাট">
      <header className="chat-head"><div className="chat-avatar">N</div><div><strong>NOVAMART Support</strong><small><i /> সহায়তা কেন্দ্র · সাধারণত দ্রুত উত্তর</small></div><button onClick={() => setOpen(false)} aria-label="বন্ধ করুন">×</button></header>
      {!conversationId ? <form className="chat-start" onSubmit={start}>
        <h3>কীভাবে সাহায্য করতে পারি?</h3><p>আপনার প্রশ্ন লিখুন। সাপোর্ট টিম উত্তর দিলে এই চ্যাটেই দেখতে পারবেন।</p>
        <label>আপনার নাম<input value={name} onChange={e => setName(e.target.value)} maxLength={100} placeholder="নাম (ঐচ্ছিক)" /></label>
        <label>ইমেইল<input type="email" value={email} onChange={e => setEmail(e.target.value)} maxLength={254} placeholder="ইমেইল (ঐচ্ছিক)" /></label>
        <label>আপনার মেসেজ<textarea value={firstMessage} onChange={e => setFirstMessage(e.target.value)} required maxLength={3000} placeholder="আপনার সমস্যাটি লিখুন..." /></label>
        {error && <p className="chat-error">{error}</p>}<button className="primary" disabled={busy || !firstMessage.trim()}>{busy ? "পাঠানো হচ্ছে..." : "চ্যাট শুরু করুন"}</button>
      </form> : <>
        <div className="chat-messages">{messages.map(m => <div key={m.id} className={`chat-bubble ${m.is_staff_reply ? "staff" : "customer"}`}><small>{m.sender_label}</small><p>{m.body}</p><time>{new Date(m.created_at).toLocaleTimeString("bn-BD", { hour: "2-digit", minute: "2-digit" })}</time></div>)}<div ref={bottomRef} /></div>
        {error && <p className="chat-error chat-inline-error">{error}</p>}
        <form className="chat-send" onSubmit={send}><input value={draft} onChange={e => setDraft(e.target.value)} maxLength={3000} placeholder="মেসেজ লিখুন..." aria-label="মেসেজ" /><button disabled={busy || !draft.trim()} aria-label="পাঠান">➤</button></form>
        <small className="chat-privacy">ব্যক্তিগত পাসওয়ার্ড, OTP বা কার্ডের গোপন তথ্য পাঠাবেন না।</small>
      </>}
    </section>}
  </>;
}
