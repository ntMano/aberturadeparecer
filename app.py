import html
import streamlit as st
import pandas as pd
from datetime import datetime
import io
import time
import pdfkit
import os
import subprocess
import platform


st.markdown("### Portal de abertura de Parecer RT/RE")


c1, c2 = st.columns(2)
st.sidebar.title('MENU')
selecao = st.sidebar.selectbox('Escolha uma opção', ['RT', 'RE'])


if selecao == 'RT':

    check = st.sidebar.radio('Escolha uma das opções abaixo: ', ('Inscrição',
                                                                 'Renovação',
                                                                 'Alteração'))
    with c1:
        st.form(key="mainform", clear_on_submit=True)
        parecer = st.text_input('Nº do Parecer: ')
        ano_parecer = st.text_input('Ano: ')
        data = st.date_input('Data da solicitação:')
        data_formatada = datetime.strftime(data, '%d/%m/%Y')

        enf_requerente = st.text_input('Enf. Requerente: ')
        numcoren = st.text_input('Número de Inscrição do COREN-MA:')
        telefonert = st.text_input('Telefone/celular:')
        email = st.text_input('Email:')
        empresa = st.text_input('Empresa: ')
        numpj = st.text_input('PJ: ')
        cnpj = st.text_input('CNPJ: ')
        municipio = st.text_input('Município: ')
        if st.button('Enviar'):
            # Criação da tabela HTML
            table_header = "<tr><th>Nº do Parecer</th><th>Ano</th><th>Data da solicitação</th><th>Enf. Requerente</th><th>Empresa</th><th>PJ</th><th>CNPJ</th><th>Município</th><th>Check</th></tr>"
            table_content = f"<tr><td>{parecer}</td><td>{ano_parecer}</td><td>{data}</td><td>{enf_requerente}</td><td>{numcoren}</td><td>{telefonert}</td><td>{email}</td><td>{empresa}</td><td>{numpj}</td><td>{cnpj}</td><td>{municipio}</td><td>{check}</td></tr>"

            # Exibição da tabela HTML
            df = pd.DataFrame({
                'Nº do Parecer': [parecer],
                'Ano': [ano_parecer],
                'Data da solicitação': [data_formatada],
                'Enf. Requerente': [enf_requerente],
                'Número do Coren': [numcoren],
                'Telefone': [telefonert],
                'Email': [email],
                'Empresa': [empresa],
                'PJ': [numpj],
                'CNPJ': [cnpj],
                'Município': [municipio],
                'Check': [check]
            })
            st.write(parecer)
            st.write(ano_parecer)
            st.write(data_formatada)
            st.write(enf_requerente)
            st.write(numcoren)
            st.write(telefonert)
            st.write(email)
            st.write(empresa)
            st.write(numpj)
            st.write(cnpj)
            st.write(municipio)
            st.write(df.to_html(index=False), unsafe_allow_html=True)
elif selecao == 'RE':
    st.markdown('Estamos em produção')

with c2:
    # Caso queira usar biblioteca weasyprint
    # with open('rt.html', 'r', encoding='utf-8') as f:
    #     html = f.read().format(PARECER=parecer, ANO=ano_parecer, DATA=data_formatada, ENF_REQUERENTE=enf_requerente,
    #                     EMPRESA=empresa, COREN=numcoren, PJ=numpj, CNPJ=cnpj, MUNICIPIO=municipio, CHECK=check)
    # st.components.v1.html(html, width=700, height=955, scrolling=True)

    # if st.button('Gerar PDF'):
    #     pdf_data = io.BytesIO()
    #     weasyprint.HTML(string=html).write_pdf(pdf_data)

    #     progress_bar = st.progress(0)
    #     for porcento in range(100):
    #         time.sleep(0.01)
    #         progress_bar.progress(porcento+1)
    #     st.success("PDF gerado com sucesso!")
    #     st.download_button(label='Baixar PDF', data=pdf_data.getvalue() ,
    #                     file_name='parecer.pdf', mime='application/pdf')

    # Caso queira usar o pdfkit utilize o código abaixo
    # with open('rt.html', 'r', encoding='utf-8') as f:
    #     html = f.read().format(PARECER=parecer, ANO=ano_parecer, DATA=data_formatada, ENF_REQUERENTE=enf_requerente,
    #                            EMPRESA=empresa, COREN=numcoren, PJ=numpj, CNPJ=cnpj, MUNICIPIO=municipio, CHECK=check)
    #     st.components.v1.html(html, width=700, height=955, scrolling=True)
    # if st.button('Gerar PDF'):
    #     pdf_data = pdfkit.from_string(
    #         html, False, options={'encoding': 'utf-8'})
    #     pdf_file = io.BytesIO(pdf_data)

    #     progress_bar = c2.progress(0)
    #     for porcento in range(100):
    #         time.sleep(0.01)
    #         progress_bar.progress(porcento+1)
    #     st.success("PDF gerado com sucesso!")
    #     st.download_button(label='Baixar PDF', data=pdf_file,
    #                        file_name='parecer.pdf', mime='application/pdf')
    if platform.system() == 'Windows':
        pdfkit_config = pdfkit.configuration(
            wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    else:
        WKHTMLTOPDF_CMD = subprocess.Popen(['which', os.environ.get(
            'WKHTMLTOPDF_PATH', '/app/bin/wkhtmltopdf')], stdout=subprocess.PIPE).communicate()[0].strip()
        pdfkit_config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)

    with open('rt.html', 'r', encoding='utf-8') as f:
        html = f.read().format(PARECER=parecer, ANO=ano_parecer, DATA=data_formatada, ENF_REQUERENTE=enf_requerente,
                               EMPRESA=empresa, COREN=numcoren, PJ=numpj, CNPJ=cnpj, MUNICIPIO=municipio, CHECK=check)
        st.components.v1.html(html, width=700, height=955, scrolling=True)

    if st.button('Gerar PDF'):
        pdf_data = pdfkit.from_string(
            html, False, options={'encoding': 'utf-8'}, configuration=pdfkit_config)
        pdf_file = io.BytesIO(pdf_data)
        progress_bar = c2.progress(0)
        for porcento in range(100):
            time.sleep(0.01)
            progress_bar.progress(porcento+1)
        st.success("PDF gerado com sucesso!")
        st.download_button(label='Baixar PDF', data=pdf_file,
                           file_name='parecer.pdf', mime='aplicativo/pdf')

if selecao == 'RE':
    st.markdown("### Em construção!")
