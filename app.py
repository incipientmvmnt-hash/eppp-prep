import streamlit as st
import json
import random
from pathlib import Path

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="EPPP Test Prep", page_icon="🧠", layout="centered")

# ── Force light theme + custom CSS ───────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Force light */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background-color: #FFFFFF !important;
    color: #1a1a2e !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}
[data-testid="stSidebar"] { display: none !important; }
[data-testid="stHeader"] { display: none !important; }
footer { display: none !important; }
#MainMenu { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }

/* Typography */
h1 { font-weight: 700 !important; color: #1a1a2e !important; }
h2, h3 { font-weight: 600 !important; color: #1a1a2e !important; }

/* Cards */
.domain-card {
    background: #F8F6FB;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 12px;
    border: 1px solid #E8E4F0;
    transition: transform 0.15s;
}
.domain-card:hover { transform: translateY(-1px); }
.domain-badge {
    display: inline-block;
    background: #6B4C9A;
    color: white;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.8rem;
    font-weight: 600;
}
.stat-card {
    background: linear-gradient(135deg, #6B4C9A 0%, #8B6DBF 100%);
    border-radius: 12px;
    padding: 20px;
    color: white;
    text-align: center;
}
.stat-card h3 { color: white !important; margin: 0 !important; font-size: 2rem !important; }
.stat-card p { color: rgba(255,255,255,0.85); margin: 4px 0 0 0; font-size: 0.85rem; }
.correct { background: #E8F5E9 !important; border-left: 4px solid #4CAF50; padding: 16px; border-radius: 8px; margin: 8px 0; }
.incorrect { background: #FFEBEE !important; border-left: 4px solid #F44336; padding: 16px; border-radius: 8px; margin: 8px 0; }
.explanation-box { background: #F3E5F5; border-radius: 8px; padding: 16px; margin: 12px 0; border-left: 4px solid #6B4C9A; }
.progress-bar { background: #E8E4F0; border-radius: 10px; height: 8px; overflow: hidden; }
.progress-fill { background: linear-gradient(90deg, #6B4C9A, #8B6DBF); height: 100%; border-radius: 10px; transition: width 0.5s; }
.flashcard {
    background: #FFFFFF;
    border: 2px solid #E8E4F0;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    box-shadow: 0 2px 8px rgba(107,76,154,0.08);
}

/* Streamlit overrides */
.stButton > button {
    background: linear-gradient(135deg, #6B4C9A 0%, #8B6DBF 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 8px 24px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
}
.stButton > button:hover { opacity: 0.9 !important; }
div[data-testid="stRadio"] label { font-family: 'Inter', sans-serif !important; }
</style>
""", unsafe_allow_html=True)

# ── Load questions ───────────────────────────────────────────────────────────
@st.cache_data
def load_questions():
    p = Path(__file__).parent / "questions.json"
    with open(p) as f:
        return json.load(f)

questions = load_questions()

DOMAINS = {
    1: ("Biological Bases of Behavior", "10%", "🧬"),
    2: ("Cognitive-Affective Bases of Behavior", "12%", "🧠"),
    3: ("Social and Cultural Bases of Behavior", "11%", "👥"),
    4: ("Growth and Lifespan Development", "12%", "🌱"),
    5: ("Assessment and Diagnosis", "15%", "📋"),
    6: ("Treatment, Intervention, Prevention and Supervision", "15%", "💊"),
    7: ("Research Methods and Statistics", "8%", "📊"),
    8: ("Ethical, Legal, and Professional Issues", "17%", "⚖️"),
}

# ── Session state defaults ───────────────────────────────────────────────────
defaults = {
    "page": "home", "quiz_questions": [], "quiz_index": 0, "quiz_answers": {},
    "quiz_submitted": {}, "quiz_domain": "All Domains", "study_domain": "All Domains",
    "quiz_complete": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def go(page):
    st.session_state.page = page


# ── NAV ──────────────────────────────────────────────────────────────────────
cols = st.columns(4)
with cols[0]:
    if st.button("🏠 Home"):
        go("home")
with cols[1]:
    if st.button("📝 Quiz"):
        go("quiz_setup")
with cols[2]:
    if st.button("📖 Study"):
        go("study")
with cols[3]:
    if st.button("📊 Results"):
        go("results")

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# PAGES
# ══════════════════════════════════════════════════════════════════════════════

# ── HOME ─────────────────────────────────────────────────────────────────────
if st.session_state.page == "home":
    st.markdown("# 🧠 EPPP Test Prep")
    st.markdown("**Examination for Professional Practice in Psychology — Part 1 (Knowledge)**")

    st.markdown("")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="stat-card"><h3>225</h3><p>Questions</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="stat-card"><h3>4h 15m</h3><p>Time Limit</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="stat-card"><h3>500</h3><p>Passing Score</p></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="stat-card"><h3>{len(questions)}</h3><p>Practice Qs</p></div>', unsafe_allow_html=True)

    st.markdown("### 📚 Content Domains")
    for num, (name, weight, icon) in DOMAINS.items():
        count = sum(1 for q in questions if q["domain_num"] == num)
        st.markdown(f"""<div class="domain-card">
            <span class="domain-badge">{weight}</span>&nbsp;&nbsp;
            <strong>{icon} Domain {num}: {name}</strong>
            <span style="float:right;color:#888;">{count} questions</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Start Practice Quiz", use_container_width=True):
            go("quiz_setup")
    with col2:
        if st.button("📖 Study Mode", use_container_width=True):
            go("study")

    with st.expander("ℹ️ About the EPPP"):
        st.markdown("""
- **225** multiple-choice questions (175 scored, 50 pretest/unscored)
- **4 answer choices** per question, one correct
- **4 hours 15 minutes** to complete
- Administered at **Pearson VUE** centers
- **$600** per sitting
- **Passing score: 500** (scaled)
- Covers **8 content domains** weighted as shown above
        """)

# ── QUIZ SETUP ───────────────────────────────────────────────────────────────
elif st.session_state.page == "quiz_setup":
    st.markdown("# 📝 Quiz Setup")

    domain_options = ["All Domains"] + [f"Domain {n}: {DOMAINS[n][0]}" for n in range(1, 9)]
    st.session_state.quiz_domain = st.selectbox("Select Domain", domain_options)

    num_q = st.slider("Number of Questions", 5, min(50, len(questions)), 10)

    if st.button("Start Quiz", use_container_width=True):
        if st.session_state.quiz_domain == "All Domains":
            pool = questions[:]
        else:
            dnum = int(st.session_state.quiz_domain.split(":")[0].replace("Domain ", ""))
            pool = [q for q in questions if q["domain_num"] == dnum]
        random.shuffle(pool)
        st.session_state.quiz_questions = pool[:num_q]
        st.session_state.quiz_index = 0
        st.session_state.quiz_answers = {}
        st.session_state.quiz_submitted = {}
        st.session_state.quiz_complete = False
        go("quiz")
        st.rerun()

# ── QUIZ ─────────────────────────────────────────────────────────────────────
elif st.session_state.page == "quiz":
    qs = st.session_state.quiz_questions
    if not qs:
        st.warning("No quiz started. Go to Quiz Setup.")
        if st.button("Go to Setup"):
            go("quiz_setup")
            st.rerun()
    else:
        idx = st.session_state.quiz_index
        total = len(qs)

        # Progress
        pct = int((idx / total) * 100) if not st.session_state.quiz_complete else 100
        st.markdown(f"""<div class="progress-bar"><div class="progress-fill" style="width:{pct}%"></div></div>""", unsafe_allow_html=True)
        st.markdown(f"**Question {min(idx+1, total)} of {total}**")

        if st.session_state.quiz_complete:
            go("results")
            st.rerun()
        else:
            q = qs[idx]
            st.markdown(f'<span class="domain-badge">{DOMAINS[q["domain_num"]][2]} {q["domain"]}</span>', unsafe_allow_html=True)
            st.markdown(f"### {q['stem']}")

            # Answer selection
            key = f"answer_{idx}"
            submitted = idx in st.session_state.quiz_submitted

            if not submitted:
                choice = st.radio("Select your answer:", q["options"], key=key, label_visibility="collapsed")
                if st.button("Submit Answer"):
                    st.session_state.quiz_answers[idx] = choice
                    st.session_state.quiz_submitted[idx] = True
                    st.rerun()
            else:
                chosen = st.session_state.quiz_answers[idx]
                correct = q["correct_answer"]
                is_correct = chosen == correct

                for opt in q["options"]:
                    if opt == correct:
                        st.markdown(f'<div class="correct">✅ {opt}</div>', unsafe_allow_html=True)
                    elif opt == chosen and not is_correct:
                        st.markdown(f'<div class="incorrect">❌ {opt}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f"&nbsp;&nbsp;&nbsp;{opt}")

                if is_correct:
                    st.success("Correct! 🎉")
                else:
                    st.error(f"Incorrect. The correct answer is: **{correct}**")

                st.markdown(f'<div class="explanation-box">💡 <strong>Explanation:</strong> {q["explanation"]}</div>', unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                with col2:
                    if idx < total - 1:
                        if st.button("Next Question →", use_container_width=True):
                            st.session_state.quiz_index += 1
                            st.rerun()
                    else:
                        if st.button("View Results 📊", use_container_width=True):
                            st.session_state.quiz_complete = True
                            go("results")
                            st.rerun()

# ── RESULTS ──────────────────────────────────────────────────────────────────
elif st.session_state.page == "results":
    st.markdown("# 📊 Results")

    qs = st.session_state.quiz_questions
    answers = st.session_state.quiz_answers

    if not qs or not answers:
        st.info("No quiz results yet. Take a quiz first!")
        if st.button("Start a Quiz"):
            go("quiz_setup")
            st.rerun()
    else:
        total = len(qs)
        answered = len(answers)
        correct_count = sum(
            1 for i, q in enumerate(qs)
            if i in answers and answers[i] == q["correct_answer"]
        )
        score_pct = int((correct_count / answered) * 100) if answered else 0

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="stat-card"><h3>{correct_count}/{answered}</h3><p>Correct</p></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="stat-card"><h3>{score_pct}%</h3><p>Score</p></div>', unsafe_allow_html=True)
        with c3:
            grade = "🟢 Pass" if score_pct >= 70 else "🔴 Keep Studying"
            st.markdown(f'<div class="stat-card"><h3>{grade}</h3><p>Estimate</p></div>', unsafe_allow_html=True)

        # Domain breakdown
        st.markdown("### Domain Breakdown")
        domain_stats = {}
        for i, q in enumerate(qs):
            if i not in answers:
                continue
            d = q["domain_num"]
            if d not in domain_stats:
                domain_stats[d] = {"correct": 0, "total": 0}
            domain_stats[d]["total"] += 1
            if answers[i] == q["correct_answer"]:
                domain_stats[d]["correct"] += 1

        for d in sorted(domain_stats):
            s = domain_stats[d]
            dpct = int((s["correct"] / s["total"]) * 100) if s["total"] else 0
            icon = DOMAINS[d][2]
            st.markdown(f"**{icon} {DOMAINS[d][0]}** — {s['correct']}/{s['total']} ({dpct}%)")
            st.progress(dpct / 100)

        # Missed questions
        missed = [(i, qs[i]) for i in range(len(qs)) if i in answers and answers[i] != qs[i]["correct_answer"]]
        if missed:
            st.markdown("### ❌ Missed Questions")
            for i, q in missed:
                with st.expander(f"{q['stem'][:80]}..."):
                    st.markdown(f"**Your answer:** {answers[i]}")
                    st.markdown(f"**Correct answer:** {q['correct_answer']}")
                    st.markdown(f'<div class="explanation-box">💡 {q["explanation"]}</div>', unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔄 Take Another Quiz", use_container_width=True):
                go("quiz_setup")
                st.rerun()
        with col_b:
            if st.button("⚡ Quick Restart (Same Settings)", use_container_width=True):
                # Re-shuffle same pool, restart immediately
                domain = st.session_state.quiz_domain
                num_q = len(qs)
                if domain == "All Domains":
                    pool = questions[:]
                else:
                    dnum = int(domain.split(":")[0].replace("Domain ", ""))
                    pool = [q for q in questions if q["domain_num"] == dnum]
                random.shuffle(pool)
                st.session_state.quiz_questions = pool[:num_q]
                st.session_state.quiz_index = 0
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = {}
                st.session_state.quiz_complete = False
                go("quiz")
                st.rerun()

# ── STUDY MODE ───────────────────────────────────────────────────────────────
elif st.session_state.page == "study":
    st.markdown("# 📖 Study Mode")

    domain_options = ["All Domains"] + [f"Domain {n}: {DOMAINS[n][0]}" for n in range(1, 9)]
    st.session_state.study_domain = st.selectbox("Filter by Domain", domain_options, key="study_filter")

    if st.session_state.study_domain == "All Domains":
        pool = questions
    else:
        dnum = int(st.session_state.study_domain.split(":")[0].replace("Domain ", ""))
        pool = [q for q in questions if q["domain_num"] == dnum]

    st.markdown(f"**{len(pool)} questions**")

    for i, q in enumerate(pool):
        st.markdown(f"""<div class="flashcard">
            <span class="domain-badge">{DOMAINS[q['domain_num']][2]} {q['domain']}</span>
            &nbsp;<span style="color:#888;font-size:0.8rem;">{q['difficulty'].upper()}</span>
        </div>""", unsafe_allow_html=True)

        with st.expander(f"**Q{i+1}.** {q['stem']}", expanded=False):
            for opt in q["options"]:
                if opt == q["correct_answer"]:
                    st.markdown(f"✅ **{opt}**")
                else:
                    st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;{opt}")
            st.markdown(f'<div class="explanation-box">💡 {q["explanation"]}</div>', unsafe_allow_html=True)
