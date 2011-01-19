function(doc) {
    if (doc.type != "user")
        return;
	
    emit([doc.name, doc.password]);
}
