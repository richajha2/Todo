let tasks = [];

function addTask() {
  const id = document.getElementById('taskId').value;
  const name = document.getElementById('taskName').value;
  const desc = document.getElementById('taskDesc').value;
  const date = document.getElementById('taskDate').value;
  const time = document.getElementById('taskTime').value;
  const photo = document.getElementById('taskPhoto').value;

  const task = new Task(id, name, desc, date, time, photo);
  tasks.push(task);
  document.getElementById('taskId').value = parseInt(id) + 1;
  renderTasks();
  clearFields();
}

function renderTasks() {
  const tbody = document.querySelector('#taskTable tbody');
  tbody.innerHTML = '';
  tasks.forEach((task, index) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${task.name}</td>
      <td>${task.desc}</td>
      <td>${task.date}</td>
      <td>${task.time}</td>
      <td><img src="${task.photo}" width="50"/></td>
      <td>
        <button onclick="editTask(${index})">Edit</button>
        <button onclick="removeTask(${index})">Delete</button>
      </td>`;
    tbody.appendChild(tr);
  });
}

function editTask(index) {
  const task = tasks[index];
  document.getElementById('taskId').value = task.id;
  document.getElementById('taskName').value = task.name;
  document.getElementById('taskDesc').value = task.desc;
  document.getElementById('taskDate').value = task.date;
  document.getElementById('taskTime').value = task.time;
  document.getElementById('taskPhoto').value = task.photo;
  tasks.splice(index, 1);
}

function removeTask(index) {
  tasks.splice(index, 1);
  renderTasks();
}

function deleteTask() {
  const id = document.getElementById('taskId').value;
  tasks = tasks.filter(task => task.id != id);
  renderTasks();
}

function updateTask() {
  addTask();
}

function saveTasks() {
  saveTasksToStorage(tasks);
  alert('Tasks saved');
}

function clearFields() {
  document.getElementById('taskName').value = '';
  document.getElementById('taskDesc').value = '';
  document.getElementById('taskDate').value = '';
  document.getElementById('taskTime').value = '';
  document.getElementById('taskPhoto').value = '';
}
