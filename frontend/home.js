const token = localStorage.getItem("access_token");
const todoList = document.getElementById("todo-list");
const caption = document.getElementById("caption");
const description = document.getElementById("description");
const completed = document.getElementById("completed");
const API_BASE = "http://127.0.0.1:8000";

const dialog = document.getElementById("todo-dialog");
const close_dialog = document.getElementById("close-dialog");
const update_btn = document.getElementById("update");
const delete_btn = document.getElementById("delete");
const create_btn = document.getElementById("create");

const caption_dialog = document.getElementById("caption-dialog");
const description_dialog = document.getElementById("description-dialog");
const completed_dialog = document.getElementById("completed-dialog");
const todoTableBody = document.getElementById("todo-table-body");
const create_form = document.getElementById("create-form");
let id;
let selectedTodoId = null;

if (!token){
    window.location.href = "error.html";
}

async function show_todos(){
    
    const response = await fetch(`${API_BASE}/uploads`, {
        method: "GET",
        headers: {
            "Authorization":`Bearer ${token}`
        }
    });

    const data = await response.json();
    todoTableBody.innerHTML = "";


    console.log(data)

    data.todos.forEach(todo => {
        const row = document.createElement("tr");

        const idCell = document.createElement("td");
        idCell.textContent = todo.id;

        const captionCell = document.createElement("td");
        captionCell.textContent = todo.caption;

        const descriptionCell = document.createElement("td");
        descriptionCell.textContent = todo.description;

        const statusCell = document.createElement("td");
        statusCell.textContent = todo.completed ? "Completed" : "Not Completed";

        const actionCell = document.createElement("td");

        const updateButton = document.createElement("button");
        updateButton.textContent = "Update";

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";


        actionCell.appendChild(updateButton);
        actionCell.appendChild(deleteButton);

        row.appendChild(idCell);
        row.appendChild(captionCell);
        row.appendChild(descriptionCell);
        row.appendChild(statusCell);
        row.appendChild(actionCell);

        todoTableBody.appendChild(row);

        updateButton.addEventListener("click", () => {

            selectedTodoId = todo.id;

            caption_dialog.value = todo.caption;
            description_dialog.value = todo.description;
            completed_dialog.checked = todo.completed;

            dialog.showModal();
        });

        deleteButton.addEventListener("click", async () => {
            delete_todos(todo.id);

            await show_todos()
        });
    });

    return data;
}

async function create_todos(){
    const response = await fetch(`${API_BASE}/uploads`, {
        method: "POST",
        headers: {
            "Content-Type":"application/json",
            "Authorization":`Bearer ${token}`
        },
        body: JSON.stringify({
            title: caption.value,
            description: description.value,
            completed: completed.checked
        })
    });

    const data = await response.json();

    if(response.ok){
        console.log("Create Succesfull")
    } else {
        console.error("Failed to create")
        console.error(data.detail)
    }
}

async function update_todos(id, title, description, completed){
    const response = await fetch(`${API_BASE}/uploads/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type":"application/json",
            "Authorization":`Bearer ${token}`
        },
        body: JSON.stringify({
            title: title,
            description: description,
            completed: completed
        })
    });

    const data = await response.json();

    if (response.ok){
        console.log(`Update Successful: ${id}`);
    } else {
        console.error(`Update Failed: ${id}`);
        console.error(data.detail);
    }
}

async function delete_todos(id){
    const response = await fetch(`${API_BASE}/uploads/${id}`, {
        method: "DELETE",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    const data = await response.json();

    if(response.ok){
        console.log(`Delete Successful: ${id}`);
    } else {
        console.error(`Delete Failed: ${id}`);
        console.error(data.detail);
    }
}

function open_dialog(){
    dialog.showModal();
}

close_dialog.addEventListener('click', () => {
    dialog.close()
});

update_btn.addEventListener('click', async () => {
    await update_todos(
        selectedTodoId,
        caption_dialog.value,
        description_dialog.value,
        completed_dialog.checked
    );

    dialog.close();
    await show_todos();

});

delete_btn.addEventListener('click', async ()=> {
    delete_todos(selectedTodoId);
    dialog.close();
    await show_todos();
});

create_btn.addEventListener('click', async (event) => {

    event.preventDefault();

    await create_todos();
    await show_todos();
})

show_todos();
