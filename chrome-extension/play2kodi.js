chrome.browserAction.onClicked.addListener((tab) => {
    var headers = new Headers();
    headers.set('Content-Type', 'application/json');

    fetch('http://192.168.0.105:5000/player', {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({
            url: tab.url
        }),
    })
});
