var querystring = require("querystring");

const { Gateway, Wallets} = require('fabric-network');
const path = require('path');
const fs = require('fs');

function iniciar(response, postData) {
  console.log("Manipulador de peticion 'inicio' fue llamado.");

  var body = '<html>'+
    '<head>'+
    '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />'+
    '</head>'+
    '<body>'+
    '<form action="/subir" method="post">'+
    '<textarea name="text" rows="20" cols="60"></textarea>'+
    '<input type="submit" value="Submit text" />'+
    '</form>'+
    '</body>'+
    '</html>';

    response.writeHead(200, {"Content-Type": "text/html", 'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Methods': 'POST'});
    response.write(body);
    response.end();
}

function subir(response, dataPosteada) {
    console.log("Manipulador de peticion 'subir' fue llamado.");
    response.writeHead(200, {"Content-Type": "text/html", 'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Methods': 'POST'});
    response.write("Tu enviaste el texto: : " +
    querystring.parse(dataPosteada)["text"]);
    response.end();
}

// this function has comments of it's construction
async function queryAllImages(response){
  try {
    // load the network configuration
    const ccpPath = path.resolve(__dirname, '..', '..', 'image-network', 'organizations', 'peerOrganizations', 'org1.example.com', 'connection-org1.json');
    const ccp = JSON.parse(fs.readFileSync(ccpPath, 'utf8'));

    // create a new file system based wallet for managing identities.
    const walletPath = path.join(process.cwd(), 'wallet');
    const wallet = await Wallets.newFileSystemWallet(walletPath);
    console.log(`Wallet path: ${walletPath}`);

    // check to see if we've already enrolled the user.
    const identity = await wallet.get('appUser');
    if (!identity) {
      console.log('An identity for the user "appUser" does not exist in the wallet');
      console.log('Run the registerUser.js application before retrying');
      response.writeHead(500, {"Content-Type": "application/json"});
      response.write(JSON.stringify({'Result':'An identity for the user "appUser" does not exist in the wallet', 'Solution':'Run the registerUser.js application before retrying'}));
      response.end();
      return;
    }
    //console.log("SIGUE A PESAR DE NO TENER LA CREDENCIAL XD XD XD")

    // create a new gateway for connecting to our peer node.
    const gateway = new Gateway();
    await gateway.connect(ccp, { wallet, identity: 'appUser', discovery: { enabled: true, asLocalhost: true } });

    // get the network (channel) our contract is deployed to.
    const network = await gateway.getNetwork('mychannel');

    // get the contract from the network.
    const contract = network.getContract('imageneslfmj');


    // evaluate the specified transaction.
    // queryImage transaction - requires 1 argument, ex: ('queryImage', 'IMAGE0').
    // queryAllImages transaction - requires no argument, ex: ('queryAllImages').
    const result = await contract.evaluateTransaction('queryAllImages');
    console.log(`Transaction has been evaluated, result is: ${result.toString()}`);

    console.log(result.toString())

    await gateway.disconnect();

    response.writeHead(200, {"Content-Type": "application/json", 'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Methods': 'POST'});
    response.write(JSON.stringify(JSON.parse(result)));
    //response.write(JSON.stringify(result.toString()));
    response.end();
  } catch(error) {
      console.error(`Failed to evaluate transaction: ${error}`);
      response.writeHead(500, {"Content-Type": "application/json", 'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Methods': 'POST'});
      response.write(JSON.stringify({'Result':`Failed to evaluate transaction: ${error}`}));
      response.end();
      return;
  }

}

async function changeOwner(response, dataPosteada){
  try {
      // load the network configuration
      const ccpPath = path.resolve(__dirname, '..', '..', 'image-network', 'organizations', 'peerOrganizations', 'org1.example.com', 'connection-org1.json');
      let ccp = JSON.parse(fs.readFileSync(ccpPath, 'utf8'));

      // Create a new file system based wallet for managing identities.
      const walletPath = path.join(process.cwd(), 'wallet');
      const wallet = await Wallets.newFileSystemWallet(walletPath);
      console.log(`Wallet path: ${walletPath}`);

      // Check to see if we've already enrolled the user.
      const identity = await wallet.get('appUser');
      if (!identity) {
          console.log('An identity for the user "appUser" does not exist in the wallet');
          console.log('Run the registerUser.js application before retrying');
          response.writeHead(500, {"Content-Type": "application/json"});
          response.write(JSON.stringify({'Result':'An identity for the user "appUser" does not exist in the wallet', 'Solution':'Run the registerUser.js application before retrying'}));
          response.end();
          return;
      }

      // Create a new gateway for connecting to our peer node.
      const gateway = new Gateway();
      await gateway.connect(ccp, { wallet, identity: 'appUser', discovery: { enabled: true, asLocalhost: true } });

      // Get the network (channel) our contract is deployed to.
      const network = await gateway.getNetwork('mychannel');

      // Get the contract from the network.
      const contract = network.getContract('imageneslfmj');

      // Submit the specified transaction.

      // Get the variables
      datos = JSON.parse(dataPosteada);
      imageId = datos['id'];
      newOwner = datos['newO'];
      newL = datos['newL'];
      newBbDes = datos['newBbDes'];
      newTranId = datos['newTranId'];
      newConId = datos['newConId'];
      newS = datos['newS'];
      newPrevious_hash = datos['newPrevious_hash'];
      newActual_hash = datos['newActual_hash'];
      newTimestamp = datos['newTimestamp'];

      await contract.submitTransaction('changeImageOwner', imageId, newOwner, newL, newBbDes, newTranId, newConId, newS, newPrevious_hash, newActual_hash, newTimestamp);
      console.log('Transaction has been submitted');
      // Disconnect from the gateway.
      await gateway.disconnect();

      response.writeHead(200, {"Content-Type": "application/json", 'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Methods': 'POST'});
      response.write(JSON.stringify({'Result:':'Transaction CO done'}));
      //response.write(JSON.stringify(result.toString()));
      response.end();


  } catch (error) {
      console.error(`Failed to evaluate transaction: ${error}`);
      response.writeHead(500, {"Content-Type": "application/json", 'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Methods': 'POST'});
      response.write(JSON.stringify({'Result':`Failed to evaluate transaction: ${error}`}));
      response.end();
      return;
  }
}

async function getHistory(response, dataPosteada){
  try {
    // load the network configuration
        const ccpPath = path.resolve(__dirname, '..', '..', 'image-network', 'organizations', 'peerOrganizations', 'org1.example.com', 'connection-org1.json');
        let ccp = JSON.parse(fs.readFileSync(ccpPath, 'utf8'));

        // Create a new file system based wallet for managing identities.
        const walletPath = path.join(process.cwd(), 'wallet');
        const wallet = await Wallets.newFileSystemWallet(walletPath);
        console.log(`Wallet path: ${walletPath}`);

        // Check to see if we've already enrolled the user.
        const identity = await wallet.get('appUser');
        if (!identity) {
            console.log('An identity for the user "appUser" does not exist in the wallet');
            console.log('Run the registerUser.js application before retrying');
            response.writeHead(500, {"Content-Type": "application/json"});
            response.write(JSON.stringify({'Result':'An identity for the user "appUser" does not exist in the wallet', 'Solution':'Run the registerUser.js application before retrying'}));
            response.end();
            return;
        }

        // Create a new gateway for connecting to our peer node.
        const gateway = new Gateway();
        await gateway.connect(ccp, { wallet, identity: 'appUser', discovery: { enabled: true, asLocalhost: true } });

        // Get the network (channel) our contract is deployed to.
        const network = await gateway.getNetwork('mychannel');

        // Get the contract from the network.
        const contract = network.getContract('imageneslfmj');

        // Submit the specified transaction.

        // Get the variables
        datos = JSON.parse(dataPosteada);
        imageId = datos['id'];

        const result = await contract.evaluateTransaction('historyImage', imageId);
        console.log(`Transaction has been evaluated, result is: ${result.toString()}`);

        // Disconnect from the gateway.
        await gateway.disconnect();

        response.writeHead(200, {"Content-Type": "application/json", 'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Methods': 'POST'});
        response.write(JSON.stringify(JSON.parse(result)));
        //response.write(JSON.stringify(result.toString()));
        response.end();
    } catch (error) {
        console.error(`Failed to evaluate transaction: ${error}`);
        response.writeHead(500, {"Content-Type": "application/json", 'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Methods': 'POST'});
        response.write(JSON.stringify({'Result':`Failed to evaluate transaction: ${error}`}));
        response.end();
        return;
    }
}

async function getImage(response, dataPosteada){
  try {
    // load the network configuration
        const ccpPath = path.resolve(__dirname, '..', '..', 'image-network', 'organizations', 'peerOrganizations', 'org1.example.com', 'connection-org1.json');
        let ccp = JSON.parse(fs.readFileSync(ccpPath, 'utf8'));

        // Create a new file system based wallet for managing identities.
        const walletPath = path.join(process.cwd(), 'wallet');
        const wallet = await Wallets.newFileSystemWallet(walletPath);
        console.log(`Wallet path: ${walletPath}`);

        // Check to see if we've already enrolled the user.
        const identity = await wallet.get('appUser');
        if (!identity) {
            console.log('An identity for the user "appUser" does not exist in the wallet');
            console.log('Run the registerUser.js application before retrying');
            response.writeHead(500, {"Content-Type": "application/json"});
            response.write(JSON.stringify({'Result':'An identity for the user "appUser" does not exist in the wallet', 'Solution':'Run the registerUser.js application before retrying'}));
            response.end();
            return;
        }

        // Create a new gateway for connecting to our peer node.
        const gateway = new Gateway();
        await gateway.connect(ccp, { wallet, identity: 'appUser', discovery: { enabled: true, asLocalhost: true } });

        // Get the network (channel) our contract is deployed to.
        const network = await gateway.getNetwork('mychannel');

        // Get the contract from the network.
        const contract = network.getContract('imageneslfmj');

        // Submit the specified transaction.

        // Get the variables
        datos = JSON.parse(dataPosteada);
        imageId = datos['id'];

        const result = await contract.evaluateTransaction('queryImage', imageId);
        console.log(`Transaction has been evaluated, result is: ${result.toString()}`);

        // Disconnect from the gateway.

        await gateway.disconnect();

        response.writeHead(200, {"Content-Type": "application/json", 'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Methods': 'POST'});
        response.write(JSON.stringify(JSON.parse(result)));
        //response.write(JSON.stringify(result.toString()));
        response.end();
    } catch (error) {
        console.error(`Failed to evaluate transaction: ${error}`);
        response.writeHead(500, {"Content-Type": "application/json", 'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Methods': 'POST'});
        response.write(JSON.stringify({'Result':`Failed to evaluate transaction: ${error}`}));
        response.end();
        return;
    }
}

async function createImage(response, dataPosteada){
  try {
    // load the network configuration
        const ccpPath = path.resolve(__dirname, '..', '..', 'image-network', 'organizations', 'peerOrganizations', 'org1.example.com', 'connection-org1.json');
        let ccp = JSON.parse(fs.readFileSync(ccpPath, 'utf8'));

        // Create a new file system based wallet for managing identities.
        const walletPath = path.join(process.cwd(), 'wallet');
        const wallet = await Wallets.newFileSystemWallet(walletPath);
        console.log(`Wallet path: ${walletPath}`);

        // Check to see if we've already enrolled the user.
        const identity = await wallet.get('appUser');
        if (!identity) {
            console.log('An identity for the user "appUser" does not exist in the wallet');
            console.log('Run the registerUser.js application before retrying');
            response.writeHead(500, {"Content-Type": "application/json"});
            response.write(JSON.stringify({'Result':'An identity for the user "appUser" does not exist in the wallet', 'Solution':'Run the registerUser.js application before retrying'}));
            response.end();
            return;
        }

        // Create a new gateway for connecting to our peer node.
        const gateway = new Gateway();
        await gateway.connect(ccp, { wallet, identity: 'appUser', discovery: { enabled: true, asLocalhost: true } });

        // Get the network (channel) our contract is deployed to.
        const network = await gateway.getNetwork('mychannel');

        // Get the contract from the network.
        const contract = network.getContract('imageneslfmj');

        // Submit the specified transaction.

        // Get the variables
        datos = JSON.parse(dataPosteada);
        imageId = datos['id'];
        organization_name = datos['organizationName'];
        level = datos['level'];
        building_block_description = datos['builDescription'];
        transaction_id = datos['tranId'];
        content_id = datos['conId'];
        file_name = datos['fileName'];
        status = datos['status'];
        newPrevious_hash = datos['newPrevious_hash'];
        newActual_hash = datos['newActual_hash'];
        newTimestamp = datos['newTimestamp'];


        await contract.submitTransaction('createImage', imageId, organization_name, level, building_block_description, transaction_id, content_id, file_name, status, newPrevious_hash, newActual_hash, newTimestamp);
        console.log('Transaction has been submitted');

        // Disconnect from the gateway.

        await gateway.disconnect();

        response.writeHead(200, {"Content-Type": "application/json", 'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Methods': 'POST'});
        response.write(JSON.stringify({'Result':'Transaction CI has been submitted'}));
        //response.write(JSON.stringify(result.toString()));
        response.end();
    } catch (error) {
        console.error(`Failed to evaluate transaction: ${error}`);
        response.writeHead(500, {"Content-Type": "application/json", 'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Methods': 'POST'});
        response.write(JSON.stringify({'Result':`Failed to evaluate transaction: ${error}`}));
        response.end();
        return;
    }
}


async function getState(response, dataPosteada){
  try {
        const ccpPath = path.resolve(__dirname, '..', '..', 'image-network', 'organizations', 'peerOrganizations', 'org1.example.com', 'connection-org1.json');
        let ccp = JSON.parse(fs.readFileSync(ccpPath, 'utf8'));

        const walletPath = path.join(process.cwd(), 'wallet');
        const wallet = await Wallets.newFileSystemWallet(walletPath);
        //console.log(`Wallet path: ${walletPath}`);

        const identity = await wallet.get('appUser');
        if (!identity) {
            console.log('An identity for the user "appUser" does not exist in the wallet');
            console.log('Run the registerUser.js application before retrying');
            response.writeHead(500, {"Content-Type": "application/json"});
            response.write(JSON.stringify({'Result':'An identity for the user "appUser" does not exist in the wallet', 'Solution':'Run the registerUser.js application before retrying'}));
            response.end();
            return;
        }

        const gateway = new Gateway();
        await gateway.connect(ccp, { wallet, identity: 'appUser', discovery: { enabled: true, asLocalhost: true } });

        const network = await gateway.getNetwork('mychannel');

        const contract = network.getContract('imageneslfmj');

        datos = JSON.parse(dataPosteada);
        imageId = datos['id'];

        const result = await contract.evaluateTransaction('getState', imageId);
        console.log(`Transaction has been evaluated, result is: ${result.toString()}`);

        await gateway.disconnect();

        data2send = JSON.parse(result);

        console.log(result.toString());

        response.writeHead(200, {"Content-Type": "application/json", 'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Methods': 'POST'});
        response.write(JSON.stringify(JSON.parse(result)));
        response.end();
    } catch (error) {
        console.error(`Failed to evaluate transaction: ${error}`);
        response.writeHead(500, {"Content-Type": "application/json", 'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Methods': 'POST'});
        response.write(JSON.stringify({'Result':`Failed to evaluate transaction: ${error}`}));
        response.end();
        return;
    }
}

async function getCreator(response){
  try {
    const ccpPath = path.resolve(__dirname, '..', '..', 'image-network', 'organizations', 'peerOrganizations', 'org1.example.com', 'connection-org1.json');
    let ccp = JSON.parse(fs.readFileSync(ccpPath, 'utf8'));

    const walletPath = path.join(process.cwd(), 'wallet');
    const wallet = await Wallets.newFileSystemWallet(walletPath);
    //console.log(`Wallet path: ${walletPath}`);

    const identity = await wallet.get('appUser');
    if (!identity) {
        console.log('An identity for the user "appUser" does not exist in the wallet');
        console.log('Run the registerUser.js application before retrying');
        response.writeHead(500, {"Content-Type": "application/json"});
        response.write(JSON.stringify({'Result':'An identity for the user "appUser" does not exist in the wallet', 'Solution':'Run the registerUser.js application before retrying'}));
        response.end();
        return;
    }

    const gateway = new Gateway();
    await gateway.connect(ccp, { wallet, identity: 'appUser', discovery: { enabled: true, asLocalhost: true } });

    const network = await gateway.getNetwork('mychannel');

    const contract = network.getContract('imageneslfmj');

    const result = await contract.evaluateTransaction('getCreator');
    console.log(`Transaction has been evaluated, result is: ${result.toString()}`);
    
    await gateway.disconnect();

    response.writeHead(200, {"Content-Type": "application/json", 'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Methods': 'POST'});
    response.write(JSON.stringify(JSON.parse(result)));
    response.end();
} catch (error) {
    console.error(`Failed to evaluate transaction: ${error}`);
    response.writeHead(500, {"Content-Type": "application/json", 'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Methods': 'POST'});
    response.write(JSON.stringify({'Result':`Failed to evaluate transaction: ${error}`}));
    response.end();
    return;
}
}

async function getBinding(response){
  try {
    const ccpPath = path.resolve(__dirname, '..', '..', 'image-network', 'organizations', 'peerOrganizations', 'org1.example.com', 'connection-org1.json');
    let ccp = JSON.parse(fs.readFileSync(ccpPath, 'utf8'));

    const walletPath = path.join(process.cwd(), 'wallet');
    const wallet = await Wallets.newFileSystemWallet(walletPath);
    //console.log(`Wallet path: ${walletPath}`);

    const identity = await wallet.get('appUser');
    if (!identity) {
        console.log('An identity for the user "appUser" does not exist in the wallet');
        console.log('Run the registerUser.js application before retrying');
        response.writeHead(500, {"Content-Type": "application/json"});
        response.write(JSON.stringify({'Result':'An identity for the user "appUser" does not exist in the wallet', 'Solution':'Run the registerUser.js application before retrying'}));
        response.end();
        return;
    }

    const gateway = new Gateway();
    await gateway.connect(ccp, { wallet, identity: 'appUser', discovery: { enabled: true, asLocalhost: true } });

    const network = await gateway.getNetwork('mychannel');

    const contract = network.getContract('imageneslfmj');

    const result = await contract.evaluateTransaction('getBinding');
    console.log(`Transaction has been evaluated, result is: ${result.toString()}`);
    
    await gateway.disconnect();

    response.writeHead(200, {"Content-Type": "application/json", 'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Methods': 'POST'});
    response.write(JSON.stringify(JSON.parse(result)));
    response.end();
} catch (error) {
    console.error(`Failed to evaluate transaction: ${error}`);
    response.writeHead(500, {"Content-Type": "application/json", 'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Methods': 'POST'});
    response.write(JSON.stringify({'Result':`Failed to evaluate transaction: ${error}`}));
    response.end();
    return;
}
}

async function getTxID(response){
  try {
    const ccpPath = path.resolve(__dirname, '..', '..', 'image-network', 'organizations', 'peerOrganizations', 'org1.example.com', 'connection-org1.json');
    let ccp = JSON.parse(fs.readFileSync(ccpPath, 'utf8'));

    const walletPath = path.join(process.cwd(), 'wallet');
    const wallet = await Wallets.newFileSystemWallet(walletPath);
    //console.log(`Wallet path: ${walletPath}`);

    const identity = await wallet.get('appUser');
    if (!identity) {
        console.log('An identity for the user "appUser" does not exist in the wallet');
        console.log('Run the registerUser.js application before retrying');
        response.writeHead(500, {"Content-Type": "application/json"});
        response.write(JSON.stringify({'Result':'An identity for the user "appUser" does not exist in the wallet', 'Solution':'Run the registerUser.js application before retrying'}));
        response.end();
        return;
    }

    const gateway = new Gateway();
    await gateway.connect(ccp, { wallet, identity: 'appUser', discovery: { enabled: true, asLocalhost: true } });

    const network = await gateway.getNetwork('mychannel');

    const contract = network.getContract('imageneslfmj');

    const result = await contract.evaluateTransaction('getTxID');
    console.log(`Transaction has been evaluated, result is: ${result.toString()}`);
    
    await gateway.disconnect();

    response.writeHead(200, {"Content-Type": "application/json", 'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Methods': 'POST'});
    response.write(JSON.stringify(JSON.parse(result)));
    response.end();
} catch (error) {
    console.error(`Failed to evaluate transaction: ${error}`);
    response.writeHead(500, {"Content-Type": "application/json", 'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Methods': 'POST'});
    response.write(JSON.stringify({'Result':`Failed to evaluate transaction: ${error}`}));
    response.end();
    return;
}
}

async function getTxTimestamp(response){
  try {
    const ccpPath = path.resolve(__dirname, '..', '..', 'image-network', 'organizations', 'peerOrganizations', 'org1.example.com', 'connection-org1.json');
    let ccp = JSON.parse(fs.readFileSync(ccpPath, 'utf8'));

    const walletPath = path.join(process.cwd(), 'wallet');
    const wallet = await Wallets.newFileSystemWallet(walletPath);
    //console.log(`Wallet path: ${walletPath}`);

    const identity = await wallet.get('appUser');
    if (!identity) {
        console.log('An identity for the user "appUser" does not exist in the wallet');
        console.log('Run the registerUser.js application before retrying');
        response.writeHead(500, {"Content-Type": "application/json"});
        response.write(JSON.stringify({'Result':'An identity for the user "appUser" does not exist in the wallet', 'Solution':'Run the registerUser.js application before retrying'}));
        response.end();
        return;
    }

    const gateway = new Gateway();
    await gateway.connect(ccp, { wallet, identity: 'appUser', discovery: { enabled: true, asLocalhost: true } });

    const network = await gateway.getNetwork('mychannel');

    const contract = network.getContract('imageneslfmj');

    const result = await contract.evaluateTransaction('getTxTimestamp');
    console.log(`Transaction has been evaluated, result is: ${result.toString()}`);
    
    await gateway.disconnect();

    response.writeHead(200, {"Content-Type": "application/json", 'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Methods': 'POST'});
    response.write(JSON.stringify(JSON.parse(result)));
    response.end();
} catch (error) {
    console.error(`Failed to evaluate transaction: ${error}`);
    response.writeHead(500, {"Content-Type": "application/json", 'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Methods': 'POST'});
    response.write(JSON.stringify({'Result':`Failed to evaluate transaction: ${error}`}));
    response.end();
    return;
}
}


async function getVerifiability(response, dataPosteada){
    try {
      // load the network configuration
          const ccpPath = path.resolve(__dirname, '..', '..', 'image-network', 'organizations', 'peerOrganizations', 'org1.example.com', 'connection-org1.json');
          let ccp = JSON.parse(fs.readFileSync(ccpPath, 'utf8'));
  
          // Create a new file system based wallet for managing identities.
          const walletPath = path.join(process.cwd(), 'wallet');
          const wallet = await Wallets.newFileSystemWallet(walletPath);
          console.log(`Wallet path: ${walletPath}`);
  
          // Check to see if we've already enrolled the user.
          const identity = await wallet.get('appUser');
          if (!identity) {
              console.log('An identity for the user "appUser" does not exist in the wallet');
              console.log('Run the registerUser.js application before retrying');
              response.writeHead(500, {"Content-Type": "application/json"});
              response.write(JSON.stringify({'Result':'An identity for the user "appUser" does not exist in the wallet', 'Solution':'Run the registerUser.js application before retrying'}));
              response.end();
              return;
          }
  
          // Create a new gateway for connecting to our peer node.
          const gateway = new Gateway();
          await gateway.connect(ccp, { wallet, identity: 'appUser', discovery: { enabled: true, asLocalhost: true } });
  
          // Get the network (channel) our contract is deployed to.
          const network = await gateway.getNetwork('mychannel');
  
          // Get the contract from the network.
          const contract = network.getContract('imageneslfmj');
  
          // Submit the specified transaction.
  
          // Get the variables
          datos = JSON.parse(dataPosteada);
          imageId = datos['id'];
          product_hash = datos['product_hash'];
  
          const result = await contract.evaluateTransaction('getVerifiability', imageId, product_hash);
          console.log(`Transaction has been evaluated, result is: ${result.toString()}`);
  
          // Disconnect from the gateway.
          await gateway.disconnect();
  
          response.writeHead(200, {"Content-Type": "application/json", 'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Methods': 'POST'});
          response.write(JSON.stringify(JSON.parse(result)));
          //response.write(JSON.stringify(result.toString()));
          response.end();
      } catch (error) {
          console.error(`Failed to evaluate transaction: ${error}`);
          response.writeHead(500, {"Content-Type": "application/json", 'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Methods': 'POST'});
          response.write(JSON.stringify({'Result':`Failed to evaluate transaction: ${error}`}));
          response.end();
          return;
      }
}

async function getLastHash(response, dataPosteada){
    try {
        // load the network configuration
            const ccpPath = path.resolve(__dirname, '..', '..', 'image-network', 'organizations', 'peerOrganizations', 'org1.example.com', 'connection-org1.json');
            let ccp = JSON.parse(fs.readFileSync(ccpPath, 'utf8'));
    
            // Create a new file system based wallet for managing identities.
            const walletPath = path.join(process.cwd(), 'wallet');
            const wallet = await Wallets.newFileSystemWallet(walletPath);
            console.log(`Wallet path: ${walletPath}`);
    
            // Check to see if we've already enrolled the user.
            const identity = await wallet.get('appUser');
            if (!identity) {
                console.log('An identity for the user "appUser" does not exist in the wallet');
                console.log('Run the registerUser.js application before retrying');
                response.writeHead(500, {"Content-Type": "application/json"});
                response.write(JSON.stringify({'Result':'An identity for the user "appUser" does not exist in the wallet', 'Solution':'Run the registerUser.js application before retrying'}));
                response.end();
                return;
            }
    
            // Create a new gateway for connecting to our peer node.
            const gateway = new Gateway();
            await gateway.connect(ccp, { wallet, identity: 'appUser', discovery: { enabled: true, asLocalhost: true } });
    
            // Get the network (channel) our contract is deployed to.
            const network = await gateway.getNetwork('mychannel');
    
            // Get the contract from the network.
            const contract = network.getContract('imageneslfmj');
    
            // Submit the specified transaction.
    
            // Get the variables
            datos = JSON.parse(dataPosteada);
            imageId = datos['id'];
    
            const result = await contract.evaluateTransaction('getLastHash', imageId);
            console.log(`Transaction has been evaluated, result is: ${result.toString()}`);
    
            // Disconnect from the gateway.
            await gateway.disconnect();
    
            response.writeHead(200, {"Content-Type": "application/json", 'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Methods': 'POST'});
            response.write(JSON.stringify(JSON.parse(result)));
            //response.write(JSON.stringify(result.toString()));
            response.end();
        } catch (error) {
            console.error(`Failed to evaluate transaction: ${error}`);
            response.writeHead(500, {"Content-Type": "application/json", 'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Methods': 'POST'});
            response.write(JSON.stringify({'Result':`Failed to evaluate transaction: ${error}`}));
            response.end();
            return;
        }
}

exports.iniciar = iniciar;
exports.subir = subir;
exports.queryAllImages = queryAllImages;
exports.changeOwner = changeOwner;
exports.getHistory = getHistory;
exports.getImage = getImage;
exports.createImage = createImage;
exports.getVerifiability = getVerifiability;
exports.getLastHash = getLastHash;
exports.getState = getState;
exports.getCreator = getCreator;
exports.getBinding = getBinding;
exports.getTxID = getTxID;
exports.getTxTimestamp = getTxTimestamp;