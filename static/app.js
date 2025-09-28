document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("uploadForm");
  const fileinput = document.getElementById("fileinput");
  const uploadResult = document.getElementById("uploadResult");
  const btnGet = document.getElementById("btnGet");
  const testTable = document.getElementById("testTable");
  const apiResult = document.getElementById("apiResult");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const f = fileinput.files[0];
    if (!f) return alert("Choose a file first");
    const fd = new FormData();
    fd.append("file", f);
    uploadResult.textContent = "Uploading...";
    try {
      const res = await fetch("/upload", { method: "POST", body: fd });
      const j = await res.json();
      uploadResult.textContent = JSON.stringify(j, null, 2);
      setTimeout(() => location.reload(), 800);
    } catch (err) {
      uploadResult.textContent = "Error: " + err;
    }
  });

  btnGet.addEventListener("click", async () => {
    const t = testTable.value.trim();
    if (!t) { alert("Enter table name exactly as shown."); return; }
    apiResult.textContent = "Loading...";
    try {
      const r = await fetch(`/api/${encodeURIComponent(t)}`);
      const j = await r.json();
      apiResult.textContent = JSON.stringify(j, null, 2);
    } catch (e) {
      apiResult.textContent = "Error: " + e;
    }
  });

  // attach small handlers to dynamic links
  document.querySelectorAll("a.view").forEach(a => {
    a.addEventListener("click", async (ev) => {
      ev.preventDefault();
      const t = ev.target.dataset.table;
      testTable.value = t;
      document.getElementById("btnGet").click();
    });
  });
});
