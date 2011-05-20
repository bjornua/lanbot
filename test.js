var net = require('net');
var sys = require('sys');

var Parser = function(){
    self.buffer = "";
}
Parser.onData = function(buffer){
    self.buffer += buffer.toString("binary");
    console.log(buffer.toString("binary"));
}

var Client = function(){}

Client.prototype.start = function(host, port){
};

var conn = net.Socket();

conn.on("connect", function(){
    console.log("Successfully connected");
    this.buffer = "";
    

});

client = new Client("irc.freenode.net", 6667);
