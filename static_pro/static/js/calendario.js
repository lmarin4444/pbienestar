function configurar(){
    var s = document.getElementById("anos");
    var m = document.getElementById("mes");
    for(var i=2011;i<=(Number({{ hoy.year }})+1);i++){
        var option=document.createElement("option");
        option.value=i;
        option.text=i;
        if(i=={{ hoy.year }})
            option.selected = true;
        s.appendChild(option);
        }
        for(var j=0;j<m.length;j++){
            if(Number(m[j].value)=={{ hoy.month }})
                m[j].selected = true;
        }
    }
window.onload = configurar;
