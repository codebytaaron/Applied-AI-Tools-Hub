function track(linkId) {
    fetch(`/click/${linkId}`)
        .then(() => loadStats());
}

function loadStats() {
    fetch("/stats")
        .then(res => res.json())
        .then(data => {
            document.getElementById("stats").textContent =
                JSON.stringify(data.links, null, 2);
        });
}

loadStats();
