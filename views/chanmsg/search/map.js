function(doc) {
    if (doc.type !== "chanmsg")
        return;
    
    words = doc.msg.split(" ");
    words.map(function(word){
        return word.trim()
    });
    words.filter(function(word){
        return word.length > 0;
    });
    
    words.forEach(function(word){
        emit([doc.channel, word, doc.time], null);
    });
    
}
