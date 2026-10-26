# NOVAMART — পেমেন্ট গ্রহণ ও ম্যানেজমেন্ট (বাংলা)

## গুরুত্বপূর্ণ বাস্তব অবস্থা
এই প্যাকেজে পেমেন্ট মেথড কনফিগারেশন, অর্ডার/পেমেন্ট রেফারেন্স সংরক্ষণ এবং অ্যাডমিন থেকে ম্যানুয়াল যাচাইয়ের ভিত্তি আছে। কিন্তু bKash/Nagad/Rocket/upay, কার্ড বা ক্রিপ্টোর জন্য কোনো লাইভ মার্চেন্ট API/গেটওয়ে credentials যুক্ত নেই। তাই UI-তে অপশন থাকলেই বাস্তব টাকা স্বয়ংক্রিয়ভাবে গ্রহণ হবে না।

## অ্যাডমিন থেকে পদ্ধতি ম্যানেজ
1. সার্ভার চালু করে Django admin-এ সুপারইউজার দিয়ে লগইন করুন।
2. **Payments → Payment methods** খুলুন।
3. পদ্ধতির `name`, `description`, `instructions`, `network` এবং `recipient_details` ঠিক করুন। `recipient_details`-এ কেবল প্রকাশযোগ্য merchant number বা public wallet address দিন—কখনো PIN, OTP, password, API secret বা private key নয়।
4. বাস্তবে পেমেন্ট গ্রহণের প্রস্তুতি না থাকলে `is_active` বন্ধ রাখুন। COD ছাড়া নতুন পদ্ধতি ডিফল্টভাবে চালু করবেন না।
5. ম্যানুয়াল পদ্ধতিতে `is_manual` চালু রাখুন। গ্রাহক ট্রানজ্যাকশন ID দিলে তা **Payments → Payments**-এ দেখা যাবে।
6. টাকা সত্যিই merchant account-এ জমা হয়েছে—নিজে অফিসিয়াল অ্যাপ/ড্যাশবোর্ডে যাচাই করার পরেই `Mark selected payments as verified/paid` action ব্যবহার করুন। শুধু গ্রাহকের স্ক্রিনশট বা ID দেখে পেইড করবেন না।
7. সন্দেহ হলে পদ্ধতি বন্ধ করুন; bulk action দিয়ে একসঙ্গে বন্ধও করা যায়।

## বাস্তব পেমেন্ট চালু করার ধাপ
- **bKash/Nagad/Rocket/upay:** ব্যবসার উপযুক্ত merchant account এবং সংশ্লিষ্ট প্রতিষ্ঠানের অনুমোদিত API/checkout/collection integration লাগবে। provider-এর callback/webhook server-side signature যাচাই, amount/order matching, duplicate-event protection এবং reconciliation যোগ করতে হবে।
- **Visa card:** অনুমোদিত card gateway/acquirer-এর hosted checkout/tokenized flow ব্যবহার করুন। নিজের সার্ভারে raw card number, CVV বা PIN সংরক্ষণ করবেন না।
- **ব্যাংক ট্রান্সফার:** ব্যবসার যাচাইকৃত ব্যাংক হিসাব, স্পষ্ট নির্দেশনা এবং bank statement/manual reconciliation workflow লাগবে; automated confirmation না থাকলে pending হিসেবেই থাকবে।
- **COD:** কুরিয়ার/ডেলিভারি থেকে টাকা সংগ্রহ নিশ্চিত করে reconciliation করতে হবে। COD order তৈরি হওয়া মানেই টাকা পাওয়া নয়।
- **USDT:** কেবল সঠিক chain-এ থাকা আপনার নিজস্ব public receiving address ব্যবহার করুন। এখানে গ্রাহককে কেবল BSC (BEP20) নেটওয়ার্ক দেখানো হবে; প্রাপকের ওয়ালেটেও BSC-তে USDT গ্রহণের সুবিধা থাকতে হবে। transaction hash, confirmations, token contract/asset, amount ও order match যাচাই না করে পেমেন্ট paid করবেন না।

## Crypto অপশন সম্পর্কে
চেকআউট থেকে আলাদা **Bitcoin Cash (BCH)** coin অপশন সরানো হয়েছে। এখন checkout-এ শুধু USDT BSC (BEP20) অপশন দেখানো হয়। **BCH আলাদা cryptocurrency; এটি USDT-এর নেটওয়ার্ক নয়।** তাই নির্ভরযোগ্য provider নিশ্চিত না করে “USDT on BCH network” নামে অপশন চালু করা হয়নি। BSC বলতে BNB Smart Chain বোঝানো হয়েছে; USDT পাঠাতে BSC/BEP20 নেটওয়ার্কই বেছে নিতে হবে।

## লাইভ করার আগে অবশ্যই
- প্রতিটি provider-এর merchant approval ও credentials নিরাপদ environment variables/secret manager-এ রাখুন।
- verified webhook/callback, idempotency, refund, timeout, failed payment ও reconciliation পরীক্ষা করুন।
- payment status শুধুমাত্র trusted server-side verification থেকে paid করুন; frontend-এর success message বিশ্বাস করবেন না।
- staging/sandbox-এ সফল ও ব্যর্থ পেমেন্ট পরীক্ষা করুন; তারপর ছোট অঙ্কে production পরীক্ষা করুন।
- স্থানীয় আইন, ব্যবসায়িক অনুমোদন, কর ও provider-এর terms যাচাই করুন।

**এই প্যাকেজে লাইভ merchant credentials বা gateway integration অন্তর্ভুক্ত নয়।** তাই বাস্তব পেমেন্ট গ্রহণের জন্য সংশ্লিষ্ট provider নির্বাচন, merchant account ও credentials প্রয়োজন; সেগুলো ছাড়া “লাইভ পেমেন্ট সেটআপ সম্পূর্ণ” বলা যাবে না।
