import streamlit as st
import pyrebase
import streamlit as st
from fpdf import FPDF
import base64

class Subheading:
        def __init__(self, name, font, text):
            self.name = name
            self.font = font
            self.text = text
            
        def add_subheading(self):
            self.name = st.selectbox('What is the subheading of your document:',
                                    ('Introduction', 'Project Overview', "Requirements", "Scope", "Another option..."),
                                    key=f"subheading-{i}-name")
            if self.name == "Another option...": 
                self.name = st.text_input("Enter your other option...", key=f"subheading-{i}-other-name")
            self.text = st.text_area("Input relevant Text here:", key=f"subheading-{i}-text")


if st.session_state['loggedIn'] == True:  
       
        num_subheadings = st.number_input("How many subheadings would you like to add?", value=2, min_value=1, max_value=10)

        selected_font = st.sidebar.selectbox('Select the font for all subheadings:',
                                            ('Arial', 'Times', 'Courier' ))
        subheadings = []


        for i in range(num_subheadings):
            subheadings.append(Subheading('', '', ''))
            subheadings[i].add_subheading()
            
        def create_download_link(val, filename):
            b64 = base64.b64encode(val)  # val looks like b'...'
            return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

        if st.button("Export Document"):
            pdf = FPDF()
            pdf.add_page()
            for subheading in subheadings:
                pdf.set_font(selected_font, 'B', 16)
                pdf.cell(40, 10, subheading.name,ln=2)
                pdf.set_font(selected_font, '', 10)
                pdf.multi_cell(190, 4, subheading.text)
                
            html = create_download_link(pdf.output(dest="S").encode("latin-1"), "test")

            st.markdown(html, unsafe_allow_html=True)

            # Create a button to view the PDF
        if st.button("View PDF"):
            pdf = FPDF()
            pdf.add_page()
            for subheading in subheadings:
                pdf.set_font(selected_font, 'B', 16)
                pdf.cell(40, 10, subheading.name,ln=2)
                pdf.set_font(selected_font, '', 10)
                pdf.multi_cell(190, 4, subheading.text)

            pdf_base64 = base64.b64encode(pdf.output(dest="S").encode("latin-1")).decode()

            # Create a data URI
            pdf_uri = f"data:application/pdf;base64,{pdf_base64}"

            # Display the PDF in an <iframe> element
            st.markdown(f'<iframe src="{pdf_uri}" width="100%" height="600"></iframe>', unsafe_allow_html=True)
else:
    st.error("Login Required to use this page")