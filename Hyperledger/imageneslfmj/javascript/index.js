var server = require("./server");
var router = require("./router");
var requestHandlers = require("./requestHandlers");

var handle = {}
handle["/"] = requestHandlers.iniciar;
handle["/iniciar"] = requestHandlers.iniciar;
handle["/subir"] = requestHandlers.subir;
handle["/getAllImages"] = requestHandlers.queryAllImages;
handle["/changeOwner"] = requestHandlers.changeOwner;
handle["/getHistory"] = requestHandlers.getHistory;
handle["/getImage"] = requestHandlers.getImage;
handle["/createImage"] = requestHandlers.createImage;
handle["/verifiability"] = requestHandlers.getVerifiability
handle["/getLastHash"] = requestHandlers.getLastHash;

handle["/state"] = requestHandlers.getState;
handle["/creator"] = requestHandlers.getCreator;
handle["/binding"] = requestHandlers.getBinding;
handle["/txid"] = requestHandlers.getTxID;
handle["/txtime"] = requestHandlers.getTxTimestamp;

server.iniciar(router.route, handle);