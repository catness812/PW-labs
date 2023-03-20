"use strict";

const hamburger = document.querySelector(".hamburger-menu");
const list_box = document.querySelector("[todo-lists]");
const task_list = document.querySelector(".todo-list");
const empty_list = document.querySelector(".empty-list");
const edit_list = document.querySelector("[edit-list-button]")
const delete_list = document.querySelector("[delete-list-button]");
const list_form = document.querySelector("[new-list-form]");
const list_input = document.querySelector("[new-list-input]");
const list_display = document.querySelector("[list-display]");
const todo_box = document.querySelector(".todo-container");
const list_title = document.querySelector("[list-title");
const list_count = document.querySelector("[remaining-count");
const add_button = document.querySelector(".add-button");
const show_all = document.querySelector("[show-all-tasks-button]");
const show_complete = document.querySelector("[show-complete-tasks-button]");
const show_incomplete = document.querySelector("[show-incomplete-tasks-button]");
const tasks_box = document.querySelector("[tasks");
const new_task_form = document.querySelector("[new-task-form]");
const form = document.querySelector(".form-container");
const close_button = document.querySelector(".close");
const new_task_input = document.querySelector("[new-task]");
const new_task_date = document.querySelector(".due-date");
const new_task_time = document.querySelector(".due-time");
const new_task_imp = document.querySelector(".priority");
const new_task_desc = document.querySelector(".description");
const shadow = document.querySelector(".form-shadow");
const task_form = document.querySelector(".task-template");

let lists = JSON.parse(localStorage.getItem("task.lists")) || [];
let selected_list_id = localStorage.getItem("task.selected_list_id");
let formIsOpen = false;


function alert_due() {
    const selected_list = lists.find((list) => list.id === selected_list_id);
    if (selected_list == null) {
        return;
    }
    const now = new Date();
    selected_list.tasks.forEach((task) => {
        const due_date_time = new Date(`${task.date} ${task.time}`);
        const time_diff = due_date_time.getTime() - now.getTime();
        const min_diff = Math.round(time_diff / 60000);
        if (min_diff == 15) {
            const message = `Task '${task.name}' is due in ${min_diff} minutes!`;
            alert(message);
        }
    });
}

function update() {
    clear_item(list_box);
    update_lists();
    const selected_list = lists.find((list) => list.id === selected_list_id);
    if (selected_list != null) {
        todo_box.style.display = "block";
        if (selected_list_id === null) {
            list_display.style.display = "none";
        } else {
            list_display.style.display = "";
            list_title.innerHTML = `${selected_list.name}`;
            update_count(selected_list);
            clear_item(tasks_box);
            update_tasks(selected_list);
            priority_tasks(selected_list);
        }
    } else {
        todo_box.style.display = "none";
        empty_list.style.background = "url(img/empty.png) center no-repeat";
        empty_list.style.backgroundSize = "50%";
    }
    localStorage.setItem("task.lists", JSON.stringify(lists));
    localStorage.setItem("task.selected_list_id", selected_list_id);
}

function clear_item(element) {
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
}

function update_lists() {
    if (lists.length === 0) {
        todo_box.style.display = "none";
        list_display.style.background =
        "url(img/empty.png) center no-repeat";
        list_display.style.backgroundSize = "50%";
        edit_list.style.display = "none";
        delete_list.style.display = "none";
    } else {
        edit_list.style.display = "block";
        delete_list.style.display = "block";
    }
    lists.forEach((list) => {
        const list_el = document.createElement("li");
        list_el.innerText = list.name;
        list_el.dataset.listId = list.id;
        if (list.id === selected_list_id) {
            list_el.classList.add("active-list");
        }
        list_box.appendChild(list_el);
    });
}

function update_count(selected_list) {
    const incomplete_count = selected_list.tasks.filter((task) => !task.complete).length;
    const task_str = incomplete_count === 1 ? "task" : "tasks";
    list_count.innerText = `${incomplete_count} ${task_str} remaining`;
}

function update_tasks(selected_list) {
    if (selected_list.tasks.length === 0) {
        list_display.style.background =
        "url(img/empty.png) center no-repeat";
        list_display.style.backgroundSize = "50%";
    } else {
        list_display.style.background = "";
    }
    selected_list.tasks.forEach((task) => {
        const now = new Date();
        const due_date_time = new Date(`${task.date} ${task.time}`);
        const time_diff = due_date_time.getTime() - now.getTime();
        const min_diff = Math.round(time_diff / 60000);
        const task_el = document.importNode(task_form.content, true);
        const checkbox = task_el.querySelector("input");
        checkbox.id = task.id;
        checkbox.checked = task.complete;
        const label = task_el.querySelector("label");
        label.htmlFor = task.id;
        const line_br = document.createElement("br");
        label.append(task.name, " ", task.date, " ", task.time, line_br, task.description);
        if (min_diff < 0) {
            label.append(" OVERDUE");
        }
        const edit_button = document.createElement("p");
        edit_button.innerHTML = `<i class="gg-pen"></i>`;
        edit_button.style.color = "#fff"
        edit_button.classList.add("edit");
        edit_button.addEventListener("click", () => edit_tasks(task, label));
        const delete_button = document.createElement("p");
        delete_button.innerHTML = `<i class="gg-trash-empty"></i>`;
        delete_button.style.color = "#fff"
        delete_button.classList.add("delete");
        delete_button.addEventListener("click", () => delete_tasks(task, label));
        const todo_task = task_el.querySelector(".task");
        todo_task.append(delete_button);
        todo_task.append(edit_button);
        tasks_box.appendChild(task_el);
    });
}

function edit_tasks(task, label) {
    toggle_update_form();
    new_task_input.value = task.name;
    new_task_date.value = task.date;
    new_task_time.value = task.time;
    new_task_imp.value = task.priority;
    new_task_desc.value = task.description;

    new_task_form.addEventListener("submit", () => {
        task.name = new_task_input.value;
        task.date = new_task_date.value;
        task.time = new_task_time.value;
        task.priority = new_task_imp.value;
        task.description = new_task_desc.value;
        label.innerHTML = `<span class="checkbox"></span>${task.name}<br>${task.date}<br>${task.time}<br>${task.description}`;
        update();
    });
}

function delete_tasks(task, label) {
    const index = task.id;
    const selected_list = lists.find((list) => list.id === selected_list_id);
    selected_list.tasks = selected_list.tasks.filter((task) => index !== task.id);
    update();
}

function priority_tasks(selected_list) {
    const todos = [...document.querySelectorAll(".todo")];
    const checkbox = [...document.querySelectorAll(".checkbox")];
    for (let i = 0; i < todos.length; i++) {
        for (let i = 0; i < selected_list.tasks.length; i++) {
            if (selected_list.tasks[i].priority === "High") {
                checkbox[i].style.border = "3px solid #991f00";
            } else if (selected_list.tasks[i].priority === "Medium") {
                checkbox[i].style.border = "3px solid #b36b00";
            } else if (selected_list.tasks[i].priority === "Low") {
                checkbox[i].style.border = "3px solid #808000";
            } else {
                checkbox[i].style.border = "3px solid #267326";
            }
        }
    }
}

list_form.addEventListener("submit", (event) => {
    event.preventDefault();
    const list_name = list_input.value;
    if (list_name === null || list_name === "") return;
    const list = create_list();
    list_input.value = null;
    lists.push(list);
    update();
});

edit_list.addEventListener("click", () => {
    const selected_list = lists.find((list) => list.id === selected_list_id);
    console.log(selected_list.name);
    const curr_name = selected_list.name;
    const new_name = prompt("Enter a new name for the list", curr_name);
    if (new_name === null || new_name === "") return;
    selected_list.name = new_name;
    update();
});

delete_list.addEventListener("click", () => {
    lists = lists.filter((list) => list.id !== selected_list_id);
    selected_list_id = null;
    update();
});

function create_list() {
    return { id: Date.now().toString(), name: list_input.value, tasks: [] };
}

new_task_form.addEventListener("submit", (event) => {
    event.preventDefault();
    const task_name = new_task_input.value;
    const h2 = document.querySelector(".form-container h2");
    if (h2.textContent === "UPDATE TASK") return;
    if (task_name === null || task_name === "") return;
    const task = create_task();
    new_task_input.value = null;
    const selected_list = lists.find((list) => list.id === selected_list_id);
    selected_list.tasks.push(task);
    update();
});

function create_task() {
    return {
        id: Date.now().toString(),
        name: new_task_input.value,
        date: new_task_date.value,
        time: new_task_time.value,
        priority: new_task_imp.value,
        description: new_task_desc.value,
        complete: false,
    };
}

function toggle_form() {
    const h2 = document.querySelector(".form-container h2");
    const submit_input = document.querySelector(`input[type="submit"]`);
    if (formIsOpen) {
        form.style.pointerEvents = "none";
        form.style.transform = "scale(0)";
        shadow.style.opacity = 0;
        formIsOpen = false;
    } else {
        submit_input.value = "Submit";
        form.style.pointerEvents = "auto";
        form.style.transform = "scale(1)";
        shadow.style.opacity = 1;
        formIsOpen = true;
    }
}

function toggle_update_form() {
    const h2 = document.querySelector(".form-container h2");
    const submit_input = document.querySelector(`input[type="submit"]`);
    if (formIsOpen) {
        form.style.pointerEvents = "none";
        form.style.transform = "scale(0)";
        shadow.style.opacity = 0;
        formIsOpen = false;
    } else {
        h2.textContent = "UPDATE TASK";
        submit_input.value = "Update";
        form.style.pointerEvents = "auto";
        form.style.transform = "scale(1)";
        shadow.style.opacity = 1;
        formIsOpen = true;
    }
}

function close_form() {
    form.style.transform = "scale(0)";
    shadow.style.opacity = 0;
    formIsOpen = false;
}

list_box.addEventListener("click", (event) => {
    if (event.target.tagName.toLowerCase() === "li") {
        selected_list_id = event.target.dataset.listId;
        update();
    }
});

tasks_box.addEventListener("click", (event) => {
    if (event.target.tagName.toLowerCase() === "input") {
        const selected_list = lists.find((list) => list.id === selected_list_id);
        const selected_task = selected_list.tasks.find(
        (task) => task.id === event.target.id
        );
        selected_task.complete = event.target.checked;
        update();
    }
});

add_button.addEventListener("click", () => {
    new_task_form.reset();
    toggle_form();
});

close_button.addEventListener("click", () => {
    close_form();
});

form.addEventListener("submit", (event) => {
    event.preventDefault();
    toggle_form();
    formIsOpen = false;
});

hamburger.addEventListener("click", () => {
    const side = document.querySelector(".side-container");
    side.classList.toggle("active");
});

show_all.addEventListener("click", () => {
    update();
});

show_complete.addEventListener("click", () => {
    const selected_list = lists.find((list) => list.id === selected_list_id);
    const completed_tasks = selected_list.tasks.filter((task) => task.complete);
    clear_item(tasks_box);
    completed_tasks.forEach((task) => {
        const now = new Date();
        const due_date_time = new Date(`${task.date} ${task.time}`);
        const time_diff = due_date_time.getTime() - now.getTime();
        const min_diff = Math.round(time_diff / 60000);
        const task_el = document.importNode(task_form.content, true);
        const checkbox = task_el.querySelector("input");
        checkbox.id = task.id;
        checkbox.checked = task.complete;
        const label = task_el.querySelector("label");
        label.htmlFor = task.id;
        const line_br = document.createElement("br");
        label.append(task.name, " ", task.date, " ", task.time, line_br, task.description);
        if (min_diff < 0) {
            label.append(" OVERDUE");
        }        
        const edit_button = document.createElement("p");
        edit_button.innerHTML = `<i class="gg-pen"></i>`;
        edit_button.style.color = "#fff"
        edit_button.classList.add("edit");
        edit_button.addEventListener("click", () => edit_tasks(task, label));
        const delete_button = document.createElement("p");
        delete_button.innerHTML = `<i class="gg-trash-empty"></i>`;
        delete_button.style.color = "#fff"
        delete_button.classList.add("delete");
        delete_button.addEventListener("click", () => delete_tasks(task, label));
        const todo_task = task_el.querySelector(".task");
        todo_task.append(delete_button);
        todo_task.append(edit_button);
        tasks_box.appendChild(task_el);
    });
    priority_tasks(selected_list);
});  

show_incomplete.addEventListener("click", () => {
    const selected_list = lists.find((list) => list.id === selected_list_id);
    const incompleted_tasks = selected_list.tasks.filter((task) => !task.complete);
    clear_item(tasks_box);
    incompleted_tasks.forEach((task) => {
        const now = new Date();
        const due_date_time = new Date(`${task.date} ${task.time}`);
        const time_diff = due_date_time.getTime() - now.getTime();
        const min_diff = Math.round(time_diff / 60000);
        const task_el = document.importNode(task_form.content, true);
        const checkbox = task_el.querySelector("input");
        checkbox.id = task.id;
        checkbox.checked = task.complete;
        const label = task_el.querySelector("label");
        label.htmlFor = task.id;
        const line_br = document.createElement("br");
        label.append(task.name, " ", task.date, " ", task.time, line_br, task.description);
        if (min_diff < 0) {
            label.append(" OVERDUE");
        }        
        const edit_button = document.createElement("p");
        edit_button.innerHTML = `<i class="gg-pen"></i>`;
        edit_button.style.color = "#fff"
        edit_button.classList.add("edit");
        edit_button.addEventListener("click", () => edit_tasks(task, label));
        const delete_button = document.createElement("p");
        delete_button.innerHTML = `<i class="gg-trash-empty"></i>`;
        delete_button.style.color = "#fff"
        delete_button.classList.add("delete");
        delete_button.addEventListener("click", () => delete_tasks(task, label));
        const todo_task = task_el.querySelector(".task");
        todo_task.append(delete_button);
        todo_task.append(edit_button);
        tasks_box.appendChild(task_el);
    });
    priority_tasks(selected_list);
});

const searchTasks = (() => {
    const search = document.querySelector(".search-bar");
  
    search.addEventListener("keyup", (event) => {
        const searchString = event.target.value.toLowerCase();
        const selected_list = lists.find((list) => list.id === selected_list_id);
        const searchedTasks = selected_list.tasks.filter((task) => {
            return (
                task.name.toLowerCase().includes(searchString) || task.description.toLowerCase().includes(searchString)
            );
        });
        update_search(searchedTasks);
    });
  
    function update_search(searchedTasks) {
        clear_item(list_box);
        update_lists();
        const selected_list = lists.find((list) => list.id === selected_list_id);
    
        if (selected_list_id === null) {
            todo_box.style.display = "none";
        } else {
            list_display.style.display = "";
            list_title.innerHTML = `${selected_list.name}`;
            clear_item(tasks_box);
            update_searched(searchedTasks);
            color_search(searchedTasks);
        }
    }
  
    function color_search(searchedTasks) {
        const todos = [...document.querySelectorAll(".todo")];
        const checkbox = [...document.querySelectorAll(".checkbox")];
        for (let i = 0; i < todos.length; i++) {
            for (let i = 0; i < searchedTasks.length; i++) {
                if (searchedTasks[i].priority === "High") {
                    checkbox[i].style.border = "3px solid #991f00";
                } else if (searchedTasks[i].priority === "Medium") {
                    checkbox[i].style.border = "3px solid #b36b00";
                } else if (searchedTasks[i].priority === "Low") {
                    checkbox[i].style.border = "3px solid #808000";
                } else {
                    checkbox[i].style.border = "3px solid #267326";
                }
            }
        }
    }
  
    function update_searched(searchedTasks) {
        searchedTasks.forEach((task) => {
            const now = new Date();
            const due_date_time = new Date(`${task.date} ${task.time}`);
            const time_diff = due_date_time.getTime() - now.getTime();
            const min_diff = Math.round(time_diff / 60000);
            const task_el = document.importNode(task_form.content, true);
            const checkbox = task_el.querySelector("input");
            checkbox.id = task.id;
            checkbox.checked = task.complete;
            const label = task_el.querySelector("label");
            label.htmlFor = task.id;
    
            const line_br = document.createElement("br");
            label.append(task.name, " ", task.date, " ", task.time, line_br, task.description);
            if (min_diff < 0) {
                label.append(" OVERDUE");
            }            
            const edit_button = document.createElement("p");
            edit_button.innerHTML = `<i class="gg-pen"></i>`;
            edit_button.style.color = "#fff"
            edit_button.classList.add("edit");
            edit_button.addEventListener("click", () => edit_tasks(task, label));
            const delete_button = document.createElement("p");
            delete_button.innerHTML = `<i class="gg-trash-empty"></i>`;
            delete_button.style.color = "#fff"
            delete_button.classList.add("delete");
            delete_button.addEventListener("click", () => delete_tasks(task, label));
            const todo_task = task_el.querySelector(".task");
            todo_task.append(delete_button);
            todo_task.append(edit_button);
            tasks_box.appendChild(task_el);
        });
    }
})();

update();
setInterval(alert_due, 60000);
setInterval(update, 20000);
