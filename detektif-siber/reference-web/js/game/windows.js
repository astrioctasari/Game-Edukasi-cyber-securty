// Layar dasar, jendela ala desktop, taskbar, dan notifikasi.

// Notifikasi kecil di layar
function toast(t, f) {
  if (!S.nt && !f) return;
  const e = $("#toast");
  e.textContent = t;
  e.style.display = "block";
  clearTimeout(toast.t);
  toast.t = setTimeout(() => (e.style.display = "none"), 2800);
  if (S.lg == "en") tr(e, "en");
}

// Warna bergantian untuk spanduk
const COL = ["#ff7a6b", "#6cc4ff", "#3dc6ff", "#ffd95a", "#a9b3ff"];

// Spanduk judul berwarna
const banner = (p) =>
  '<div class="sbn" style="background:' +
  COL[p[0].length % 5] +
  '"><b>' +
  p[1] +
  "</b><small>" +
  p[0] +
  "</small></div>";

// Sesuaikan tinggi jendela supaya tidak keluar dari meja
function fit(d) {
  if (matchMedia("(max-width:760px)").matches || d.id == "w-err") return;
  d.style.maxHeight = Math.max(160, desk.clientHeight - 46 - d.offsetTop) + "px";
}

// Bawa jendela ke depan dan jadikan aktif
function focus(d) {
  d.classList.remove("min");
  fit(d);
  desk.querySelectorAll(".w").forEach((x) => x.classList.remove("act"));
  d.classList.add("act");
  d.style.zIndex = ++z;
  tbar();
}

// Gambar ulang taskbar (daftar jendela yang terbuka)
function tbar() {
  const b = $("#tbw");
  if (!b || !desk) return;
  b.innerHTML = [...desk.querySelectorAll(".w.on")]
    .filter((w) => w.id != "w-err")
    .map(
      (w) =>
        '<button class="btn g tbb' +
        (w.classList.contains("act") ? " on" : "") +
        (w.classList.contains("min") ? " mn" : "") +
        '" data-w="' +
        w.id +
        '">' +
        w.querySelector(".tb span").innerHTML +
        "</button>"
    )
    .join("");
  b.onclick = (e) => {
    const t = e.target.closest("[data-w]");
    if (t) {
      const x = $("#" + t.dataset.w);
      if (x.classList.contains("act") && !x.classList.contains("min")) {
        x.classList.add("min");
        x.classList.remove("act");
        tbar();
      } else focus(x);
    }
  };
}

// Jendela kecil untuk pesan kesalahan
function errBox(m) {
  const o = $("#w-err");
  if (o) o.remove();
  const d = document.createElement("div");
  d.className = "w on act";
  d.id = "w-err";
  d.style.cssText =
    "left:50%;top:34%;width:310px;transform:translate(-50%,-50%);z-index:" + (z + 60);
  d.innerHTML =
    '<div class="tb"><span>⛔ Error</span><span class="wc"><button aria-label="Tutup">×</button></span></div><div class="bd" style="display:flex;gap:12px;align-items:center"><div style="font-size:42px">🚨</div><div>' +
    esc(m) +
    '</div></div><div class="bd" style="text-align:right;padding-top:0"><button class="btn" id="eok">OK</button></div>';
  desk.append(d);
  const c = () => d.remove();
  d.querySelector("button").onclick = c;
  $("#eok").onclick = c;
}

// Buat jendela beserta ikonnya dari daftar W; yang ada di open langsung dibuka
function mk(W, open) {
  Object.entries(W).forEach(([k, v]) => {
    const d = document.createElement("div");
    d.className = "w";
    d.id = "w-" + k;
    d.style.cssText =
      "left:" +
      ($("#ics2") && !matchMedia("(max-width:760px)").matches ? Math.max(v[2], 156) : v[2]) +
      "px;top:" +
      v[3] +
      "px;width:" +
      v[4] +
      "px";
    d.innerHTML =
      '<div class="tb"><span>' +
      ico(v[0]) +
      " " +
      v[1] +
      '</span><span class="wc"><i>–</i><i>▢</i><button aria-label="Tutup">×</button></span></div><div class="bd">' +
      v[5] +
      "</div>";
    desk.append(d);
    const h = d.querySelector(".tb");
    d.onpointerdown = () => focus(d);
    h.querySelector("button").onclick = () => {
      d.classList.remove("on");
      tbar();
    };
    const wi = h.querySelectorAll("i");
    wi[0].title = "Perkecil";
    wi[1].title = "Perbesar";
    wi[0].onclick = () => {
      d.classList.add("min");
      d.classList.remove("act");
      tbar();
    };
    wi[1].onclick = () => {
      d.classList.toggle("mx");
      focus(d);
    };
    h.ondblclick = (e) => {
      if (e.target.tagName != "BUTTON" && e.target.tagName != "I") {
        d.classList.toggle("mx");
        focus(d);
      }
    };
    h.onpointerdown = (e) => {
      if (e.target.tagName == "BUTTON" || e.target.tagName == "I" || d.classList.contains("mx"))
        return;
      h.setPointerCapture(e.pointerId);
      const ox = e.clientX - d.offsetLeft,
        oy = e.clientY - d.offsetTop;
      h.onpointermove = (m) => {
        d.style.left = Math.max(0, Math.min(desk.clientWidth - 60, m.clientX - ox)) + "px";
        d.style.top = Math.max(0, Math.min(desk.clientHeight - 70, m.clientY - oy)) + "px";
        fit(d);
      };
      h.onpointerup = () => {
        h.onpointermove = null;
      };
    };
    const b = document.createElement("button");
    b.className = "ic";
    b.innerHTML = "<span>" + ico(v[0]) + "</span>" + v[1];
    b.onclick = () => {
      d.classList.add("on");
      focus(d);
    };
    ($("#ics2") && ["edu", "profil", "set"].includes(k) && !matchMedia("(max-width:760px)").matches
      ? $("#ics2")
      : $("#ics")
    ).append(b);
  });
  (open || []).forEach((k) => {
    const e = $("#w-" + k);
    e.classList.add("on");
    fit(e);
  });
  if (open && open.length) focus($("#w-" + open[open.length - 1]));
  else tbar();
}

// Tampilkan satu layar dengan jendela di tengah
const show = (h, t) => {
  cancelAnimationFrame(raf);
  $("#scr").innerHTML =
    '<div class="desk" id="desk">' +
    WALL +
    '<div class="winC"><div class="tb"><span>' +
    (t || "") +
    '</span><span class="wc"><i>–</i><i>▢</i><i>×</i></span></div><div class="bd2">' +
    h +
    "</div></div></div>";
};
