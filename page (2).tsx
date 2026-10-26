"use client";
import { useState } from "react";
import { apiPost } from "../auth";

export default function LoginPage() {
  const [username,setUsername]=useState(""); const [password,setPassword]=useState("");
  const [error,setError]=useState(""); const [busy,setBusy]=useState(false); const [ok,setOk]=useState("");
  async function submit(e:React.FormEvent){e.preventDefault();setError("");setOk("");setBusy(true);try{const r=await apiPost("/auth/login/",{username,password});setOk(r.detail+" এখন অ্যাকাউন্ট পেজ তৈরির পর সেখানে নেওয়া হবে।");}catch(err){setError(err instanceof Error?err.message:"লগইন করা যায়নি।");}finally{setBusy(false);}}
  return <main className="auth-wrap"><section className="auth-card"><a className="brand" href="/"><span className="brandmark">N</span>NOVAMART</a><h1>আবার স্বাগতম 👋</h1><p className="sub">আপনার অ্যাকাউন্টে লগইন করে কেনাকাটা চালিয়ে যান।</p><form onSubmit={submit}><label className="field"><span>ইউজারনেম</span><input autoComplete="username" value={username} onChange={e=>setUsername(e.target.value)} required placeholder="আপনার ইউজারনেম"/></label><label className="field"><span>পাসওয়ার্ড</span><input type="password" autoComplete="current-password" value={password} onChange={e=>setPassword(e.target.value)} required placeholder="আপনার পাসওয়ার্ড"/></label>{error&&<div className="message">{error}</div>}{ok&&<div className="message" style={{background:"#ecfdf3",color:"#067647"}}>{ok}</div>}<button className="primary" disabled={busy}>{busy?"লগইন হচ্ছে…":"নিরাপদে লগইন করুন"}</button></form><div className="auth-foot" style={{marginTop:12}}><a href="/forgot-password">পাসওয়ার্ড ভুলে গেছেন?</a></div><div className="auth-foot">নতুন NOVAMART ব্যবহারকারী? <a href="/register">অ্যাকাউন্ট তৈরি করুন</a></div><p className="note">সুরক্ষার জন্য বারবার ভুল লগইন করলে সাময়িকভাবে চেষ্টা সীমিত হতে পারে। কখনোই আপনার পাসওয়ার্ড কারও সঙ্গে শেয়ার করবেন না।</p><div className="auth-foot"><a href="/">← হোমপেজে ফিরে যান</a></div></section></main>
}
