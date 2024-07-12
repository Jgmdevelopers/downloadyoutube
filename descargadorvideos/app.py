import yt_dlp as youtube_dl
import streamlit as st

class YouTubeDownloader:
    def __init__(self, url):
        self.url = url
        self.info = None
        self.stream = None

    def fetch_info(self):
        ydl_opts = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            self.info = ydl.extract_info(self.url, download=False)

    def showTitle(self):
        st.write(f"**Título:** {self.info['title']}")
        self.showStreams()

    def showStreams(self):
        formats = self.info['formats']
        stream_options = [
            f"Resolución: {f.get('height', 'N/A')} / FPS: {f.get('fps', 'N/A')} / Tipo: {f.get('ext', 'N/A')} / Audio: {'Sí' if f.get('acodec') != 'none' else 'No'}"
            for f in formats if f.get('height') is not None or f.get('acodec') != 'none'
        ]
        choice = st.selectbox("Elija una opción de stream: ", stream_options)
        self.stream = formats[stream_options.index(choice)]

    def getFileSize(self):
        file_size = self.stream.get('filesize', 0) / 1000000
        return file_size

    def getPermissionToContinue(self, file_size):
        st.write(f"**Titulo:** {self.info['title']}")
        st.write(f"**Autor:** {self.info['uploader']}")
        st.write(f"**Tamaño:** {file_size:.2f} MB")
        st.write(f"**Resolución:** {self.stream.get('height', 'N/A')}")
        st.write(f"**FPS:** {self.stream.get('fps', 'N/A')}")
        st.write(f"**Audio:** {'Sí' if self.stream.get('acodec') != 'none' else 'No'}")

        if st.button("Descargar"):
            self.download()

    def download(self):
        # Verificar si el formato seleccionado tiene audio y video
        has_audio = self.stream.get('acodec') != 'none'
        has_video = self.stream.get('vcodec') != 'none'

        if has_audio and has_video:
            ydl_opts = {'format': self.stream['format_id']}
        else:
            # Descargar video y audio por separado y combinarlos
            ydl_opts = {'format': 'bestvideo+bestaudio/best'}

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])

        st.success("Descarga Completa!")

if __name__ == "__main__":
    st.title("Descargador de videos de YouTube")
    url = st.text_input("Ingrese la URL del video: ")
    if url:
        downloader = YouTubeDownloader(url)
        downloader.fetch_info()
        downloader.showTitle()
        file_size = downloader.getFileSize()
        downloader.getPermissionToContinue(file_size)
