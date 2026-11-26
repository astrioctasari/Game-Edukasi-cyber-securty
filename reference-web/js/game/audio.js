// Suara: bunyi umpan balik dan musik latar.

// Konteks audio dan nada latar yang sedang menyala
let AX,
  PAD = null;

// Buat AudioContext saat pertama kali dibutuhkan
const actx = () => AX || (AX = new (window.AudioContext || window.webkitAudioContext)());

// Bunyi pendek untuk umpan balik
function beep(f) {
  if (!S.sf) return;
  try {
    const a = actx(),
      o = a.createOscillator(),
      g = a.createGain();
    o.frequency.value = f;
    o.type = "sine";
    g.gain.value = 0.05;
    o.connect(g);
    g.connect(a.destination);
    o.start();
    g.gain.exponentialRampToValueAtTime(0.0001, a.currentTime + 0.16);
    o.stop(a.currentTime + 0.18);
  } catch (e) {}
}

// Nyalakan atau matikan musik latar sesuai pengaturan
function ambient() {
  try {
    if (PAD) {
      PAD.forEach((o) => o.stop());
      PAD = null;
    }
    if (!S.mu) return;
    const a = actx(),
      g = a.createGain();
    g.gain.value = 0.02;
    g.connect(a.destination);
    PAD = [110, 164.8, 220.5].map((f) => {
      const o = a.createOscillator();
      o.type = "sine";
      o.frequency.value = f;
      o.connect(g);
      o.start();
      return o;
    });
  } catch (e) {}
}
