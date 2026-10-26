# NOVAMART — পেমেন্ট ও লাইভ চ্যাট সেটআপ (বাংলা)

## লাইভ চ্যাট কীভাবে কাজ করে
- সাইটের নিচের ডান পাশে `লাইভ চ্যাট` বোতাম থাকে।
- ভিজিটর নাম/ইমেইল (ঐচ্ছিক) ও প্রথম মেসেজ দিয়ে চ্যাট শুরু করতে পারে।
- মেসেজ ডেটাবেসে সংরক্ষিত হয় এবং প্রতি ৪ সেকেন্ডে নতুন মেসেজ চেক করা হয়।
- Django Admin → Livechat → Conversations থেকে কর্মীরা কথোপকথন দেখতে ও উত্তর দিতে পারেন।
- বর্তমান সংস্করণটি polling-ভিত্তিক MVP; এটি WebSocket-ভিত্তিক instant chat নয়। সত্যিকারের agent availability, push notification, SLA, file attachment, assignment workflow ও live typing indicator পরবর্তী পর্যায়ে দরকার।
- Django Admin লগইন করা কর্মীরাই conversation পড়তে/পরিচালনা করতে পারবেন। পাবলিক chat conversation ID গোপন রাখুন; প্রোডাকশনের আগে guest conversation access আরও শক্তভাবে session/token-bound করতে হবে এবং abuse/rate-limit পরীক্ষা করতে হবে।

## পেমেন্ট অপশন
প্রথমে backend container-এ চালান:
`python manage.py seed_payment_methods`

এরপর Django Admin → Payments → Payment methods থেকে প্রয়োজনীয় অপশন কনফিগার করুন:
- Cash on Delivery (COD)
- bKash
- Nagad
- Rocket
- upay
- Visa Card
- USDT (BSC / BEP20) — একমাত্র ক্রিপ্টো অপশন

পুরোনো TRC20/BEP20 আলাদা এবং BCH রেকর্ড থাকলে seed command সেগুলো নিষ্ক্রিয় করবে; পুরোনো payment history অক্ষত রাখতে রেকর্ড মুছে ফেলা হবে না.

শুধু যে পেমেন্ট পদ্ধতি বাস্তবে গ্রহণ ও যাচাই করার ব্যবস্থা আছে সেটিই সক্রিয় করুন। bKash/Nagad/Rocket/upay/Visa Card-এর live automated payment এই প্যাকেজে এখনো যুক্ত নয়; সেজন্য অনুমোদিত মার্চেন্ট অ্যাকাউন্ট ও অফিসিয়াল API/গেটওয়ে ইন্টিগ্রেশন দরকার। USDT BSC (BEP20) বর্তমানে manual reference submission + admin verification-এর জন্য প্রস্তুত—স্বয়ংক্রিয় blockchain confirmation নেই। কোনো বাস্তব wallet address না থাকলে recipient details খালি রাখুন এবং পদ্ধতি disabled রাখুন। ভুল নেটওয়ার্কে পাঠানো টাকা ফেরত নাও পাওয়া যেতে পারে; USDT নেটওয়ার্ক স্পষ্ট করে দেখাতে হবে।

Payment API:
- `GET /api/payments/methods/` — সক্রিয় পেমেন্ট পদ্ধতি
- `POST /api/payments/submit/` — লগইন করা ক্রেতার নিজের অর্ডারের পেমেন্ট রেফারেন্স জমা
- `GET /api/payments/mine/` — নিজের পেমেন্ট তালিকা

Live chat API:
- `POST /api/chat/start/` — কথোপকথন শুরু
- `GET /api/chat/<conversation_uuid>/messages/` — মেসেজ পড়া
- `POST /api/chat/<conversation_uuid>/messages/` — মেসেজ পাঠানো
- `GET /api/chat/staff/conversations/` — staff/admin কথোপকথন তালিকা
- `POST /api/chat/staff/<conversation_uuid>/reply/` — staff উত্তর

## গুরুত্বপূর্ণ
এই কোডটি ইন্টিগ্রেশন-ভিত্তি, সম্পূর্ণ production-verified payment/live-chat service নয়। প্রোডাকশনের আগে migration তৈরি/প্রয়োগ, API permission test, rate-limit test, guest chat ownership validation, real payment gateway sandbox test, webhook signature validation, refund/duplicate callback tests, HTTPS, real email configuration এবং backup/restore test করতে হবে।

## কার্ট, চেকআউট ও অর্ডার (নতুন)
- `/cart` পেজে কার্ট দেখা/পরিমাণ বদল/পণ্য সরানো যায়; কার্ট ব্রাউজারের localStorage-এ থাকে।
- `/checkout`-এ ডেলিভারি তথ্য, পেমেন্ট পদ্ধতি ও অর্ডার সাবমিট করা যায়।
- `POST /api/orders/create/` সার্ভার থেকে বর্তমান মূল্য ও স্টক যাচাই করে, transaction-এর মধ্যে অর্ডার তৈরি করে এবং স্টক কমায়।
- `GET /api/orders/mine/` লগইন করা গ্রাহকের নিজের অর্ডার দেখায়।
- অনলাইন/ম্যানুয়াল পেমেন্টে অর্ডার তৈরি হওয়ার পরে রেফারেন্স সাবমিট হয়। যদি পেমেন্ট সাবমিট ব্যর্থ হয়, অর্ডার ইতিমধ্যে তৈরি হয়ে থাকতে পারে—ডুপ্লিকেট অর্ডার এড়াতে অর্ডার তালিকা যাচাই করুন।
- বর্তমান ডেলিভারি চার্জ ০; production-এ এলাকার ভিত্তিতে চার্জ ও return/refund rules কনফিগার করতে হবে।

- চেকআউটের অর্ডার ও ম্যানুয়াল পেমেন্ট রেফারেন্স এখন একই ডেটাবেস transaction-এ তৈরি হয়; পেমেন্ট পদ্ধতি বন্ধ থাকলে বা প্রয়োজনীয় রেফারেন্স না থাকলে অর্ডার তৈরি হবে না।


## বর্তমান পেমেন্ট UI
- Checkout-এ মোবাইল ব্যাংকিং (bKash, Nagad, Rocket, upay), Visa Card, USDT BSC (BEP20) এবং Cash on Delivery আলাদা গ্রুপে দেখানো হয়।
- যেসব পদ্ধতি Django Admin-এ সক্রিয় করা হয়নি, সেগুলো "শীঘ্রই আসছে" হিসেবে disabled থাকবে; এভাবে ভুল করে ব্যবহারকারীকে পেমেন্ট পাঠাতে বলা হবে না।
- Card gateway বা crypto wallet বাস্তবে চালু করতে হলে অনুমোদিত provider/merchant details এবং নিরাপদ verification workflow সেট করতে হবে।
