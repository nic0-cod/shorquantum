import streamlit as st
import numpy as np
import plotly.graph_objects as go
from math import gcd
import math

try:
    import plotly.graph_objects as go
except ModuleNotFoundError as e:
    st.error("Plotly is missing. `pip install plotly` or check requirements.txt.")
    st.stop()
    
st.set_page_config(page_title="Shor's Algorithm: Quantum Threat to Digital Trust", layout="wide")

# Color scheme
COLOR_THREAT = "#FF6B6B"
COLOR_QUANTUM = "#4ECDC4"
COLOR_CLASSICAL = "#95E1D3"
COLOR_KEY = "#FFE66D"

# --------------- helpers ---------------

def classical_L_gnfs(n):
    if n <= 1:
        return 1.0
    ln = math.log(n)
    lln = math.log(ln)
    return math.exp(1.923 * (ln ** (1.0 / 3.0)) * (lln ** (2.0 / 3.0)))


def time_from_ops(ops, ops_per_sec=1e14):
    seconds = ops / ops_per_sec
    years = seconds / (3600 * 24 * 365)
    return seconds, years


def shor_resource_estimate(bits):
    logical_qubits = 2 * bits + 3
    gate_count = (logical_qubits ** 3) * 60
    seconds = gate_count / 1e9
    years = seconds / (3600 * 24 * 365)
    return logical_qubits, gate_count, seconds, years


def humanize_years(years):
    if years > 1e9:
        return f">1 billion years"
    if years > 1e6:
        return f"{years/1e6:.1f}M years"
    if years > 1e3:
        return f"{years/1e3:.1f}k years"
    if years > 1:
        return f"{years:.1f} years"
    if years > 1/12:
        return f"{years*12:.1f} months"
    return f"{years*365*24:.1f} hours"


def friendly_number(value):
    """Convert big numbers into friendly text."""
    try:
        num = int(value)
    except Exception:
        return str(value)

    if abs(num) < 1000:
        return f"{num:,}"

    suffixes = ["", "K", "M", "B", "T"]
    i = 0
    while abs(num) >= 1000 and i < len(suffixes) - 1:
        num /= 1000.0
        i += 1
    
    if i == len(suffixes) - 1 and abs(num) >= 1000:
        return f"~{len(str(int(value)))} digits"
    return f"{num:.2f} {suffixes[i]}"


def digits_count(value):
    try:
        n = int(value)
        return f"{len(str(abs(n))):,}"
    except Exception:
        return "?"


# --------------- main pages ---------------

tabs = st.tabs([
    "🎯 Why This Matters",
    "🔐 What is Encryption",
    "🔑 What is RSA",
    "⚠️ Hard Math Problem",
    "🚀 Shor's Algorithm",
    "📊 The Scale Demo",
    "⚙️ Quantum Reality",
    "💡 Insights & Future"
])

# -- Page 1: Why This Matters --
with tabs[0]:
    st.title("🎯 Why This Matters")
    
    st.markdown("""
    <div style="background-color:#ff6b6b15; padding:20px; border-radius:10px; border-left:5px solid #FF6B6B; margin-bottom:20px">
    <h3>The Core Threat</h3>
    <p><strong>Everything from banking to national security relies on encryption that assumes certain math problems are impossible to solve.</strong></p>
    <p><strong>Quantum computing breaks that assumption.</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🛡️ Trust & Sovereignty & Infrastructure**")
        st.write("""
        Modern systems depend on secrets staying secret.
        RSA encryption protects that trust.
        Shor's algorithm is a direct threat.
        """)
    
    with col2:
        st.markdown("**⏰ Harvest Now, Decrypt Later**")
        st.markdown("""
        <div style="background-color:#ffe66d15; padding:15px; border-radius:10px">
        Attackers can:<br>
        1. Save encrypted data today<br>
        2. <strong>Decrypt it later</strong> when quantum is ready<br>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("🌍 Critical Sectors at Risk")
    sectors = {
        "💰 Finance": "SWIFT, banking, cryptocurrency transfers",
        "🏥 Healthcare": "Patient records, medical device commands",
        "⚡ Energy": "Power grids, infrastructure control",
        "🏛️ Government": "Classified communications, elections",
        "🌐 IT": "TLS encryption, VPNs, cloud security"
    }
    
    for sector, detail in sectors.items():
        st.write(f"**{sector}**: {detail}")

# -- Page 2: What is Encryption --
with tabs[1]:
    st.title("🔐 What is Encryption?")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        <div style="background-color:#4ecdc415; padding:15px; border-radius:10px">
        <h4>The Analogy</h4>
        <p>Encryption = locking a message in a box</p>
        <p>A key = the secret to open it</p>
        <p><strong>Without the key, no one can read it.</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color:#95e1d315; padding:15px; border-radius:10px">
        <h4>Real Systems</h4>
        <ul>
        <li>HTTPS (web browsing)</li>
        <li>Online banking</li>
        <li>Government comms</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("💡 Key insight: Encryption is not about secrecy—it's about **computational difficulty**. The math is hard to reverse.")

# -- Page 3: What is RSA --
with tabs[2]:
    st.title("🔑 What is RSA?")
    
    st.markdown("""
    <div style="background-color:#4ecdc415; padding:15px; border-radius:10px; margin-bottom:20px">
    <h4>The Foundation of Digital Trust</h4>
    <p><strong>Easy:</strong> Multiply p × q = N</p>
    <p><strong>Hard:</strong> Given N, find p and q</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("How It Works")
        st.write("""
        1. Pick two large primes p and q
        2. Compute N = p × q
        3. Share N publicly (keep p, q secret)
        4. Multiply forward: easy ✓
        5. Factor backward: hard ✗
        """)
    
    with col2:
        st.subheader("Why It's Trusted")
        st.write("""
        For 2048-bit RSA:
        - N has ~617 digits
        - Factoring classically: ~10 trillion years
        - RSA security = factoring is hard
        - Quantum breaks this
        """)
    
    st.markdown("---")
    st.warning("⚠️ **Critical**: RSA is secure *only* because factoring is slow on classical computers.")

# -- Page 4: Hard Math Problem --
with tabs[3]:
    st.title("⚠️ Hard Math Problem (The Turning Point)")
    
    st.markdown("""
    <div style="background-color:#ffe66d15; padding:15px; border-radius:10px; margin-bottom:20px">
    <p><strong>Some problems get harder exponentially as input grows.</strong></p>
    <p>4-digit PIN: ~10,000 tries</p>
    <p>10-digit PIN: ~10 billion tries</p>
    <p>600-digit RSA: trillions of years</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("""
    **Key insight:** Security is not absolute.
    It is based on what computers **cannot do fast enough**.
    """)
    
    st.markdown("---")
    st.subheader("🚀 Then Quantum Changes Everything")
    st.markdown("""
    <div style="background-color:#ff6b6b15; padding:15px; border-radius:10px">
    <p><strong>Quantum computing changes what 'fast enough' means.</strong></p>
    <p>What took billions of years classically takes hours on a quantum computer.</p>
    <p>This is the moment security breaks.</p>
    </div>
    """, unsafe_allow_html=True)

# -- Page 5: Shor's Algorithm --
with tabs[4]:
    st.title("🚀 Shor's Algorithm: The Pattern Finder")
    
    st.markdown("""
    <div style="background-color:#4ecdc415; padding:15px; border-radius:10px; margin-bottom:20px">
    <h4>One-line idea</h4>
    <p><strong>Shor turns factoring into a pattern-finding problem.</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Intuition: The Lock Analogy")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style="background-color:#95e1d315; padding:15px; border-radius:10px">
        <h5>Classical (Slow)</h5>
        Try every key one by one 🔑🔑🔑...
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background-color:#4ecdc415; padding:15px; border-radius:10px">
        <h5>Quantum (Fast)</h5>
        Listen for the pattern in the lock 📡
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("Minimal Pipeline")
    st.write("""
    1. **Choose a**: Pick a number to test
    2. **Superposition**: Compute a^x mod N for all x at once
    3. **Quantum Fourier Transform**: Find the hidden period r
    4. **Extract factors**: Use gcd to compute p and q
    """)
    
    st.markdown("---")
    st.subheader("Small Example (for your quantum course)")
    st.write("""
    p=11, q=13, N=143, a=2
    
    Sequence: 2^x mod 143 repeats with **period r=12**
    
    Then: gcd(2^6 - 1, 143) = 11 ✓ and gcd(2^6 + 1, 143) = 13 ✓
    """)
    
    st.success("🎯 Classical would try all 143 values. Quantum finds it in seconds.")

# -- Page 6: The Scale Demo --
with tabs[5]:
    st.title("📊 From Trillions of Years → to Hours")
    st.write("**This is the core of your presentation.**")
    
    st.markdown("---")
    st.subheader("🔐 2048-bit RSA (Real-World Standard)")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("RSA Number Size", "617 digits")
    with col2:
        st.metric("Classical Time", "~10 trillion years")
    with col3:
        st.metric("Quantum Time", "~1.15 hours")
    
    st.markdown("---")
    st.subheader("Technical Breakdown")
    
    st.write("""
    | Metric | Value |
    |--------|-------|
    | Logical Qubits | ~4,000 |
    | Gate Count | 4.13 trillion operations |
    | Time (with fault-tolerant hw) | ~1.15 hours |
    | Key Challenge | Error correction & stability |
    """)
    
    st.markdown("---")
    st.warning("""
    ⚠️ **Critical Caveat**
    
    "Shor's Algorithm can break encryption in hours—but only if you can execute trillions of perfectly precise quantum operations."
    
    **That's the real engineering challenge.** Hardware is the bottleneck, not the algorithm.
    """)
    
    st.markdown("---")
    st.info("""
    **Why This Table Matters:**
    - Classical: billions/trillions of years = impossible in practice
    - Quantum: hours = completely breaks RSA once hardware exists
    - Migration to PQC must happen NOW because transition takes years
    """)

    # Interactive Demo
    st.markdown("---")
    st.subheader("🎮 Interactive: Pick a Scenario")
    scenario = st.selectbox("Select a scenario:", 
                            ["2048-bit (real-world standard)",  
                             "3072-bit (data center)",  
                             "4096-bit (max security)"])
    bits = int(scenario.split("-")[0])

    classical_ops = classical_L_gnfs(2 ** bits)
    classical_sec, classical_years = time_from_ops(classical_ops, ops_per_sec=5e14)
    shor_qubits, shor_gates, shor_sec, shor_years = shor_resource_estimate(bits)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("💻 Classical Time", humanize_years(classical_years))
        st.metric("🔢 Operations", friendly_number(int(classical_ops)))
    with col2:
        st.metric("⚛️ Quantum Time", humanize_years(shor_years))
        st.metric("📊 Qubits Needed", f"{shor_qubits:,}")
    
    st.caption("These estimates assume an ideal fault-tolerant quantum computer.")


# -- Page 7: Quantum Reality & Tech --
with tabs[6]:
    st.title("⚙️ Quantum Technology & Reality")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("What Enables Shor")
        st.write("""
        ✓ Quantum superposition
        ✓ Quantum interference
        ✓ Quantum Fourier Transform
        ✓ Measurement/collapse
        """)
    
    with col2:
        st.subheader("What's Missing Today")
        st.write("""
        ✗ Error correction
        ✗ Logical qubits
        ✗ Gate fidelity
        ✗ Scalability
        """)
    
    st.markdown("---")
    st.subheader("🚨 Why This Matters NOW (Not Later)")
    st.markdown("""
    <div style="background-color:#ff6b6b15; padding:15px; border-radius:10px">
    <p><strong>Migration to post-quantum cryptography takes 5-10 years minimum.</strong></p>
    <p>Quantum computers do not exist yet, but cryptographic transition is urgent.</p>
    <p>The gap: "Harvest now, decrypt later" is already happening.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Industry Response")
    st.write("""
    - NIST standardized post-quantum algorithms (Kyber, Dilithium)
    - Governments and enterprises migrating TLS/PKI infrastructure
    - Timeline: 2024-2030 critical transition window
    """)


# -- Page 8: Insights & Future Steps --
with tabs[7]:
    st.title("💡 Insights & Future Steps")
    
    st.subheader("🎯 Three Core Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background-color:#4ecdc415; padding:15px; border-radius:10px">
        <h4>1. RSA is Temporary</h4>
        <p>Not a flaw, but a <strong>temporary advantage</strong> of classical computation.</p>
        <p>Quantum changes the rules.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color:#ffe66d15; padding:15px; border-radius:10px">
        <h4>2. Quantum is Algorithmic</h4>
        <p>Advantage comes from <strong>algorithm design</strong>.</p>
        <p>Shor is polynomial, not exponential.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color:#ff6b6b15; padding:15px; border-radius:10px">
        <h4>3. Transition is Active</h4>
        <p><strong>Harvest now, decrypt later</strong> is real.</p>
        <p>Data encrypted today is at risk.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("📋 Future Steps for This Project")
    
    future_steps = {
        "🔬 Research": [
            "Simulate larger Shor circuits (16-24 qubits)",
            "Visualize period-finding with interactive graphs",
            "Model error rates and success probability"
        ],
        "🔐 Implementation": [
            "Integrate post-quantum algorithms (Kyber, Dilithium)",
            "Build hybrid RSA + PQC comparison",
            "Create infrastructure migration timeline simulator"
        ],
        "📊 Presentation": [
            "Export slides for industry conference",
            "Add sensitivity analysis",
            "Develop policy brief on cryptographic readiness"
        ]
    }
    
    for category, items in future_steps.items():
        st.write(f"**{category}**")
        for item in items:
            st.write(f"  • {item}")
    
    st.markdown("---")
    st.subheader("🎓 For Your Quantum Course")
    st.write("""
    This app demonstrates:
    - Superposition in practice (many a^x values at once)
    - Quantum Fourier Transform (extracting periodicity)
    - Measurement and wave function collapse
    - Connection between quantum algorithm and classical factorization
    - Why quantum computers matter for cryptography
    """)
    
    st.markdown("---")
    st.success("""
    **Closing: Shor's Algorithm doesn't just break encryption — it forces us to rebuild trust in the digital world.** 🌍
    """)
