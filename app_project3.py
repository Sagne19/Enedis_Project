# import streamlit as st
# import pandas as pd
# import requests
# from bs4 import BeautifulSoup
# from PIL import Image
# import io
# import base64
# from urllib.parse import urljoin

# # Image en local
# image_path = "/Users/mathieusagne/Downloads/logo-sud-ouest-3-1.jpg"

# # Charger l'image
# with open(image_path, "rb") as file:
#     image_base64 = base64.b64encode(file.read()).decode("utf-8")

# st.markdown(
#     f"""
#     <style>
#     .logo-container {{
#         position: absolute;
#         top: 10px;
#         right: 10px;
#         z-index: 1;
#     }}
#     .logo-image {{
#         max-width: 150px;
#         max-height: 150px;
#     }}
#     </style>
#     <div class="logo-container">
#         <img class="logo-image" src="data:image/jpeg;base64,{image_base64}" alt="Logo">
#         <h1 class="title">Les dernières actualités Enedis</h1>
#     </div>
#     """,
#     unsafe_allow_html=True
# )

# # Bloc d'espace
# st.markdown(
#     """
#     <div style="height: 100px;"></div>
#     """,
#     unsafe_allow_html=True
# )

# def parse_articles(url):
#     try:
#         r = requests.get(url)
#         soup = BeautifulSoup(r.content, 'html.parser')
#         articles = soup.find_all('div', class_='article-wrapper')

#         news_articles = []
#         for i, article in enumerate(articles):
#             try:
#                 if i >= 6:
#                     break

#                 news_i = {}
#                 news_i['title'] = article.find('div', class_='article-title').text.strip().replace('\xa0', '')
#                 image_tag = article.find('div', class_='article-title').find_previous('img')
#                 if image_tag and 'src' in image_tag.attrs:
#                     news_i['image'] = image_tag['src']
#                 else:
#                     news_i['image'] = None
#                 relative_link = article.find('a').get('href')
#                 absolute_link = urljoin(url, relative_link)
#                 news_i['link'] = absolute_link
#                 news_articles.append(news_i)

#             except AttributeError:
#                 print(f"Erreur lors de l'extraction des données de l'article sur {url}")

#         return news_articles
#     except requests.exceptions.RequestException as e:
#         print(f"Erreur de requête lors de l'accès à l'URL : {url}")
#         return []

# def parse_all_articles():
#     url = "https://www.sudouest.fr/recherche/?query=enedis"
#     articles = parse_articles(url)
    
#     for article in articles:
#         article_url = article['link']
#         try:
#             r = requests.get(article_url)
#             soup = BeautifulSoup(r.content, 'html.parser')
#             publishing_divs = soup.find_all('div', class_='publishing')

#             for div in publishing_divs:
#                 time = div.find('time')
#                 if time:
#                     article['publishing_time'] = time.text.strip()
#                     break

#         except requests.exceptions.RequestException as e:
#             print(f"Erreur de requête lors de l'accès à l'URL : {article_url}")

#     df = pd.DataFrame(articles)
#     df['only_date'] = df['publishing_time'].str.extract(r'(\d{2}/\d{2}/\d{4})')
#     df['only_date'] = pd.to_datetime(df['only_date'], format='%d/%m/%Y')
#     df = df.sort_values('only_date', ascending=False)
#     return df

# result_df = parse_all_articles()

# def display_article(article):
#     article_link = article['link']
#     if article['image']:
#         try:
#             image = Image.open(io.BytesIO(requests.get(article['image']).content))
#             st.image(image, use_column_width=True, caption=article['title'])

#             # Date de publication
#             st.markdown("<div style='text-align: center;'><p style='font-size: 14px;'>{}</p></div>".format(article['publishing_time']), unsafe_allow_html=True)

#             # Lien de l'article
#             st.markdown("<div style='text-align: center;'><a href='{0}' target='_blank'>Voir l'article complet</a></div>".format(article_link), unsafe_allow_html=True)

#         except requests.exceptions.RequestException as e:
#             st.write(f"Erreur lors du chargement de l'image : {article['image']}")


# num_articles = len(result_df)
# for i in range(0, num_articles, 2):
#     st.write('---')
#     col1, col2 = st.columns([1, 1])

#     if i+1 < num_articles:
#         article1 = result_df.iloc[i]
#         article2 = result_df.iloc[i+1]


#         with col1:
#             display_article(article1)

#         with col2:
#             display_article(article2)
#     else:

#         with col1:
#             display_article(result_df.iloc[i])


import streamlit as st
import pandas as pd
import requests
from PIL import Image
import io
import base64
import streamlit.components.v1 as components
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# Nouveau chemin d'image
image_path = "/Users/mathieusagne/Desktop/Streamlit_project3/google_news_logo_icon_159341.png"

# Charger l'image
with open(image_path, "rb") as file:
    image_base64 = base64.b64encode(file.read()).decode("utf-8")


# Fonction pour récupérer les articles depuis l'API News
def get_news_from_api():
    url_api = 'https://newsapi.org/v2/everything?language=fr&q=Enedis&sortBy=publishedAt&apiKey=6333ea8eea65457a8f3250b947738292'
    req = requests.get(url_api)
    wb = req.json()
    articles = wb['articles']
    df_google_news = pd.DataFrame(articles)

    # Formater la date
    df_google_news['publishedAt'] = pd.to_datetime(df_google_news['publishedAt']).dt.date

    return df_google_news

# Fonction pour afficher un article
def display_article(article):
    article_link = article['url']
    if article['urlToImage']:
        try:
            # Charger l'image avec une taille maximale
            image = Image.open(io.BytesIO(requests.get(article['urlToImage']).content))

            # Afficher l'image dans un bloc avec une hauteur fixe
            st.markdown(
                """
                <div class="image-container">
                    <img src="{0}" alt="{1}" width="100%">
                </div>
                """.format(article['urlToImage'], article['title']),
                unsafe_allow_html=True
            )

            # Afficher le titre de l'article avec le texte "Titre :" en gras avant
            st.markdown("<div style='text-align: center;'><p style='font-size: 14px;'><span style='font-weight: bold;'>{}</span></p></div>".format(article['title']), unsafe_allow_html=True)

            # Date de publication
            formatted_date = pd.to_datetime(article['publishedAt']).strftime('%d/%m/%Y')
            st.markdown("<div style='text-align: center;'><p style='font-size: 14px;'>Date de publication : {}</p></div>".format(formatted_date), unsafe_allow_html=True)

            # Lien de l'article
            st.markdown("<div style='text-align: center;'><a href='{0}' target='_blank'>Voir l'article complet</a></div>".format(article_link), unsafe_allow_html=True)

        except requests.exceptions.RequestException as e:
            st.write(f"Erreur lors du chargement de l'image : {article['urlToImage']}")

# Page pour le scrapping
def page_scrapping():
    st.title("")
    st.markdown(
        f"""
        <style>
        .logo-container {{
            position: relative;
            width: 100%;
            text-align: center;
        }}
        .logo-image {{
            max-width: 150px;
            max-height: 150px;
            margin: 0 auto;
        }}
        .title {{
            text-align: center;
        }}
        .image-container img {{
            max-height: 180px;
        }}
        </style>
        <div class="logo-container">
            <img class="logo-image" src="data:image/jpeg;base64,{image_base64}" alt="Logo">
            <h1 class="title">Les dernières actualités Enedis</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Récupérer les articles
    result_df = get_news_from_api()

    # Afficher les 10 actualités les plus récentes
    num_articles = min(10, len(result_df))  # Limitation aux 10 articles les plus récents

    # Display articles in two columns
    for i in range(0, num_articles, 2):
        st.write('---')
        col1, col2 = st.columns([1, 1])

        article1 = result_df.iloc[i]

        # Check if there is another article for the second column
        if i+1 < num_articles:
            article2 = result_df.iloc[i+1]
        else:
            article2 = None

        with col1:
            display_article(article1)

        with col2:
            if article2 is not None:
                display_article(article2)


def page_lien_tableau():
    # Specify your Tableau Public visualization HTML code
    tableau_html = """
    <div class='tableauPlaceholder' id='viz1690297103889' style='position: relative'><noscript><a href='#'><img alt='ETUDE ENEDIS ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Pr&#47;Projet3_16902815278390&#47;ETUDEENEDIS&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Projet3_16902815278390&#47;ETUDEENEDIS' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Pr&#47;Projet3_16902815278390&#47;ETUDEENEDIS&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='fr-FR' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1690297103889');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='1016px';vizElement.style.height='991px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
    """
    # Render the Tableau Public visualization
    st.components.v1.html(tableau_html, height=1827, width=1000)


def main():
    pages = {
        "Fil d'actualités": page_scrapping,
        "Tableau de bord": page_lien_tableau
    }

    st.sidebar.title("Navigation")
    choix_page = st.sidebar.selectbox("Choisissez une page", tuple(pages.keys()))

    # Appeler la fonction correspondant à la page sélectionnée
    pages[choix_page]()

if __name__ == "__main__":
    main()
