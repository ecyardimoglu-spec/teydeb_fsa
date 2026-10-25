import streamlit as st
import pandas as pd
import numpy as np

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

# Demo Sample Data
sample_project_title = "Yapay Zekâ Destekli Otonom Tarım Dronu ile Hedeflenmiş İlaçlama ve Haritalama Sistemi"
sample_abstract = """Proje kapsamında, tarımsal arazilerde rekor sürede yüksek çözünürlüklü spektral haritalama yapan ve derin öğrenme algoritmalarıyla hastalık tespiti gerçekleştirerek yalnızca enfekte olmuş alanlara nokta atışı mikro dozajlı pestisit püskürten otonom bir insansız hava aracı (İHA) geliştirilmektedir. Sistem, çoklu spektral kamera, derin öğrenme tabanlı görüntü işleme kartı, değişken debili akıllı nozul mekanizması ve gerçek zamanlı RTK-GPS konumlandırma modülünden oluşmaktadır."""

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
        p_title = st.text_input("Proje Adı / Başlığı:", sample_project_title)
        p_abstract = st.text_area("Proje Özeti ve Teknik Detaylar:", sample_abstract, height=180)
        btn_analyze = st.button("🚀 YZ ile Teknik Özellikleri Ayrıştır ve Sorgu Üret", type="primary")
    
    with col_inp2:
        st.markdown("##### 🔍 YZ Tarafından Ayrıştırılan Teknik Bileşenler")
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
        st.dataframe(features_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("🔎 Otomatik Oluşturulan IPC/CPC Sınıfları ve Boolean Arama Sorgusu")
    col_q1, col_q2 = st.columns([1, 2])
    
    with col_q1:
        st.markdown("**Tespit Edilen Patent Sınıfları (IPC/CPC):**")
        st.code("""• A01M 7/00: Bitki Koruma / İlaçlama Püskürtücüleri\n• B64C 39/02: İnsansız Hava Araçları (İHA / Dron)\n• G06N 3/08: Derin Öğrenme / Yapay Zekâ Algoritmaları\n• G01N 21/84: Spektral Analiz ve Görüntüleme""", language="text")
        
    with col_q2:
        st.markdown("**Oluşturulan Yapılandırılmış Boolean Arama Sorgusu (Structured Query):**")
        st.code("""(CPC: A01M7/00 OR B64C39/02 OR G06N3/08) \nAND \n("agricultural drone" OR "unmanned aerial vehicle" OR "UAV") \nAND \n("deep learning" OR "convolutional neural network" OR "spectral imaging") \nAND \n("variable rate" OR "precision spraying" OR "micro dosage")""", language="sql")

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
            "Proje Eşleşme Analizi": "Projenizdeki 'Kenar Bilişimli Püskürtme Kontrolü' ve 'Değişken Debili Nozul' bileşeni, bu patentin 1. Bağımsız İstemi ile %100 birebir çakışmaktadır."
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
        st.error("""* **Bileşen:** Kenar Bilişim Kartı + Değişken Debili Solenoid Valf Nozul.\n* **Çalışma Prensibi:** Görüntü İHA üzerinde anlık işlenip vanalara doğrudan aç/kapat komutu gönderiliyor.\n* **İhlal Nedeni:** AgroTech firmasının 1. İstemindeki 'İHA üzeri anlık işleme ile orantılı vana tetikleme' tanımına birebir girmektedir.""")
        
    with col_act2:
        st.markdown("### ✅ Önerilen Design-Around Tasarımı (Güvenli)")
        st.success("""* **Alternatif Yöntem:** İHA uçuş esnasında görüntüyü bulut/yer istasyonuna aktarır; ilaçlama haritası önceden taranmış 'Grid Haritası' üzerinden nozullara iletilir.\n* **Hukuki Etki:** İstemdeki 'İHA üzerinde kenar bilişim ile anlık görüntüden vana tetikleme' bağımsız istem unsurunun dışına çıkılmakta ve **patent ihlal riski ortadan kalkmaktadır.**""")

    st.markdown("---")
    st.subheader("📌 Önerilen Yönetsel Karar (Go / No-Go)")
    st.warning("""**TEYDEB Uzman Değerlendirme Notu Önerisi:**\nProje teknik olarak nitelikli olmakla birlikte, ticarileşme aşamasında TR 2021/014892 B patenti engel teşkil etmektedir. Proje firmasına **'Design-Around (Tasarım Değişikliği)'** yapması veya ilgili patent sahibi ile **'Lisans / İş Birliği'** seçeneğini değerlendirmesi yönünde revizyon kararı verilmesi önerilir.""")

# TAB 5: RAPORLAMA VE İNDİRME
with tab5:
    st.subheader("📄 Otomatik FSA & Patent Risk Değerlendirme Raporu")
    st.write("Hazırlanan analiz sonuçlarını TEYDEB Değerlendirme Raporuna veya Proje Dosyasına eklemek üzere resmi formatta indirebilirsiniz.")

    report_summary = f"""================================================================================\n          TEYDEB FAALİYET SERBESTLİĞİ ANALİZİ (FSA) ÖN DEĞERLENDİRME RAPORU\n================================================================================\nProje Adı: {p_title}\nTarih: {pd.Timestamp.now().strftime('%Y-%m-%d')}\nMetodoloji Standartı: WIPO Tool 5 (Freedom to Operate Assessment) & TEYDEB Rehberi\n\n1. GENEL RİSK DEĞERLENDİRMESİ\n--------------------------------------------------------------------------------\n• Genel FSA Risk Skoru  : %78 (YÜKSEK RİSK / KIRMIZI FLAG)\n• Taranan Patent Sayısı  : 1,248\n• Riskli Patent Sayısı   : 2 Adet (Yürürlükte)\n\n2. KRİTİK ÇAKIŞAN PATENT\n--------------------------------------------------------------------------------\n• Patent No      : TR 2021/014892 B\n• Başlık         : Otonom İHA ile Hassas Tarımsal İlaçlama Püskürtme Sistemi\n• Patent Sahibi  : AgroTech Inc.\n• Hukuki Durum   : Yürürlükte (In Force)\n• Çakışma Nedeni : Projedeki kenar bilişim ve akıllı nozul tasarımı, 1. Bağımsız \n                   İstem (Independent Claim) ile birebir çakışmaktadır.\n\n3. STRATEJİK ÖNERİ VE DESİGN-AROUND\n--------------------------------------------------------------------------------\nProjenin ticarileşme safhasında davalara ve toplama kararlarına maruz kalmaması \niçin Anlık Kenar Bilişim Tetikleme mekanizması yerine "Önceden İşlenmiş Grid \nHaritası Üzerinden Tetikleme" mimarisine geçilmesi (Design-Around) önerilir.\n================================================================================\n"""
    
    st.code(report_summary, language="text")
    
    st.download_button(
        label="📥 Resmi FSA Risk Raporunu İndir (.TXT / .DOC)",
        data=report_summary,
        file_name="TEYDEB_FSA_Risk_Raporu.txt",
        mime="text/plain"
    )
