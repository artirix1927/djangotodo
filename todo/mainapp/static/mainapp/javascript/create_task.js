var create_task_div = document.getElementById("create_task");
var create_task_buttons = document.getElementsByClassName("create_task_btn");
var b = document.getElementById('body');
var close_task_button = document.getElementById('close_create_task_window');
create_task_div.style.display = 'none';
var modal_windows = document.getElementsByClassName('modal');

function CloseModalWindows(){
    for (let item of modal_windows) {
        if (typeof item != 'number'){
            item.style.display = 'none';
        }
}}


if (create_task_buttons.length > 0){
    for (let index=0; index<create_task_buttons.length; index++){
    const create_task_btn = create_task_buttons[index];
    create_task_btn.addEventListener('click', function(e){
            if (create_task_div.style.display == 'none'){
            create_task_div.style.display = 'flex';
            close_task_button.style.zIndex = '119';
            CloseModalWindows();
            }else{
            create_task_div.style.display = 'none';
            close_task_button.style.zIndex = '-1';
            };
        });
    }
}


close_task_button.onclick = ('click', function(e){
    create_task.style.display = 'none';
    close_task_button.style.zIndex = '-1';
});
