"""
Gramin Udyam Sathi (ग्रामीण उद्यम साथी) — AI Rural Business Advisory Chatbot.
Provides contextual, multilingual NLP guidance tailored to the user's specific
enterprise category, location, project scale, and MoSJE / SCA scheme norms.
"""

from typing import Dict, List, Any
import re

class GraminUdyamSathi:
    """AI Rural Business Advisory Engine."""

    def __init__(self, state: str, district: str, block: str, business_name: str, margin_capital: float, scheme_name: str, lang: str = "en"):
        self.state = state
        self.district = district
        self.block = block
        self.business_name = business_name
        self.margin_capital = margin_capital
        self.project_cost = margin_capital * 10.0
        self.scheme_name = scheme_name
        self.lang = lang

    def get_suggested_prompts(self) -> List[Dict[str, str]]:
        """Returns localized quick suggestion questions for the micro-entrepreneur."""
        if self.lang == "hi":
            return [
                {"q": "मुझे MoSJE रियायती ऋण के लिए कौन-कौन से दस्तावेज चाहिए?", "id": "docs"},
                {"q": "मोराटोरियम (Moratorium) का क्या फायदा है और मुझे पहली किस्त कब देनी होगी?", "id": "moratorium"},
                {"q": "गांव में ग्राहकों से उधारी (Credit) कैसे रोकें और नकद बिक्री कैसे बढ़ाएं?", "id": "credit_mgmt"},
                {"q": "बिजली कटौती या कच्चे माल की महंगाई से मुनाफा कैसे बचाएं?", "id": "cost_cutting"},
                {"q": "साप्ताहिक हाट और नजदीकी मंडी में ज्यादा ग्राहक कैसे आकर्षित करें?", "id": "marketing"}
            ]
        elif self.lang == "mr":
            return [
                {"q": "MoSJE सवलतीच्या कर्जासाठी कोणती कागदपत्रे लागतील?", "id": "docs"},
                {"q": "मोरेटोरियमचा काय फायदा आहे आणि पहिला हप्ता कधी भरावा लागेल?", "id": "moratorium"},
                {"q": "उधारी कशी नियंत्रित करावी आणि रोख विक्री कशी वाढवावी?", "id": "credit_mgmt"},
                {"q": "खर्च कसा कमी करावा आणि नफा कसा वाढवावा?", "id": "cost_cutting"},
                {"q": "आठवडी बाजारात जास्त ग्राहक कसे मिळवायचे?", "id": "marketing"}
            ]
        elif self.lang == "bn":
            return [
                {"q": "MoSJE ঋণের জন্য কোন কোন নথিপত্র প্রয়োজন?", "id": "docs"},
                {"q": "মোরাটোরিয়াম কী এবং প্রথম কিস্তি কখন দিতে হবে?", "id": "moratorium"},
                {"q": "বাকিতে বিক্রি কীভাবে নিয়ন্ত্রণ করব?", "id": "credit_mgmt"},
                {"q": "উৎপাদন খরচ কমিয়ে কীভাবে বেশি লাভ করব?", "id": "cost_cutting"},
                {"q": "সাপ্তাহিক হাটে কীভাবে বেশি বিক্রি করব?", "id": "marketing"}
            ]
        else:
            return [
                {"q": "What documents are required to apply for MoSJE / SCA concessional loan?", "id": "docs"},
                {"q": "How does the moratorium grace period work and when is my first repayment due?", "id": "moratorium"},
                {"q": "How can I avoid village credit (Udhaar) losses and ensure fast cash recovery?", "id": "credit_mgmt"},
                {"q": "How do I cut raw material costs and survive power outages / price spikes?", "id": "cost_cutting"},
                {"q": "What is the best marketing strategy for Weekly Haats and nearby mandi buyers?", "id": "marketing"}
            ]

    def respond(self, query: str) -> str:
        """
        Processes natural language query and produces detailed institutional-grade rural advice.
        """
        q_lower = query.lower()
        
        # 1. Documents / Application Checklist
        if any(k in q_lower for k in ["doc", "dastavej", "kagadpatra", "certificate", "apply", "form", "patra", "দস্তাবেজ", "कागजात", "दस्तावेज", "कागदपत्रे"]):
            if self.lang == "hi":
                return (
                    f"### 📋 **{self.business_name} के लिए MoSJE / SCA ऋण आवेदन दस्तावेज चेकलिस्ट**:\n\n"
                    f"1. **पहचान एवं निवास प्रमाण**: आधार कार्ड (Aadhaar), मतदाता पहचान पत्र, राशन कार्ड / बिजली बिल।\n"
                    f"2. **जाति / श्रेणी प्रमाण पत्र (यदि लागू हो)**: SC/ST/OBC/सफाई कर्मचारी विकास निगम हेतु सक्षम अधिकारी द्वारा जारी प्रमाण पत्र।\n"
                    f"3. **उद्यम का विस्तृत प्रोजेक्ट रिपोर्ट (DPR)**: इस सहायक के 'DPR' टैब से स्वतः जनरेटेड बैंक-तैयार प्रोजेक्ट रिपोर्ट डाउनलोड करें (परियोजना लागत: ₹{self.project_cost:,.0f})।\n"
                    f"4. **मशीनरी / उपकरण कोटेशन (Quotations)**: अधिकृत सप्लायर्स से 2 प्रतिस्पर्धी कोटेशन।\n"
                    f"5. **स्थान / दुकान प्रमाण**: ग्राम पंचायत अनापत्ति प्रमाण पत्र (NOC) अथवा किरायानामा / भूमि स्वामित्व पर्चा।\n"
                    f"6. **बैंक खाता पासबुक**: पिछले 6 माह का बैंक स्टेटमेंट व 2 पासपोर्ट साइज फोटो।\n\n"
                    f"💡 *सलाह: अपने जिले के SCA (State Channelizing Agency) अथवा जिला उद्योग केंद्र (DIC) में यह फ़ाइल जमा करें।*"
                )
            else:
                return (
                    f"### 📋 **Document Checklist for MoSJE / SCA Concessional Loan ({self.business_name})**:\n\n"
                    f"1. **Identity & Address Proof**: Aadhaar Card, Voter ID, Ration Card or Village Electricity Bill.\n"
                    f"2. **Category / Caste Certificate (if applicable)**: Valid SC / OBC / EBC / Safai Karamchari certificate issued by Tehsildar/SDM for NBCFDC / NSFDC / NSKFDC schemes.\n"
                    f"3. **Bank-Ready Detailed Project Report (DPR)**: Download the complete automated DPR from the 'DPR Tab' in this portal (Total Project Cost: ₹{self.project_cost:,.0f}).\n"
                    f"4. **Machinery & Equipment Quotations**: 2 competitive quotations from certified vendors for CapEx machinery.\n"
                    f"5. **Premises Proof**: Gram Panchayat NOC or registered Rent/Lease Agreement / Land Record (Khatiyan/7/12).\n"
                    f"6. **Bank Account Details**: 6-month bank passbook/statement + 3 passport-sized photographs.\n\n"
                    f"💡 *Tip: Submit this dossier directly to your District SCA Officer or District Industries Centre (DIC).*"
                )

        # 2. Moratorium & Repayment Grace
        elif any(k in q_lower for k in ["moratorium", "grace", "kist", "emi", "repay", "first payment", "मोराटोरियम", "किस्त", "हप्ता"]):
            mor_months = 3 if self.project_cost <= 140000 else 6
            scheme = "Micro Finance Scheme" if self.project_cost <= 140000 else "Term Loan Scheme"
            if self.lang == "hi":
                return (
                    f"### ⏳ **मोराटोरियम (अनुग्रह अवधि) का लाभ — {scheme}**\n\n"
                    f"- आपकी योजना में **{mor_months} महीने का मोराटोरियम** उपलब्ध है।\n"
                    f"- **इसका क्या अर्थ है?**: ऋण मिलने के शुरुआती {mor_months} महीनों में आपको कोई मूलधन (Principal) किस्त नहीं चुकानी है।\n"
                    f"- **उद्देश्य**: इस समय में आप शेड का निर्माण, मशीनरी की स्थापना, और पहले बैच के उत्पादन को स्थिर कर सकते हैं।\n"
                    f"- **पहली किस्त**: आपकी नियमित किस्त **महीने {mor_months + 1}** से शुरू होगी।\n"
                    f"- **त्रैमासिक विकल्प**: राज्य चैनलाइजिंग एजेंसियां फसल कटाई चक्र के अनुसार हर 3 महीने (Quarterly) में भी किस्त स्वीकार करती हैं।"
                )
            else:
                return (
                    f"### ⏳ **Moratorium Period Benefit — {scheme}**\n\n"
                    f"- Your approved project includes a **{mor_months}-Month Moratorium Grace Period**.\n"
                    f"- **What this means**: During the first {mor_months} months after loan disbursement, you are **NOT** required to pay any principal installment.\n"
                    f"- **Strategic Goal**: Allows you to construct shed/shop, install equipment, acquire initial raw materials, and achieve positive sales flow before debt obligations kick in.\n"
                    f"- **First EMI Due Date**: Your active regular repayment begins from **Month {mor_months + 1}**.\n"
                    f"- **Quarterly Option**: SCAs also support post-harvest quarterly repayments to match rural agricultural cash cycles."
                )

        # 3. Credit / Udhaar Management
        elif any(k in q_lower for k in ["udhaar", "credit", "cash", "recovery", "payment", "baki", "उधार", "उधारी", "बाकी"]):
            if self.lang == "hi":
                return (
                    f"### 💡 **ग्रामीण व्यापार में उधारी (Udhaar) रोकने के 4 स्वर्णिम नियम**:\n\n"
                    f"1. **डिजिटल UPI डिस्काउंट**: नकद या UPI (QR कोड) से तुरंत भुगतान करने वाले ग्राहकों को ₹2 या 2% तत्काल छूट दें।\n"
                    f"2. **उधारी की सख्त सीमा तय करें**: किसी भी ग्रामीण ग्राहक को ₹500 से अधिक की उधारी न दें और 15 दिन की समय सीमा तय करें।\n"
                    f"3. **डिजिटल खाताबुक**: हर लेन-देन का तुरंत SMS / WhatsApp रिमाइंडर भेजें।\n"
                    f"4. **मूल्य-संवर्धित उत्पादों पर केवल नकद**: उच्च मांग वाले उत्पादों (जैसे पनीर/शुद्ध तेल/विशेष कपड़े) को केवल नकद या अग्रिम पर बेचें।"
                )
            else:
                return (
                    f"### 💡 **4 Golden Rules to Control Village Credit (Udhaar) & Protect Cash Flow**:\n\n"
                    f"1. **Instant UPI / Cash Incentive**: Offer an instant 2% discount for spot cash or QR-code UPI payment.\n"
                    f"2. **Strict Credit Cap & Ledger**: Cap informal credit at maximum ₹500 per customer with a mandatory 14-day settlement cycle.\n"
                    f"3. **Digital Khata SMS Alerts**: Use smartphone digital ledger apps to automatically dispatch WhatsApp/SMS reminders on settlement days.\n"
                    f"4. **Cash-Only Policy on Value-Added Items**: High-demand premium products (Paneer, Ghee, Branded Atta, Bridal Wear) should strictly be sold on cash/advance terms."
                )

        # 4. Cost Cutting & Risk Mitigation
        elif any(k in q_lower for k in ["cost", "power", "spoil", "loss", "electric", "expensive", "kharcha", "बचत", "खर्च", "बिजली"]):
            if self.lang == "hi":
                return (
                    f"### ⚙️ **{self.business_name} में लागत घटाने और जोखिम कम करने की रणनीति ({self.district}, {self.state})**:\n\n"
                    f"1. **कच्चे माल की सीधी थोक खरीद**: फसल कटाई के समय सीधे स्थानीय कृषकों / FPO से 2-3 महीने का कच्चा माल कम कीमत पर सुरक्षित करें।\n"
                    f"2. **सौर ऊर्जा बैकअप**: ग्रामीण 3-फेज बिजली कटौती से बचने के लिए DC सोलर इन्वर्टर का उपयोग करें ताकि मशीनरी न रुके।\n"
                    f"3. **अपशिष्ट का मुद्रीकरण (Waste-to-Value)**: उप-उत्पादों (जैसे गोबर से वर्मीकम्पोस्ट, तेल खली को पशु आहार के रूप में) को बेचकर अतिरिक्त 15-20% आय बनाएं।\n"
                    f"4. **सामूहिक परिवहन**: साप्ताहिक हाट जाते समय अन्य स्थानीय कारीगरों के साथ वाहन साझा करें।"
                )
            else:
                return (
                    f"### ⚙️ **Cost Reduction & Resilience Strategy for {self.business_name} in {self.district}**:\n\n"
                    f"1. **Direct Seasonal Farm Sourcing**: Procure 2-3 months of raw inputs directly from local farmer producer organizations (FPOs) during peak harvest when wholesale prices are lowest.\n"
                    f"2. **Solar Hybrid Power Backup**: Prevent rural grid blackout interruptions by incorporating solar inverter backup for continuous processing.\n"
                    f"3. **By-Product Monetization**: Turn waste into profit (e.g. converting cattle dung into Vermicompost, oil cakes into high-protein cattle feed, fabric scraps into quilt stuffing).\n"
                    f"4. **Shared Logistics**: Pool tempo transportation with neighboring village entrepreneurs for weekly Haat and APMC Mandi trips."
                )

        # 5. Marketing & Expanding Reach
        elif any(k in q_lower for k in ["market", "sell", "customer", "haat", "mandi", "bazaar", "growth", "बिक्री", "ग्राहक", "बाजार"]):
            if self.lang == "hi":
                return (
                    f"### 🚀 **{self.block} और नजदीकी मंडियों में बिक्री बढ़ाने की मास्टर रणनीति**:\n\n"
                    f"1. **साप्ताहिक हाटों (Haats) में प्रमुख स्थान**: सप्ताह में 3-4 दिन स्थानीय हाटों में आकर्षक बैनर और शुद्धता की गारंटी के साथ स्टॉल लगाएं।\n"
                    f"2. **गांव के शादियों/समारोहों के कैटरर्स से संपर्क**: विवाह व त्योहारों के सीजन में स्थानीय हलवाई, रसोइयों और टेंट हाउस को बल्क डिस्काउंट ऑफर करें।\n"
                    f"3. **पारदर्शी और शुद्ध पैकेजिंग**: 100% शुद्धता और बिना मिलावट के स्थानीय ब्रांड लेबल लगाएं।\n"
                    f"4. **सरकारी मेलों (Saras Melas) में भागीदारी**: MoSJE और राज्य हस्तशिल्प/खादी विकास बोर्ड के मेलों में सीधे शहरी ग्राहकों को प्रीमियम दाम पर बेचें।"
                )
            else:
                return (
                    f"### 🚀 **Master Marketing & Sales Acceleration Strategy in {self.block}**:\n\n"
                    f"1. **Weekly Haat Dominance**: Set up attractive branded stalls at the 3-4 weekly village markets with visible purity certifications and sample testing.\n"
                    f"2. **Bulk Catering & Wedding Tie-ups**: Partner with local community caterers, halwais, and wedding planners for bulk advance orders during auspicious seasons.\n"
                    f"3. **Transparent Brand Packaging**: Use clean, food-grade/sealed packaging with contact numbers and local origin branding ('Gramin Pure').\n"
                    f"4. **Exhibition & Saras Melas**: Register through MoSJE / SCA to exhibit at state-level Saras Melas and district exhibitions to access high-margin urban buyers."
                )

        # General / Custom query response
        else:
            if self.lang == "hi":
                return (
                    f"### 🌾 **ग्रामीण उद्यम साथी परामर्श ({self.business_name})**\n\n"
                    f"नमस्ते! आपके द्वारा चुने गए **{self.business_name}** उद्यम के लिए **{self.district} ({self.state})** में बहुत अच्छी संभावनाएं हैं।\n\n"
                    f"**मुख्य वित्तीय बिंदु**:\n"
                    f"- आपकी मार्जिन राशि (10%): ₹{self.margin_capital:,.0f}\n"
                    f"- कुल अनुशंसित परियोजना लागत: ₹{self.project_cost:,.0f}\n"
                    f"- पात्रता योजना: **{self.scheme_name}** (रियायती ब्याज दर)\n\n"
                    f"**अगला कदम**: ऊपर दिए गए बटनों में से किसी एक पर क्लिक करें, अथवा ऋण दस्तावेज, उत्पादन लागत, या बिक्री बढ़ाने के बारे में सीधे पूछें!"
                )
            else:
                return (
                    f"### 🌾 **Gramin Udyam Advisory Intelligence ({self.business_name})**\n\n"
                    f"Welcome! Your proposed **{self.business_name}** micro-enterprise has strong economic fundamentals in **{self.block}, {self.district} ({self.state})**.\n\n"
                    f"**Key Financial Metrics**:\n"
                    f"- Your Margin Money (10%): ₹{self.margin_capital:,.0f}\n"
                    f"- Total Feasible Enterprise Scale: ₹{self.project_cost:,.0f}\n"
                    f"- Recommended Funding Route: **{self.scheme_name}**\n\n"
                    f"**Actionable Next Steps**: Select one of the suggested quick questions above, or ask any question regarding bank documentation, equipment pricing, or rural sales acceleration!"
                )
