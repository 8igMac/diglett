async function get_emb(name) {
  // Decide which audio file to request.
  let filename = "";
  let id = "";
  if (name == "homer") {
    filename = "homer.wav";
    id = "homer_status";
  } else if (name == "marge") {
    filename = "marge.wav";
    id = "marge_status";
  }

  // Fetch audio from the server.
  let res = await fetch(`/demo/${filename}`);
  const data = await res.blob();

  // Craft multipart/formdata.
  const formData = new FormData();
  formData.append("file", data);

  // Send POST request for embeddings.
  res = await fetch("/embed", {
    method: "POST",
    body: formData,
  });
  const json = await res.json();
  console.log(json);

  // Update status.
  let status = document.getElementById(id);
  status.innerHTML = "got embeddings"
  
}