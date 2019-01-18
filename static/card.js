var btn = document.getElementById("add");
var container = document.getElementById("termcontainer");
var countbox = document.getElementById("count");
var count = Number(countbox.getAttribute("value"));
//
//#007bff

var makecell = (type) => {
    var top = document.createElement("div");
    top.classList.add("col-6","text-center");
    var ele = document.createElement("input");
    var typecount = type + count;
    ele.id = typecount;
    ele.name = typecount;
    ele.classList.add("form-control");
    var ph;
    if (type == "term") {
        ph = "Term";
    }
    else {
        ph = "Definition"
    }
    ele.placeholder=ph;
    top.appendChild(ele);
    return top;
};

var btnevent = () => {
    btn.addEventListener('click', function () {
        var newrow = document.createElement("div");
        newrow.classList.add("row");
        var term = makecell("term");
        var def = makecell("def");
        newrow.appendChild(term);
        newrow.appendChild(def);
        //console.log("------");
        //console.log(term);
        container.appendChild(newrow);
        //console.log(count);
        count = count + 1;
        //console.log(count);
        countbox.setAttribute("value",count);
    })
};



btnevent();
// <div class="row">
//                     <div class="col-lg-6 col-md-6 col-sm-6 text-center">
//                             <input name="term0" class="form-control" id="term0"
//                                    placeholder="Term"
//                                    required>
//
//                     </div>
//                     <div class="col-lg-6 col-md-6 col-sm-6  text-center">
//                             <input name="def0" class="form-control" id="def0"
//                                    placeholder="Definition"
//                                    required>
//                     </div>
//                 </div>
