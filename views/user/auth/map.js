function(doc) {
    if (doc.type != "user")
        return;
	
    emit([doc.username, doc.password]);
}
