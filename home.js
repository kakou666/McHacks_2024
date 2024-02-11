let clickedBtnHome=document.getElementById("btnHome")

clickedBtnIndex.addEventListener('click',function(event){
  if(confirm("Make sure you save your flashcards before exiting!")){
    window.open("home.html")
  }
})