**Autorzy**: Maciej Kozłowski, Jakub Stacherski

**Temat projektu**: Symulacja zawieszenia samochodowego

**Cel**: Znalezienie optymalnych parametrów zawieszenia samochodu, poruszającego się w danym środowisku.

**Założenia**:

- grafika 2D, widok od boku na pojedyncze koło

- samochód poruszający się ze stałą prędkością po płaskiej nawierzchni, na której pojawiają się przeszkody w kształcie półkoli

- możliwość regulacji parametrów sprężyny - współczynnik sprężystości, współczynnik tłumienia

- możliwość regulacji parametrów środowiska - grawitacja, częstotliwość występowania przeszkód

- reprezentacja położenia nadwozia oraz wychyłu sprężyny na wykresie aktualizowanym w czasie rzeczywistym

**Wykorzystane oprogramowanie:**

- Python 3.12 z wykorzystaniem bibliotek matplotlib (do generowania wykresów), pygame, pygame-widgets

**Dokładny sposób uruchomienia:**

- git clone <https://github.com/kozlowskimaciej/fizyka.git>

- cd fizyka

- pip install -r requirements.txt

- python simulation.py
