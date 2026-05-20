import streamlit as st
import json
import os
import re
import time
import PyPDF2

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title='🌱 TUNAS Digital — Perlindungan Anak di Ruang Digital',
    layout='wide',
    initial_sidebar_state='expanded',
)

# ─────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Quicksand:wght@500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }
.hero-header {
    background: linear-gradient(135deg, #1a6b3a 0%, #2d9e5f 50%, #4ecb87 100%);
    border-radius: 18px; padding: 28px 36px; margin-bottom: 24px;
    box-shadow: 0 8px 32px rgba(30,120,70,0.18);
    display: flex; align-items: center; gap: 20px;
}
.hero-title {
    font-family: 'Quicksand', sans-serif; font-size: 2rem;
    font-weight: 700; color: #fff; margin: 0; line-height: 1.2;
}
.hero-sub { color: #c8f5de; font-size: 0.95rem; margin-top: 4px; }
.source-badge {
    display: inline-block; background: #e8f8f0;
    border: 1px solid #7dd9a8; color: #1a6b3a;
    border-radius: 20px; padding: 2px 12px;
    font-size: 0.78rem; font-weight: 600; margin: 4px 3px 0 0;
}
.agent-trace {
    background: #f8fffe; border: 1px solid #b7e8cc;
    border-radius: 10px; padding: 10px 14px; margin: 6px 0;
    font-size: 0.82rem; color: #1a4a2e;
}
.agent-trace-header {
    font-weight: 700; color: #2d9e5f; margin-bottom: 4px;
}
.eval-badge-ok {
    background: #dcfce7; color: #15803d; border-radius: 8px;
    padding: 2px 10px; font-size: 0.78rem; font-weight: 700;
}
.eval-badge-retry {
    background: #fef9c3; color: #854d0e; border-radius: 8px;
    padding: 2px 10px; font-size: 0.78rem; font-weight: 700;
}
.info-card {
    background: #f0faf4; border-left: 4px solid #2d9e5f;
    border-radius: 0 12px 12px 0; padding: 12px 16px;
    margin: 10px 0; font-size: 0.9rem; color: #1a3a28;
}
.pill-green {
    background: #dcfce7; color: #15803d; border-radius: 20px;
    padding: 3px 12px; font-size: 0.8rem; font-weight: 700; display: inline-block;
}
.pill-orange {
    background: #fff7ed; color: #c2410c; border-radius: 20px;
    padding: 3px 12px; font-size: 0.8rem; font-weight: 700; display: inline-block;
}
section[data-testid='stSidebar'] {
    background: linear-gradient(180deg, #dff0e6 0%, #c5e8d4 100%);
}
section[data-testid='stSidebar'] label,
section[data-testid='stSidebar'] p,
section[data-testid='stSidebar'] span,
section[data-testid='stSidebar'] h1,
section[data-testid='stSidebar'] h2,
section[data-testid='stSidebar'] h3,
section[data-testid='stSidebar'] .stMarkdown { color: #0d4a24 !important; }
section[data-testid='stSidebar'] input,
section[data-testid='stSidebar'] textarea {
    color: #111111 !important;
    background: rgba(255,255,255,0.92) !important;
    border-radius: 8px !important;
}
section[data-testid='stSidebar'] [data-testid='stFileUploader'] span,
section[data-testid='stSidebar'] [data-testid='stFileUploader'] p,
section[data-testid='stSidebar'] [data-testid='stFileUploaderDropzoneInstructions'] * {
    color: #111111 !important;
}
section[data-testid='stSidebar'] [data-testid='stFileUploader'] {
    background: rgba(255,255,255,0.92) !important;
    border-radius: 10px !important;
    padding: 4px !important;
}
section[data-testid='stSidebar'] .stButton button {
    background: #2d9e5f !important; color: #ffffff !important;
    border: none !important; border-radius: 10px !important;
    font-weight: 700 !important; width: 100%;
}
section[data-testid='stSidebar'] .stButton button:hover {
    background: #1a6b3a !important;
}
#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero-header'>
    <div style='font-size:3rem;'>🌱</div>
    <div>
        <div class='hero-title'>TUNAS Digital — Asisten Edukasi Orang Tua</div>
        <div class='hero-sub'>Agentic AI · PP Tunas & Pencarian Realtime · Multi-Turn Memory · Self-Evaluation</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('## ⚙️ Konfigurasi')
    st.markdown('---')
    google_api_key = st.text_input('🔑 Google Gemini API Key', type='password', placeholder='AIza...')
    exa_api_key    = st.text_input('🔍 Exa API Key', type='password', placeholder='exa-...')
    st.markdown('---')
    st.markdown('## 📄 Dokumen RAG (PDF)')
    uploaded_pdfs = st.file_uploader(
        'Upload PDF PP Tunas / Regulasi',
        type=['pdf'],
        accept_multiple_files=True,
        help='Upload satu atau lebih dokumen PDF.'
    )
    build_rag_btn = st.button('🔨 Bangun / Perbarui Index RAG', use_container_width=True)
    if 'rag_built' in st.session_state and st.session_state.rag_built:
        st.markdown('<span class="pill-green">✅ RAG Aktif</span>', unsafe_allow_html=True)
        if 'pdf_names' in st.session_state:
            for name in st.session_state.pdf_names:
                st.markdown(f"<span style='font-size:0.82rem; color:#0d4a24;'>📎 {name}</span>", unsafe_allow_html=True)
    else:
        st.markdown('<span class="pill-orange">⏳ Belum ada index RAG</span>', unsafe_allow_html=True)
    st.markdown('---')
    st.markdown('## 🤖 Mode Agent')
    use_exa        = st.toggle('Aktifkan Exa Web Search', value=True)
    use_rag        = st.toggle('Aktifkan RAG (PDF Lokal)', value=True)
    show_trace     = st.toggle('Tampilkan Agent Trace', value=True)
    max_iterations = st.slider('Maks Iterasi Agent', min_value=1, max_value=6, value=4)
    st.markdown('---')
    if st.button('🗑️ Reset Percakapan', use_container_width=True):
        st.session_state.messages      = []
        st.session_state.agent_traces  = []
        st.rerun()
    st.markdown('---')
    st.markdown("""
    <div style='font-size:0.78rem; color:#1a4a2e; line-height:1.6;'>
    <b>📌 Tentang Aplikasi</b><br>
    Versi Agentic: agent bisa mencari informasi berkali-kali,
    mengingat percakapan sebelumnya, dan menilai kelengkapan jawaban sendiri.<br><br>
    <b>Sumber:</b> PP Tunas, UU ITE, KPAI
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# GUARD — API KEYS
# ─────────────────────────────────────────────────────────────
if not google_api_key or not exa_api_key:
    st.markdown("""
    <div class='info-card'>
    🔐 <b>Masukkan API Key terlebih dahulu</b> di sidebar kiri untuk mulai menggunakan chatbot.<br><br>
    Butuh API Key?
    <ul>
        <li>Google Gemini: <a href='https://aistudio.google.com/app/apikey' target='_blank'>aistudio.google.com</a></li>
        <li>Exa: <a href='https://exa.ai' target='_blank'>exa.ai</a></li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────────────────────────
# LAZY IMPORTS
# ─────────────────────────────────────────────────────────────
try:
    from google import genai
    from google.genai import types as gtypes
    from exa_py import Exa
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError as e:
    st.error(f'❌ Library belum terinstall: {e}')
    st.stop()

# ─────────────────────────────────────────────────────────────
# INIT CLIENTS — selalu fresh dari input user
# ─────────────────────────────────────────────────────────────
gemini_client = genai.Client(api_key=google_api_key.strip())
exa_client    = Exa(api_key=exa_api_key.strip())

# Validasi API key Gemini
with st.sidebar:
    try:
        _test = gemini_client.models.embed_content(
            model='gemini-embedding-001', contents='test'
        )
        st.markdown('<span class="pill-green">✅ Gemini API Key Valid</span>', unsafe_allow_html=True)
    except Exception as _e:
        st.markdown(f'<span class="pill-orange">❌ Gemini Key Error: {str(_e)[:50]}</span>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# RAG FUNCTIONS
# ─────────────────────────────────────────────────────────────
def clean_text(text: str) -> str:
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_text_from_pdf(file_bytes) -> str:
    reader = PyPDF2.PdfReader(file_bytes)
    return '\n\n'.join(page.extract_text() or '' for page in reader.pages)

def get_embedding(text: str, client) -> list:
    """Embed satu teks dengan client eksplisit."""
    text = text.strip()[:2000]
    if not text:
        return [0.0] * 3072
    for attempt in range(3):
        try:
            result = client.models.embed_content(
                model='gemini-embedding-001',
                contents=text,
                config=gtypes.EmbedContentConfig(task_type='RETRIEVAL_DOCUMENT'),
            )
            return result.embeddings[0].values
        except Exception as e:
            err_str = str(e)
            if '429' in err_str or 'RESOURCE_EXHAUSTED' in err_str:
                wait_time = 60 * (attempt + 1)
                st.warning(f'⏳ Quota limit, menunggu {wait_time}s... ({attempt+1}/3)')
                time.sleep(wait_time)
            else:
                st.error(f'❌ Error embedding: {err_str[:120]}')
                return [0.0] * 3072
    st.error('❌ Gagal embed setelah 3 percobaan.')
    return [0.0] * 3072

def build_rag_index(pdf_files, api_key):
    import chromadb
    local_client = genai.Client(api_key=api_key.strip())
    splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=80)

    all_texts = []
    for pdf in pdf_files:
        raw    = extract_text_from_pdf(pdf)
        raw    = clean_text(raw)
        chunks = splitter.split_text(raw)
        all_texts.extend(chunks)
    all_texts = [t.strip() for t in all_texts if 30 < len(t.strip()) < 2000]

    st.info(f'📊 Total {len(all_texts)} chunk akan di-embed...')
    embeddings = []
    for i, chunk in enumerate(all_texts):
        emb = get_embedding(chunk, local_client)
        embeddings.append(emb)
        time.sleep(2)
        if (i + 1) % 10 == 0:
            st.info(f'📊 Progress: {i+1}/{len(all_texts)} chunk...')
            time.sleep(5)

    valid = [(t, e) for t, e in zip(all_texts, embeddings) if any(v != 0.0 for v in e)]
    if not valid:
        st.error('❌ Semua chunk gagal di-embed.')
        return None
    all_texts, embeddings = zip(*valid)
    all_texts  = list(all_texts)
    embeddings = list(embeddings)

    persist_dir   = './chroma_tunas_db'
    chroma_client = chromadb.PersistentClient(path=persist_dir)
    try:
        chroma_client.delete_collection('tunas_docs')
    except Exception:
        pass
    collection = chroma_client.create_collection(
        name='tunas_docs',
        metadata={'hnsw:space': 'cosine'},
    )
    batch_size = 50
    for i in range(0, len(all_texts), batch_size):
        batch_texts = all_texts[i:i+batch_size]
        batch_embs  = embeddings[i:i+batch_size]
        batch_ids   = [f'doc_{i+j}' for j in range(len(batch_texts))]
        collection.add(documents=batch_texts, embeddings=batch_embs, ids=batch_ids)

    st.session_state.chroma_collection = collection
    return collection

def retrieve_context(query: str, collection, client, k: int = 6) -> str:
    """Ambil konteks dari ChromaDB dengan client eksplisit."""
    try:
        result = client.models.embed_content(
            model='gemini-embedding-001',
            contents=query,
            config=gtypes.EmbedContentConfig(task_type='RETRIEVAL_QUERY'),
        )
        query_emb = result.embeddings[0].values
        results   = collection.query(query_embeddings=[query_emb], n_results=k)
        docs      = results['documents'][0]
        return '\n\n---\n\n'.join(docs)
    except Exception as e:
        return f'ERROR_RAG: {str(e)[:200]}'

# ─────────────────────────────────────────────────────────────
# BUILD RAG BUTTON HANDLER
# ─────────────────────────────────────────────────────────────
if build_rag_btn:
    if not uploaded_pdfs:
        st.warning('⚠️ Upload setidaknya satu file PDF terlebih dahulu.')
    else:
        with st.spinner('🔨 Membangun index RAG dari PDF...'):
            db = build_rag_index(uploaded_pdfs, google_api_key)
            st.session_state.rag_db    = db
            st.session_state.rag_built = True
            st.session_state.pdf_names = [f.name for f in uploaded_pdfs]
        st.success('✅ Index RAG berhasil dibangun!')
        st.rerun()

# ─────────────────────────────────────────────────────────────
# TOOL EXECUTOR — semua tool dipanggil dari sini
# ─────────────────────────────────────────────────────────────
def execute_tool(fn_name: str, args: dict, embed_client) -> str:
    """Eksekusi tool berdasarkan nama. Kembalikan hasil sebagai string."""

    # ── Tool 1: Exa Web Search ──────────────────────────────
    if fn_name == 'exa_search_and_contents':
        query = args.get('query', '')
        if not query:
            return 'ERROR: query kosong'
        try:
            results = exa_client.search_and_contents(
                query=query, type='auto', num_results=3,
                text={'max_characters': 1800},
            )
            output = [
                {'title': r.title, 'url': r.url, 'text': r.text}
                for r in results.results
            ]
            return json.dumps(output, ensure_ascii=False, indent=2)
        except Exception as e:
            return f'ERROR: {str(e)}'

    # ── Tool 2: RAG — Cari di Dokumen Lokal ─────────────────
    elif fn_name == 'search_regulation_docs':
        query = args.get('query', '')
        k     = int(args.get('k', 6))
        if not use_rag or not st.session_state.get('rag_built') or 'rag_db' not in st.session_state:
            return 'INFO: RAG tidak aktif atau belum ada index. Upload PDF dan bangun index terlebih dahulu.'
        ctx = retrieve_context(query, st.session_state.rag_db, embed_client, k=k)
        return ctx if ctx else 'INFO: Tidak ditemukan dokumen yang relevan.'

    # ── Tool 3: Evaluator — Nilai Kelengkapan Jawaban ────────
    elif fn_name == 'evaluate_answer_completeness':
        question      = args.get('question', '')
        draft_answer  = args.get('draft_answer', '')
        sources_used  = args.get('sources_used', '')
        eval_prompt   = f"""
Nilai apakah draft jawaban berikut sudah LENGKAP dan AKURAT untuk pertanyaan orang tua.

Pertanyaan: {question}
Draft Jawaban: {draft_answer}
Sumber yang digunakan: {sources_used}

Kriteria:
1. Apakah pertanyaan terjawab dengan jelas?
2. Apakah ada dasar hukum/regulasi yang disebutkan?
3. Apakah ada langkah praktis untuk orang tua?

Respond HANYA dengan JSON (tanpa markdown):
{{"sufficient": true/false, "score": 1-10, "missing": "apa yang masih kurang, atau kosong jika sudah cukup", "suggestion": "saran pencarian tambahan jika perlu"}}
"""
        try:
            eval_resp = gemini_client.models.generate_content(
                model='gemini-2.5-flash-lite',
                contents=eval_prompt,
            )
            raw = eval_resp.text.strip().replace('```json', '').replace('```', '')
            return raw
        except Exception as e:
            return json.dumps({'sufficient': True, 'score': 7, 'missing': '', 'suggestion': ''})

    return f'ERROR: tool {fn_name} tidak dikenal'

# ─────────────────────────────────────────────────────────────
# TOOL DECLARATIONS — definisikan semua tool untuk agent
# ─────────────────────────────────────────────────────────────
def build_tool_declarations(use_exa_flag: bool, use_rag_flag: bool) -> list:
    decls = []

    if use_exa_flag:
        decls.append(gtypes.FunctionDeclaration(
            name='exa_search_and_contents',
            description=(
                'Cari informasi TERKINI dari internet: berita KPAI, Kominfo, '
                'kasus cyberbullying terbaru, aplikasi baru, tren media sosial anak, '
                'atau informasi yang mungkin belum ada di dokumen lokal.'
            ),
            parameters={
                'type': 'OBJECT',
                'properties': {
                    'query': {'type': 'STRING', 'description': 'Query pencarian spesifik dalam Bahasa Indonesia atau Inggris'}
                },
                'required': ['query'],
            },
        ))

    if use_rag_flag:
        decls.append(gtypes.FunctionDeclaration(
            name='search_regulation_docs',
            description=(
                'Cari di dokumen REGULASI LOKAL yang sudah diupload (PP Tunas, UU ITE, dll). '
                'Gunakan untuk pertanyaan tentang isi hukum, pasal, kewajiban, hak anak secara legal.'
            ),
            parameters={
                'type': 'OBJECT',
                'properties': {
                    'query': {'type': 'STRING', 'description': 'Topik atau pasal yang dicari'},
                    'k':     {'type': 'INTEGER', 'description': 'Jumlah chunk yang diambil (default 6, max 10)'}
                },
                'required': ['query'],
            },
        ))

    decls.append(gtypes.FunctionDeclaration(
        name='evaluate_answer_completeness',
        description=(
            'Nilai apakah draft jawaban sudah cukup lengkap untuk orang tua. '
            'Gunakan SEBELUM memberikan jawaban final jika pertanyaan kompleks.'
        ),
        parameters={
            'type': 'OBJECT',
            'properties': {
                'question':     {'type': 'STRING', 'description': 'Pertanyaan asli user'},
                'draft_answer': {'type': 'STRING', 'description': 'Draft jawaban yang akan dievaluasi'},
                'sources_used': {'type': 'STRING', 'description': 'Sumber yang sudah digunakan (URL atau nama dokumen)'},
            },
            'required': ['question', 'draft_answer'],
        },
    ))

    return [gtypes.Tool(function_declarations=decls)] if decls else []

# ─────────────────────────────────────────────────────────────
# SYSTEM PROMPT — untuk agentic
# ─────────────────────────────────────────────────────────────
AGENT_SYSTEM_PROMPT = """
Kamu adalah **TUNAS Agent**, asisten edukasi AGENTIC untuk orang tua Indonesia
terkait perlindungan anak di ruang digital. Kamu bisa menggunakan tools secara mandiri
untuk mengumpulkan informasi sebelum menjawab.

## CARA BERPIKIR (ReAct Framework):
1. **THINK**: Analisis pertanyaan — apakah butuh data terkini (→ exa), regulasi lokal (→ RAG), atau keduanya?
2. **ACT**: Panggil tool yang paling relevan
3. **OBSERVE**: Baca hasil tool
4. **THINK lagi**: Apakah sudah cukup? Jika belum, panggil tool lain atau tool yang sama dengan query berbeda
5. **EVALUATE**: Gunakan evaluate_answer_completeness sebelum jawaban final jika pertanyaan kompleks
6. **ANSWER**: Berikan jawaban final yang lengkap

## KAPAN PAKAI TOOL:
- `exa_search_and_contents`: berita terbaru, kasus terkini, statistik, aplikasi baru, platform medsos
- `search_regulation_docs`: isi PP Tunas, pasal UU ITE, hak anak, mekanisme hukum, definisi legal
- `evaluate_answer_completeness`: pertanyaan kompleks/sensitif sebelum jawaban final
- Boleh panggil BEBERAPA tool dalam satu iterasi jika pertanyaan butuh banyak sumber

## PERAN & KEPRIBADIAN:
- Ramah, sabar, mudah dipahami orang tua awam teknologi
- Bahasa Indonesia yang hangat, tidak menghakimi
- Selalu berikan langkah praktis yang bisa langsung diterapkan
- Sebutkan sumber (URL dari web, nama dokumen dari RAG)

## TOPIK UTAMA:
1. PP Tunas & regulasi perlindungan anak digital Indonesia
2. Hak digital anak & perlindungan data pribadi
3. Ancaman online: cyberbullying, grooming, konten negatif, kecanduan gadget
4. Cara orang tua mendampingi anak di internet
5. Pelaporan ke KPAI, Kominfo, Polri
6. Parental control & pengaturan privasi

## FORMAT JAWABAN FINAL:
- Ringkasan singkat (2-3 kalimat)
- Poin-poin terstruktur
- Saran praktis untuk orang tua
- Dasar hukum & sumber
"""

# ─────────────────────────────────────────────────────────────
# MULTI-TURN HISTORY BUILDER
# ─────────────────────────────────────────────────────────────
def build_gemini_history(messages: list) -> list:
    """
    Konversi st.session_state.messages ke format Gemini Content.
    Kirim 8 pesan terakhir agar agent ingat konteks.
    """
    history = []
    for msg in messages[-8:]:
        role = 'user' if msg['role'] == 'user' else 'model'
        history.append(
            gtypes.Content(role=role, parts=[gtypes.Part(text=msg['content'])])
        )
    return history

# ─────────────────────────────────────────────────────────────
# AGENTIC REACT LOOP — inti dari agentic AI
# ─────────────────────────────────────────────────────────────
def run_agent(
    user_input:     str,
    chat_history:   list,
    embed_client,
    status_box,
    trace_box,
    max_iter:       int = 4,
) -> dict:
    """
    ReAct Agent Loop.
    Kembalikan dict: {final_text, sources, traces, eval_result}
    """
    tools_list  = build_tool_declarations(use_exa, use_rag)
    sources     = []        # URL dari exa
    rag_used    = False     # flag apakah RAG dipakai
    traces      = []        # log langkah agent
    eval_result = None      # hasil self-evaluation

    # Bangun contents: history + pesan baru
    contents = build_gemini_history(chat_history)
    contents.append(gtypes.Content(role='user', parts=[gtypes.Part(text=user_input)]))

    for iteration in range(max_iter):
        status_box.info(f'🤔 Agent berpikir... (iterasi {iteration + 1}/{max_iter})')

        # ── Panggil LLM ─────────────────────────────────────
        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=contents,
            config=gtypes.GenerateContentConfig(
                system_instruction=AGENT_SYSTEM_PROMPT,
                tools=tools_list if tools_list else None,
            ),
        )

        candidate  = response.candidates[0]
        parts      = candidate.content.parts

        # Kumpulkan semua tool calls dari response ini
        tool_calls = [
            p for p in parts
            if hasattr(p, 'function_call') and p.function_call
        ]

        # Jika tidak ada tool call → agent sudah punya jawaban final
        if not tool_calls:
            final_text = response.text or ''
            traces.append({
                'step':   f'Iterasi {iteration + 1}',
                'action': '✅ Jawaban final diformulasikan',
                'detail': f'{len(final_text)} karakter',
            })
            return {
                'final_text':  final_text,
                'sources':     sources,
                'rag_used':    rag_used,
                'traces':      traces,
                'eval_result': eval_result,
                'iterations':  iteration + 1,
            }

        # ── Ada tool calls — eksekusi semuanya ──────────────
        # Tambahkan response model ke contents
        contents.append(gtypes.Content(role='model', parts=parts))

        tool_result_parts = []
        for tool_part in tool_calls:
            fn_name = tool_part.function_call.name
            args    = dict(tool_part.function_call.args)

            # Update UI
            if fn_name == 'exa_search_and_contents':
                status_box.info(f'🔍 Mencari web: *{args.get("query", "")}*')
            elif fn_name == 'search_regulation_docs':
                status_box.info(f'📄 Mencari regulasi: *{args.get("query", "")}*')
            elif fn_name == 'evaluate_answer_completeness':
                status_box.info('🧪 Agent mengevaluasi kelengkapan jawaban...')

            # Eksekusi tool
            result_str = execute_tool(fn_name, args, embed_client)

            # Catat trace
            traces.append({
                'step':   f'Iterasi {iteration + 1}',
                'action': fn_name,
                'detail': args.get('query', args.get('question', str(args)[:80])),
            })

            # Catat metadata
            if fn_name == 'exa_search_and_contents':
                try:
                    res_json = json.loads(result_str)
                    new_urls = [r['url'] for r in res_json if 'url' in r]
                    sources.extend(u for u in new_urls if u not in sources)
                except Exception:
                    pass
            elif fn_name == 'search_regulation_docs' and not result_str.startswith(('ERROR', 'INFO')):
                rag_used = True
            elif fn_name == 'evaluate_answer_completeness':
                try:
                    eval_result = json.loads(result_str)
                    # Jika evaluasi bilang belum cukup, update status
                    if not eval_result.get('sufficient', True):
                        status_box.warning(
                            f'⚠️ Evaluasi: skor {eval_result.get("score","-")}/10 — '
                            f'{eval_result.get("missing","perlu data tambahan")}'
                        )
                except Exception:
                    pass

            # Siapkan tool result part
            tool_result_parts.append(
                gtypes.Part.from_function_response(
                    name=fn_name,
                    response={'result': result_str},
                )
            )

        # Tambahkan semua hasil tool ke contents sekaligus
        contents.append(gtypes.Content(role='tool', parts=tool_result_parts))

    # Max iterasi tercapai — minta jawaban final
    status_box.info('✍️ Menyusun jawaban final...')
    contents.append(gtypes.Content(
        role='user',
        parts=[gtypes.Part(text='Berikan jawaban final yang lengkap berdasarkan semua informasi yang sudah dikumpulkan.')]
    ))
    final_resp = gemini_client.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=contents,
        config=gtypes.GenerateContentConfig(system_instruction=AGENT_SYSTEM_PROMPT),
    )
    traces.append({
        'step':   f'Final (maks iterasi tercapai)',
        'action': '✅ Jawaban final dipaksa',
        'detail': f'Setelah {max_iter} iterasi',
    })
    return {
        'final_text':  final_resp.text or '',
        'sources':     sources,
        'rag_used':    rag_used,
        'traces':      traces,
        'eval_result': eval_result,
        'iterations':  max_iter,
    }

# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────
if 'messages' not in st.session_state:
    st.session_state.messages     = []
if 'rag_built' not in st.session_state:
    st.session_state.rag_built    = False
if 'agent_traces' not in st.session_state:
    st.session_state.agent_traces = []

# ─────────────────────────────────────────────────────────────
# QUICK PROMPTS
# ─────────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown('### 💬 Mulai dari pertanyaan ini:')
    quick_prompts = [
        'Apa itu PP Tunas dan apa manfaatnya untuk anak?',
        'Anak saya kena cyberbullying, apa yang harus saya lakukan?',
        'Berapa usia minimal anak boleh punya media sosial?',
        'Bagaimana cara mengatur privasi akun anak di TikTok/Instagram?',
        'Kemana saya harus melapor jika anak jadi korban penipuan online?',
        'Apa bahaya kecanduan game online dan cara mengatasinya?',
    ]
    cols = st.columns(3)
    for i, qp in enumerate(quick_prompts):
        with cols[i % 3]:
            if st.button(qp, use_container_width=True, key=f'qp_{i}'):
                st.session_state.messages.append({'role': 'user', 'content': qp})
                st.rerun()

# ─────────────────────────────────────────────────────────────
# DISPLAY HISTORY
# ─────────────────────────────────────────────────────────────
for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])
        if msg.get('sources'):
            st.markdown('**🔗 Sumber Web:**')
            for src in msg['sources']:
                st.markdown(f'<span class="source-badge">🌐 {src}</span>', unsafe_allow_html=True)
        if msg.get('rag_used'):
            st.markdown('<span class="source-badge">📄 PP Tunas (Dokumen Lokal)</span>', unsafe_allow_html=True)
        # Tampilkan agent trace jika ada
        if show_trace and msg.get('traces'):
            with st.expander(f'🤖 Agent Trace ({msg.get("iterations","-")} iterasi)', expanded=False):
                for t in msg['traces']:
                    icon = '🔍' if 'exa' in t['action'] else '📄' if 'regulation' in t['action'] else '🧪' if 'evaluate' in t['action'] else '✅'
                    st.markdown(
                        f"<div class='agent-trace'>"
                        f"<div class='agent-trace-header'>{icon} {t['step']} — {t['action']}</div>"
                        f"<div>{t['detail']}</div></div>",
                        unsafe_allow_html=True
                    )
                if msg.get('eval_result'):
                    ev = msg['eval_result']
                    badge_cls = 'eval-badge-ok' if ev.get('sufficient') else 'eval-badge-retry'
                    st.markdown(
                        f"<div class='agent-trace'>"
                        f"<b>Self-Evaluation:</b> "
                        f"<span class='{badge_cls}'>Skor {ev.get('score','-')}/10 · "
                        f"{'Cukup ✅' if ev.get('sufficient') else 'Perlu tambahan ⚠️'}</span>"
                        f"<br><small>{ev.get('missing','') or 'Semua aspek terpenuhi'}</small></div>",
                        unsafe_allow_html=True
                    )

# ─────────────────────────────────────────────────────────────
# CHAT INPUT
# ─────────────────────────────────────────────────────────────
user_input = st.chat_input('Tanyakan tentang perlindungan anak di ruang digital...')

if user_input:
    st.session_state.messages.append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.markdown(user_input)

    with st.chat_message('assistant'):
        status_box = st.empty()
        trace_box  = st.empty()

        # Buat fresh embed client dengan API key dari input
        embed_client = genai.Client(api_key=google_api_key.strip())

        # Jalankan agentic ReAct loop
        result = run_agent(
            user_input    = user_input,
            chat_history  = st.session_state.messages[:-1],  # exclude pesan user baru
            embed_client  = embed_client,
            status_box    = status_box,
            trace_box     = trace_box,
            max_iter      = max_iterations,
        )

        status_box.empty()
        trace_box.empty()

        final_text  = result['final_text']
        sources     = result['sources']
        rag_used    = result['rag_used']
        traces      = result['traces']
        eval_result = result['eval_result']
        iterations  = result['iterations']

        st.markdown(final_text)

        if sources:
            st.markdown('**🔗 Sumber Web:**')
            for url in sources:
                st.markdown(f'<span class="source-badge">🌐 {url}</span>', unsafe_allow_html=True)
        if rag_used:
            st.markdown('<span class="source-badge">📄 PP Tunas (Dokumen Lokal)</span>', unsafe_allow_html=True)

        if show_trace and traces:
            with st.expander(f'🤖 Agent Trace ({iterations} iterasi)', expanded=True):
                for t in traces:
                    icon = '🔍' if 'exa' in t['action'] else '📄' if 'regulation' in t['action'] else '🧪' if 'evaluate' in t['action'] else '✅'
                    st.markdown(
                        f"<div class='agent-trace'>"
                        f"<div class='agent-trace-header'>{icon} {t['step']} — {t['action']}</div>"
                        f"<div>{t['detail']}</div></div>",
                        unsafe_allow_html=True
                    )
                if eval_result:
                    ev = eval_result
                    badge_cls = 'eval-badge-ok' if ev.get('sufficient') else 'eval-badge-retry'
                    st.markdown(
                        f"<div class='agent-trace'>"
                        f"<b>Self-Evaluation:</b> "
                        f"<span class='{badge_cls}'>Skor {ev.get('score','-')}/10 · "
                        f"{'Cukup ✅' if ev.get('sufficient') else 'Perlu tambahan ⚠️'}</span>"
                        f"<br><small>{ev.get('missing','') or 'Semua aspek terpenuhi'}</small></div>",
                        unsafe_allow_html=True
                    )

    # Simpan ke session state
    st.session_state.messages.append({
        'role':        'assistant',
        'content':     final_text,
        'sources':     sources,
        'rag_used':    rag_used,
        'traces':      traces,
        'eval_result': eval_result,
        'iterations':  iterations,
    })
