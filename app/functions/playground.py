import streamlit as st


def MOLs(p):
    st.markdown("Meaning(s) of Life")
    for m in range(st.session_state.game["n_MOLs"]):
        st.selectbox(
            "MOL_" + str(p) + "_" + str(m),
            st.session_state.deck,
            format_func=lambda x: st.session_state.deck_str[x],
            index=None,
            placeholder="MOL #" + str(m + 1),
            label_visibility="collapsed",
            disabled=False if m == 0 else True,
        )
