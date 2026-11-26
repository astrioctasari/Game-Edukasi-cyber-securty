// Titik awal game.

// Muat progres lalu tampilkan layar masuk
function init() {
  load();
  loginScreen();
  if (S.lg == "en") tr(document.body, "en");
}

// Jalankan game
init();
