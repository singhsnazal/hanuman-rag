const chat = document.getElementById("chat");
const query = document.getElementById("query");
const sendBtn = document.getElementById("sendBtn");
const clearBtn = document.getElementById("clearBtn");
const fileInput = document.getElementById("fileInput");
const uploadBtn = document.getElementById("uploadBtn");
const newSessionBtn = document.getElementById("newSessionBtn");

// ✅ Production: keep session stable in localStorage
let SESSION_ID = localStorage.getItem("session_id");

async function initSession(){
  try{
    if(!SESSION_ID){
      const res = await fetch("/session");
      if(!res.ok) throw new Error("Failed to create session");
      const data = await res.json();
      SESSION_ID = data.session_id;
      localStorage.setItem("session_id", SESSION_ID);
    }
    bubble(`✅ Session ready: ${SESSION_ID.slice(0, 8)}...`, "ai");
  }catch(err){
    bubble("❌ Session init failed: " + err.message, "ai");
  }
}

function timeNow(){
  const d = new Date();
  return d.toLocaleTimeString([], {hour:"2-digit", minute:"2-digit"});
}

function bubble(text, who="ai", sources=null){
  const wrap = document.createElement("div");
  wrap.className = `bubble ${who}`;
  wrap.innerHTML = `
    <div>${escapeHtml(text)}</div>
    <div class="meta">${who === "user" ? "You" : "Hanuman AI"} • ${timeNow()}</div>
  `;

  if (sources && sources.length){
    const s = document.createElement("div");
    s.className = "sources";
    s.innerHTML = `
      <b>📌 Sources</b>
      <ul>${sources.map(x => `<li>${escapeHtml(x)}</li>`).join("")}</ul>
    `;
    wrap.appendChild(s);
  }

  chat.appendChild(wrap);
  chat.scrollTop = chat.scrollHeight;
}

function typingIndicator(){
  const t = document.createElement("div");
  t.className = "typing";
  t.id = "typing";
  t.innerHTML = `<div class="dot"></div><div class="dot"></div><div class="dot"></div>`;
  chat.appendChild(t);
  chat.scrollTop = chat.scrollHeight;
}

function removeTyping(){
  const t = document.getElementById("typing");
  if (t) t.remove();
}

function escapeHtml(str){
  return str.replace(/[&<>"']/g, m => ({
    "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"
  }[m]));
}

// ✅ UPDATED askApi: includes session_id
async function askApi(question){
  const res = await fetch("/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      session_id: SESSION_ID,
      question: question
    })
  });

  if(!res.ok){
    const txt = await res.text();
    throw new Error(`API Error ${res.status}: ${txt}`);
  }
  return await res.json();
}

async function send(){
  const q = query.value.trim();
  if(!q) return;

  if(!SESSION_ID){
    bubble("❌ Session not ready. Refresh page.", "ai");
    return;
  }

  bubble(q, "user");
  query.value = "";
  query.focus();

  typingIndicator();

  try{
    const data = await askApi(q);
    removeTyping();
    bubble(data.answer || "No answer", "ai", data.sources || []);
  }catch(err){
    removeTyping();
    bubble("❌ " + err.message, "ai");
  }
}

sendBtn.addEventListener("click", send);
query.addEventListener("keydown", (e)=>{
  if(e.key === "Enter") send();
});

clearBtn.addEventListener("click", ()=>{
  chat.innerHTML = "";
  bubble("Hi 👋 I’m Hanuman AI. Upload PDFs and ask questions.", "ai");
});

bubble("Hi 👋 I’m Hanuman AI. Upload PDFs and ask questions.", "ai");

// ✅ Upload multiple PDFs at once
async function uploadPDF(){
  if(!SESSION_ID){
    bubble("❌ Session not ready. Refresh page.", "ai");
    return;
  }

  const files = fileInput.files;
  if(!files || files.length === 0){
    bubble("❌ Please select PDF file(s) first.", "ai");
    return;
  }

  bubble(`📄 Uploading ${files.length} PDF(s)...`, "user");

  for(let i = 0; i < files.length; i++){
    const file = files[i];

    typingIndicator();

    const formData = new FormData();
    formData.append("file", file);

    try{
      const res = await fetch(`/upload?session_id=${encodeURIComponent(SESSION_ID)}`, {
        method: "POST",
        body: formData
      });

      const data = await res.json();
      removeTyping();

      if(!res.ok){
        bubble(`❌ Upload failed: ${file.name} → ${data.error || "Unknown error"}`, "ai");
      } else {
        bubble(`✅ Indexed: ${file.name}`, "ai");
      }
    }catch(err){
      removeTyping();
      bubble(`❌ Upload error: ${file.name} → ${err.message}`, "ai");
    }
  }

  bubble("✅ All uploads completed.", "ai");
  fileInput.value = "";
}

uploadBtn.addEventListener("click", uploadPDF);

// ✅ New Session button
newSessionBtn.addEventListener("click", async ()=>{
  localStorage.removeItem("session_id");
  SESSION_ID = null;
  chat.innerHTML = "";
  bubble("🆕 Starting new session...", "ai");
  await initSession();
});

// ✅ init session immediately on page load
initSession();
