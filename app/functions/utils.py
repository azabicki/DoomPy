import streamlit as st


# -----------------------------------------------------------------------------
def style():
    css = """
    <style>
        [data-testid="stSidebar"]{
            min-width: 250px;
            max-width: 250px;
        }

        .parent-div{
            height: 50px;
            border: 1px solid green
        }

        .text-div{
            position: relative;
            top: 50%;
            transform: translateY(-50%);
        }

        .img_center{
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 50%;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
def h_spacer(height, sb=False) -> None:
    for _ in range(height):
        if sb:
            st.sidebar.write("\n")
        else:
            st.write("\n")
