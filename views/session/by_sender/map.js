function(doc) {
    if (doc.type !== "session")
        return;
	
    emit([doc.nickname, doc.host]);
}
