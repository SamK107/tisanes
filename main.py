from turtle import title
from unittest import defaultTestLoader, result
import streamlit as st
import pandas as pd
import numpy as np
import plotly_express as px
import base64
from io import StringIO, BytesIO
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import matplotlib.pyplot as plt


print("Hello main")

st.set_page_config(page_title="TISANE",
                    page_icon="🌿",
                    layout='wide',
                    initial_sidebar_state="collapsed")


def pourcentage(nombre, nbtotal):
    if nbtotal!=0:
        pourcentage = 100 * float(nombre)/float(nbtotal)
        return str(f'{pourcentage:,.2f}') +  '%'

def generate_excel_download_link(df):

    towrite = BytesIO()
    df.to_excel(towrite, encoding = "utf-8", index = False, header=True)
    towrite.seek(0)
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheets;base64,{b64}" download="data_download.xlsx">Télécharger le fichier Excel<a/>'
    return st.markdown(href, unsafe_allow_html=True)

def generate_html_download_link(fig):

    towrite = StringIO()
    fig.write_html(towrite, include_plotlyjs="cdn")
    towrite = BytesIO(towrite.getvalue().encode())
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:text/html;charset=utf-0;base64, {b64}" download="plot.html">Télécharger le graphique<a/>'
    return st.markdown(href, unsafe_allow_html=True)


def app():
    st.title('📈gestion de Tisane Madouwa')
    st.subheader("Situation des recettes")

    # uploaded_file = st.file_uploader('Choisir un fichier XLSX', type='xlsx')
    # if uploaded_file:
    #     st.markdown('------')
    df = pd.read_excel("gestion.xlsx", engine='openpyxl', sheet_name='recettes')
    # df.loc[:,'Valeur'] = df["Valeur"].map('{:,}'.format)
    # df.loc[:,'Ventes'] = df["Ventes"].map('{:,}'.format)
    mois = st.sidebar.multiselect(
            "Selectionner le mois",
            options=df["MOIS"].unique(),
            default=df["MOIS"].unique()
    )

    annee = st.sidebar.multiselect(
            "Selectionner l'année",
            options=df["ANNEE"].unique(),
            default=df["ANNEE"].unique()
    )

    df_selection = df.query(
        "MOIS == @mois & ANNEE == @annee"
    )


    with st.expander("Afficher l'ensemble des données"):
        # st.dataframe(df_selection)
        AgGrid(df_selection)

    groupby_column = st.selectbox(
        'Que voulez-vous analyser ?',
        ('ITEMS', 'TIERS')
    )

   
    #GROU DATAFRAME
    output_columns = ['MONTANT']
    # column_names = ['DATES', 'PRODUITS', 'CLIENTS', 'FOURNISSEURS',	'LIBELLES',	'RECETTES',	'DEPENSES',	'SOLDES', 'MOIS', 'ANNEE']

    # df.groupby(['col5','col2']).size().reset_index().groupby('col2')[[0]].max()


    df_grouped = df_selection.groupby(by=[groupby_column], as_index=False)[output_columns].sum()
    
    # df_selection = df_grouped.query(
    #         "MOIS == @mois & ANNEE==@annee"
    # )

    with st.expander('Afficher les données'):
        # df_grouped.loc[:,'Valeur'] = df_grouped['Valeur'].map('{:,}'.format)

        # st.markdown(f"Vente mois : {mois} et années : {annee}")
        # st.dataframe(df_grouped)
        AgGrid(df_grouped)
    with st.expander("Afficher la représentation graphique"):
    #-------PLOT DATAFRAME
        fig = px.bar(
            df_grouped,
            x=groupby_column,
            y='MONTANT',
            color='MONTANT',
            color_continuous_scale=['red', 'yellow', 'green'],
            template='plotly_white',
            # title=f'<b> Valeur et Ventes par {groupby_column}</b>'
                )
        fig.update_layout({
            'plot_bgcolor':'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)'
        })

        if groupby_column == "ITEMS":
            groupby_column = 'RECETTES'

        if groupby_column == "TIERS":
            groupby_column = "RECETTES PAR CLIENTS"

            st.markdown(groupby_column)

        st.plotly_chart(fig, use_container_width=True)

        #SECTION TELECHARGEMENT
        st.subheader('Télécharger:')
        generate_excel_download_link(df_grouped)
        generate_html_download_link(fig)

# app()

#----------------------------------------------------END

def app2():

    st.title('📈gestion de Tisane Madouwa')
    st.subheader("Situation des dépenses")

    # uploaded_file = st.file_uploader('Choisir un fichier XLSX', type='xlsx')
    # if uploaded_file:
    #     st.markdown('------')
    df = pd.read_excel("gestion.xlsx", engine='openpyxl', sheet_name="depenses")
    # df.loc[:,'Valeur'] = df["Valeur"].map('{:,}'.format)
    # df.loc[:,'Ventes'] = df["Ventes"].map('{:,}'.format)
    mois = st.sidebar.multiselect(
            "Selectionner le mois",
            options=df["MOIS"].unique(),
            default=df["MOIS"].unique()
    )

    annee = st.sidebar.multiselect(
            "Selectionner l'année",
            options=df["ANNEE"].unique(),
            default=df["ANNEE"].unique()
    )

    type_depenses = st.sidebar.multiselect(
        'Sélection un type de dépenses',
        options=df["TYPE_DEPENSES"].unique(),
        default=df["TYPE_DEPENSES"].unique()
    )

    df_selection = df.query(
        "MOIS == @mois & ANNEE == @annee & TYPE_DEPENSES == @type_depenses"
    )

    with st.expander("Afficher l'ensemble des données"):
        # st.dataframe(df_selection)
        AgGrid(df_selection)

    groupby_column = st.selectbox(
        'Que voulez-vous analyser ?',
        ('ITEMS', 'TIERS')
    )
    #GROU DATAFRAME
    output_columns = ['MONTANT']
    # column_names = ['DATES', 'PRODUITS', 'CLIENTS', 'FOURNISSEURS',	'LIBELLES',	'RECETTES',	'DEPENSES',	'SOLDES', 'MOIS', 'ANNEE']

    # df.groupby(['col5','col2']).size().reset_index().groupby('col2')[[0]].max()


    df_grouped = df_selection.groupby(by=[groupby_column], as_index=False)[output_columns].sum()
    
    # df_selection = df_grouped.query(
    #         "MOIS == @mois & ANNEE==@annee"
    # )

    with st.expander('Afficher les données'):
        # df_grouped.loc[:,'Valeur'] = df_grouped['Valeur'].map('{:,}'.format)

        # st.markdown(f"Vente mois : {mois} et années : {annee}")
        # st.dataframe(df_grouped)
        AgGrid(df_grouped)

    #-------PLOT DATAFRAME
    fig = px.bar(
        df_grouped,
        x=groupby_column,
        y='MONTANT',
        color='MONTANT',
        color_continuous_scale=['#117A65', '#F4D03F', '#CB4335'],
        template='plotly_white',
        # title=f'<b> Valeur et Ventes par {groupby_column}</b>'
    )

    fig.update_layout({
        'plot_bgcolor':'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)'
    })

    

    if groupby_column == "ITEMS":
        groupby_column = 'DEPENSES'

    if groupby_column == "TIERS":
        groupby_column = "DEPENSES PAR TYPE"

    st.plotly_chart(fig, use_container_width=True)

    #SECTION TELECHARGEMENT
    st.subheader('Télécharger:')
    generate_excel_download_link(df_grouped)
    generate_html_download_link(fig)

def etat_produits():

    st.title('📈gestion de Tisane Madouwa')
    st.subheader("Situation générale des recettes")

    #recettes
    df_recettes = pd.read_excel("gestion.xlsx", engine='openpyxl', sheet_name="recettes", usecols="a:i")

    column_names = ['DATES', 'ITEMS', 'TIERS', 'LIBELLES', 'MONTANT', 'SOLDES', 'MOIS', 'ANNEE', 'NATURE']

    df_recettes = pd.DataFrame(df_recettes, columns=column_names)

    mois =  st.multiselect(
        "Sélectionner un mois",
        options=df_recettes['MOIS'].unique(),
        default=df_recettes['MOIS'].unique()
    )


    with st.expander("Les recettes par mois"):
        
        

        # st.write(df_recettes)
        produit = st.sidebar.multiselect(
            "Sélectionner un produit",
            options=df_recettes['ITEMS'].unique(),
            default=df_recettes['ITEMS'].unique()
        )

     
        annee =  st.sidebar.multiselect(
            "Sélectionner une année",
            options=df_recettes['ANNEE'].unique(),
            default=df_recettes['ANNEE'].unique()
        )

        df_selection = df_recettes.query(
            "ITEMS == @produit & MOIS == @mois & ANNEE == @annee"
        )

        # st.dataframe(df_selection)
        
        df_rtt = df_selection.pivot_table(index='ITEMS', columns='MOIS', values='MONTANT',aggfunc="sum" )

        df_rtt = pd.DataFrame(df_rtt, columns=['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 
        'Novembre', 'Décembre'])


        df_rtt = df_rtt.fillna(0).astype(int)

        st.dataframe(df_rtt)

      

    with st.expander("Montant total des recettes par mois et année"):
        df_total = df_rtt.sum() 
        coltitre, col_j, col_f, col_m, col_a, col_mai, col_juin, col_juil, col_aout, col_sept, col_oct, col_nov, col_dec = st.columns(13)
        
        with coltitre:
            st.write("Mois")
            st.write("Montant")
        with col_j:
            valeur=df_total[0]
            st.write("Janvier")
            st.write(f'{valeur:,}'.replace(',',' '))
        with col_f:
            valeur =df_total[1]
            st.write("Février")
            st.write(f'{valeur:,}'.replace(',',' '))
        with col_m:
            valeur =df_total[2]
            st.write("Mars")
            st.write(f'{valeur:,}'.replace(',',' '))
        with col_a:
            valeur =df_total[3]
            st.write("Avril")
            st.write(f'{valeur:,}'.replace(',',' '))
        with col_mai:
            valeur =df_total[4]
            st.write("Mai")
            st.write(f'{valeur:,}'.replace(',',' '))
        with col_juin:
            valeur =df_total[5]
            st.write("Juin")
            st.write(f'{valeur:,}'.replace(',',' '))
        with col_juil:
            valeur =df_total[6]
            st.write("Juillet")
            st.write(f'{valeur:,}'.replace(',',' '))
        with col_aout:
            valeur =df_total[7]
            st.write("Août")
            st.write(f'{valeur:,}'.replace(',',' '))
        with col_sept:
            valeur =df_total[8]
            st.write("Septembre")
            st.write(f'{valeur:,}'.replace(',',' '))
        with col_oct:
            valeur =df_total[9]
            st.write("Octobre")
            st.write(f'{valeur:,}'.replace(',',' '))
        with col_nov:
            valeur =df_total[10]
            st.write("Novembre")
            st.write(f'{valeur:,}'.replace(',',' '))
        with col_dec:
            valeur =df_total[11]
            st.write("Décembre")
            st.write(f'{valeur:,}'.replace(',',' '))
  

def depenses_par_nature():

    st.title('📈gestion de Tisane Madouwa')
    st.subheader("Situation des dépenses par nature")

     #recettes
    df_depenses = pd.read_excel("gestion.xlsx", engine='openpyxl', sheet_name="depenses", usecols="a:j")

    # df_matieres = pd.read_excel("gestion.xlsx", engine="openpyxl", sheet_name="depenses", usecols="a:i")

    column_names = ['DATES', 'ITEMS', 'TIERS', 'LIBELLES', 'MONTANT', 'SOLDES', 'MOIS', 'ANNEE', 'NATURE', 'TYPE_DEPENSES']

    df_depenses = pd.DataFrame(df_depenses, columns=column_names)

    mois =  st.multiselect(
        "Sélectionner un mois",
        options=df_depenses['MOIS'].unique(),
        default=df_depenses['MOIS'].unique()
    )

    type_depense = st.sidebar.multiselect(
        "Sélectionner un type de dépenses",
        options=df_depenses["TYPE_DEPENSES"].unique(),
        default=df_depenses["TYPE_DEPENSES"].unique()
    )

    with st.expander("Dépenses par mois"):

        # st.write(df_recettes)
        # depenses = st.multiselect(
        #     "Sélectionner un produit",
        #     options=df_depenses['ITEMS'].unique(),
        #     default=df_depenses['ITEMS'].unique()
        # )

     
        annee =  st.sidebar.multiselect(
            "Sélectionner une année",
            options=df_depenses['ANNEE'].unique(),
            default=df_depenses['ANNEE'].unique()
        )

        df_selection = df_depenses.query(
            "MOIS == @mois & ANNEE == @annee & TYPE_DEPENSES == @type_depense"
        )

        # st.dataframe(df_selection)
        
        df_rtt = df_selection.pivot_table(index='ITEMS', columns='MOIS', values='MONTANT', aggfunc="sum" )

        df_rtt = pd.DataFrame(df_rtt, columns=['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 
        'Novembre', 'Décembre'])


        df_rtt = df_rtt.fillna(0).astype(int)

        st.dataframe(df_rtt)

      

    with st.expander("Montant total des dépenses par mois et année"):
        df_total = df_rtt.sum() 
        coltitre, col_j, col_f, col_m, col_a, col_mai, col_juin, col_juil, col_aout, col_sept, col_oct, col_nov, col_dec = st.columns(13)
        
       
        with coltitre:
            st.write("Mois")
            st.write("Montant")
        with col_j:
            valeur=df_total[0]
            st.write("Janvier")
            st.write(f'{valeur:,}'.replace(',',' '))
        with col_f:
            valeur =df_total[1]
            st.write("Février")
            st.write(f'{valeur:,}'.replace(',',' '))
        with col_m:
            valeur =df_total[2]
            st.write("Mars")
            st.write(f'{valeur:,}'.replace(',',' '))
        with col_a:
            valeur =df_total[3]
            st.write("Avril")
            st.write(f'{valeur:,}'.replace(',',' '))
        with col_mai:
            valeur =df_total[4]
            st.write("Mai")
            st.write(f'{valeur:,}'.replace(',',' '))
        with col_juin:
            valeur =df_total[5]
            st.write("Juin")
            st.write(f'{valeur:,}'.replace(',',' '))
        with col_juil:
            valeur =df_total[6]
            st.write("Juillet")
            st.write(f'{valeur:,}'.replace(',',' '))
        with col_aout:
            valeur =df_total[7]
            st.write("Août")
            st.write(f'{valeur:,}'.replace(',',' '))
        with col_sept:
            valeur =df_total[8]
            st.write("Septembre")
            st.write(f'{valeur:,}'.replace(',',' '))
        with col_oct:
            valeur =df_total[9]
            st.write("Octobre")
            st.write(f'{valeur:,}'.replace(',',' '))
        with col_nov:
            valeur =df_total[10]
            st.write("Novembre")
            st.write(f'{valeur:,}'.replace(',',' '))
        with col_dec:
            valeur =df_total[11]
            st.write("Décembre")
            st.write(f'{valeur:,}'.replace(',',' '))

    with st.expander("Répresentation graphique du détail des dépenses"):
        chart_data =pd.DataFrame(
            df_rtt,
            columns=['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 
        'Novembre', 'Décembre'] )
        st.bar_chart(chart_data, height=500)

      




def etat_gestion():
    st.title('📈gestion de Tisane Madouwa')
    st.subheader("Situation générale")

    #recettes
    df_recettes = pd.read_excel("gestion.xlsx", engine='openpyxl', sheet_name="recettes")

    df_depenses = pd.read_excel("gestion.xlsx", engine='openpyxl', sheet_name="depenses")

   

    frames = [df_recettes, df_depenses]

    df = pd.concat(frames)

    # st.dataframe(df)

    mois = st.sidebar.multiselect(
            "Selectionner le mois",
            options=df["MOIS"].unique(),
            default=df["MOIS"].unique()
    )

    annee = st.sidebar.selectbox(
            "Selectionner l'année",
            options=df["ANNEE"].unique(),
            # default=df["ANNEE"].unique()
    )

    type_depenses = st.sidebar.multiselect(
        "Sélectionner un type de dépenses",
        options=df["TYPE_DEPENSES"].unique(),
        default=df['TYPE_DEPENSES'].unique()
    )

    

    # options_r = ("RECETTES", "DEPENSES")
    # radio = st.sidebar.radio(label="Choisir l'item", options=options_r, key='kradio')
    # st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

    df_selection = df.query(
        "MOIS == @mois & ANNEE == @annee & TYPE_DEPENSES == @type_depenses"
    )

    # with st.expander("Afficher l'ensemble des données"):
    #     # st.dataframe(df_selection)
    #     AgGrid(df_selection)

    total_r_g = int(df.loc[df['NATURE']=='RECETTES', 'MONTANT'].sum())
    total_d_g = int(df.loc[df['NATURE']=='DEPENSES', 'MONTANT'].sum())

    
    # st.write(total_d_g, total_r_g)

    total_recettes = int(df_selection.loc[df_selection['NATURE']=='RECETTES', 'MONTANT'].sum())                     #['NATURE'].where("NATURE").equals("RECETTES").sum())
    total_depenses = int(df_selection.loc[df_selection['NATURE']=='DEPENSES', 'MONTANT'].sum())
    ecart = total_recettes - total_depenses
    taux = pourcentage(total_depenses, total_recettes)


    #------------
    delta_r = pourcentage(total_recettes, total_r_g)
    delta_g = pourcentage(total_depenses, total_d_g)
    with st.expander("Indicateurs de gestion"):
        left_column, middle_column, right_column = st.columns([1,1,1])
        left_column.metric('TOTAL RECETTES', f'FCFA {total_recettes:,}'.replace(',',' '),delta_color='normal', delta=delta_r)
        middle_column.metric('TOTAL DEPENSES', f'FCFA {total_depenses:,}'.replace(',',' '), delta_color='inverse', delta=delta_g)
        right_column.metric("MARGE BRUTE", f'FCFA {ecart:,}'.replace(',',' '), delta_color='inverse', delta=taux)
        right_column.metric('TAUX DE MARGE', taux )
   


def main():

    options = ["Recettes", "Dépenses", "Etat recettes", "Etat dépenses", "Etat"]
    choose = st.sidebar.selectbox("Choisir un item", options=options)
    if choose == "Recettes":
        app()
    elif choose == "Dépenses":
        app2()
    elif choose == "Etat recettes":
        etat_produits()
    elif choose == "Etat dépenses":
        depenses_par_nature()
    elif choose == 'Etat':
        etat_gestion()
    
if __name__=='__main__':
       main()