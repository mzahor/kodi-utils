chrome.browserAction.onClicked.addListener((tab) => {
    var headers = new Headers();
    headers.set('Content-Type', 'application/json');

    fetch('http://localhost:5000/player', {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({
            url: tab.url
        }),
    })
});
