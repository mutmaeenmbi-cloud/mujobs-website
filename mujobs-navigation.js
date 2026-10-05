const menu=document.querySelector('.mj-menu');
if(menu){
 menu.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>menu.open=false));
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu.open){menu.open=false;menu.querySelector('summary').focus();}});
 document.addEventListener('click',e=>{if(!menu.contains(e.target))menu.open=false;});
}
