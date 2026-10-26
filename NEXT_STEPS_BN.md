# NOVAMART — পরবর্তী কাজের তালিকা

## এই ZIP-এ এখন যা আছে
- প্রিমিয়াম-ধাঁচের responsive হোমপেজ ও বাংলা UI
- রেজিস্ট্রেশন/লগইন ফর্ম এবং API সংযোগ
- Django modular backend, PostgreSQL, category/product/order data models
- ব্যর্থ লগইনে সীমা (৫ বার/১ ঘণ্টা) এবং auth API throttle
- Django admin-এ category, product, order পরিচালনার প্রাথমিক ব্যবস্থা

## এখনো সম্পূর্ণ করতে হবে — লঞ্চের আগে বাধ্যতামূলক
1. API session + CSRF flow-কে production frontend domain-এ সঠিকভাবে configure এবং integration test করা।
2. Email/phone verification, password reset, MFA (বিশেষত admin), CAPTCHA/bot protection।
3. Customer profile, cart, checkout, stock reservation, order creation, cancellation/return/refund।
4. Seller onboarding, seller-only product/order access, commission and payout ledger।
5. Payment gateway (official merchant account), webhook signature validation, reconciliation।
6. Courier/shipping integration, delivery status sync।
7. Audit log, rate-limit monitoring, Redis/background tasks, backups/restore test, security and load test।
8. UI-তে demo products বদলে database API থেকে real products, images, cart state, filters and pagination দেখানো।
9. CI checks, automated tests, staging deployment, independent security review।

**গুরুত্বপূর্ণ:** এই ZIP-কে production-ready বা ১০০% secure বলা যাবে না। বাস্তব নিরাপত্তা পরীক্ষা, deployment configuration ও end-to-end testing ছাড়া কোনো সফটওয়্যারকে শতভাগ নিরাপদ নিশ্চয়তা দেওয়া যায় না।


## পেমেন্ট গ্রহণ সেটআপ
বাংলা নির্দেশিকার জন্য `PAYMENT_RECEIVING_MANAGEMENT_BN.md` দেখুন। পেমেন্ট পদ্ধতি অ্যাডমিন থেকে কনফিগার করা যায়, তবে বাস্তব gateway/API চালু করতে সংশ্লিষ্ট merchant account ও credentials লাগবে।
