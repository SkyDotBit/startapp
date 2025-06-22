const statuselement = document.getElementById("status");
const statuelement = document.getElementById("statu");
function statuss() {
    fetch("/status")
        .then(response => {
            if (response.ok) {
                statuselement.textContent = "Online 🟢";
                statuselement.style = "color: green;";
            } else {
                statuselement.textContent = "Offline 🔴";
                statuselement.style = "color: red;";
                window.location.reload();
            }
        })
        .catch(error => {
            statuselement.textContent = "Offline 🔴";
            statuselement.style = "color: red;";
            window.location.reload();
        });
    fetch("/statusscript")
        .then(response => {
            if (response.ok) {
                statuelement.textContent = "Online 🟢";
                statuelement.style = "color: green;";
            } else {
                statuelement.textContent = "Offline 🔴";
                statuelement.style = "color: red;";
                
            }
        })
        .catch(error => {
            statuelement.textContent = "Offline 🔴";
            statuelement.style = "color: red;";
            
        });
}
setInterval(statuss, 500);