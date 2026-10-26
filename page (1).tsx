"use client";
import { useEffect, useMemo, useState } from "react";
import { API } from "../auth";

type Product = { id:number; name:string; price:string; image_url:string; stock:number; category_name:string };
type CartItem = { product_id:number; quantity:number; product:Product };
const key = "novamart_cart_v1";
export default function CartPage(){
 const [items,setItems]=useState<CartItem[]>([]);
 const [loading,setLoading]=useState(true);
 useEffect(()=>{ try{const raw=localStorage.getItem(key); const parsed=raw?JSON.parse(raw):[]; if(Array.isArray(parsed))setItems(parsed);}catch{} finally{setLoading(false);} },[]);
 useEffect(()=>{if(!loading)localStorage.setItem(key,JSON.stringify(items.map(i=>({product_id:i.product_id,quantity:i.quantity,product:i.product}))))},[items,loading]);
 const total=useMemo(()=>items.reduce((s,i)=>s+Number(i.product.price)*i.quantity,0),[items]);
 function change(id:number,q:number){setItems(old=>old.map(i=>i.product_id===id?{...i,quantity:Math.max(1,Math.min(99,q))}:i));}
 function remove(id:number){setItems(old=>old.filter(i=>i.product_id!==id));}
 if(loading)return <main className="container page-shell">কার্ট লোড হচ্ছে...</main>;
 return <main className="container page-shell"><a href="/">← কেনাকাটায় ফিরুন</a><h1>আপনার শপিং ব্যাগ</h1>{!items.length?<section className="empty-state"><h2>আপনার কার্ট খালি</h2><p>পছন্দের পণ্য যোগ করে এখানে ফিরে আসুন।</p><a className="primary" href="/">পণ্য দেখুন</a></section>:<div className="checkout-layout"><section className="cart-list">{items.map(i=><article className="cart-row" key={i.product_id}><div className="cart-thumb">{i.product.image_url?<img src={i.product.image_url} alt={i.product.name}/>:<span>🛍️</span>}</div><div className="cart-info"><strong>{i.product.name}</strong><small>{i.product.category_name}</small><b>৳ {Number(i.product.price).toLocaleString("en-BD")}</b><div className="qty"><button onClick={()=>change(i.product_id,i.quantity-1)}>-</button><span>{i.quantity}</span><button onClick={()=>change(i.product_id,i.quantity+1)}>+</button><button className="remove" onClick={()=>remove(i.product_id)}>সরান</button></div></div></article>)}</section><aside className="summary"><h2>অর্ডার সারাংশ</h2><div><span>সাবটোটাল</span><b>৳ {total.toLocaleString("en-BD",{maximumFractionDigits:2})}</b></div><div><span>ডেলিভারি চার্জ</span><span>চেকআউটে নির্ধারিত</span></div><p>চূড়ান্ত মূল্য সার্ভার পুনরায় যাচাই করবে।</p><a className="primary full" href="/checkout">চেকআউট করুন →</a></aside></div>}</main>;
}
