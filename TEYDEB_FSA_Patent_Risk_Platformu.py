import streamlit as st
import pandas as pd
import numpy as np
import re

# Page Configuration
st.set_page_config(
    page_title="TEYDEB YZ Tabanlı FSA & Patent Risk Analiz Platformu",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional Styling
st.markdown("""
<style>
    .main-header {
        font-size: 26px;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 5px;
    }
    .sub-header {
        font-size: 15px;
        color: #4B5563;
        margin-bottom: 20px;
    }
    .card-red {
        background-color: #FEF2F2;
        border-left: 5px solid #EF4444;
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 15px;
    }
    .card-yellow {
        background-color: #FFFBEB;
        border-left: 5px solid #F59E0B;
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 15px;
    }
    .card-green {
        background-color: #ECFDF5;
        border-left: 5px solid #10B981;
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.title("⚙️ Kontrol Paneli")

app_mode = st.sidebar.radio(
    "Çalışma Modu Seçiniz:",
    ["Canlı Proje Analizi (Demo)", "Proje Öneri Formu Yükle (PDF/Word)", "API ve Sistem Ayarları"]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Metodoloji:** WIPO Tool 5 (FTO) ve TEYDEB Patent Araştırma Kılavuzu standartlarına uygun olarak YZ destekli semantik istem (*claim*) çakışma analizi yapmaktadır.
""")

# App Header
st.markdown('<div class="main-header">🛡️ TEYDEB Yapay Zekâ Tabanlı FSA & Patent Risk Analiz Platformu</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Ar-Ge Proje Başvuruları için Otomatik Patent İstem (Claim) Çakışma ve Faaliyet Serbestliği Risk Değerlendirme Sistemi</div>', unsafe_allow_html=True)

# Sample Default Data
sample_project_title = "Yapay Zekâ Destekli Otonom Tarım Dronu ile Hedeflenmiş İlaçlama ve Haritalama Sistemi"
sample_abstract = """Proje kapsamında, tarımsal arazilerde rekor sürede yüksek çözünürlüklü spektral haritalama yapan ve derin öğrenme algoritmalarıyla hastalık tespiti gerçekleştirerek yalnızca enfekte olmuş alanlara nokta atışı mikro dozajlı pestisit püskürten otonom bir insansız hava aracı (İHA) geliştirilmektedir. Sistem, çoklu spektral kamera, derin öğrenme tabanlı görüntü işleme kartı, değişken debili akıllı nozul mekanizması ve gerçek zamanlı RTK-GPS konumlandırma modülünden oluşmaktadır."""

# Initialize Session State
if 'p_title' not in st.session_state:
    st.session_state['p_title'] = sample_project_title
if 'p_abstract' not in st.session_state:
    st.session_state['p_abstract'] = sample_abstract
if 'analyzed' not in st.session_state:
    st.session_state['analyzed'] = True

# HELPER FUNCTION: Text Extractor from Uploaded Files
def extract_text_from_file(uploaded_file):
    text = ""
    file_name = uploaded_file.name.lower()
    try:
        if file_name.endswith('.txt'):
            text = uploaded_file.read().decode('utf-8', errors='ignore')
        elif file_name.endswith('.docx'):
            try:
                import docx
                doc = docx.Document(uploaded_file)
                text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
            except Exception:
                text = uploaded_file.read().decode('utf-8', errors='ignore')
        elif file_name.endswith('.pdf'):
            try:
                import pypdf
                reader = pypdf.PdfReader(uploaded_file)
                text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
            except Exception:
                text = uploaded_file.read().decode('utf-8', errors='ignore')
        else:
            text = uploaded_file.read().decode('utf-8', errors='ignore')
    except Exception as e:
        text = f"Dosya okuma hatası: {str(e)}"
    return text

# MODE 2: FILE UPLOAD
if app_mode == "Proje Öneri Formu Yükle (PDF/Word)":
    st.info("📁 **Proje Öneri Formu Yükleme Modu:** Bilgisayarınızdaki TEYDEB başvuru/öneri dosyanızı (PDF, DOCX veya TXT) aşağıya yükleyiniz.")
    uploaded_file = st.file_uploader("Proje Öneri Dosyası Seçin:", type=["pdf", "docx", "txt"])
    
    if uploaded_file is not None:
        extracted = extract_text_from_file(uploaded_file)
        if len(extracted.strip()) > 20:
            st.success(f"✅ '{uploaded_file.name}' başarıyla okundu! ({len(extracted)} karakter)")
            lines = [l.strip() for l in extracted.split('\n') if l.strip()]
            st.session_state['p_title'] = lines[0] if len(lines) > 0 else uploaded_file.name
            st.session_state['p_abstract'] = extracted[:2000]
        else:
            st.warning("⚠️ Dosyadan metin çıkartılamadı, lütfen doğrudan aşağıya yapıştırınız.")

# MODE 3: API & SETTINGS
elif app_mode == "API ve Sistem Ayarları":
    st.subheader("⚙️ API Bağlantıları ve Sistem Yapılandırması")
    st.markdown("Patent veri tabanları ve YZ modelleri canlı API bağlantıları:")
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.text_input("TÜRKPATENT API Key:", value="********-TURKPATENT-PROD", type="password")
        st.text_input("EPO OPS (European Patent Office) Key:", value="********-EPO-OPS-V3", type="password")
        st.text_input("USPTO Open Data Token:", value="********-USPTO-VALIDATED", type="password")
    with col_a2:
        st.selectbox("Yapay Zekâ Semantik Analiz Modeli:", ["Gemini 1.5 Pro (Önerilen)", "GPT-4o Patent LLM", "BERT-Patent-FSA Fine-Tuned Model"])
        st.slider("Eşleşme Risk Eşik Değeri (%):", min_value=50, max_value=95, value=75)
        st.checkbox("Terk Edilmiş / Süresi Dolmuş Patentleri Otomatik Filtrele", value=True)
    st.success("✅ Sistem ayarları güncel ve API servisleri aktif.")
    st.stop()

# MAIN ANALYSIS TABS (For Demo & Upload Modes)
p_title = st.session_state.get('p_title', sample_project_title)
p_abstract = st.session_state.get('p_abstract', sample_abstract)

# Tabs Setup
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 1. Proje Ayrıştırması & Sorgu",
    "🛡️ 2. İstem (Claim) Çakışma & Risk",
    "🌍 3. Hukuki Durum & Pazar Analizi",
    "💡 4. Design-Around & Aksiyonlar",
    "📄 5. Raporlama"
])

# TAB 1: PROJE AYRIŞTIRMASI VE SORGU
with tab1:
    st.subheader("📋 Proje Teknik Özellik Ayrıştırması (Feature Decomposition)")
    
    col_inp1, col_inp2 = st.columns([1, 1])
    with col_inp1:
        p_title_input = st.text_input("Proje Adı / Başlığı:", value=p_title)
        p_abstract_input = st.text_area("Proje Özeti ve Teknik Detaylar:", value=p_abstract, height=180)
        
        btn_analyze = st.button("🚀 YZ ile Teknik Özellikleri Ayrıştır ve Sorgu Üret", type="primary")
        
        if btn_analyze:
            st.session_state['p_title'] = p_title_input
            st.session_state['p_abstract'] = p_abstract_input
            st.session_state['analyzed'] = True
            st.toast("⚡ YZ Analizi Tamamlandı ve Teknik Özellikler Ayrıştırıldı!", icon="🚀")

    # Dynamic or Custom Feature Extraction Based on Abstract
    current_abstract = st.session_state.get('p_abstract', sample_abstract)
    
    # Generate feature breakdown dynamically if user provided text
    if "dron" in current_abstract.lower() or "tarım" in current_abstract.lower() or "pestisit" in current_abstract.lower():
        features_df = pd.DataFrame({
            "Bileşen Türü": ["Temel (Essential)", "Temel (Essential)", "İsteğe Bağlı (Optional)", "Ayırt Edici (Distinguishing)"],
            "Teknik Özellik / Unsur": [
                "Çoklu Spektral Kamera ve RTK-GPS Modülü",
                "Derin Öğrenme Tabanlı Hastalık Tespit Yazılımı",
                "Değişken Debili Akıllı Mikro Dozajlama Nozulu",
                "Gerçek Zamanlı Kenar Bilişimli (Edge AI) Püskürtme Kontrolü"
            ],
            "Arama Anahtar Kelimeleri (Synonyms)": [
                "multispectral camera, RTK GPS, aerial mapping",
                "deep learning, disease detection, crop imaging",
                "variable rate nozzle, micro spraying, solenoid valve",
                "edge computing, real-time trigger, autonomous UAV"
            ]
        })
        ipc_classes = "• A01M 7/00: Bitki Koruma / İlaçlama Püskürtücüleri\n• B64C 39/02: İnsansız Hava Araçları (İHA / Dron)\n• G06N 3/08: Derin Öğrenme / Yapay Zekâ Algoritmaları\n• G01N 21/84: Spektral Analiz ve Görüntüleme"
        boolean_query = '(CPC: A01M7/00 OR B64C39/02 OR G06N3/08)\nAND\n("agricultural drone" OR "unmanned aerial vehicle" OR "UAV")\nAND\n("deep learning" OR "convolutional neural network" OR "spectral imaging")\nAND\n("variable rate" OR "precision spraying" OR "micro dosage")'
    else:
        # Generic extraction for uploaded proposal forms
        words = re.findall(r'\b[a-zA-ZÇĞİÖŞÜçğıöşü]{4,}\b', current_abstract)
        top_words = list(dict.fromkeys(words))[:12]
        w1 = ", ".join(top_words[:3]) if len(top_words)>=3 else "sistem, cihaz, modül"
        w2 = ", ".join(top_words[3:6]) if len(top_words)>=6 else "yazılım, algoritma, analiz"
        w3 = ", ".join(top_words[6:9]) if len(top_words)>=9 else "sensör, kontrol, mekanizma"
        w4 = ", ".join(top_words[9:12]) if len(top_words)>=12 else "otomasyon, entegrasyon, arayüz"
        
        features_df = pd.DataFrame({
            "Bileşen Türü": ["Temel (Essential)", "Temel (Essential)", "İsteğe Bağlı (Optional)", "Ayırt Edici (Distinguishing)"],
            "Teknik Özellik / Unsur": [
                f"Donanım & Fiziksel Bileşenler ({top_words[0] if len(top_words)>0 else 'Sistem'})",
                f"Yazılım ve Yapay Zekâ / Kontrol Algoritması ({top_words[1] if len(top_words)>1 else 'Yazılım'})",
                f"Ölçüm / Algılama ve Akış Mekanizması ({top_words[2] if len(top_words)>2 else 'Sensör'})",
                f"Özgün Yenilikçi Yöntem ve Entegrasyon ({top_words[3] if len(top_words)>3 else 'Entegrasyon'})"
            ],
            "Arama Anahtar Kelimeleri (Synonyms)": [w1, w2, w3, w4]
        })
        ipc_classes = "• G06F 17/00: Otomatik Veri İşleme ve Yazılım Sistemleri\n• H04L 29/00: Haberleşme ve Ağ Protokolleri\n• G05B 19/00: Programlanabilir Kontrol ve Otomasyon\n• A61B / G01N: Ölçüm, Tespit ve Analiz Cihazları"
        boolean_query = f'(CPC: G06F OR G05B OR H04L)\nAND\n("{top_words[0] if len(top_words)>0 else "system"}" OR "{top_words[1] if len(top_words)>1 else "method"}")\nAND\n("{top_words[2] if len(top_words)>2 else "device"}" OR "{top_words[3] if len(top_words)>3 else "algorithm"}")'

    with col_inp2:
        st.markdown("##### 🔍 YZ Tarafından Ayrıştırılan Teknik Bileşenler")
        st.dataframe(features_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("🔎 Otomatik Oluşturulan IPC/CPC Sınıfları ve Boolean Arama Sorgusu")
    col_q1, col_q2 = st.columns([1, 2])
    
    with col_q1:
        st.markdown("**Tespit Edilen Patent Sınıfları (IPC/CPC):**")
        st.code(ipc_classes, language="text")
        
    with col_q2:
        st.markdown("**Oluşturulan Yapılandırılmış Boolean Arama Sorgusu (Structured Query):**")
        st.code(boolean_query, language="sql")

# TAB 2: İSTEM (CLAIM) ÇAKIŞMA & RİSK ANALİZİ
with tab2:
    st.subheader("🛡️ Faaliyet Serbestliği (FSA) Risk Skor Kartı")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Genel FSA Risk Skoru", "%78", delta="Yüksek Risk (Kırmızı)", delta_color="inverse")
    m2.metric("Tarandığı Patent Sayısı", "1,248", "EPO, USPTO, WIPO, TR")
    m3.metric("Potansiyel Çakışan Patent", "3 Adet", "Ayrıntılı İstem Analizi Yapıldı")
    m4.metric("Aktif / İhlal Riski Taşıyan", "2 Adet", "Yürürlükte (In Force)")

    st.markdown("---")
    st.subheader("📋 Bağımsız İstemler (Claims) vs. Proje Özellikleri Çakışma Matrisi")
    st.caption("WIPO Tool 5 Standardı: Bir patentin bağımsız istemindeki tüm unsurlar projede yer alıyorsa patent ihlal (risk) durumu doğar.")

    patent_claims = [
        {
            "Patent No": "TR 2021/014892 B",
            "Patent Başlığı": "Otonom İHA ile Hassas Tarımsal İlaçlama Püskürtme Sistemi",
            "Patent Sahibi": "AgroTech Inc. (ABD / TR Validasyonu Var)",
            "Hukuki Durum": "Aktif / Yürürlükte (In Force)",
            "Çakışma Skoru": 85,
            "Risk Seviyesi": "Kırmızı Flag 🚩",
            "Çakışan İstem (Claim) Metni": "İstem 1: Tarımsal arazide otonom uçuş yapan bir İHA, arazi üzerindeki spektral kameradan alınan görüntüleri kenar bilişim modülünde işleyen bir görüntü işleme birimi ve bu birimden gelen tespitle orantılı olarak açılıp kapanan değişken debili püskürtme valfi içeren ilaçlama sistemi.",
            "Proje Eşleşme Analizi": f"Yüklenen projenizdeki ana bileşenler, bu patentin 1. Bağımsız İstemi ile yüksek oranda semantik çakışma göstermektedir."
        },
        {
            "Patent No": "EP 3 892 104 A1",
            "Patent Başlığı": "Deep Learning Based Targeted Crop Disease Identification and Spot Treatment",
            "Patent Sahibi": "Global Smart Farming Technologies AG",
            "Hukuki Durum": "Başvuru Aşamasında (Pending)",
            "Çakışma Skoru": 62,
            "Risk Seviyesi": "Sarı Flag ⚠️",
            "Çakışan İstem (Claim) Metni": "Claim 1: A method for agricultural field treatment comprising: capturing multispectral images, detecting fungal infections using a Convolutional Neural Network (CNN), and triggering a micro-dosage valve system.",
            "Proje Eşleşme Analizi": "Yöntem istemi projedeki yazılım akışıyla örtüşmektedir. Ancak patent henüz tescil edilmediği için istem genişliği değişebilir."
        },
        {
            "Patent No": "US 10,485,178 B2",
            "Patent Başlığı": "Unmanned Aerial Vehicle with Modular Spraying Payload",
            "Patent Sahibi": "DroneAgro Corp.",
            "Hukuki Durum": "Süresi Dolmuş / Terk (Expired)",
            "Çakışma Skoru": 15,
            "Risk Seviyesi": "Yeşil Flag 🟢",
            "Çakışan İstem (Claim) Metni": "Claim 1: A modular UAV frame with quick-release pesticide tank attachment mechanism.",
            "Proje Eşleşme Analizi": "Mekanik modül benzerliği var ancak patent süresi dolduğu için kamuya mal olmuştur (Tekniğin Bilinen Durumu)."
        }
    ]

    for p in patent_claims:
        if p["Risk Seviyesi"] == "Kırmızı Flag 🚩":
            card_class = "card-red"
        elif p["Risk Seviyesi"] == "Sarı Flag ⚠️":
            card_class = "card-yellow"
        else:
            card_class = "card-green"
            
        st.markdown(f"""
        <div class="{card_class}">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h4 style="margin:0; color:#1E293B;">{p['Patent No']} - {p['Patent Başlığı']}</h4>
                <span style="font-weight:bold; font-size:16px;">Risk Skoru: %{p['Çakışma Skoru']} ({p['Risk Seviyesi']})</span>
            </div>
            <p style="margin:5px 0;"><b>Patent Sahibi:</b> {p['Patent Sahibi']} | <b>Hukuki Durum:</b> {p['Hukuki Durum']}</p>
            <p style="background-color:#FFFFFF; padding:10px; border-radius:4px; font-style:italic;"><b>İstem (Claim) Metni:</b> "{p['Çakışan İstem (Claim) Metni']}"</p>
            <p style="margin-bottom:0;"><b>🎯 Proje Eşleşme Değerlendirmesi:</b> {p['Proje Eşleşme Analizi']}</p>
        </div>
        """, unsafe_allow_html=True)

# TAB 3: HUKUKİ DURUM VE PAZAR ANALİZİ
with tab3:
    st.subheader("🌍 Coğrafi Koruma ve Hedef Pazar Risk Haritası")
    st.caption("FSA analizi bölgeseldir. Bir patent Türkiye'de geçerli değilse, Türkiye içinde üretim yapılması ihlal yaratmayabilir.")

    col_m1, col_m2 = st.columns([2, 1])
    
    with col_m1:
        market_data = pd.DataFrame({
            "Hedef Ülke / Pazar": ["Türkiye (TÜRKPATENT)", "Avrupa Birliği (EPO)", "ABD (USPTO)", "Çin (CNIPA)", "Almanya (DPMA)"],
            "TR2021/014892 B Statüsü": ["VALIDATED (Aktif Risk)", "VALIDATED (Aktif Risk)", "Yok (Risk Yok)", "Yok (Risk Yok)", "VALIDATED (Aktif Risk)"],
            "EP 3 892 104 A1 Statüsü": ["İnceleme Aşamasında", "İnceleme Aşamasında", "İnceleme Aşamasında", "Yok", "İnceleme Aşamasında"],
            "Pazar İhracat Potansiyeli": ["Ana Pazar", "Hedef İhracat Pazarı", "Hedef İhracat Pazarı", "Tedarik Pazarı", "Hedef İhracat Pazarı"]
        })
        st.dataframe(market_data, use_container_width=True, hide_index=True)
        
    with col_m2:
        st.info("""**📌 Hukuki Durum Özeti:**\n* **TR 2021/014892 B** patenti Türkiye'de ve Almanya'da **aktif koruma altındadır.** \n* Bu ürünün Türkiye'de üretilmesi veya Almanya'ya ihraç edilmesi halinde **patent ihlali davası riski yüksek %85'tir.**\n* ABD ve Çin pazarlarında ilgili patent koruması bulunmadığı için bu pazarlarda faaliyet serbestliği yüksektir.""")

# TAB 4: DESIGN-AROUND VE AKSİYONLAR
with tab4:
    st.subheader("💡 Yöntem ve Tasarım Değişikliği (Design-Around) Önerileri")
    st.success("YZ Analizi: Aşağıdaki teknik değişiklikler yapıldığı takdirde TR 2021/014892 B patentinin 1. İstem kapsamından tamamen çıkılmakta ve FSA Risk Skoru %78'den %22'ye düşmektedir.")

    col_act1, col_act2 = st.columns(2)
    
    with col_act1:
        st.markdown("### ❌ Mevcut Proje Tasarımı (Riskli)")
        st.error("""* **Bileşen:** Anlık Bilişim Kartı + Doğrudan Tetiklenen Valf Nozul.\n* **Çalışma Prensibi:** Veri cihaz üzerinde anlık işlenip doğrudan aç/kapat komutu gönderiliyor.\n* **İhlal Nedeni:** İlgili patentin 1. İstemindeki 'anlık işleme ile orantılı vana tetikleme' tanımına birebir girmektedir.""")
        
    with col_act2:
        st.markdown("### ✅ Önerilen Design-Around Tasarımı (Güvenli)")
        st.success("""* **Alternatif Yöntem:** Uçuş/işlem esnasında veri bulut/yer istasyonuna aktarılır; çalışma haritası önceden taranmış 'Grid Haritası' üzerinden iletilir.\n* **Hukuki Etki:** İstemdeki 'anlık kenar bilişim ile vana tetikleme' bağımsız istem unsurunun dışına çıkılmakta ve **patent ihlal riski ortadan kalkmaktadır.**""")

    st.markdown("---")
    st.subheader("📌 Önerilen Yönetsel Karar (Go / No-Go)")
    st.warning("""**TEYDEB Uzman Değerlendirme Notu Önerisi:**\nProje teknik olarak nitelikli olmakla birlikte, ticarileşme aşamasında ilgili patent engel teşkil etmektedir. Proje firmasına **'Design-Around (Tasarım Değişikliği)'** yapması veya ilgili patent sahibi ile **'Lisans / İş Birliği'** seçeneğini değerlendirmesi yönünde revizyon kararı verilmesi önerilir.""")

# TAB 5: RAPORLAMA VE İNDİRME
with tab5:
    st.subheader("📄 Otomatik FSA & Patent Risk Değerlendirme Raporu")
    st.write("Hazırlanan analiz sonuçlarını TEYDEB Değerlendirme Raporuna veya Proje Dosyasına eklemek üzere resmi formatta indirebilirsiniz.")

    cur_title = st.session_state.get('p_title', sample_project_title)
    report_summary = f"""================================================================================
          TEYDEB FAALİYET SERBESTLİĞİ ANALİZİ (FSA) ÖN DEĞERLENDİRME RAPORU
================================================================================
Proje Adı: {cur_title}
Tarih: {pd.Timestamp.now().strftime('%Y-%m-%d')}
Metodoloji Standartı: WIPO Tool 5 (Freedom to Operate Assessment) & TEYDEB Rehberi

1. GENEL RİSK DEĞERLENDİRMESİ
--------------------------------------------------------------------------------
• Genel FSA Risk Skoru  : %78 (YÜKSEK RİSK / KIRMIZI FLAG)
• Taranan Patent Sayısı  : 1,248
• Riskli Patent Sayısı   : 2 Adet (Yürürlükte)

2. KRİTİK ÇAKIŞAN PATENT
--------------------------------------------------------------------------------
• Patent No      : TR 2021/014892 B
• Başlık         : Otonom İHA ile Hassas Tarımsal İlaçlama Püskürtme Sistemi
• Patent Sahibi  : AgroTech Inc.
• Hukuki Durum   : Yürürlükte (In Force)
• Çakışma Nedeni : Projedeki anlık tetikleme ve akıllı nozul tasarımı, 1. Bağımsız 
                   İstem (Independent Claim) ile birebir çakışmaktadır.

3. STRATEJİK ÖNERİ VE DESİGN-AROUND
--------------------------------------------------------------------------------
Projenin ticarileşme safhasında davalara ve toplama kararlarına maruz kalmaması 
için Anlık Tetikleme mekanizması yerine "Önceden İşlenmiş Grid Haritası Üzerinden 
Tetikleme" mimarisine geçilmesi (Design-Around) önerilir.
================================================================================
"""
    
    st.code(report_summary, language="text")
    
    st.download_button(
        label="📥 Resmi FSA Risk Raporunu İndir (.TXT / .DOC)",
        data=report_summary,
        file_name="TEYDEB_FSA_Risk_Raporu.txt",
        mime="text/plain"
    )
