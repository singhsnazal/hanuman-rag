// ✅ Upload multiple PDFs at once (robust JSON handling)
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

    // ✅ file size limit (Render free tier safety)
    if(file.size > 10 * 1024 * 1024){
      bubble(`❌ Skipped ${file.name} (Too large > 10MB)`, "ai");
      continue;
    }

    typingIndicator();

    const formData = new FormData();
    formData.append("file", file);

    try{
      const res = await fetch(`/upload?session_id=${encodeURIComponent(SESSION_ID)}`, {
        method: "POST",
        body: formData
      });

      // ✅ Read plain text first
      const txt = await res.text();

      // ✅ Try JSON parse safely
      let data = {};
      try{
        data = JSON.parse(txt);
      }catch(e){
        removeTyping();
        bubble(`❌ Upload failed: ${file.name} → Server returned non-JSON response`, "ai");
        bubble(`⚠️ Response preview: ${txt.slice(0, 200)}`, "ai");
        continue;
      }

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
