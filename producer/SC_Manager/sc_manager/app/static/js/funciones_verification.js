
//function hash64(str) {
//    var h1 = hash32(str);  // returns 32 bit (as 8 byte hex string)
//    return h1 + hash32(h1 + str);  // 64 bit (as 16 byte hex string)
//}

$(document).ready(function(){
    //Por si se ocupa

    $("#boton_informacion").click(function(){
        //alert("Click en el boton");
        //console.log("Entra s");

        

        $.ajax(
            {
                url : 'http://localhost:8002/verifiability',
                type: "POST",
                data: JSON.stringify({'id':$("#assetIdInput").val(), 'product_hash':$("#productHashInput").val()}),
                accept: "application/json",
                crossDomain: true,
                dataType : 'json',
                
                success : function(data){
                    $(".general_container").remove();
                    cantidad = Object.keys(data).length;
                    //alert(cantidad);

                    $("#main_container").data("cantidad", cantidad);

                    var allData = data;
                    //console.log(allData.length)

                    if(allData.length == 0){
                        alert("The product information is wrong or there may be a problem on your product processing\nPlease verify the input data")
                    }

                    else{
                        $.each(allData, function(index, value){
                            //alert(index);
                            //console.log(index + ": " + value);
                            //indice = cantidad - index - 1;
                            indice = index;
                            //alert("Indice: " + indice);
                            var fechaHora = value['newTimestamp'];
                            var previousHash = value['newPrevious_hash'];
                            var actualHash = value['newActual_hash'];
    
                            //var actualHash = "actual" + indice;
                            var contentID = value['content_id'];
                            var level = value['level'];
                            var organizationName = value['organization_name'];
                            var buildingBlockDescription = value['building_block_description'];
                            var transactionID = value['transaction_id'];
                            var status = value['status'];
                            var fileName = value['file_name'];
    
                            alert("The product has been processed on: \n" + "Organization: " + organizationName + "\nBuilding block Description: " + buildingBlockDescription + "\nStatus: " + status + "\nFile name: " + fileName);
    
                            var sentence = "";
    
                            sentence = '<div class="general_container">';
    
                            sentence = sentence + "<div class='container' id='otro'>";
                            sentence = sentence + "<div class = 'card'>";
    
                            sentence = sentence + "<h3 class='card-header'>Result</h3>";
                            
                            
                            sentence = sentence + '<div class="card-body" id="div' + indice + '">';
                        
                            sentence = sentence + '<div class="input-group mb-3">';
                            sentence = sentence + '<div class="input-group-prepend">';
                            sentence = sentence + '<span class="input-group-text" id="inputGroup-sizing-default">Previous Hash</span>';
                            sentence = sentence + '</div>';
                            sentence = sentence + '<input type="text" class="form-control" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-default" value="' + previousHash + '" id = "inputPrevio' + indice + '" disabled></div>';
    
                            sentence = sentence + '<div class="input-group mb-3">';
                            sentence = sentence + '<div class="input-group-prepend">';
                            sentence = sentence + '<span class="input-group-text" id="inputGroup-sizing-default">Actual Hash</span></div>';
                            sentence = sentence + '<input type="text" class="form-control" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-default" value="' + actualHash + '" id = "input' + indice + '" disabled></div>';
                            
                            //alert(indiceCompuesto);
    
                            
                            
    
                            sentence = sentence + '<div class="input-group mb-3">';
                            sentence = sentence + '<div class="input-group-prepend">';
                            sentence = sentence + '<span class="input-group-text" id="inputGroup-sizing-default">Content ID (File Hash)</span></div>';
                            sentence = sentence + '<input type="text" id="contentID" class="form-control" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-default" value="' + contentID + '" disabled></div>';
                            
                            sentence = sentence + '<div class="input-group mb-3">';
                            sentence = sentence + '<div class="input-group-prepend">';
                            sentence = sentence + '<span class="input-group-text" id="inputGroup-sizing-default">File name</span></div>';
                            sentence = sentence + '<input type="text" id="fileName" class="form-control" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-default" value="' + fileName + '" disabled></div>';
    
                            sentence = sentence + '<div class="input-group mb-3">';
                            sentence = sentence + '<div class="input-group-prepend">';
                            sentence = sentence + '<span class="input-group-text" id="inputGroup-sizing-default">Level</span></div>';
                            sentence = sentence + '<input type="text" id="level" class="form-control" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-default" value="' + level + '" disabled></div>';
    
    
                            sentence = sentence + '<div class="input-group mb-3">';
                            sentence = sentence + '<div class="input-group-prepend">';
                            sentence = sentence + '<span class="input-group-text" id="inputGroup-sizing-default">Organization name</span></div>';
                            sentence = sentence + '<input type="text" id="organization_name" class="form-control" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-default" value="' + organizationName + '" disabled></div>';
    
                            sentence = sentence + '<div class="input-group mb-3">';
                            sentence = sentence + '<div class="input-group-prepend">';
                            sentence = sentence + '<span class="input-group-text" id="inputGroup-sizing-default">Building block description</span></div>';
                            sentence = sentence + '<input type="text" id="building_block_description" class="form-control" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-default" value="' + buildingBlockDescription + '" disabled></div>';
    
                            sentence = sentence + '<div class="input-group mb-3">';
                            sentence = sentence + '<div class="input-group-prepend">';
                            sentence = sentence + '<span class="input-group-text" id="inputGroup-sizing-default">Transaction ID</span></div>';
                            sentence = sentence + '<input type="text" id="transactionID" class="form-control" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-default" value="' + transactionID + '" disabled></div>';
    
    
                            sentence = sentence + '<div class="input-group mb-3">';
                            sentence = sentence + '<div class="input-group-prepend">';
                            sentence = sentence + '<span class="input-group-text" id="inputGroup-sizing-default">Status</span></div>';
                            sentence = sentence + '<input type="text" id="status" class="form-control" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-default" value="' + status + '" disabled></div>';
    
    
                            sentence = sentence + '<div class="input-group mb-3">';
                            sentence = sentence + '<div class="input-group-prepend">';
                            sentence = sentence + '<span class="input-group-text" id="inputGroup-sizing-default">Timestamp</span></div>';
                            sentence = sentence + '<input type="text" id="transactionID" class="form-control" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-default" value="' + fechaHora + '" disabled></div></div>';
    
                            sentence = sentence + "</div>";
                            sentence = sentence + "</div>";
    
                            sentence = sentence + '</div>';
                            $("body").append(sentence);
    
                            //alert('$(#' + indice + ').data("actualHash");');
                            var indiceCompuesto = "#input" + indice;
                            var elemento = $("#input" + indice);
                            $(indiceCompuesto).data("previousHash", previousHash);
                            $(indiceCompuesto).data("actualHash", actualHash);
                            $(indiceCompuesto).data("indice", indice);
                            //console.log($(indiceCompuesto).data("actualHash"));
    
                            previousHash = actualHash;
                        })
                    }
                },

                error : function(err){
                    //alert("Disculpe, existió un problema " + JSON.stringify(xhr));
                    //alert("The product information is wrong or there may be a problem on your product processing")
                    alert("Error: Please check the key existence and verify that the server is listening");
                    console.log("AJAX error in request: " + JSON.stringify(err, null, 2));
                },

                complete : function(xhr, status){
                    //alert("Petición realizada " + status);
                    //alert("Cantidad: " + $("#main_container").data("cantidad"));
                }
            });
            
            console.log("sale");
    });


});