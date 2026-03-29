import streamlit as st
import numpy as np
import plotly.graph_objects as go
from math import gcd
import math
import random

# Configuration de la page
st.set_page_config(page_title="Algorithme de Shor : Menace sur la Confiance Numérique", layout="wide")

# Schéma de couleurs
COLOR_THREAT = "#FF6B6B"
COLOR_QUANTUM = "#4ECDC4"
COLOR_CLASSICAL = "#95E1D3"
COLOR_KEY = "#FFE66D"

# --------------- Fonctions de calcul (Helpers) ---------------

def classical_L_gnfs(n):
    """Estimation de la complexité de l'algorithme GNFS (classique)."""
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
    """Estimation des ressources pour Shor (qubits logiques)."""
    logical_qubits = 2 * bits + 3
    gate_count = (logical_qubits ** 3) * 60
    seconds = gate_count / 1e9  # Hypothèse d'une horloge à 1GHz
    years = seconds / (3600 * 24 * 365)
    return logical_qubits, gate_count, seconds, years


def humanize_years(years):
    if years > 1e9:
        return f">1 milliard d'années"
    if years > 1e6:
        return f"{years/1e6:.1f}M d'années"
    if years > 1e3:
        return f"{years/1e3:.1f}k années"
    if years > 1:
        return f"{years:.1f} ans"
    if years > 1 / 12:
        return f"{years*12:.1f} mois"
    return f"{years*365*24:.1f} heures"


def friendly_number(value):
    try:
        num = int(value)
    except:
        return str(value)
    if abs(num) < 1000:
        return f"{num:,}"
    suffixes = ["", "K", "M", "Mrd", "B"]
    i = 0
    while abs(num) >= 1000 and i < len(suffixes) - 1:
        num /= 1000.0
        i += 1
    return f"{num:.2f} {suffixes[i]}"


def is_coprime(a, N):
    return gcd(a, N) == 1


def find_period(a, N, max_x=1000):
    x = 1
    val = a % N
    while x <= max_x:
        if val == 1:
            return x
        x += 1
        val = (val * a) % N
    return None


def shor_factorization_demo(N, a):
    if not is_coprime(a, N):
        return None, None, "a n'est pas premier avec N"

    r = find_period(a, N)
    if r is None or r % 2 != 0:
        return None, None, "Période invalide (impair ou introuvable)"

    p = gcd(pow(a, r // 2, N) - 1, N)
    q = gcd(pow(a, r // 2, N) + 1, N)
    if p in (1, N) or q in (1, N):
        return None, None, "Facteurs triviaux obtenus"

    if p * q != N:
        return None, None, "Échec de la factorisation"

    return int(p), int(q), f"Succès : période r={r}"


def plot_periodicity(a, N, x_max=20):
    x = np.arange(1, x_max + 1)
    y = [(int(a) ** int(i)) % N for i in x]
    r = find_period(a, N, max_x=x_max)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode='lines+markers',
            name=f'f(x)= {a}^x mod {N}',
            line=dict(color=COLOR_QUANTUM, width=3),
            marker=dict(size=8),
        )
    )

    if r is not None:
        for k in range(1, int(x_max / r) + 1):
            fig.add_vline(x=k * r, line_dash='dot', line_color=COLOR_KEY, opacity=0.6,
                          annotation_text=f'r={r}', annotation_position='top right')

    fig.update_layout(
        title=f"Motif périodique : f(x) = {a}^x mod {N} (période r={r if r else 'non trouvé'})",
        xaxis_title="x (pas)",
        yaxis_title="f(x)",
        template="plotly_dark",
        height=340,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig


# --------------- Structure principale ---------------

tabs = st.tabs([
    "🎯 Enjeux",
    "🔐 Chiffrement",
    "🔑 Le système RSA",
    "⚠️ Complexité",
    "🚀 Algorithme de Shor",
    "📊 Démo d'Échelle",
    "🧪 Simulations",
    "⚙️ Réalité Quantique",
    "💡 Futur",
])

# -- Page 1: Pourquoi c'est important --
with tabs[0]:
    st.title("🎯 Pourquoi est-ce crucial ?")
    st.markdown(
        f"""
    <div style="background-color:{COLOR_THREAT}15; padding:20px; border-radius:10px; border-left:5px solid {COLOR_THREAT}; margin-bottom:20px">
    <h3>La Menace Fondamentale</h3>
    <p><strong>Nos banques et notre sécurité nationale reposent sur l'hypothèse que certains problèmes mathématiques sont impossibles à résoudre rapidement.</strong></p>
    <p><strong>L'informatique quantique brise cette hypothèse.</strong></p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🛡️ Souveraineté et Infrastructure**")
        st.write("Le chiffrement RSA protège nos secrets. L'algorithme de Shor est une attaque directe contre ce pilier.")

    with col2:
        st.markdown("**⏰ Récolter maintenant, décrypter plus tard**")
        st.markdown(
            f"""
        <div style="background-color:{COLOR_KEY}15; padding:15px; border-radius:10px">
        Les attaquants peuvent :<br>
        1. Stocker des données chiffrées aujourd'hui<br>
        2. <strong>Les décrypter plus tard</strong> dès que l'ordinateur quantique sera prêt.
        </div>
        """,
            unsafe_allow_html=True,
        )

# -- Page 2: Qu'est-ce que le chiffrement --
with tabs[1]:
    st.title("🔐 Qu'est-ce que le chiffrement ?")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
        <div style="background-color:{COLOR_QUANTUM}15; padding:15px; border-radius:10px">
        <h4>L'Analogie</h4>
        <p>Chiffrer = Verrouiller un message dans un coffre-fort.</p>
        <p>Une clé = Le secret unique pour l'ouvrir.</p>
        <p><strong>Sans la clé, le contenu est illisible.</strong></p>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col2:
        st.info(
            "💡 Le chiffrement n'est pas une question de magie, mais de **difficulté computationnelle**. Les mathématiques sont faciles dans un sens, mais quasi-impossibles à inverser."
        )

# -- Page 3: Le système RSA --
with tabs[2]:
    st.title("🔑 Le système RSA")
    st.markdown("Le standard RSA repose sur la multiplication de nombres premiers.")
    st.latex(r"p \times q = N")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Le principe")
        st.write(
            """
        1. Choisir deux grands nombres premiers **p** et **q**.
        2. Calculer **N = p × q**.
        3. Diffuser **N** publiquement.
        4. Garder **p** et **q** secrets (la clé privée).
        """
        )
    with col2:
        st.subheader("La sécurité")
        st.write(
            """
        Pour un RSA de 2048 bits :
        - **N** possède environ 617 chiffres.
        - Factoriser **N** avec un supercalculateur classique prendrait des **trillions d'années**.
        """
        )

# -- Page 4: Complexité mathématique --
with tabs[3]:
    st.title("⚠️ Le mur de la complexité")
    st.write("La sécurité actuelle repose sur la croissance **exponentielle** du temps de calcul.")

    st.markdown(
        f"""
    <div style="background-color:{COLOR_KEY}15; padding:15px; border-radius:10px">
    <p>PIN à 4 chiffres : 10 000 essais</p>
    <p>PIN à 10 chiffres : 10 milliards d'essais</p>
    <p>RSA-2048 : Plus de temps que l'âge de l'univers</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.subheader("🚀 Le changement de paradigme quantique")
    st.warning(
        "L'informatique quantique transforme un problème exponentiel en un problème **polynomial**. Ce qui prenait des millénaires ne prend plus que quelques heures."
    )

# -- Page 5: Algorithme de Shor --
with tabs[4]:
    st.title("🚀 L'Algorithme de Shor : Le détecteur de motifs")
    st.markdown("Shor transforme la factorisation en un problème de **recherche de période**.")

    st.subheader("Visualisation de la Périodicité")
    col1, col2 = st.columns([2, 3])
    with col1:
        N_period = st.selectbox("Choisir N (semi-premier)", [15, 21, 35, 77, 143, 221, 391], index=0)
        a_period = st.selectbox("Choisir a (coprime avec N)", [x for x in range(2, N_period) if is_coprime(x, N_period)], index=0)
        x_max = st.slider("Longueur de la séquence (x max)", min_value=8, max_value=50, value=20)

    with col2:
        fig_period = plot_periodicity(a=a_period, N=N_period, x_max=x_max)
        st.plotly_chart(fig_period, use_container_width=True)

    r = find_period(a_period, N_period, max_x=x_max)
    if r is not None:
        st.success(f"Période détectée : r = {r} (pour N={N_period}, a={a_period})")
    else:
        st.warning(f"Période non trouvée dans x<= {x_max}. Essayez d'augmenter x_max ou de changer 'a'.")

    st.markdown("**Table de valeurs**")
    coeffs = [(x, (a_period**x) % N_period) for x in range(1, x_max + 1)]
    st.table([{"x": x, "f(x)": y} for x, y in coeffs])

    st.markdown("---")
    st.subheader("Le Pipeline Quantique")
    st.write(
        """
    1. **Superposition** : Calculer toutes les valeurs de $a^x \pmod N$ simultanément.
    2. **Transformation de Fourier Quantique (TFQ)** : Extraire la fréquence (la période $r$) par interférence.
    3. **Extraction** : Utiliser le PGCD classique pour trouver les facteurs à partir de $r$.
    """
    )

# -- Page 6: Démo d'Échelle --
with tabs[5]:
    st.title("📊 Comparaison : Classique vs Quantique")

    scenario = st.selectbox(
        "Sélectionnez un scénario :",
        ["RSA-2048 (Standard actuel)", "RSA-3072 (Haute sécurité)", "RSA-4096 (Maximum)"]
    )
    bits = int(scenario.split("-")[1].split(" ")[0])

    classical_ops = classical_L_gnfs(2 ** bits)
    _, classical_years = time_from_ops(classical_ops)
    shor_qubits, _, _, shor_years = shor_resource_estimate(bits)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("💻 Temps Classique", humanize_years(classical_years))
        st.write(f"Opérations : {friendly_number(classical_ops)}")
    with col2:
        st.metric("⚛️ Temps Quantique", humanize_years(shor_years))
        st.write(f"Qubits Logiques nécessaires : {shor_qubits:,}")

    st.warning("⚠️ Note : Ces calculs supposent un ordinateur quantique parfait (tolérant aux fautes).")

# -- Page 7: Simulations --
with tabs[6]:
    st.title("🧪 Simulations de Factorisation")

    st.markdown("### 7.1. Simulation de Shor étape par étape")
    N = st.selectbox("Choisir N (semi-premier)", [15, 21, 35, 77, 143, 221, 391])
    a = st.number_input("Choisir a (1 < a < N)", min_value=2, max_value=N-1, value=2)

    if st.button("Lancer la démo de Shor"):
        p, q, message = shor_factorization_demo(N, a)
        st.info(message)
        if p and q:
            st.success(f"Facteurs trouvés : p={p}, q={q}")
        else:
            st.error("Échec de la démo sur ce couple (N,a). Essayez un autre 'a'.")

    st.markdown("---")
    st.markdown("### 7.2. Collection de simulations")

    results = []
    for N_test in [15, 21, 35, 77, 143, 221, 391]:
        a_test = random.choice([x for x in range(2, N_test) if is_coprime(x, N_test)])
        p_test, q_test, msg = shor_factorization_demo(N_test, a_test)
        results.append({"N": N_test, "a": a_test, "p": p_test or "??", "q": q_test or "??", "statut": msg})

    import pandas as pd

    df_sim = pd.DataFrame(results)
    st.table(df_sim)

    st.markdown("---")
    st.markdown("### 7.3. Échelle : croissance de la complexité")
    bit_ranges = [512, 1024, 2048, 3072, 4096]
    costs = [classical_L_gnfs(2 ** b) for b in bit_ranges]
    years = [time_from_ops(c)[1] for c in costs]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=[str(b) for b in bit_ranges], y=years, name='Temps GNFS (années)', marker_color=COLOR_CLASSICAL))
    fig.update_layout(title="Croissance du temps classique selon la taille RSA", yaxis_type='log', template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

# -- Page 8: Réalité Technologique --
with tabs[7]:
    st.title("⚙️ État de l'Art et Réalité")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Ce qui rend Shor possible")
        st.write("- Superposition\n- Interférence quantique\n- TFQ")
    with col2:
        st.subheader("Les défis actuels")
        st.write("- Taux d'erreur élevé\n- Décohérence\n- Besoin de millions de qubits physiques pour quelques qubits logiques")

    st.markdown(
        f"""
    <div style="background-color:{COLOR_THREAT}15; padding:15px; border-radius:10px">
    <strong>Urgence :</strong> La migration vers la cryptographie post-quantique (CPQ) prend 5 à 10 ans. Il faut agir maintenant.
    </div>
    """,
        unsafe_allow_html=True,
    )

# -- Page 9: Insights et Futur --
with tabs[8]:
    st.title("💡 Perspectives")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**1. RSA est temporaire**\nCe n'est pas une faille, mais une limite de la physique classique.")
    with col2:
        st.markdown("**2. Avantage Algorithmique**\nLe gain vient de la structure de l'algorithme, pas seulement de la puissance brute.")
    with col3:
        st.markdown("**3. Transition Active**\nLe NIST standardise déjà de nouveaux algorithmes (ex: Kyber) résistants aux ordinateurs quantiques.")

    st.success("Conclusion : L'algorithme de Shor ne fait pas que briser le chiffrement — il nous force à réinventer la confiance numérique pour l'ère quantique. 🌍")

# Footer
st.markdown("---")
st.caption("Démo interactive réalisée pour votre cours de calcul quantique.")
