
//function hash64(str) {
//    var h1 = hash32(str);  // returns 32 bit (as 8 byte hex string)
//    return h1 + hash32(h1 + str);  // 64 bit (as 16 byte hex string)
//}

function hash64(string) { 
                  
    var hash = 0; 
      
    if (string.length == 0) return hash; 
      
    for (i = 0; i < string.length; i++) { 
        char = string.charCodeAt(i); 
        hash = ((hash << 5) - hash) + char; 
        hash = hash & hash; 
    } 
      
    return hash; 
} 

function checkHashes(id, previous, actual){
    document.getElementById("inputPrevio" + id).value = previous;
    document.getElementById("input" + id).value = hash64(previous.toString());
    //alert("si");
    var valor = document.getElementById("input" + id).value;
    hashPrevio = $("#input" + id).data("previousHash");
    hashActual = $("#input" + id).data("actualHash");

    
    if(previous!=hashPrevio || actual!= valor){
        console.info("El previo: " + previous);
        console.info("El hash previo: " + hashPrevio);
        console.info("El actual: " + actual);
        console.info("El valor: " + valor);
        alert("Entra");
        document.getElementById("div" + id).style.backgroundColor = "red";
    }
    else{
        document.getElementById("div" + id).style.backgroundColor = "#fdfdfd7a";
    }
}


function checkBlocks(idInput){
    id = $("#" + idInput).data("indice");
    //alert("El id del input sin input es : " + id);
    hashPrevioBlockAnterior = document.getElementById("input" + id).value;
    //alert(hashPrevioBlockAnterior)
    hashActualBlockAnterior =  $("#input" + id).data("actualHash");
    //alert( document.getElementById("input" + id).value);
    cantidad = $("#main_container").data("cantidad");

    if(document.getElementById("input" + id).value != hashActualBlockAnterior){
        //alert("Something is wrong");
        document.getElementById("div" + id).style.backgroundColor = "red";
        for(var i=id+1; i<cantidad; i++){
            alert("Entra en: " + i);
            var actualHashi = $("#input" + i).data("actualHash");
            checkHashes(i, hashPrevioBlockAnterior, actualHashi);
            hashPrevioBlockAnterior = document.getElementById("input" + i).value;
        }

    }
    else{
        //alert("All is correct");
        document.getElementById("div" + id).style.backgroundColor = "#fdfdfd7a";
        for(var j=id+1; j<cantidad; j++){
            var actualHashi = $("#input" + j).data("actualHash");
            checkHashes(j, hashPrevioBlockAnterior, actualHashi);
            hashPrevioBlockAnterior = document.getElementById("input" + j).value;
            //alert(actualHashi + "\t" + valor);
        }
    }


    
};

$(document).ready(function(){
    //Por si se ocupa

    $("#boton_informacion").click(function(){
        //alert("Click en el boton");
        //console.log("Entra s");

        

        $.ajax(
            {
                url : 'http://localhost:8002/getHistory',
                type: "POST",
                data: JSON.stringify({'id':$("#assetIdInput").val()}),
                accept: "application/json",
                crossDomain: true,
                dataType : 'json',
                
                success : function(data){
                    $(".general_container").remove();
                    cantidad = Object.keys(data).length;
                    //alert(cantidad);

                    $("#main_container").data("cantidad", cantidad);

                    var allData = data;
                    var previousHash = hash64("bloque genesis");

                    allData = data.reverse();
                    $.each(allData, function(index, value){
                        //alert(index);
                        //console.log(index + ": " + value);
                        //indice = cantidad - index - 1;
                        indice = index;
                        //alert("Indice: " + indice);
                        var fechaHora = value['newTimestamp'];
                        
                        var actualHash = hash64(previousHash.toString());

                        //var actualHash = "actual" + indice;
                        var contentID = value['content_id'];
                        var level = value['level'];
                        var organizationName = value['organization_name'];
                        var buildingBlockDescription = value['building_block_description'];
                        var transactionID = value['transaction_id'];
                        var status = value['status'];
                        var fileName = value['file_name'];

                        var sentence = "";

                        sentence = '<div class="general_container">';

                        sentence = sentence + "<div class='container' id='otro'>";
                        sentence = sentence + "<div class = 'card'>";

                        sentence = sentence + "<h3 class='card-header'>" + indice + "</h3>";
                        
                        
                        sentence = sentence + '<div class="card-body" id="div' + indice + '">';
                    
                        sentence = sentence + '<div class="input-group mb-3">';
                        sentence = sentence + '<div class="input-group-prepend">';
                        sentence = sentence + '<span class="input-group-text" id="inputGroup-sizing-default">Previous Hash</span>';
                        sentence = sentence + '</div>';
                        sentence = sentence + '<input type="text" class="form-control" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-default" value="' + previousHash + '" id = "inputPrevio' + indice + '" disabled></div>';

                        sentence = sentence + '<div class="input-group mb-3">';
                        sentence = sentence + '<div class="input-group-prepend">';
                        sentence = sentence + '<span class="input-group-text" id="inputGroup-sizing-default">Actual Hash</span></div>';
                        sentence = sentence + '<input type="text" class="form-control" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-default" value="' + actualHash + '" id = "input' + indice + '" oninput="checkBlocks(this.id)"></div>';
                        
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
                },

                error : function(err){
                    //alert("Disculpe, existió un problema " + JSON.stringify(xhr));
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