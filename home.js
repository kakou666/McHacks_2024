let clickedBtnHome=document.getElementById("btnHome")

clickedBtnHome.addEventListener('click',function(event){
  if(confirm("Make sure you saved your flashcards before exiting! If not click on 'Cancel' and save them")){
    window.open("home.html")
  }
})