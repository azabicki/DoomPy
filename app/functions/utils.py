import streamlit as st
import base64
from pathlib import Path


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


# -----------------------------------------------------------------------------
def img2html(img_path, div: str = "", cls: str = ""):
    img_html = """
        <div class={div}>
        <div class="div_yCenter">
        <img src='data:image/png;base64,{img}' class={cls}>
        </img></div></div>""".format(
        img=img_to_bytes(img_path), div=div, cls=cls
    )
    return img_html


# -----------------------------------------------------------------------------
def img2html_doubles(img_path, cls: str = ""):
    img_html = """
        <div class="Xtra_row">
            <div class="Xtra_col">
                <img src='data:image/png;base64,{img0}' class={cls}></img>
            </div>
            <div class="Xtra_col">
                <img src='data:image/png;base64,{img1}' class={cls}></img>
            </div>
        </div>""".format(
        img0=img_to_bytes(img_path[0]), img1=img_to_bytes(img_path[1]), cls=cls
    )
    return img_html


# -----------------------------------------------------------------------------
def img2html_triples(img_path, cls: str = ""):
    img_html = """
        <div class="Xtra_row">
            <div class="Xtra_col">
                <img src='data:image/png;base64,{img0}' class={cls}></img>
            </div>
            <div class="Xtra_col">
                <img src='data:image/png;base64,{img1}' class={cls}></img>
            </div>
            <div class="Xtra_col">
                <img src='data:image/png;base64,{img2}' class={cls}></img>
            </div>
        </div>""".format(
        img0=img_to_bytes(img_path[0]),
        img1=img_to_bytes(img_path[1]),
        img2=img_to_bytes(img_path[2]),
        cls=cls,
    )
    return img_html


# -----------------------------------------------------------------------------
def style():
    css = """
    <style>
        /* -------------------------------- */
        [data-testid="stSidebar"]{
            min-width: 260px;
            max-width: 260px;
        }

        /* -------------------------------- */
        .div_yCenter{
            position: relative;
            top: 50%;
            transform: translateY(-50%);
        }

        /* -------------------------------- */
        .div_score_upper{
            height: 50px;
            border: 0px solid green
        }

        .div_points{
            height: 30px;
            width: 30px;
            border: 0px solid green
        }

        p.points{
            font-size: 22px;
            font-weight: bold;
            text-align: left;
        }

        p.points_total{
            font-size: 80px;
            font-weight: bold;
            text-align: center;
        }

        .div_points_total{
            height: 60px;
            border: 0px solid red
        }

        img.score_icons{
            width: 20px;
            display: block;
            margin-left: auto;
            margin-right: auto;
        }

        /* -------------------------------- */
        img.star{
            width: 30px;
            display: block;
            margin-left: auto;
            margin-right: auto;
        }

        /* -------------------------------- */
        .div_icons{
            height: 20px;
            width: 20px;
            border: 0px solid green
        }

        img.icons{
            width: 22px;
            display: block;
            margin-left: auto;
            margin-right: auto;
        }

        /* -------------------------------- */
        .div_MOL{
            height: 40px;
            width: 35px;
            border: 0px solid green
        }

        img.MOL{
            width: 30px;
        }

        /* -------------------------------- */
        .Xtra_row::after {
            content: "";
            clear: both;
            display: table;
        }

        .Xtra_col {
            float: left;
            width: 33%;
            position: relative;
            top: 50%;
            transform: translateY(-15%);
        }

        img.Xtra_icons{
            width: 22px;
        }

        /* -------------------------------- */
        .div_WE{
            height: 40px;
            display: block;
            margin-left: auto;
            margin-right: auto;
            border: 0px solid green
        }


        .div_WE_icons_L{
            height: 40px;
            width: 40px;
            display: block;
            margin-left: auto;
            margin-right: auto;
            border: 0px solid red;
        }

        .div_WE_icons_R{
            height: 40px;
            width: 40px;
            display: block;
            margin-left: auto;
            margin-right: auto;
            border: 0px solid green;
        }

        img.WE_icons{
            width: 30px;
            display: block;
            margin-left: auto;
            margin-right: auto;
        }

        p.WE{
            font-weight: bold;
            font-size: 25px;
            text-align: center
        }

        .div_WE_points{
            height: 40px;
            display: block;
            margin-left: auto;
            margin-right: auto;
            border: 0px solid green;
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
