"use client";
import {useEffect, useState} from "react";
import {apiPost} from "../auth";
export default function ResetPassword(){
 const [uid,setUid]=useState("");const [token,setToken]=useState("");const [password,setPassword]=useState("");const [error,setError]=useState("");const [ok,setOk]=useState("");const [busy,setBusy]=useState(false);
 useEffect(()=>{const p=new URLSearchParams(window.location.search);setUid(p.get("uid")||"");setToken(p.get("token")||"");},[]);
 async function submit(e:React.FormEvent){e.preventDefault();setError("");setOk("");setBusy(true);try{const r=await apiPost("/auth/password-reset/confirm/",{uid,token,password});setOk(r.detail);}catch(err){setError(err instanceof Error?err.message:"রিসেট করা যায়নি।");}finally{setBusy(false);}}
 return <main className="auth-wrap"><section className="auth-card"><a className="brand" href="/"><span className="brandmark">N</span>NOVAMART</a><h1>নতুন পাসওয়ার্ড সেট করুন</h1><p className="sub">শক্তিশালী নতুন পাসওয়ার্ড দিন।</p>{(!uid||!token)&&<div className="message">রিসেট লিংকটি অসম্পূর্ণ। ইমেইলের সম্পূর্ণ লিংক ব্যবহার করুন।</div>}<form onSubmit={submit}><label className="field"><span>নতুন পাসওয়ার্ড (কমপক্ষে ১২ অক্ষর)</span><input type="password" autoComplete="new-password" minLength={12} value={password} onChange={e=>setPassword(e.target.value)} required placeholder="নতুন পাসওয়ার্ড"/></label>{error&&<div className="message">{error}</div>}{ok&&<div className="message" style={{background:"#ecfdf3",color:"#067647"}}>{ok} <a href="/login">লগইন করুন</a></div>}<button className="primary" disabled={busy||!uid||!token}>{busy?"পরিবর্তন হচ্ছে…":"পাসওয়ার্ড পরিবর্তন করুন"}</button></form><div className="auth-foot"><a href="/login">← লগইনে ফিরে যান</a></div></section></main>
}
