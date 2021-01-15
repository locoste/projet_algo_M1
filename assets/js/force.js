var links_word;
var cur_list_word = []

var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function (d) {
        return d.id;
    }))
    .force("charge", d3.forceManyBody())
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("x", d3.forceX())
    .force("y", d3.forceY());

d3.json("json/force.json?_="+ Date.now(), function (error, graph) {
    if (error) throw error;
    links_word = graph.links

    console.log(graph)
    // console.log(JSON.parse(graph))

    var link = svg.append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(graph.links)
        .enter().append("line");

    var node = svg.append("g")
    .attr("class", "nodes")
    .selectAll("circle")
    .data(graph.nodes)
    .enter().append("circle")
    .call(d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended));

    var node_attributes = node
        .attr("r", 5)
        .style("fill", function(d) {return d.color})
        .attr('text', function(d) {return d.mot})
        .attr("transform", d => `translate(${0})`);

    node.append("title")
        .text(function (d) {
            return d.mot;
        });

    node.append("text")
      .attr("x", 8)
      .attr("y", "0.31em")
      .text(d => d.mot)

    node.on("click", display_author_infos);

    simulation
        .nodes(graph.nodes)
        .on("tick", ticked);

    simulation.force("link")
        .links(graph.links);

    function ticked() {
        link
            .attr("x1", function (d) {
                return d.source.x;
            })
            .attr("y1", function (d) {
                return d.source.y;
            })
            .attr("x2", function (d) {
                return d.target.x;
            })
            .attr("y2", function (d) {
                return d.target.y;
            });

        node
            .attr("cx", function (d) {
                return d.x;
            })
            .attr("cy", function (d) {
                return d.y;
            });
    }

//     svg.call(d3.zoom()
//       .extent([[0, 0], [width, height]])
//       .scaleExtent([1, 8])
//       .on("zoom", zoomed));

//       function zoomed({transform}) {
//         svg.attr("transform", transform);
//       }
});

function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}

function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
}

function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
}

function display_author_infos(d){
    document.getElementById("prediction_graph").style.display = "block";
    cur_list_word = []
    document.getElementById("word_label").innerHTML = d.mot

    var ul = document.getElementById('cooc_word');
    while (ul.hasChildNodes()) {  
        ul.removeChild(ul.firstChild);
    }
    links_word.forEach(elem => {
        if(elem.source.id == d.id && !cur_list_word.includes(d.id)){
            var li = document.createElement("li");
            li.appendChild(document.createTextNode(elem.target.mot));
            ul.appendChild(li);
            cur_list_word.push(elem.target.mot)
        }
        if(elem.target.id == d.id && !cur_list_word.includes(d.id)){
            var li = document.createElement("li");
            li.appendChild(document.createTextNode(elem.source.mot));
            ul.appendChild(li);
            cur_list_word.push(elem.source.mot)
        }
    })

    var ul = document.getElementById('cooc_doc');
    while (ul.hasChildNodes()) {  
        ul.removeChild(ul.firstChild);
    }
    doc_liste = []
    for (i=0; i<d.documents.length; i++){
        if (!doc_liste.includes(d.documents[i])){
            var li = document.createElement("li");
            li.appendChild(document.createTextNode(d.documents[i]));
            ul.appendChild(li);
            doc_liste.push(d.documents[i])
        }
    }
}

function set_graph(){
    var xhttp = new XMLHttpRequest();
    var path = "http://localhost:10546/graph/set_graph"
    console.log(document.getElementById('start_month').value)
    if(document.getElementById('start_month').value!=""){
        if(path=="http://localhost:10546/graph/set_graph")
            path += "?";
        else {
            path += "&";
        }
        console.log('start_month')
        path += "start_date="+document.getElementById('start_month').value;
    }
    console.log(document.getElementById('end_mounth').value)
    if(document.getElementById('end_mounth').value!=""){
        if(path=="http://localhost:10546/graph/set_graph")
            path += "?";
        else {
            path += "&";
        }
        path += "end_date="+document.getElementById('end_mounth').value;
    }
    if(document.getElementById('documents_list_input').value!=""){
        if(path=="http://localhost:10546/graph/set_graph")
            path += "?";
        else {
            path += "&";
        }
        path += "documents="+document.getElementById('documents_list_input').value;
    }
    if(path=="http://localhost:10546/graph/set_graph")
            path += "?_="+ new Date().getTime();
        else {
            path += "&_="+ new Date().getTime();
        }
    console.log(path)
    // xhttp.open("GET", path);
    // xhttp.send();
    // window.location.assign(path)
    httpRequest_graph = new XMLHttpRequest();
    httpRequest_graph.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            window.location.reload()
            // 
        }
    };
    console.log(path)
    httpRequest_graph.open('GET', path, true);
    httpRequest_graph.send();
}

function get_predict_graph(){
    predict_list = []
    console.log(cur_list_word)
    cur_list_word.forEach(elem => {
        predict_list.push(document.getElementById("word_label").innerHTML + "_" + elem)
    })
    console.log(predict_list)
    httpRequest_graph = new XMLHttpRequest();
    httpRequest_graph.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log(httpRequest_graph.response);
            window.open("http://localhost:10546/predict/graph.html?_=" +Date.now());
            // 
        }
    };
    console.log({"mots": predict_list})
    httpRequest_graph.open('POST', "http://localhost:10546/predict/graph", true);
    httpRequest_graph.send(JSON.stringify({"mots": predict_list}));
}

httpRequest_doc_list = new XMLHttpRequest();
httpRequest_doc_list.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        doc_liste = httpRequest_doc_list.response
        console.log(JSON.parse(doc_liste))
        var ul = document.getElementById('documents_list');

        while (ul.hasChildNodes()) {  
            ul.removeChild(ul.firstChild);
        }

        for (i=0; i<JSON.parse(doc_liste).doc_list.length; i++){
            var option = document.createElement("option");
            option.appendChild(document.createTextNode(JSON.parse(doc_liste).doc_list[i]));
            ul.appendChild(option);
        }
    }
};
httpRequest_doc_list.open('GET', "http://localhost:10546/graph/get_doc_list", true);
httpRequest_doc_list.send();