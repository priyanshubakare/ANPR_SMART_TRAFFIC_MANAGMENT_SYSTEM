const file=document.getElementById("file"),go=document.getElementById("go");
const status=document.getElementById("status"),result=document.getElementById("result");
const image=document.getElementById("image"),details=document.getElementById("details");

go.onclick=async()=>{
 if(!file.files.length){status.textContent="Select an image first.";return}
 const fd=new FormData(); fd.append("file",file.files[0]);
 status.textContent="Processing..."; result.classList.add("hidden");
 try{
  const r=await fetch("/api/detect",{method:"POST",body:fd});
  const d=await r.json(); if(!r.ok) throw new Error(d.error);
  status.textContent=d.plate_model_loaded?"Detection completed.":"Plate model missing: add weights/plate_detector.pt";
  image.src="/outputs/"+d.result_image;
  details.innerHTML=d.plates.map((p,i)=>`<p><b>Plate ${i+1}:</b> ${p.text||"Not recognized"}<br>Detection: ${p.detection_confidence}<br>OCR: ${p.ocr_confidence}</p>`).join("");
  details.innerHTML+=`<p><b>Traffic:</b> ${d.traffic.traffic_level} — ${d.traffic.recommendation}</p>`;
  result.classList.remove("hidden");
 }catch(e){status.textContent=e.message}
};
