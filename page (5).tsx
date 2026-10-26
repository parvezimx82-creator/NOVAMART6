 "use client";
import { useEffect, useMemo, useState } from "react";
import { API } from "../auth";

type Product={id:number;name:string;price:string;image_url:string;stock:number;category_name:string};
type CartItem={product_id:number;quantity:number;product:Product};
type Method={code:string;name:string;category:string;description:string;instructions:string;network:string;recipient_details:string;is_manual:boolean;is_active:boolean};
const CART_KEY="novamart_cart_v1";
const paymentGroups = [
 { title:"মোবাইল ব্যাংকিং", subtitle:"বাংলাদেশের জনপ্রিয় পেমেন্ট", codes:["bkash","nagad","rocket","upay"] },
 { title:"কার্ড পেমেন্ট", subtitle:"Visa কার্ড — গেটওয়ে সংযুক্ত হলে চালু হবে", codes:["card"] },
 { title:"ক্রিপ্টোকারেন্সি", subtitle:"শুধু USDT — BSC (BEP20) নেটওয়ার্ক", codes:["usdt_bsc"] },
 { title:"অন্যান্য", subtitle:"ডেলিভারির সময় পেমেন্ট", codes:["cod"] },
];
const paymentMeta:Record<string,{mark:string;className:string;title?:string}> = {
 bkash:{mark:"bK",className:"pay-bkash"}, nagad:{mark:"N",className:"pay-nagad"},
 rocket:{mark:"R",className:"pay-rocket"}, upay:{mark:"u",className:"pay-upay"},
 card:{mark:"VISA",className:"pay-card"}, usdt_bsc:{mark:"₮",className:"pay-usdt",title:"BSC / BEP20"},
 cod:{mark:"৳",className:"pay-cod"}
};
export default function CheckoutPage(){
 const [items,setItems]=useState<CartItem[]>([]);
 const [methods,setMethods]=useState<Method[]>([]);
 const [name,setName]=useState("");const [phone,setPhone]=useState("");const [address,setAddress]=useState("");
 const [method,setMethod]=useState("cod");const [transactionId,setTransactionId]=useState("");
 const [busy,setBusy]=useState(false);const [error,setError]=useState("");const [success,setSuccess]=useState("");
 useEffect(()=>{
  try{const raw=localStorage.getItem(CART_KEY);const val=raw?JSON.parse(raw):[];if(Array.isArray(val))setItems(val)}catch{}
  fetch(`${API}/payments/methods/`).then(r=>r.json()).then(d=>{
   if(Array.isArray(d)){setMethods(d);const active=d.find((m:Method)=>m.code==="cod"&&m.is_active)||d.find((m:Method)=>m.is_active);if(active)setMethod(active.code)}
  }).catch(()=>{});
 },[]);
 const total=useMemo(()=>items.reduce((s,i)=>s+Number(i.product.price)*i.quantity,0),[items]);
 const selected=methods.find(m=>m.code===method);
 const methodByCode=(code:string)=>methods.find(m=>m.code===code);
 async function submit(e:React.FormEvent){
  e.preventDefault();setBusy(true);setError("");setSuccess("");
  try{
   if(!selected?.is_active)throw new Error("এই পেমেন্ট পদ্ধতিটি এখনো চালু হয়নি। অন্য পদ্ধতি নির্বাচন করুন।");
   const csrfRes=await fetch(`${API}/auth/csrf/`,{credentials:"include"});const csrfData=await csrfRes.json().catch(()=>({}));
   const res=await fetch(`${API}/orders/create/`,{method:"POST",credentials:"include",headers:{"Content-Type":"application/json","X-CSRFToken":csrfData.csrfToken||""},body:JSON.stringify({customer_name:name,phone,address,payment_method:method,transaction_id:transactionId,items:items.map(i=>({product_id:i.product_id,quantity:i.quantity}))})});
   const order=await res.json();if(!res.ok)throw new Error(order.detail||"অর্ডার তৈরি করা যায়নি। আগে লগইন করুন।");
   localStorage.removeItem(CART_KEY);setItems([]);setSuccess(`আপনার অর্ডার #${order.id} তৈরি হয়েছে। মোট ৳ ${Number(order.total).toLocaleString("en-BD")}. ${selected.category==="cash"?"ক্যাশ অন ডেলিভারি নির্বাচিত হয়েছে।":"পেমেন্ট রেফারেন্স যাচাইয়ের অপেক্ষায় আছে।"}`);
  }catch(err){setError(err instanceof Error?err.message:"সার্ভারের সঙ্গে সংযোগ করা যায়নি।")}finally{setBusy(false)}
 }
 function choose(code:string){const m=methodByCode(code);if(m?.is_active){setMethod(code);setTransactionId("");setError("")}}
 return <main className="container page-shell checkout-page">
  <a className="back-link" href="/cart">← কার্টে ফিরুন</a>
  <header className="checkout-hero"><div><span className="eyebrow">NOVAMART SECURE CHECKOUT</span><h1>নিরাপদ চেকআউট</h1><p>আপনার পছন্দের পেমেন্ট পদ্ধতি বেছে নিন</p></div><div className="checkout-shield">✦<small>সুরক্ষিত অর্ডার</small></div></header>
  {success?<section className="empty-state success-state"><h2>অর্ডার গ্রহণ করা হয়েছে</h2><p>{success}</p><a className="primary" href="/">হোমপেজে ফিরুন</a></section>:!items.length?<section className="empty-state"><h2>কার্টে পণ্য নেই</h2><a className="primary" href="/">পণ্য দেখুন</a></section>:<div className="checkout-layout">
   <form className="checkout-form" onSubmit={submit}>
    <div className="checkout-section-title"><span className="step-number">01</span><div><h2>ডেলিভারি তথ্য</h2><p>পণ্য পৌঁছে দেওয়ার তথ্য দিন</p></div></div>
    <label>সম্পূর্ণ নাম<input required maxLength={150} value={name} onChange={e=>setName(e.target.value)} placeholder="আপনার নাম"/></label>
    <label>মোবাইল নম্বর<input required minLength={7} maxLength={30} value={phone} onChange={e=>setPhone(e.target.value)} placeholder="01XXXXXXXXX"/></label>
    <label>সম্পূর্ণ ঠিকানা<textarea required maxLength={1500} value={address} onChange={e=>setAddress(e.target.value)} placeholder="বাড়ি, রাস্তা, এলাকা, জেলা"/></label>
    <div className="checkout-section-title payment-heading"><span className="step-number">02</span><div><h2>পেমেন্ট পদ্ধতি</h2><p>আপনার জন্য সুবিধাজনক পদ্ধতি নির্বাচন করুন</p></div></div>
    <div className="payment-groups">{paymentGroups.map(group=><section className="payment-group" key={group.title}><div className="payment-group-heading"><h3>{group.title}</h3><p>{group.subtitle}</p></div><div className="payment-grid">{group.codes.map(code=>{
      const m=methodByCode(code);const meta=paymentMeta[code];const active=!!m?.is_active;const selectedNow=method===code;
      const fallback:Method={code,name:code==="card"?"Visa Card":code==="usdt_bsc"?"USDT (BSC / BEP20)":code.toUpperCase(),category:"other",description:"",instructions:"",network:"",recipient_details:"",is_manual:true,is_active:false};
      const item=m||fallback;
      return <button type="button" key={code} disabled={!active} onClick={()=>choose(code)} className={`payment-tile ${meta.className} ${selectedNow?"is-selected":""} ${!active?"is-unavailable":""}`} aria-pressed={selectedNow}>
       <span className="payment-mark">{meta.mark}</span><span className="payment-tile-copy"><strong>{code==="card"?"Visa Card":item.name}{meta.title?` · ${meta.title}`:""}</strong><small>{active?(item.description||"চালু আছে"):"শীঘ্রই আসছে"}</small></span><span className="payment-radio">{selectedNow?"✓":""}</span>
      </button>
    })}</div></section>)}</div>
    {selected&&selected.category!=="cash"&&<div className="payment-reference"><label>লেনদেন / রেফারেন্স আইডি<input required maxLength={160} value={transactionId} onChange={e=>setTransactionId(e.target.value)} placeholder="পেমেন্টের রেফারেন্স আইডি"/></label>{selected.instructions&&<p>{selected.instructions}</p>}{selected.recipient_details&&<p>প্রাপকের তথ্য: <strong>{selected.recipient_details}</strong></p>}</div>}
    {error&&<p className="form-error">{error}</p>}
    <button className="primary full checkout-submit" disabled={busy||!selected?.is_active}>{busy?"প্রক্রিয়া চলছে...":"অর্ডার নিশ্চিত করুন  →"}</button>
    <p className="form-hint">বাস্তব পেমেন্ট গ্রহণের আগে অ্যাডমিন প্যানেলে অনুমোদিত গেটওয়ে বা সঠিক প্রাপকের তথ্য সেট করে যাচাই করুন। USDT পাঠানোর সময় BSC (BEP20) নেটওয়ার্কই নির্বাচন করুন; অন্য নেটওয়ার্ক ব্যবহার করবেন না। চালু না থাকা পদ্ধতিতে টাকা পাঠাবেন না।</p>
   </form>
   <aside className="summary checkout-summary"><div className="summary-top"><span className="eyebrow">YOUR ORDER</span><h2>অর্ডার সারাংশ</h2></div>{items.map(i=><div className="summary-item" key={i.product_id}><span>{i.product.name} <small>× {i.quantity}</small></span><b>৳ {(Number(i.product.price)*i.quantity).toLocaleString("en-BD")}</b></div>)}<hr/><div className="summary-total"><strong>পণ্যের মোট</strong><strong>৳ {total.toLocaleString("en-BD")}</strong></div><div className="summary-security">✦ <span>আপনার অর্ডারের তথ্য সুরক্ষিতভাবে প্রক্রিয়া করা হবে।</span></div><p>ডেলিভারি চার্জ বর্তমানে ০; লাইভ করার আগে এলাকা অনুযায়ী চার্জ কনফিগার করতে হবে।</p></aside>
  </div>}
 </main>
}
