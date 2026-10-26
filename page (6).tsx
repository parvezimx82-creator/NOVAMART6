"use client";
import {useState} from "react";
import {apiPost} from "../auth";
export default function ForgotPassword(){
 const [email,setEmail]=useState("");const [error,setError]=useState("");const [ok,setOk]=useState("");const [busy,setBusy]=useState(false);
 async function submit(e:React.FormEvent){e.preventDefault();setError("");setOk("");setBusy(true);try{const r=await apiPost("/auth/password-reset/request/",{email});setOk(r.detail+" স্থানীয়ভাবে নির্দেশনা backend terminal-এ দেখা যাবে।");}catch(err){setError(err instanceof Error?err.message:"অনুরোধ পাঠানো যায়নি।");}finally{setBusy(false);}}
 return <main className="auth-wrap"><section className="auth-card"><a className="brand" href="/"><span className="brandmark">N</span>NOVAMART</a><h1>পাসওয়ার্ড রিসেট</h1><p className="sub">অ্যাকাউন্টের ইমেইল দিন। ইমেইলটি সিস্টেমে থাকলে রিসেট লিংক পাঠানো হবে।</p><form onSubmit={submit}><label className="field"><span>ইমেইল</span><input type="email" value={email} onChange={e=>setEmail(e.target.value)} required placeholder="you@example.com"/></label>{error&&<div className="message">{error}</div>}{ok&&<div className="message" style={{background:"#ecfdf3",color:"#067647"}}>{ok}</div>}<button className="primary" disabled={busy}>{busy?"পাঠানো হচ্ছে…":"রিসেট লিংক পাঠান"}</button></form><div className="auth-foot"><a href="/login">← লগইনে ফিরে যান</a></div><p className="note">উন্নয়ন পরিবেশে ইমেইল backend terminal-এ দেখায়। লাইভ করার আগে transactional email provider কনফিগার করতে হবে।</p></section></main>
}
