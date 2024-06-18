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
            border: 0px solid green
        }

        .clr-cnt-div{
            height: 30px;
            width: 30px;
            border: 0px solid green
        }

        p.clr-cnt{
            font-size: 22px;
            font-weight: bold;
        }

        .ttl-scr-div{
            height: 60px;
            border: 0px solid green
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
