"""Streamlit frontend for the existing AI Interview Assistant RAG backend."""

from __future__ import annotations

import html
from src.memory import clear_session_history
import json
import re
from pathlib import Path

import streamlit as st

from src.chains import get_rag_chain
from src.config import EMBEDDING_MODEL, LLM_MODEL
from src.largelanguagemodel import get_llm
from styles import inject_styles


APP_DIR = Path(__file__).resolve().parent
HERO_IMAGE = APP_DIR / "assets" / "interview-hero.png"
TOPICS = [
    "SQL", "Python", "Machine Learning", "Deep Learning", "Data Science",
    "Generative AI", "NLP", "Computer Vision", "Statistics", "HR",
    "Behavioral", "Company Specific",
]
QUICK_QUESTIONS = [
    "Explain SQL JOIN with a simple example.",
    "What is the difference between a list and a tuple in Python?",
    "Explain overfitting and how to prevent it.",
    "How should I answer: Tell me about yourself?",
]


def initialize_state() -> None:
    """Create stable session-state defaults used by the UI."""
    defaults = {
        "mode": "AI Interview Assistant",
        "nav_mode": "AI Interview Assistant",
        "assistant_topic": "SQL",
        "assistant_open": False,
        "messages": [],
        "pending_question": None,
        "interview": None,
        "conversation_count": 0,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


@st.cache_resource(show_spinner=False)
def load_rag_chain():
    """Load the existing persisted RAG pipeline exactly once per server."""
    return get_rag_chain()


@st.cache_resource(show_spinner=False)
def load_llm():
    """Reuse the existing project-configured Groq model."""
    return get_llm()


def select_topic(label: str, key: str, default: str = "SQL") -> str:
    """Render the shared interview-topic selector without duplicated options."""
    index = TOPICS.index(default) if default in TOPICS else 0
    return st.selectbox(label, TOPICS, index=index, key=key)


def switch_mode(mode: str) -> None:
    st.session_state.mode = mode
    st.session_state.nav_mode = mode
    st.rerun()


def sidebar() -> None:
    with st.sidebar:
        st.markdown(
            """<div class='brand'>
            <div class='brand-mark'>AI</div><div><div class='brand-title'>Interview Studio</div>
            <div class='brand-subtitle'>Practice with precision</div></div></div>""",
            unsafe_allow_html=True,
        )
        selected = st.radio(
            "Navigation",
            ["AI Interview Assistant", "AI Mock Interview"],
            key="nav_mode",
            label_visibility="collapsed",
        )
        st.session_state.mode = selected
        st.markdown("<div class='side-label'>SYSTEM OVERVIEW</div>", unsafe_allow_html=True)
        st.markdown(
            f"""<div class='system-card'><span class='system-icon'>◈</span><div><b>Current model</b>
            <small>{html.escape(LLM_MODEL)}</small></div></div>
            <div class='system-card'><span class='system-icon'>◌</span><div><b>Embedding model</b>
            <small>{html.escape(EMBEDDING_MODEL)}</small></div></div>
            <div class='system-card'><span class='system-icon'>⬡</span><div><b>Vector database</b>
            <small>ChromaDB · persistent</small></div></div>""",
            unsafe_allow_html=True,
        )
        st.markdown("<div class='ready-badge'>● SYSTEM READY</div>", unsafe_allow_html=True)
        st.caption(f"{st.session_state.conversation_count} assistant conversations")
        if st.button("Clear assistant chat", use_container_width=True):
            st.session_state.assistant_open = False
            st.session_state.messages = []
            st.session_state.conversation_count = 0
            clear_session_history("assistant_chat")
            st.rerun()

        if st.button("Reset mock interview", use_container_width=True):
            st.session_state.interview = None
            st.rerun()

def footer() -> None:
    st.markdown(
        "<div class='footer'>Built with <strong>LangChain · Groq · ChromaDB · HuggingFace · Streamlit</strong><br>Designed for thoughtful interview preparation</div>",
        unsafe_allow_html=True,
    )


def invoke_rag(question: str, topic: str) -> str:
    """
    Send a topic-aware question through the conversational RAG chain.
    """

    query = (
        f"The candidate is preparing for {topic} interviews. "
        f"Keep the response focused on {topic} interview preparation.\n\n"
        f"Question: {question}"
    )

    try:
        with st.status("Preparing your answer…", expanded=True) as status:

            st.write("Searching the interview knowledge base…")

            answer = load_rag_chain().invoke(
                {
                    "question": query
                },
                config={
                    "configurable": {
                        "session_id": "assistant_chat"
                    }
                }
            )

            status.update(
                label="Response ready",
                state="complete",
                expanded=False,
            )

        return answer

    except Exception as error:

        return (
            "I couldn’t complete that request.\n\n"
            f"Details:\n{error}"
        )


def landing_section() -> None:
    left, right = st.columns([1.15, 0.85], gap="large")
    with left:
        st.markdown(
            """<div class='hero'><div class='eyebrow'>AI-POWERED INTERVIEW PRACTICE</div>
            <h1>Master interviews with <span>clarity and confidence.</span></h1>
            <p>Practice technical concepts, simulate real interviews, and turn each answer into actionable feedback.</p></div>""",
            unsafe_allow_html=True,
        )
        first, second = st.columns(2)
        if first.button("Ask the assistant", type="primary", use_container_width=True):
            st.session_state.assistant_open = True
            st.rerun()
        if second.button("Start mock interview", use_container_width=True):
            switch_mode("AI Mock Interview")
    with right:
        if HERO_IMAGE.exists():
            st.image(str(HERO_IMAGE), use_container_width=True)
    st.markdown("<div class='section-title'>Everything you need to improve</div>", unsafe_allow_html=True)
    cards = [
        ("✦", "AI Interview Assistant", "Grounded, structured answers from your curated interview knowledge base."),
        ("◎", "Adaptive Mock Interviews", "A context-aware interviewer that naturally follows your answers."),
        ("↗", "Instant Answer Evaluation", "Scores, gaps, stronger answers, and practical coaching in the moment."),
    ]
    cols = st.columns(3)
    for col, (icon, title, copy) in zip(cols, cards):
        col.markdown(
            f"<div class='feature-card'><div class='feature-icon'>{icon}</div><h3>{title}</h3><p>{copy}</p></div>",
            unsafe_allow_html=True,
        )


def assistant_page() -> None:
    st.markdown(
        "<div class='page-kicker'>KNOWLEDGE ASSISTANT</div><h2 class='page-title'>Interview questions, answered clearly.</h2>",
        unsafe_allow_html=True,
    )
    topic = select_topic("Choose your interview focus", "assistant_topic", st.session_state.assistant_topic)
    st.caption(f"Answers will be tailored for **{topic}** interview preparation.")
    if not st.session_state.messages and not st.session_state.assistant_open:
        landing_section()
        st.markdown("<div class='section-title'>Suggested starting points</div>", unsafe_allow_html=True)
        for row in (QUICK_QUESTIONS[:2], QUICK_QUESTIONS[2:]):
            row_columns = st.columns(2)
            for column, prompt in zip(row_columns, row):
                if column.button(prompt, use_container_width=True):
                    st.session_state.pending_question = prompt
                    st.rerun()
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🧑‍💻" if message["role"] == "user" else "✦"):
            st.markdown(message["content"])
    question = st.chat_input("Ask an interview question…") or st.session_state.pop("pending_question", None)
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(question)
        with st.chat_message("assistant", avatar="🧑‍💻"):
            with st.spinner("Thinking through this…"):
                answer = invoke_rag(question, topic)
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.session_state.conversation_count += 1


def transcript(interview: dict) -> str:
    return "\n\n".join(
        f"Question {position + 1}: {item['question']}\nCandidate answer: {item['answer']}"
        for position, item in enumerate(interview["history"])
    ) or "No earlier turns."


def question_prompt(interview: dict) -> str:
    return f"""You are a professional {interview['type']} interviewer conducting a {interview['difficulty']} {interview['topic']} interview for {interview['company']}.
Use the complete prior transcript below to ask exactly one natural next question. Ask an opening question when there is no history. Follow up intelligently on previous answers, avoid repeated questions, and do not give hints, answers, scores, or feedback. Return only the interview question.

Transcript:
{transcript(interview)}"""


def answer_evaluation_prompt(interview: dict, question: str, answer: str) -> str:
    return f"""You are evaluating a candidate in a {interview['difficulty']} {interview['topic']} {interview['type']} interview. Consider the conversation context, current question, and answer. Return ONLY valid JSON with these keys:
score (number 0-10), technical_accuracy (number 0-10), completeness (number 0-10), communication (number 0-10), confidence (number 0-10), clarity (number 0-10), problem_solving (number 0-10), strengths (list of strings), weaknesses (list of strings), missing_concepts (list of strings explaining what was omitted), better_answer (string with a concise ideal interview-quality answer), interview_tips (list of 3-5 actionable strings), final_verdict (one of Strong Hire, Hire, Borderline, No Hire).

Previous transcript:
{transcript(interview)}

Current question: {question}
Candidate answer: {answer}"""


def ask_interviewer(interview: dict) -> str:
    try:
        with st.status("Preparing the next question…", expanded=True) as status:
            st.write("Reviewing interview history…")
            question = load_llm().invoke(question_prompt(interview)).content.strip()
            status.update(label="Question ready", state="complete", expanded=False)
        return question
    except Exception as error:
        return f"Unable to generate a question. Please check your connection. ({error})"


def parse_evaluation(raw: str) -> dict:
    fallback = {
        "score": 0, "technical_accuracy": 0, "completeness": 0, "communication": 0,
        "confidence": 0, "clarity": 0, "problem_solving": 0,
        "strengths": [], "weaknesses": [], "missing_concepts": [], "better_answer": raw,
        "interview_tips": [], "final_verdict": "Borderline",
    }
    try:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        parsed = json.loads(match.group(0) if match else raw)
        return {**fallback, **parsed}
    except (AttributeError, json.JSONDecodeError):
        fallback["strengths"] = ["The evaluation service returned a non-structured response."]
        return fallback


def evaluate_interview_answer(interview: dict, question: str, answer: str) -> dict:
    try:
        with st.status("Evaluating your answer…", expanded=True) as status:
            st.write("Reviewing accuracy, clarity, and interview impact…")
            raw = load_llm().invoke(answer_evaluation_prompt(interview, question, answer)).content
            status.update(label="Feedback ready", state="complete", expanded=False)
        return parse_evaluation(raw)
    except Exception as error:
        st.error(f"Evaluation failed. Check your Groq connection and try again. Details: {error}")
        return {}


def score_value(value: object) -> float:
    try:
        return min(max(float(value), 0), 10)
    except (TypeError, ValueError):
        return 0.0


def feedback_card(evaluation: dict) -> None:
    score = score_value(evaluation.get("score"))
    verdict = html.escape(str(evaluation.get("final_verdict", "Borderline")))
    st.markdown(
        f"<div class='feedback-header'><div><span>ANSWER EVALUATION</span><h3>{score:.1f} <small>/ 10</small></h3></div><div class='verdict'>{verdict}</div></div>",
        unsafe_allow_html=True,
    )
    ratings = [
        ("Technical accuracy", "technical_accuracy"), ("Completeness", "completeness"),
        ("Communication", "communication"), ("Confidence", "confidence"),
        ("Clarity", "clarity"), ("Problem solving", "problem_solving"),
    ]
    left, right = st.columns(2)
    for index, (label, key) in enumerate(ratings):
        target = left if index < 3 else right
        rating = score_value(evaluation.get(key))
        target.progress(rating / 10, text=f"{label} · {rating:.1f}/10")
    sections = [
        ("Strengths", evaluation.get("strengths", [])),
        ("Weaknesses", evaluation.get("weaknesses", [])),
        ("Missing concepts", evaluation.get("missing_concepts", [])),
        ("Interview tips", evaluation.get("interview_tips", [])),
    ]
    first, second = st.columns(2)
    for column, (title, items) in zip((first, second, first, second), sections):
        with column:
            st.markdown(f"<div class='feedback-block'><h4>{title}</h4></div>", unsafe_allow_html=True)
            if items:
                for item in items:
                    st.markdown(f"- {item}")
            else:
                st.caption("No feedback returned for this section.")
    st.markdown("<div class='feedback-block'><h4>Better answer</h4></div>", unsafe_allow_html=True)
    st.markdown(str(evaluation.get("better_answer", "No ideal answer returned.")))


def render_interview_history(interview: dict) -> None:
    for item in interview["history"]:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(item["question"])
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(item["answer"])
        with st.container(border=True):
            feedback_card(item["evaluation"])


def final_report(interview: dict) -> str:
    prompt = f"""Create a concise Markdown report for this completed {interview['difficulty']} {interview['topic']} interview. Include overall impression, recurring strengths, highest-impact improvement, and hiring recommendation.\n\n{transcript(interview)}"""
    return load_llm().invoke(prompt).content


def interview_setup() -> None:
    st.markdown("<div class='page-kicker'>ADAPTIVE PRACTICE</div><h2 class='page-title'>Set the room. We’ll run the interview.</h2>", unsafe_allow_html=True)
    with st.form("interview_setup"):
        left, right = st.columns(2)
        with left:
            topic = select_topic("Interview topic", "setup_topic")
            company = st.text_input("Company context (optional)", placeholder="e.g. a product-focused SaaS company")
        with right:
            difficulty = st.select_slider("Difficulty", ["Beginner", "Intermediate", "Advanced"], value="Intermediate")
            interview_type = st.selectbox("Interview type", ["Technical", "HR", "Mixed"])
        question_count = st.slider("Practice questions", min_value=3, max_value=10, value=5)
        started = st.form_submit_button("Start interview", type="primary", use_container_width=True)
    if started:
        st.session_state.interview = {
            "topic": topic, "difficulty": difficulty, "company": company or "a leading technology company",
            "type": interview_type, "count": question_count, "history": [], "current": None,
            "awaiting_next": False, "report": None,
        }
        st.rerun()


def mock_interview_page() -> None:
    interview = st.session_state.interview
    if interview is None:
        interview_setup()
        return
    st.markdown(
        f"<div class='interview-topline'><span>{html.escape(interview['topic'])}</span><span>{html.escape(interview['difficulty'])}</span><span>{html.escape(interview['type'])}</span></div>",
        unsafe_allow_html=True,
    )
    if interview["report"]:
        st.markdown("<div class='page-kicker'>INTERVIEW COMPLETE</div><h2 class='page-title'>Your final interview report</h2>", unsafe_allow_html=True)
        st.markdown(interview["report"])
        return
    progress = len(interview["history"]) / interview["count"]
    st.progress(progress, text=f"{len(interview['history'])} of {interview['count']} answers evaluated")
    render_interview_history(interview)
    if interview["awaiting_next"]:
        if len(interview["history"]) >= interview["count"]:
            if st.button("Generate final interview report", type="primary"):
                with st.status("Preparing your final report…", expanded=True):
                    interview["report"] = final_report(interview)
                st.rerun()
        elif st.button("Next question", type="primary"):
            interview["current"] = ask_interviewer(interview)
            interview["awaiting_next"] = False
            st.rerun()
        return
    if interview["current"] is None:
        interview["current"] = ask_interviewer(interview)
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(interview["current"])
    with st.form("evaluate_answer_form", clear_on_submit=True):
        answer = st.text_area("Your answer", placeholder="Write your response as you would deliver it in the interview…", height=180)
        submitted = st.form_submit_button("Evaluate answer", type="primary", use_container_width=True)
    if submitted:
        if not answer.strip():
            st.warning("Please write an answer before asking for feedback.")
            return
        evaluation = evaluate_interview_answer(interview, interview["current"], answer.strip())
        if evaluation:
            interview["history"].append({"question": interview["current"], "answer": answer.strip(), "evaluation": evaluation})
            interview["current"] = None
            interview["awaiting_next"] = True
            st.rerun()


def main() -> None:
    st.set_page_config(page_title="Interview Studio", page_icon="✦", layout="wide", initial_sidebar_state="expanded")
    initialize_state()
    inject_styles(st)
    sidebar()
    if st.session_state.mode == "AI Mock Interview":
        mock_interview_page()
    else:
        assistant_page()
    footer()


if __name__ == "__main__":
    main()
