function search(){
    var text = document.querySelector(".search#place").value;
    var url = "http://"+window.location.host+"/search/?q="+text;

    window.open(url);

}