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

const budgetDisplay = document.getElementById("budget_display");
const budgetValue = document.getElementById("total_budget");

budgetDisplay.addEventListener("input", function(){
    let value = this.value.replace(/\D/g,"");

    budgetValue.value = value;

    if(value){
        this.value = "Rp" + Number(value).toLocaleString("id-ID");
    }else{
        this.value = "";
    }
});