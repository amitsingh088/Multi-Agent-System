"""
Streamlit front-end for the multi-agent research pipeline defined in pipeline.py.

Setup
-----
Put this file, together with the .streamlit/config.toml theme, in the same
folder as pipeline.py, agents.py and tools.py:

    .
    ├── .streamlit/
    │   └── config.toml
    ├── agents.py
    ├── app.py          <- this file
    ├── pipeline.py
    ├── requirements.txt
    └── tools.py

Then install streamlit and run it:

    pip install streamlit
    streamlit run app.py
"""

import contextlib
import html
import time
import traceback
from datetime import datetime

import streamlit as st

st.set_page_config(
    page_title="Research Agent",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Import after set_page_config so a broken import (missing API keys, missing
# deps, etc.) still shows a styled, readable error instead of a bare crash.
try:
    from pipeline import run_research_pipeline
except Exception as exc:
    st.error(f"Couldn't import `run_research_pipeline` from pipeline.py: {exc}")
    st.info(
        "Make sure app.py sits in the same folder as pipeline.py, agents.py "
        "and tools.py, and that any API keys the agents need are set, the "
        "same way they need to be set when you run pipeline.py from the terminal."
    )
    st.stop()


# ---------------------------------------------------------------- styling --
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&display=swap');

    .block-container { padding-top: 2.5rem; max-width: 980px; }

    h1 {
        font-family: 'Fraunces', Georgia, serif;
        font-weight: 700;
        font-size: 2.5rem;
        letter-spacing: -0.01em;
        margin-bottom: 0.15rem;
    }

    .raa-eyebrow {
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: 0.75rem;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: #8A5A2B;
        margin-bottom: 0.9rem;
    }

    .raa-console {
        background: #14181A;
        color: #E8A33D;
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: 0.82rem;
        line-height: 1.55;
        white-space: pre-wrap;
        word-break: break-word;
        padding: 1rem 1.15rem;
        border-radius: 8px;
        max-height: 360px;
        overflow-y: auto;
    }
    .raa-cursor {
        display: inline-block;
        width: 0.5em;
        background: #E8A33D;
        animation: raa-blink 1s step-end infinite;
    }
    @keyframes raa-blink { 50% { opacity: 0; } }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------- helpers --
def as_text(value) -> str:
    """Agents/chains may hand back a plain string or a message object
    (e.g. LangChain's AIMessage) that carries a `.content` attribute.
    Normalize either shape to plain text for display."""
    return getattr(value, "content", value)


class LiveConsole:
    """File-like object. Redirecting stdout into an instance of this
    makes every print() call already inside pipeline.py show up live,
    styled as a terminal panel, instead of only in the server's own
    console window."""

    def __init__(self, placeholder):
        self._placeholder = placeholder
        self.buffer = ""
        self._running = False
        self.render()

    def write(self, s):
        self.buffer += s
        self._running = True
        self.render()
        return len(s)

    def flush(self):
        pass

    def stop(self):
        self._running = False
        self.render()

    def render(self):
        cursor = '<span class="raa-cursor">&nbsp;</span>' if self._running else ""
        shown = html.escape(self.buffer.strip()) or "waiting for the pipeline to start…"
        self._placeholder.markdown(
            f'<div class="raa-console">{shown}{cursor}</div>',
            unsafe_allow_html=True,
        )


# ------------------------------------------------------------ app state --
if "result" not in st.session_state:
    st.session_state.result = None
if "history" not in st.session_state:
    st.session_state.history = []


# ------------------------------------------------------------------ main --
st.title("Research Agent")
st.markdown(
    '<div class="raa-eyebrow">search · read · write · critique</div>',
    unsafe_allow_html=True,
)
st.caption("Runs the multi-agent pipeline from pipeline.py and lays out what each stage produced.")

with st.form("research_form"):
    topic = st.text_input(
        "Research topic",
        placeholder="e.g. Advances in solid-state EV batteries in 2026",
    )
    submitted = st.form_submit_button("Run research", use_container_width=True)

if submitted:
    if not topic.strip():
        st.warning("Enter a topic to research first.")
    else:
        st.session_state.result = None
        with st.status("Running the research pipeline…", expanded=True) as status:
            console = LiveConsole(st.empty())
            start = time.monotonic()
            try:
                with contextlib.redirect_stdout(console):
                    result = run_research_pipeline(topic)
                console.stop()

                elapsed = time.monotonic() - start
                st.session_state.result = result
                st.session_state.history.insert(
                    0,
                    {
                        "topic": topic,
                        "time": datetime.now().strftime("%H:%M"),
                        "result": result,
                    },
                )
                status.update(
                    label=f"Research complete in {elapsed:.0f}s",
                    state="complete",
                    expanded=False,
                )

            except Exception as exc:
                console.stop()
                status.update(label="Pipeline failed", state="error", expanded=True)
                st.error(f"The pipeline raised an error: {exc}")
                with st.expander("Full traceback"):
                    st.code(traceback.format_exc())


# --------------------------------------------------------------- results --
result = st.session_state.result
if result:
    report = as_text(result.get("report", ""))
    feedback = as_text(result.get("feedback", ""))
    search_results = as_text(result.get("search_results", ""))
    scraped_content = as_text(result.get("scraped_content", ""))

    tab_report, tab_feedback, tab_search, tab_scraped = st.tabs(
        ["Report", "Critic feedback", "Search results", "Scraped content"]
    )

    with tab_report:
        with st.container(border=True):
            st.markdown(report)
        st.download_button(
            "Download report as Markdown",
            data=report,
            file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown",
        )

    with tab_feedback:
        with st.container(border=True):
            st.markdown("**🧐 Critic's review**")
            st.markdown(feedback)

    with tab_search:
        st.text_area(
            "Raw search results",
            search_results,
            height=380,
            disabled=True,
            label_visibility="collapsed",
        )

    with tab_scraped:
        st.text_area(
            "Raw scraped content",
            scraped_content,
            height=380,
            disabled=True,
            label_visibility="collapsed",
        )
else:
    st.info("Enter a topic above and click **Run research** to get started.")


# --------------------------------------------------------------- sidebar --
# Placed after the logic above (which can append to history on this same
# run) so a run that just finished shows up immediately, not one run late.
with st.sidebar:
    st.markdown("### 🔎 Research Agent")
    st.caption("search → read → write → critique")
    st.divider()
    st.markdown("**History**")
    if not st.session_state.history:
        st.caption("Runs from this session will show up here.")
    for idx, item in enumerate(st.session_state.history):
        with st.expander(f"{item['time']} · {item['topic'][:34]}", key=f"history_{idx}"):
            st.markdown(as_text(item["result"].get("report", "")))