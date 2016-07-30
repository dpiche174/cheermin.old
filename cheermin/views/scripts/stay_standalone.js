(function(document, navigator, standalone) {
    // Prevents links from apps from opening in mobile safari this javascript must be the first script in your <head>.
    if ((standalone in navigator) && navigator[standalone]) {
        document.addEventListener('click', function(event) {
            noddy = event.target;

            // Bubble up until we hit link or top HTML element. Warning: BODY element is not compulsory so better to stop on HTML
            while (noddy.nodeName !== "A" && noddy.nodeName !== "HTML") {
                noddy = noddy.parentNode;
            }

            if ('href' in noddy && noddy.href.indexOf('http') !== -1 && noddy.href.indexOf(document.location.host) !== -1) {
                event.preventDefault();
                document.location.href = noddy.href;
            }
        }, false);
    }
})(document, window.navigator, 'standalone');
