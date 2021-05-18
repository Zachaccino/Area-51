function(keys, values) {
    var pos_polarity = [];
    // var langs = [];
    var count = 0;
    keys.forEach(function (key) {
        var pol = key[0]
        if (pol > 0) {
            pos_polarity.push(pol);
            count++;
        }
    })
    return { positive_polarity: pos_polarity };
}