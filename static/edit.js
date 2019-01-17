// Edit
//
// TO DO

//                <div class="row">
//                    <div class="col-lg-6 col-md-6 col-sm-6 text-center">
//                        <input name="term0" class="form-control" id="term0"
//                               placeholder="Term"
//                               required>
//                    </div>
//                    <div class="col-lg-6 col-md-6 col-sm-6  text-center">
//                        <input name="def0" class="form-control" id="def0"
//                               placeholder="Definition"
//                               required>
//                    </div>
//                </div>

var row = document.getElementsByName("content");
console.log(row);
for (var i = 0; i < row.length; i++){
    var term = row[i].childNodes[1].childNodes[1].innerText;
    var def = row[i].childNodes[1].childNodes[3].innerText;
    var editBut = row[i].childNodes[1].childNodes[5].childNodes[1];
    var delBut = row[i].childNodes[1].childNodes[7].childNodes[1];
    //console.log("term: " + term);
    //console.log("def: " + def);
    //editBut.addEventListener('click', function(){
    //    console.log("EDITING");

    //    // add form: term, def, submit but
    //    row[i].appendChild();
    //});
    delBut.addEventListener('click', function(){
        console.log("DELETE");
    });
}


//var editBut = editButList[i];
//editBut.addEventListener('click', function(){
//    console.log("EDITING");
//});








