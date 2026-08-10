const overlayAddTrip = document.getElementById("overlayAddTrip");
const btnAddTrip = document.getElementById("btnAddTrip");

btnAddTrip.addEventListener("click", () =>{
    overlayAddTrip.style.display = "flex";
});

overlayAddTrip.addEventListener("click", (e) =>{
    if(e.target === overlayAddTrip){
        overlayAddTrip.style.display = "none";
    }
});