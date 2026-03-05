import streamlit as st
import pandas as pd
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="Fertilisation Agroécologique",
    page_icon="🌱",
    layout="wide"
)

# Sidebar avec logo et université
with st.sidebar:
    try:
        # Affiche le logo s'il est présent dans le même dossier (logo.jpg)
        st.image("images.jpg", width=120)
    except:
        # Si le logo n'est pas trouvé, on affiche un emoji en remplacement
        st.markdown("# 🌿")
    st.markdown("### UNIVERSITE DE L'ITASY")
    st.markdown("---")
    
    st.header("📋 Navigation")
    page = st.radio(
        "Choisissez une page :",
        ["Assistant de fertilisation", "Catalogue des cultures", "Catalogue des fertilisants", "Calculateur personnalisé"]
    )
    
    st.markdown("---")
    st.header("⚙️ Paramètres")
    surface = st.number_input("Surface à cultiver (m²)", min_value=1, max_value=10000, value=100, step=10)
    unite_surface = "m²"

# Titre principal (plus petit)
st.markdown("<h1 style='text-align: center; font-size: 2em;'>🌱 AGRICULTURE ECOLOGIQUE</h1>", unsafe_allow_html=True)
st.markdown("---")

# Dictionnaire des besoins NPK (kg/100m² ou kg/arbre/pied)
cultures_npk = {
    "Tomate": {"N": 1.5, "P": 1.0, "K": 2.2, "unite": "kg/100m²"},
    "Pomme de terre": {"N": 1.5, "P": 1.0, "K": 2.5, "unite": "kg/100m²"},
    "Carotte": {"N": 1.0, "P": 0.8, "K": 1.8, "unite": "kg/100m²"},
    "Laitue (salade)": {"N": 1.0, "P": 0.6, "K": 1.4, "unite": "kg/100m²"},
    "Courgette": {"N": 1.2, "P": 0.8, "K": 1.8, "unite": "kg/100m²"},
    "Fraise": {"N": 1.0, "P": 0.8, "K": 1.6, "unite": "kg/100m²"},
    "Oignon": {"N": 1.0, "P": 0.7, "K": 1.5, "unite": "kg/100m²"},
    "Ail": {"N": 1.0, "P": 0.7, "K": 1.5, "unite": "kg/100m²"},
    "Haricot vert": {"N": 0.5, "P": 0.6, "K": 1.2, "unite": "kg/100m²"},
    "Pois potager": {"N": 0.3, "P": 0.6, "K": 1.1, "unite": "kg/100m²"},
    "Aubergine": {"N": 1.4, "P": 0.9, "K": 2.0, "unite": "kg/100m²"},
    "Poivron": {"N": 1.3, "P": 0.9, "K": 1.9, "unite": "kg/100m²"},
    "Concombre": {"N": 1.2, "P": 0.8, "K": 1.8, "unite": "kg/100m²"},
    "Betterave": {"N": 1.2, "P": 0.8, "K": 2.0, "unite": "kg/100m²"},
    "Chou-fleur": {"N": 2.0, "P": 1.0, "K": 2.2, "unite": "kg/100m²"},
    "Brocoli": {"N": 1.7, "P": 0.9, "K": 1.8, "unite": "kg/100m²"},
    "Épinard": {"N": 1.2, "P": 0.8, "K": 1.8, "unite": "kg/100m²"},
    "Poireau": {"N": 1.4, "P": 0.8, "K": 1.8, "unite": "kg/100m²"},
    "Melon": {"N": 1.0, "P": 0.8, "K": 1.7, "unite": "kg/100m²"},
    "Pommier": {"N": 0.8, "P": 0.4, "K": 1.2, "unite": "kg/arbre"},
    "Poirier": {"N": 0.8, "P": 0.4, "K": 1.2, "unite": "kg/arbre"},
    "Pêcher": {"N": 0.9, "P": 0.5, "K": 1.5, "unite": "kg/arbre"},
    "Abricotier": {"N": 0.7, "P": 0.4, "K": 1.0, "unite": "kg/arbre"},
    "Cerisier": {"N": 0.6, "P": 0.3, "K": 0.9, "unite": "kg/arbre"},
    "Prunier": {"N": 0.6, "P": 0.3, "K": 0.9, "unite": "kg/arbre"},
    "Olivier": {"N": 0.5, "P": 0.3, "K": 0.8, "unite": "kg/arbre"},
    "Oranger": {"N": 0.8, "P": 0.4, "K": 1.2, "unite": "kg/arbre"},
    "Citronnier": {"N": 0.7, "P": 0.3, "K": 1.0, "unite": "kg/arbre"},
    "Noyer": {"N": 0.8, "P": 0.4, "K": 1.1, "unite": "kg/arbre"},
    "Noisetier": {"N": 0.6, "P": 0.3, "K": 0.8, "unite": "kg/arbre"},
    "Amandier": {"N": 0.6, "P": 0.3, "K": 0.9, "unite": "kg/arbre"},
    "Figuier": {"N": 0.5, "P": 0.2, "K": 0.8, "unite": "kg/arbre"},
    "Kiwi": {"N": 0.9, "P": 0.5, "K": 1.5, "unite": "kg/arbre"},
    "Vigne": {"N": 0.5, "P": 0.3, "K": 1.0, "unite": "kg/pied"},
    "Blé": {"N": 1.8, "P": 1.0, "K": 1.2, "unite": "kg/100m²"},
    "Maïs": {"N": 2.0, "P": 0.9, "K": 1.5, "unite": "kg/100m²"},
    "Riz": {"N": 1.2, "P": 0.6, "K": 1.0, "unite": "kg/100m²"},
}

# Dictionnaire des fertilisants avec leurs teneurs NPK (%)
fertilisants = {
    "Compost maison": {"N": 1.5, "P": 0.8, "K": 1.5, "type": "amendement", "rapidite": "lente"},
    "Lombricompost": {"N": 1.8, "P": 1.0, "K": 1.0, "type": "amendement", "rapidite": "moyenne"},
    "Fumier bovin composté": {"N": 1.5, "P": 0.8, "K": 2.5, "type": "fond", "rapidite": "lente"},
    "Fiente de volaille": {"N": 5.0, "P": 4.0, "K": 2.5, "type": "coup de pouce", "rapidite": "rapide", "attention": "risque de brûlure"},
    "Fumier de porc composté": {"N": 1.2, "P": 0.8, "K": 1.2, "type": "fond", "rapidite": "lente"},
    "Fumier de cheval composté": {"N": 1.5, "P": 0.8, "K": 2.0, "type": "fond", "rapidite": "lente"},
    "Fumier de lapin": {"N": 2.5, "P": 2.0, "K": 2.0, "type": "fond", "rapidite": "moyenne"},
    "Tithonia frais": {"N": 2.5, "P": 0.5, "K": 4.0, "type": "coup de pouce", "rapidite": "rapide"},
    "Purin d'orties": {"N": 0.2, "P": 0.05, "K": 0.3, "type": "purin", "rapidite": "très rapide", "usage": "foliaire/arrosage"},
    "Purin de consoude": {"N": 0.2, "P": 0.05, "K": 0.6, "type": "purin", "rapidite": "très rapide", "usage": "foliaire/arrosage"},
    "Cendre de bois": {"N": 0.0, "P": 1.5, "K": 7.0, "type": "coup de pouce", "rapidite": "rapide", "attention": "ne pas mélanger avec fumier frais"},
    "Poudre d'os": {"N": 3.0, "P": 20.0, "K": 0.0, "type": "coup de pouce", "rapidite": "lente"},
    "Poudre de poisson": {"N": 9.0, "P": 6.5, "K": 1.5, "type": "coup de pouce", "rapidite": "rapide"},
}

# Formules pré-définies (pour le plan standard)
formules_recommandees = {
    "Tomate": {
        "nom": "Formule Tomate équilibrée",
        "fond": ["Fumier bovin composté"],
        "coup_de_pouce": ["Cendre de bois", "Purin de consoude"],
        "quantites_fond": [15],
        "quantites_coup_de_pouce": [1.0, "pulvérisation"]
    },
    "Pomme de terre": {
        "nom": "Formule Pomme de terre",
        "fond": ["Fumier de cheval composté"],
        "coup_de_pouce": ["Cendre de bois", "Poudre de poisson"],
        "quantites_fond": [20],
        "quantites_coup_de_pouce": [1.5, 0.3]
    },
    "Carotte": {
        "nom": "Formule Carotte (racines)",
        "fond": ["Compost maison"],
        "coup_de_pouce": ["Cendre de bois", "Poudre d'os"],
        "quantites_fond": [10],
        "quantites_coup_de_pouce": [0.8, 0.3]
    },
    "Laitue (salade)": {
        "nom": "Formule Salade",
        "fond": ["Lombricompost"],
        "coup_de_pouce": ["Purin d'orties"],
        "quantites_fond": [5],
        "quantites_coup_de_pouce": ["arrosage"]
    },
    "Courgette": {
        "nom": "Formule Courgette gourmande",
        "fond": ["Compost maison", "Fiente de volaille"],
        "coup_de_pouce": ["Purin de consoude"],
        "quantites_fond": [10, 2],
        "quantites_coup_de_pouce": ["arrosage"]
    },
    "Fraise": {
        "nom": "Formule Fraises sucrées",
        "fond": ["Fumier de lapin"],
        "coup_de_pouce": ["Cendre de bois", "Purin d'orties + consoude"],
        "quantites_fond": [5],
        "quantites_coup_de_pouce": [0.5, "pulvérisation"]
    },
    "Oignon": {
        "nom": "Formule Oignon/Ail",
        "fond": ["Compost maison"],
        "coup_de_pouce": ["Cendre de bois", "Poudre d'os"],
        "quantites_fond": [8],
        "quantites_coup_de_pouce": [0.7, 0.2]
    },
    "Haricot vert": {
        "nom": "Formule Haricot (peu d'azote)",
        "fond": ["Compost maison"],
        "coup_de_pouce": ["Cendre de bois"],
        "quantites_fond": [5],
        "quantites_coup_de_pouce": [0.5]
    },
    "Pommier": {
        "nom": "Formule Arbre fruitier (pommier)",
        "fond": ["Fumier bovin composté"],
        "coup_de_pouce": ["Cendre de bois", "Poudre d'os", "Purin de consoude"],
        "quantites_fond": [4],
        "quantites_coup_de_pouce": [0.2, 0.1, "arrosage"]
    },
    "Poirier": {
        "nom": "Formule Poirier",
        "fond": ["Fumier bovin composté"],
        "coup_de_pouce": ["Cendre de bois", "Poudre d'os", "Purin de consoude"],
        "quantites_fond": [4],
        "quantites_coup_de_pouce": [0.2, 0.1, "arrosage"]
    },
    "Pêcher": {
        "nom": "Formule Pêcher",
        "fond": ["Fumier bovin composté"],
        "coup_de_pouce": ["Cendre de bois", "Poudre d'os", "Purin de consoude"],
        "quantites_fond": [4],
        "quantites_coup_de_pouce": [0.2, 0.1, "arrosage"]
    },
    "Vigne": {
        "nom": "Formule Vigne",
        "fond": ["Fumier de cheval composté"],
        "coup_de_pouce": ["Cendre de bois", "Purin d'orties"],
        "quantites_fond": [2.5],
        "quantites_coup_de_pouce": [0.15, "pulvérisation"]
    },
    "Blé": {
        "nom": "Formule Céréale",
        "fond": ["Fumier bovin composté"],
        "coup_de_pouce": ["Poudre d'os"],
        "quantites_fond": [15],
        "quantites_coup_de_pouce": [0.5]
    },
    "Maïs": {
        "nom": "Formule Maïs",
        "fond": ["Fumier bovin composté", "Fiente de volaille"],
        "coup_de_pouce": ["Poudre de poisson"],
        "quantites_fond": [18, 3],
        "quantites_coup_de_pouce": [0.4]
    },
    "Riz": {
        "nom": "Formule Riz (culture inondée)",
        "fond": ["Fumier bovin composté"],
        "coup_de_pouce": ["Poudre de poisson"],
        "quantites_fond": [15],
        "quantites_coup_de_pouce": [0.5]
    },
    "Abricotier": {
        "nom": "Formule Abricotier",
        "fond": ["Fumier bovin composté"],
        "coup_de_pouce": ["Cendre de bois", "Poudre d'os", "Purin de consoude"],
        "quantites_fond": [4],
        "quantites_coup_de_pouce": [0.2, 0.1, "arrosage"]
    },
    "Cerisier": {
        "nom": "Formule Cerisier",
        "fond": ["Fumier bovin composté"],
        "coup_de_pouce": ["Cendre de bois", "Poudre d'os", "Purin d'orties"],
        "quantites_fond": [4],
        "quantites_coup_de_pouce": [0.15, 0.1, "pulvérisation"]
    },
    "Prunier": {
        "nom": "Formule Prunier",
        "fond": ["Fumier bovin composté"],
        "coup_de_pouce": ["Cendre de bois", "Poudre d'os"],
        "quantites_fond": [4],
        "quantites_coup_de_pouce": [0.15, 0.1]
    },
    "Olivier": {
        "nom": "Formule Olivier",
        "fond": ["Fumier bovin composté"],
        "coup_de_pouce": ["Cendre de bois", "Purin de consoude"],
        "quantites_fond": [3],
        "quantites_coup_de_pouce": [0.2, "arrosage"]
    },
    "Oranger": {
        "nom": "Formule Agrumes",
        "fond": ["Fumier bovin composté"],
        "coup_de_pouce": ["Cendre de bois", "Poudre d'os", "Purin de consoude"],
        "quantites_fond": [5],
        "quantites_coup_de_pouce": [0.3, 0.15, "arrosage"]
    },
    "Citronnier": {
        "nom": "Formule Citronnier",
        "fond": ["Fumier bovin composté"],
        "coup_de_pouce": ["Cendre de bois", "Poudre d'os"],
        "quantites_fond": [4],
        "quantites_coup_de_pouce": [0.2, 0.1]
    },
    "Noyer": {
        "nom": "Formule Noyer",
        "fond": ["Fumier bovin composté"],
        "coup_de_pouce": ["Cendre de bois", "Poudre d'os"],
        "quantites_fond": [5],
        "quantites_coup_de_pouce": [0.2, 0.15]
    },
    "Noisetier": {
        "nom": "Formule Noisetier",
        "fond": ["Fumier bovin composté"],
        "coup_de_pouce": ["Cendre de bois"],
        "quantites_fond": [3],
        "quantites_coup_de_pouce": [0.15]
    },
    "Amandier": {
        "nom": "Formule Amandier",
        "fond": ["Fumier bovin composté"],
        "coup_de_pouce": ["Cendre de bois", "Poudre d'os"],
        "quantites_fond": [3],
        "quantites_coup_de_pouce": [0.15, 0.1]
    },
    "Figuier": {
        "nom": "Formule Figuier",
        "fond": ["Compost maison"],
        "coup_de_pouce": ["Cendre de bois"],
        "quantites_fond": [3],
        "quantites_coup_de_pouce": [0.1]
    },
    "Kiwi": {
        "nom": "Formule Kiwi",
        "fond": ["Fumier bovin composté"],
        "coup_de_pouce": ["Cendre de bois", "Poudre d'os", "Purin de consoude"],
        "quantites_fond": [5],
        "quantites_coup_de_pouce": [0.3, 0.15, "arrosage"]
    },
}

# ------------------------------------------------------------
# PAGE ASSISTANT DE FERTILISATION
# ------------------------------------------------------------
if page == "Assistant de fertilisation":
    st.header("🌿 Assistant de fertilisation")
    st.markdown("Sélectionnez votre culture et obtenez un plan de fertilisation personnalisé, ou indiquez un fertilisant que vous possédez pour combler les manques.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        culture_choisie = st.selectbox("Choisissez une culture :", sorted(cultures_npk.keys()))
        
        if culture_choisie:
            st.subheader(f"📊 Besoins NPK pour {culture_choisie}")
            besoins = cultures_npk[culture_choisie]
            
            # Facteur multiplicateur
            if "arbre" in besoins["unite"]:
                nb_pieds = st.number_input("Nombre d'arbres :", min_value=1, value=1, step=1, key="nb_arbres_assist")
                facteur = nb_pieds
                unite_affichage = f"pour {nb_pieds} arbre(s)"
            elif "pied" in besoins["unite"]:
                nb_pieds = st.number_input("Nombre de pieds :", min_value=1, value=1, step=1, key="nb_pieds_assist")
                facteur = nb_pieds
                unite_affichage = f"pour {nb_pieds} pied(s)"
            else:
                facteur = surface / 100
                unite_affichage = f"pour {surface} {unite_surface}"
            
            besoins_total = {
                "N": round(besoins["N"] * facteur, 2),
                "P": round(besoins["P"] * facteur, 2),
                "K": round(besoins["K"] * facteur, 2)
            }
            
            st.write(f"**Unité de base :** {besoins['unite']}")
            
            col_n, col_p, col_k = st.columns(3)
            with col_n:
                st.metric("Azote (N)", f"{besoins_total['N']} kg")
                st.progress(min(besoins_total['N'] / 5, 1.0))
            with col_p:
                st.metric("Phosphore (P)", f"{besoins_total['P']} kg")
                st.progress(min(besoins_total['P'] / 5, 1.0))
            with col_k:
                st.metric("Potassium (K)", f"{besoins_total['K']} kg")
                st.progress(min(besoins_total['K'] / 5, 1.0))
    
    with col2:
        if culture_choisie:
            # Plan standard (replié par défaut)
            with st.expander("🌱 Plan de fertilisation préconisé (standard)", expanded=False):
                if culture_choisie in formules_recommandees:
                    formule = formules_recommandees[culture_choisie]
                    st.markdown(f"**{formule['nom']}**")
                    
                    st.markdown("##### 🧺 Fertilisation de fond")
                    for i, fert in enumerate(formule['fond']):
                        if fert in fertilisants and i < len(formule['quantites_fond']):
                            qte_base = formule['quantites_fond'][i]
                            if "arbre" in besoins["unite"] or "pied" in besoins["unite"]:
                                qte_ajustee = round(qte_base * facteur, 2)
                            else:
                                qte_ajustee = round(qte_base * facteur, 2)
                            st.markdown(f"• **{fert}** : {qte_ajustee} kg")
                            details = fertilisants[fert]
                            st.caption(f"  ↳ N:{details['N']}% P:{details['P']}% K:{details['K']}% - Action {details['rapidite']}")
                            if "attention" in details:
                                st.warning(f"⚠️ {details['attention']}")
                    
                    st.markdown("##### ⚡ Coups de pouce")
                    for i, fert in enumerate(formule['coup_de_pouce']):
                        if i < len(formule['quantites_coup_de_pouce']):
                            qte = formule['quantites_coup_de_pouce'][i]
                            if isinstance(qte, (int, float)):
                                if "arbre" in besoins["unite"] or "pied" in besoins["unite"]:
                                    qte_ajustee = round(qte * facteur, 2)
                                else:
                                    qte_ajustee = round(qte * facteur, 2)
                                st.markdown(f"• **{fert}** : {qte_ajustee} kg")
                            else:
                                st.markdown(f"• **{fert}** : {qte}")
                            if fert in fertilisants:
                                details = fertilisants[fert]
                                st.caption(f"  ↳ Usage: {details.get('usage', 'épandage')} - Action {details['rapidite']}")
                else:
                    st.info("Pas de formule standard pour cette culture.")
            
            # NOUVELLE FONCTIONNALITÉ : fertilisant disponible
            with st.expander("🔍 J'ai déjà un fertilisant, que me manque-t-il ?", expanded=True):
                st.markdown("Sélectionnez un fertilisant que vous possédez et indiquez la quantité que vous souhaitez apporter.")
                
                col_fert1, col_fert2 = st.columns(2)
                with col_fert1:
                    fert_dispo = st.selectbox("Fertilisant disponible :", ["Choisir..."] + sorted(fertilisants.keys()), key="fert_dispo")
                with col_fert2:
                    quantite_fert = st.number_input("Quantité (kg) :", min_value=0.0, value=10.0, step=1.0, key="qte_fert")
                
                if fert_dispo != "Choisir..." and quantite_fert > 0:
                    props = fertilisants[fert_dispo]
                    
                    apport_n = quantite_fert * props["N"] / 100
                    apport_p = quantite_fert * props["P"] / 100
                    apport_k = quantite_fert * props["K"] / 100
                    
                    st.markdown("**Apports de votre fertilisant :**")
                    col_a1, col_a2, col_a3 = st.columns(3)
                    col_a1.metric("N apporté", f"{apport_n:.2f} kg")
                    col_a2.metric("P apporté", f"{apport_p:.2f} kg")
                    col_a3.metric("K apporté", f"{apport_k:.2f} kg")
                    
                    reste_n = besoins_total["N"] - apport_n
                    reste_p = besoins_total["P"] - apport_p
                    reste_k = besoins_total["K"] - apport_k
                    
                    st.markdown("**Besoins restants (déficit / excès) :**")
                    col_r1, col_r2, col_r3 = st.columns(3)
                    col_r1.metric("N restant", f"{reste_n:.2f} kg")
                    col_r2.metric("P restant", f"{reste_p:.2f} kg")
                    col_r3.metric("K restant", f"{reste_k:.2f} kg")
                    
                    # Suggestions pour combler les manques
                    st.markdown("**Suggestions pour équilibrer :**")
                    
                    recommandations = {
                        "N": [("Fiente de volaille", 5.0), ("Poudre de poisson", 9.0), ("Purin d'orties", 0.2)],
                        "P": [("Poudre d'os", 20.0), ("Fiente de volaille", 4.0)],
                        "K": [("Cendre de bois", 7.0), ("Tithonia frais", 4.0), ("Purin de consoude", 0.6)]
                    }
                    
                    suggestions = []
                    
                    if reste_n > 0.1:
                        for nom, pct in recommandations["N"]:
                            qte_necessaire = reste_n / (pct/100)
                            if qte_necessaire > 0:
                                suggestions.append(f"• **{nom}** : environ {qte_necessaire:.1f} kg (pour combler le manque de N)")
                                break
                    elif reste_n < -0.1:
                        st.warning(f"⚠️ Excès d'azote de {abs(reste_n):.2f} kg. Réduisez la quantité de {fert_dispo} ou choisissez un autre fertilisant.")
                    
                    if reste_p > 0.1:
                        for nom, pct in recommandations["P"]:
                            qte_necessaire = reste_p / (pct/100)
                            if qte_necessaire > 0:
                                suggestions.append(f"• **{nom}** : environ {qte_necessaire:.1f} kg (pour combler le manque de P)")
                                break
                    elif reste_p < -0.1:
                        st.warning(f"⚠️ Excès de phosphore de {abs(reste_p):.2f} kg.")
                    
                    if reste_k > 0.1:
                        for nom, pct in recommandations["K"]:
                            qte_necessaire = reste_k / (pct/100)
                            if qte_necessaire > 0:
                                suggestions.append(f"• **{nom}** : environ {qte_necessaire:.1f} kg (pour combler le manque de K)")
                                break
                    elif reste_k < -0.1:
                        st.warning(f"⚠️ Excès de potassium de {abs(reste_k):.2f} kg.")
                    
                    if suggestions:
                        for s in suggestions:
                            st.markdown(s)
                        st.caption("Les quantités sont théoriques, ajustez selon vos observations.")
                    elif reste_n <= 0.1 and reste_p <= 0.1 and reste_k <= 0.1:
                        st.success("✅ Votre fertilisant couvre déjà les besoins ! Pas de manque significatif.")

# ------------------------------------------------------------
# PAGE CATALOGUE DES CULTURES
# ------------------------------------------------------------
elif page == "Catalogue des cultures":
    st.header("📚 Catalogue des cultures")
    filtre = st.text_input("🔍 Rechercher une culture", "")
    
    data = []
    for culture, besoins in cultures_npk.items():
        if filtre.lower() in culture.lower():
            data.append({
                "Culture": culture,
                "N (kg)": besoins["N"],
                "P (kg)": besoins["P"],
                "K (kg)": besoins["K"],
                "Unité": besoins["unite"]
            })
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.caption("Les doses sont données pour 100 m² sauf indication contraire.")

# ------------------------------------------------------------
# PAGE CATALOGUE DES FERTILISANTS
# ------------------------------------------------------------
elif page == "Catalogue des fertilisants":
    st.header("🧪 Catalogue des fertilisants")
    
    data = []
    for nom, props in fertilisants.items():
        data.append({
            "Fertilisant": nom,
            "N (%)": props["N"],
            "P (%)": props["P"],
            "K (%)": props["K"],
            "Type": props["type"],
            "Rapidité": props["rapidite"],
            "Attention": props.get("attention", "")
        })
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("""
    ### 💡 Comment utiliser ces fertilisants ?
    - **Fertilisation de fond** : Compost, fumiers compostés (action lente, à incorporer avant plantation)
    - **Coups de pouce** : Fientes, poudres, cendres (action rapide, en cours de culture)
    - **Purins** : En pulvérisation foliaire ou arrosage (très dilués, action immédiate)
    
    ⚠️ **Règles d'or :**
    - Ne pas mélanger cendre et fumier frais (perte d'azote)
    - La fiente de volaille doit être utilisée avec précaution (risque de brûlure)
    - Alternez les sources pour une fertilisation équilibrée
    """)

# ------------------------------------------------------------
# PAGE CALCULATEUR PERSONNALISÉ
# ------------------------------------------------------------
else:
    st.header("🧮 Calculateur personnalisé")
    st.markdown("Créez votre propre formule de fertilisation et comparez avec les besoins NPK.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1. Choisissez votre culture")
        culture_calc = st.selectbox("Culture :", sorted(cultures_npk.keys()), key="calc_culture")
        
        if culture_calc:
            besoins = cultures_npk[culture_calc]
            if "arbre" in besoins["unite"]:
                nb = st.number_input("Nombre d'arbres :", min_value=1, value=1, key="nb_arbres_calc")
                facteur = nb
            elif "pied" in besoins["unite"]:
                nb = st.number_input("Nombre de pieds :", min_value=1, value=1, key="nb_pieds_calc")
                facteur = nb
            else:
                facteur = surface / 100
            
            besoins_total = {
                "N": round(besoins["N"] * facteur, 2),
                "P": round(besoins["P"] * facteur, 2),
                "K": round(besoins["K"] * facteur, 2)
            }
            st.metric("Besoins NPK totaux", f"N:{besoins_total['N']} kg | P:{besoins_total['P']} kg | K:{besoins_total['K']} kg")
    
    with col2:
        st.subheader("2. Composez votre fertilisation")
        fert_choisis = st.multiselect("Fertilisants à utiliser :", sorted(fertilisants.keys()))
        
        apports = {"N": 0, "P": 0, "K": 0}
        details_apports = []
        
        if fert_choisis:
            st.markdown("**Quantités à apporter :**")
            for fert in fert_choisis:
                props = fertilisants[fert]
                qte = st.number_input(f"{fert} (kg)", min_value=0.0, value=1.0, step=0.5, key=f"qte_{fert}")
                if qte > 0:
                    apport_n = round(qte * props["N"] / 100, 2)
                    apport_p = round(qte * props["P"] / 100, 2)
                    apport_k = round(qte * props["K"] / 100, 2)
                    apports["N"] += apport_n
                    apports["P"] += apport_p
                    apports["K"] += apport_k
                    details_apports.append({
                        "Fertilisant": fert,
                        "Quantité (kg)": qte,
                        "N apporté (kg)": apport_n,
                        "P apporté (kg)": apport_p,
                        "K apporté (kg)": apport_k
                    })
    
    if culture_calc and fert_choisis:
        st.markdown("---")
        st.subheader("3. Comparaison besoins vs apports")
        
        col_res1, col_res2, col_res3 = st.columns(3)
        diff_n = apports["N"] - besoins_total["N"]
        diff_p = apports["P"] - besoins_total["P"]
        diff_k = apports["K"] - besoins_total["K"]
        
        col_res1.metric("Azote (N)", f"{apports['N']} kg / {besoins_total['N']} kg", 
                        f"{'+' if diff_n > 0 else ''}{diff_n} kg", delta_color="inverse" if abs(diff_n) > 0.5 else "off")
        col_res2.metric("Phosphore (P)", f"{apports['P']} kg / {besoins_total['P']} kg", 
                        f"{'+' if diff_p > 0 else ''}{diff_p} kg", delta_color="inverse" if abs(diff_p) > 0.3 else "off")
        col_res3.metric("Potassium (K)", f"{apports['K']} kg / {besoins_total['K']} kg", 
                        f"{'+' if diff_k > 0 else ''}{diff_k} kg", delta_color="inverse" if abs(diff_k) > 0.5 else "off")
        
        if details_apports:
            st.markdown("##### Détail des apports")
            st.dataframe(pd.DataFrame(details_apports), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        if abs(diff_n) > 1 or abs(diff_p) > 0.5 or abs(diff_k) > 1:
            st.warning("⚠️ **Équilibre à revoir :** Certains éléments sont en excès ou en déficit significatif.")
            if diff_n < -1:
                st.markdown("• Manque d'azote → Ajoutez un fertilisant riche en N (fiente, poudre de poisson, purin d'ortie)")
            elif diff_n > 1:
                st.markdown("• Excès d'azote → Risque de sensibilité aux maladies, réduisez les apports azotés")
            if diff_p < -0.5:
                st.markdown("• Manque de phosphore → Ajoutez de la poudre d'os")
            if diff_k < -1:
                st.markdown("• Manque de potassium → Ajoutez de la cendre de bois ou du tithonia")
        else:
            st.success("✅ Fertilisation équilibrée !")

# Footer
st.markdown("---")
st.markdown("🌿 **Application de Fertilisation Agroécologique** - Données indicatives à adapter selon votre sol et vos observations.")