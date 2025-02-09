var windows = document.getElementsByClassName('modal');
var open_buttons = document.getElementsByClassName("openmodal");
var close_buttons = document.getElementsByClassName('closemodal');
var opened_window = 0;
var id = document.getElementById('id_id');


function CloseWindow(item){
    if (typeof item != 'number'){
    item.style.display = 'none';
    }
}

function SetFormDefault(task_info) {
    task_info_keys = Object.keys(task_info);
    task_info_values = Object.values(task_info);
    for (let index=0; index < task_info_keys.length; index++) {
        if ("id_"+task_info_keys[index] != 'id_starred'){
        element = document.getElementById("id_"+task_info_keys[index]);
        element.value = task_info_values[index];}
    }
    if (task_info['starred'] == 'True'){
        document.getElementById('id_starred').checked = true;

    }else{document.getElementById('id_starred').checked = false;}
}


function GetTaskInfo(button_id){
    var searchEles = document.getElementById("hiddeninfo"+button_id).children;
    var task_info = {};
    for (let i = 0; i < searchEles.length; i++){
        task_info[searchEles[i].className] = searchEles[i].getAttribute("value");
    }
    return task_info;
}


function CloseAllModalWindows(){
    for (let item of windows) {
        CloseWindow(item);
    };
}

window.CloseAllModalWindows = CloseAllModalWindows;

CloseAllModalWindows()


if (open_buttons.length > 0){
    for (let index=0; index<open_buttons.length; index++){
    const open_button = open_buttons[index];
    open_button.addEventListener('click', function(e){
        const button_id= open_button.getAttribute('id').replace('openmodal','');
        window_to_open =document.getElementById('modal');
        CloseWindow(opened_window);
        window_to_open.style.display = 'block';
        opened_window = window_to_open;
        id.value = parseInt(button_id);
        let task_info = GetTaskInfo(button_id);
        SetFormDefault(task_info);
        });
    }
}

if (close_buttons.length > 0){
    for (let index=0; index<close_buttons.length; index++){
    const close_button = close_buttons[index];
    close_button.addEventListener('click', function(e){
        const button_id=close_button.getAttribute('id').replace('closemodal','');
        window_to_close=document.getElementById('modal' + button_id);
        CloseWindow(window_to_close);
        opened_window = 0;
        });
    }
}