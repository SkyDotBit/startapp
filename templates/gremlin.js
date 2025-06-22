const gremlin = document.getElementById("gremlin")
function grimlies () {
    fetch('/output')
        .then(response => {
            console.log(response.text);
            for (line in response.text) {
                buildline += line + "\n";
            gremlin.innerHTML = buildline;
        }})
        .catch(error => {
            console.log(error);
            gremlin.innerHTML = error;
})};
setInterval(grimlies, 100);