# NOVAMART v8 — Responsive Design ও প্রয়োজনীয় সার্ভিস

## Responsive UI আপডেট
- 320px থেকে বড় ফোন, ট্যাবলেট, ল্যাপটপ ও প্রশস্ত ডেস্কটপে লেআউট মানিয়ে নেওয়ার জন্য responsive CSS যোগ করা হয়েছে।
- মোবাইলে পণ্য দুই কলামে, মাঝারি স্ক্রিনে জায়গা অনুযায়ী তিন কলামে এবং প্রশস্ত ডেস্কটপে পাঁচ কলাম পর্যন্ত দেখানোর নিয়ম যোগ করা হয়েছে।
- Checkout ও cart ছোট স্ক্রিনে এক কলামে যায়; পেমেন্টের অপশন ও সারাংশে overflow কমানোর নিয়ম যোগ করা হয়েছে।
- স্পর্শে ব্যবহারযোগ্য বাটন, keyboard focus indicator, reduced-motion preference, safe-area spacing ও horizontal overflow প্রতিরোধ যোগ করা হয়েছে।
- এগুলো CSS-ভিত্তিক responsive hardening; বাস্তব ফোন/ব্রাউজারে হাতে পরীক্ষা এখনও deployment-এর আগে করতে হবে।

## চালানোর জন্য কী লাগবে?
1. **হোস্টিং/সার্ভার:** Frontend-এর জন্য Node.js সমর্থিত hosting এবং Django backend চালানোর hosting। একই deployment-এ container ব্যবহার করলেও চলবে।
2. **PostgreSQL database:** অর্ডার, পণ্য, অ্যাকাউন্ট, পেমেন্ট স্ট্যাটাস ও inventory সংরক্ষণের জন্য persistent database।
3. **ডোমেইন ও HTTPS:** যেমন নিজের কেনা domain; checkout ও login-এর জন্য HTTPS আবশ্যক।
4. **পেমেন্ট provider account:** bKash/Nagad/Rocket/upay ও Visa-এর live payment চালু করতে সংশ্লিষ্ট provider-এর merchant approval, API credentials এবং sandbox/live testing প্রয়োজন। UI-তে অপশন থাকা মানেই live payment চালু নয়।
5. **USDT BSC (BEP20):** গ্রহণের জন্য সঠিক wallet address, network/confirmation policy এবং নিরাপদ transaction verification দরকার। ভুল নেটওয়ার্কের পেমেন্ট যেন সফল না ধরা হয়।
6. **Email/SMS (ঐচ্ছিক কিন্তু উপকারী):** OTP, order confirmation, password reset ও delivery update-এর জন্য provider account।
7. **Courier integration (ঐচ্ছিক):** স্বয়ংক্রিয় shipping charge, parcel booking ও tracking-এর জন্য courier API/merchant account; না থাকলে অ্যাডমিন হাতে tracking update করতে পারে।
8. **Backup ও monitoring:** database backup, error logs, access control, secret environment variables এবং নিয়মিত security updates।

## টাকা ও নিরাপত্তা বিষয়ে
- Client/browser থেকে আসা amount-কে বিশ্বাস না করে backend-এ product price, discount, delivery fee ও total পুনরায় হিসাব করতে হবে।
- Payment provider-এর server-side confirmation/webhook ছাড়া online payment-কে Paid করা যাবে না।
- COD-এর জন্য payment collected এবং order delivered আলাদা status হিসেবে ট্র্যাক করতে হবে।
- Live payment credentials কখনও GitHub repository বা frontend code-এ রাখা যাবে না; server environment variables-এ রাখতে হবে।

## সীমাবদ্ধতা
এই responsive CSS আপডেটটি নিজে থেকে payment gateway, SMS provider, courier API, production server বা domain তৈরি/সংযুক্ত করে না। এগুলোর জন্য account, credentials ও deployment configuration আলাদাভাবে প্রয়োজন।
