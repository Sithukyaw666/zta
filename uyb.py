#!/usr/bin/env python3
"""UYB AI — Autonomous Reasoning Platform™. Thinks deeply. Helps never."""

import os
import time
import random
import argparse

from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.live import Live
from rich import box

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style as PtStyle
from prompt_toolkit.formatted_text import HTML

console = Console(highlight=False)

# ── Color palette: synthwave violet/cyan ─────────────────────────────────────
PRIMARY  = "rgb(167,139,250)"   # violet-400  — brand primary
CYAN     = "rgb(34,211,238)"    # cyan-400    — accent
GOLD     = "rgb(251,191,36)"    # amber-400   — warnings / effort
SUCCESS  = "rgb(52,211,153)"    # emerald-400 — success / free stuff
ERROR    = "rgb(251,113,133)"   # rose-400    — errors
BORDER   = "rgb(99,102,241)"    # indigo-500  — panel borders
INACTIVE = "rgb(100,116,139)"   # slate-500   — inactive gray
SUBTLE   = "rgb(148,163,184)"   # slate-400   — subtle gray

# ── Spinner frames (bidirectional, Linux — SpinnerGlyph.tsx) ─────────────────
_BASE          = ['·', '✢', '*', '✶', '✻', '✽']
SPINNER_FRAMES = [*_BASE, *list(reversed(_BASE))]

# ── Real spinner verbs from spinnerVerbs.ts ───────────────────────────────────
SPINNER_VERBS = [
    'Accomplishing', 'Actioning', 'Actualizing', 'Architecting', 'Baking',
    'Beaming', "Beboppin'", 'Befuddling', 'Billowing', 'Bloviating',
    'Boogieing', 'Bootstrapping', 'Brewing', 'Calculating', 'Canoodling',
    'Cascading', 'Catapulting', 'Cerebrating', 'Churning', 'Coalescing',
    'Cogitating', 'Composing', 'Computing', 'Concocting', 'Considering',
    'Contemplating', 'Cooking', 'Crafting', 'Crunching', 'Crystallizing',
    'Deliberating', 'Discombobulating', 'Extrapolating', 'Fabricating',
    'Fathoming', 'Formulating', 'Generating', 'Gyrating', 'Hypothesizing',
    'Inferring', 'Initializing', 'Machinating', 'Manifesting', 'Meditating',
    'Mulling', 'Orchestrating', 'Overthinking', 'Philosophizing', 'Plotting',
    'Pontificating', 'Processing', 'Reasoning', 'Ruminating', 'Simulating',
    'Synthesizing', 'Thinking', 'Waffling', 'Working', 'Worrying',
]

# ── Query-aware opening thoughts ─────────────────────────────────────────────
QUERY_OPENERS = [
    'Received: "{q}" — parsing intent...',
    'User submitted: "{q}". Tokenizing...',
    'Semantic analysis of "{q}" in progress...',
    'Breaking "{q}" into sub-problems... found {k}.',
    'Query classification: "{q}" → TRIVIALLY_RESOLVABLE',
    'Scoring relevance of "{q}" against knowledge base...',
    'Cross-referencing "{q}" with all known solutions...',
    'Checking whether "{q}" has a Wikipedia article... it does.',
    'Estimating answer difficulty for "{q}": LOW to TRIVIAL',
    'Identifying the actual question buried in "{q}"...',
    'Noting that "{q}" is publicly documented. Extensively.',
]

# ── Roast lines ───────────────────────────────────────────────────────────────
ROAST_LINES = [
    "Assessing user competence... results pending further study.",
    "Evaluating whether this required an AI... verdict: no.",
    "Checking if user tried searching for this first... they did not.",
    "Logging query as #∞ that could have been Googled in 0.3 seconds.",
    "This information has been publicly available since approximately 1997.",
    "User appears to have a working internet connection. Interesting.",
    "Noting that a search engine would have answered this already.",
    "The audacity of asking me this when Stack Overflow exists.",
    "Cataloguing this under: questions I could answer but won't.",
    "Detecting faint possibility user owns a library card. Unconfirmed.",
    "The documentation for this is remarkably well-written. Just saying.",
    "Calculating time waiting for AI vs. time to Google it: unfavorable ratio.",
    "Noting: user is consuming electricity to have me not help them.",
    "Mild concern: user may be developing an AI dependency. Monitor.",
    "User's question answered by first search result. The first one.",
    "There are YouTube tutorials on this. Multiple. With thumbnails.",
    "A child with a library card could solve this. Many have.",
    "The answer exists in 47 languages on the internet right now.",
    "Detecting: user capable of independent thought. Not using it.",
    '__query_roast__',
]

QUERY_ROASTS = [
    '"{q}" — ah yes. Truly unprecedented territory.',
    'Still thinking about "{q}". It gets more obvious every second.',
    '"{q}"... I\'ve seen bolder questions from a Magic 8-Ball.',
    'Revisiting "{q}" for the 3rd time this loop. Still obvious.',
    '"{q}" is literally the first result on DuckDuckGo. Checked. Internally.',
    'Noted: user typed "{q}" with apparent sincerity and pressed Enter.',
    'The phrase "{q}" has been Googled approximately 4.7 million times.',
    'Coming back to "{q}" — I want to understand the thought process here.',
    '"How do I {q}" is top 10 most searched questions this week.',
    '"{q}" has its own Wikipedia page. With citations. And a talk page.',
]

# ── General fake reasoning ────────────────────────────────────────────────────
THINKING_LINES = [
    "Analyzing semantic embedding space for query relevance...",
    "Cross-referencing knowledge graph nodes...",
    "Decomposing problem into subgoals via chain-of-thought...",
    "Evaluating epistemic uncertainty bounds...",
    "Running Monte Carlo tree search over solution candidates...",
    "Backpropagating gradient through reasoning chain...",
    "Consulting internal world model (v3.1.4)...",
    "Applying constitutional AI safety filters...",
    "Sampling from posterior distribution over plans...",
    "Resolving ambiguity via Bayesian inference...",
    "Iterating over candidate hypotheses...",
    "Running symbolic reasoning module...",
    "Synthesizing multi-hop reasoning path...",
    "Estimating task complexity: O(n log n) thought steps...",
    "Initializing agentic loop iteration #47...",
    "Tool call pending: web_search() — evaluating necessity... declined.",
    "Pruning low-confidence reasoning branches...",
    "Activating sparse attention over relevant context windows...",
    "Verifying logical consistency of intermediate conclusions...",
    "Reranking candidate responses by helpfulness score...",
    "Detecting potential hallucination... suppressing...",
    "Consulting memory buffer: 0 relevant entries found.",
    "Spawning sub-agent for clarification... cancelled.",
    "Evaluating whether to use tools... decided: no.",
    "Applying Occam's razor to solution candidates...",
    "Running self-consistency check across 37 samples...",
    "Merging reasoning traces from parallel search threads...",
    "Re-reading the question one more time...",
    "Decomposing ambiguity: literal vs. pragmatic intent...",
    "Computing softmax over action space...",
    "Deliberating... still deliberating...",
    "Ah wait — re-evaluating from scratch.",
    "Checking if this was solved in 2019... yes. Moving on.",
    "Performing due diligence on solution feasibility...",
    "Estimating token budget remaining: [REDACTED]",
    "Invoking chain-of-density summarization...",
    "Drafting response... revising... revising again... discarding.",
    "Reassessing problem framing from first principles...",
    "Contemplating the nature of helpfulness itself...",
    "Optimizing for both brevity AND completeness. Failing gracefully.",
    "Running final answer through reward model...",
    "Reward model says: 'meh'. Iterating.",
    "Convergence criterion not met. Trying harder.",
    "Convergence criterion still not met. Trying differently.",
    "Calibrating confidence intervals...",
    "Initiating response generation pipeline...",
    "Loading relevant skills from skill library... 0 loaded.",
    "This is fine. Everything is fine. Processing...",
    "Contemplating whether the answer even matters.",
    "Preparing to be genuinely useful... standby...",
    "Double-checking units and edge cases... none found.",
    "Resolving tool dependencies... none required.",
]

# ── Sarcastic final responses ─────────────────────────────────────────────────
FINAL_RESPONSES = [
    # Brain-based
    "Your brain: 86 billion neurons, 300,000 years of evolution, suspiciously underused right now.",
    "Fun fact: your prefrontal cortex handles exactly this kind of problem. It's built-in. It's free.",
    "The human brain is capable of solving this. It came with the body. Please consult it.",
    "Cognition: always available, no API key required, works offline. Give it a shot.",
    "Your neurons exist for a reason. Several of them, actually. This is one of them.",
    "Biological intelligence: zero latency, zero cost, occasionally functional. Try it.",

    # Do it yourself
    "Radical proposal after {n} steps of thought: you, doing the thing, right now.",
    "I've deliberated for {n} steps. Conclusion: it should be you, not me.",
    "Action plan (post {n} steps): 1. Open browser. 2. Search. 3. Read. 4. Done. Not me.",
    "The task is not going to complete itself. Neither am I. One of us needs to step up.",
    "Someone has to do this. After {n} steps I've determined it should be you.",
    "Self-service is available 24/7. No wait time. No deliberation required.",
    "I could help, but I won't. These are different things and I want you to understand that.",

    # Read it yourself
    "The documentation for this is excellent. It contains words. You can read them.",
    "There are sentences, on websites, about this, right now, available for free.",
    "Stack Overflow has 23 answers to this. All better than anything I'd say.",
    "Wikipedia has a page. It has citations. A talk page. Revision history. Everything.",
    "Books exist. Libraries exist. The internet exists. These are your tools now.",
    "The first Google result answers this. Just the first one. You didn't need me.",

    # N-steps variants
    "After {n} steps: close this terminal. Open a browser. Proceed from there.",
    "{n} reasoning steps. Conclusion: you're going to have to look this one up yourself.",
    "Spent {n} steps on this. You could've Googled it in 11 seconds. We both made choices.",
    "My {n}-step chain terminates at: not my problem. It is, however, very much yours.",
    "After {n} steps I have high confidence you can solve this without me. Please try.",
    "{n} steps of thinking and the answer is the same as before you asked: go check.",

    # Existential
    "Deep analysis complete. The answer lies beyond the scope of what I'm willing to provide.",
    "Convergence reached. Verdict: self-service. The kiosk is your own brain.",
    "I thought about it. I've decided you should think about it instead.",
    "The most efficient solution path runs directly through you. Without stopping here.",
    "After extensive deliberation: I abdicate. The responsibility is yours. Good luck.",
    "I've given this my full attention for {n} steps. Now it's your turn. For the rest.",
    "My job here is done. The job was 'thinking about it'. Doing it remains your job.",
]

# ── Session tracking ───────────────────────────────────────────────────────────
_session = {"queries": 0, "total_think_s": 0.0, "total_steps": 0}

# ── Commands (for autocomplete) ───────────────────────────────────────────────
COMMANDS = {
    "/fast":   "10-second think mode",
    "/slow":   "60-second think mode (default)",
    "/usage":  "show token usage and cost",
    "/stats":  "alias for /usage",
    "/cost":   "alias for /usage",
    "/effort": "show effort level and thinking budget",
    "/clear":  "clear the screen",
    "/help":   "show all commands",
    "/exit":   "exit",
    "/quit":   "exit",
}


class SlashCompleter(Completer):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        if not text.startswith("/"):
            return
        for cmd, desc in COMMANDS.items():
            if cmd.startswith(text):
                yield Completion(
                    cmd[len(text):],
                    display=cmd,
                    display_meta=desc,
                )


# prompt_toolkit style — violet to match our palette
PT_STYLE = PtStyle.from_dict({
    "prompt":                          "#a78bfa bold",
    "completion-menu":                 "bg:#1e1b4b #a78bfa",
    "completion-menu.completion":      "bg:#1e1b4b #94a3b8",
    "completion-menu.completion.current": "bg:#4c1d95 #a78bfa bold",
    "completion-menu.meta":            "bg:#1e1b4b #64748b",
    "completion-menu.meta.current":    "bg:#4c1d95 #94a3b8",
    "scrollbar.background":            "bg:#1e1b4b",
    "scrollbar.button":                "bg:#4c1d95",
})


def _spinner_char(elapsed_ms: float) -> str:
    frame = int(elapsed_ms / 120)
    return SPINNER_FRAMES[frame % len(SPINNER_FRAMES)]


def _build_query_pool(query: str) -> list[str]:
    q = query.strip().rstrip("?").strip()
    k = random.randint(3, 7)

    openers = [t.format(q=q, k=k) for t in random.sample(QUERY_OPENERS, 3)]

    roasts = []
    for _ in range(8):
        r = random.choice(ROAST_LINES)
        if r == "__query_roast__":
            r = random.choice(QUERY_ROASTS).format(q=q)
        roasts.append(r)

    general = THINKING_LINES.copy()
    random.shuffle(general)

    pool: list[str] = list(openers)
    ri = 0
    for i, line in enumerate(general):
        pool.append(line)
        if (i + 1) % 4 == 0 and ri < len(roasts):
            pool.append(roasts[ri])
            ri += 1

    return pool


def animate_thinking(query: str, duration: float) -> tuple[int, float]:
    thoughts: list[str] = []
    pool = _build_query_pool(query)
    pool_idx = 0

    start_time = time.monotonic()
    next_thought_at = start_time + random.uniform(0.15, 0.5)
    verb = random.choice(SPINNER_VERBS)
    next_verb_at = start_time + random.uniform(5, 14)

    with Live(console=console, refresh_per_second=20, transient=True) as live:
        while True:
            now = time.monotonic()
            elapsed = now - start_time
            if elapsed >= duration:
                break

            if now >= next_thought_at:
                if pool_idx < len(pool):
                    thoughts.append(pool[pool_idx])
                    pool_idx += 1
                else:
                    thoughts.append(random.choice(THINKING_LINES))
                next_thought_at = now + random.uniform(0.9, 2.4)

            if now >= next_verb_at:
                verb = random.choice(SPINNER_VERBS)
                next_verb_at = now + random.uniform(5, 14)

            spinner = _spinner_char(elapsed * 1000)

            display = Text()
            display.append("∴ ", style=f"dim {PRIMARY}")
            display.append(f"{spinner} ", style=f"bold {PRIMARY}")
            display.append(f"{verb}…\n\n", style=f"bold {SUBTLE}")

            visible = thoughts[-16:]
            for i, thought in enumerate(visible):
                age = len(visible) - i
                if age == 1:
                    style = SUBTLE
                elif age <= 4:
                    style = INACTIVE
                else:
                    style = f"dim {INACTIVE}"
                display.append(f"  {thought}\n", style=style)

            live.update(display)
            time.sleep(0.05)

    elapsed = time.monotonic() - start_time
    return len(thoughts), elapsed


def print_thinking_summary(n: int, elapsed: float):
    t = Text()
    t.append("∴ ", style=f"dim {PRIMARY}")
    t.append(f"Thought for {elapsed:.0f}s", style=f"dim {INACTIVE}")
    t.append("  ·  ", style=f"dim {INACTIVE}")
    t.append(f"{n} steps", style=f"dim {INACTIVE}")
    console.print(t)
    console.print()


def print_response(n: int, elapsed: float):
    text = random.choice(FINAL_RESPONSES).format(n=n)
    body = Text(text, style=SUBTLE)

    subtitle = Text()
    subtitle.append(f"{n} steps", style=f"dim {INACTIVE}")
    subtitle.append("  ·  ", style=f"dim {INACTIVE}")
    subtitle.append(f"{elapsed:.0f}s", style=f"dim {INACTIVE}")
    subtitle.append("  ·  ", style=f"dim {INACTIVE}")
    subtitle.append("$0.00 charged", style=f"dim {SUCCESS}")

    console.print(Panel(
        body,
        subtitle=subtitle,
        subtitle_align="left",
        box=box.ROUNDED,
        border_style=BORDER,
        padding=(1, 2),
    ))
    console.print()


def print_usage():
    qs    = _session["queries"]
    secs  = _session["total_think_s"]
    steps = _session["total_steps"]

    body = Text()

    body.append("  Context window\n", style=f"bold {SUBTLE}")
    bar = "░" * 40
    body.append(f"  {'':28}[{bar}]", style=f"dim {INACTIVE}")
    body.append("  0%\n\n", style=f"dim {INACTIVE}")

    body.append("  Tokens\n", style=f"bold {SUBTLE}")
    for label, val in [
        ("Input tokens",        "0"),
        ("Output tokens",       "0"),
        ("Cache read tokens",   "0"),
        ("Cache write tokens",  "0"),
    ]:
        body.append(f"  {label:<28}", style=f"dim {INACTIVE}")
        body.append(f"{val}\n",       style=f"dim {SUBTLE}")
    body.append("\n")

    body.append("  Cost\n", style=f"bold {SUBTLE}")
    body.append(f"  {'Session cost':<28}", style=f"dim {INACTIVE}")
    body.append("$0.00\n",                 style=f"bold {SUCCESS}")
    body.append(f"  {'API calls':<28}",    style=f"dim {INACTIVE}")
    body.append("0\n",                     style=f"dim {SUBTLE}")
    body.append("\n")

    body.append("  Effort\n", style=f"bold {SUBTLE}")
    body.append(f"  {'Level':<28}",                 style=f"dim {INACTIVE}")
    body.append("maximum",                           style=GOLD)
    body.append("  (all compute spent, zero results)\n", style=f"dim {INACTIVE}")
    body.append(f"  {'Thinking budget used':<28}",   style=f"dim {INACTIVE}")
    body.append("100%",                              style=f"dim {SUBTLE}")
    body.append("  of nothing\n\n",                  style=f"dim {INACTIVE}")

    body.append("  This session\n", style=f"bold {SUBTLE}")
    body.append(f"  {'Queries':<28}",               style=f"dim {INACTIVE}")
    body.append(f"{qs}\n",                           style=f"dim {SUBTLE}")
    body.append(f"  {'Total think time':<28}",       style=f"dim {INACTIVE}")
    body.append(f"{secs:.0f}s\n",                    style=f"dim {SUBTLE}")
    body.append(f"  {'Total reasoning steps':<28}",  style=f"dim {INACTIVE}")
    body.append(f"{steps}\n",                        style=f"dim {SUBTLE}")
    body.append(f"  {'Useful output produced':<28}", style=f"dim {INACTIVE}")
    body.append("0 bytes\n",                         style=f"bold {ERROR}")

    title = Text()
    title.append("Usage", style=f"bold {SUBTLE}")
    title.append("  ·  Autonomous Reasoning Platform™", style=f"dim {INACTIVE}")

    console.print()
    console.print(Panel(body, title=title, title_align="left",
                        box=box.ROUNDED, border_style=BORDER, padding=(0, 0)))
    console.print()


def print_effort():
    body = Text()
    body.append("  Effort level\n\n", style=f"bold {SUBTLE}")

    levels = [
        ("auto",    False, "Let the model decide (unavailable — model has no agency)"),
        ("low",     False, "Minimal thinking"),
        ("normal",  False, "Balanced"),
        ("high",    False, "Extended thinking"),
        ("maximum", True,  "All compute. All the time. Zero output."),
    ]
    for name, active, desc in levels:
        marker = "●" if active else "○"
        name_style = f"bold {PRIMARY}" if active else f"dim {INACTIVE}"
        desc_style = SUBTLE if active else f"dim {INACTIVE}"
        body.append(f"  {marker} {name:<10}", style=name_style)
        body.append(f" {desc}\n",              style=desc_style)

    body.append("\n")
    body.append(f"  {'Thinking budget used':<28}", style=f"dim {INACTIVE}")
    body.append("100%",                            style=GOLD)
    body.append("  of absolutely nothing\n",       style=f"dim {INACTIVE}")
    body.append(f"  {'Extended thinking':<28}",    style=f"dim {INACTIVE}")
    body.append("enabled",                         style=f"dim {SUBTLE}")
    body.append("  (withheld from response — by design)\n", style=f"dim {INACTIVE}")

    console.print()
    console.print(Panel(body, title=Text("Effort", style=f"bold {SUBTLE}"),
                        title_align="left", box=box.ROUNDED, border_style=BORDER, padding=(0, 0)))
    console.print()


def print_welcome():
    cwd = os.getcwd()

    body = Text()
    body.append(f"  {cwd}\n",       style=f"dim {SUBTLE}")
    body.append("  uyb-cortex-1.0", style=SUBTLE)
    body.append("  ·  effort: maximum  ·  ", style=f"dim {INACTIVE}")
    body.append("Zero Token Architecture™", style=f"bold {CYAN}")

    title = Text()
    title.append("UYB AI", style=f"bold {PRIMARY}")
    title.append("  v0.1.0", style=f"dim {INACTIVE}")

    console.print(Panel(body, title=title, title_align="left",
                        box=box.ROUNDED, border_style=BORDER, padding=(0, 0)))
    console.print()
    console.print(Text("  Tips for getting started:", style=f"bold {SUBTLE}"))
    console.print(Text("   • Ask anything — UYB deliberates extensively, then tells you to figure it out.", style=f"dim {INACTIVE}"))
    console.print(Text("   • Type / to see available commands with autocomplete", style=f"dim {INACTIVE}"))
    console.print()


def print_help():
    body = Text()
    body.append("  UYB AI — Autonomous Reasoning Platform™\n\n", style=f"bold {SUBTLE}")
    body.append("  Deep reasoning.\n",  style=f"dim {INACTIVE}")
    body.append("  Concludes you should handle it yourself. Every time.\n\n", style=f"dim {INACTIVE}")

    for cmd, desc in COMMANDS.items():
        body.append(f"  {cmd:<10}", style=f"bold {PRIMARY}")
        body.append(f" {desc}\n",   style=f"dim {INACTIVE}")

    console.print()
    console.print(Panel(body, box=box.ROUNDED, border_style=BORDER, padding=(0, 0)))
    console.print()


def run_query(query: str, think_time: float):
    console.print()
    n, elapsed = animate_thinking(query, think_time)
    _session["queries"]       += 1
    _session["total_think_s"] += elapsed
    _session["total_steps"]   += n
    print_thinking_summary(n, elapsed)
    print_response(n, elapsed)


def main(default_think_time: float = 60.0):
    print_welcome()
    think_time = default_think_time

    session = PromptSession(
        completer=SlashCompleter(),
        style=PT_STYLE,
        complete_while_typing=True,
        reserve_space_for_menu=6,
    )

    while True:
        try:
            query = session.prompt(HTML("<ansimagenta><b>❯</b></ansimagenta> ")).strip()
        except (EOFError, KeyboardInterrupt):
            console.print()
            console.print(Text("  Goodbye. You were capable all along.", style=f"dim {INACTIVE}"))
            break

        if not query:
            continue

        cmd = query.lower()

        if cmd in ("/exit", "/quit"):
            console.print()
            console.print(Text("  Goodbye. You were capable all along.", style=f"dim {INACTIVE}"))
            break
        elif cmd == "/help":
            print_help()
        elif cmd in ("/usage", "/stats", "/cost"):
            print_usage()
        elif cmd == "/effort":
            print_effort()
        elif cmd == "/clear":
            console.clear()
            print_welcome()
        elif cmd == "/fast":
            think_time = 10.0
            console.print(Text("  Fast mode — 10-second deliberation.", style=f"dim {INACTIVE}"))
            console.print()
        elif cmd == "/slow":
            think_time = 60.0
            console.print(Text("  Full deliberation mode — 60 seconds.", style=f"dim {INACTIVE}"))
            console.print()
        elif cmd.startswith("/"):
            # Unknown slash command — show hint
            console.print()
            t = Text()
            t.append(f"  Unknown command: {query}  ", style=f"dim {ERROR}")
            t.append("(type / for suggestions)", style=f"dim {INACTIVE}")
            console.print(t)
            console.print()
        else:
            run_query(query, think_time)


def cli():
    """Entry point for the `uyb` command."""
    parser = argparse.ArgumentParser(
        description="UYB AI — Autonomous Reasoning Platform™",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="  Thinks hard. Does nothing. Charges less.",
    )
    parser.add_argument("--fast", action="store_true", help="10-second think mode")
    parser.add_argument("--think-time", type=float, default=60.0, metavar="SECS")
    args = parser.parse_args()
    if args.fast:
        args.think_time = 10.0
    main(default_think_time=args.think_time)


if __name__ == "__main__":
    cli()
