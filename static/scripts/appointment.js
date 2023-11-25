// script.js

function handleInput() {
    var search = document.getElementById('name').value;
    var dropdown = document.getElementById('name-list');

    if (search.length >= 2) {
        fetch('/autocomplete?search=' + search)
            .then(response => response.json())
            .then(data => {
                displayResults(data);
            });
    } else {
        dropdown.style.display = 'none';
    }
}

function displayResults(results) {
    var dropdown = document.getElementById('name-list');
    dropdown.innerHTML = '';

    results.forEach(function (name) {
        var listItem = document.createElement('li');
        listItem.textContent = name;
        listItem.onclick = function () {
            document.getElementById('name').value = name;
            fetchUserInfo(name);
            dropdown.style.display = 'none';

            // Show the additional fields and labels
            document.getElementById('additional-fields').style.display = 'block';
            document.getElementById('region-label').style.display = 'block';
            document.getElementById('topic-label').style.display = 'block';

            // Show the button
            document.getElementById('availability-button').style.display = 'block';
        };
        dropdown.appendChild(listItem);
    });

    dropdown.style.display = 'block';
}

function fetchUserInfo(name) {
    fetch('/patient_info?name=' + name)
        .then(response => response.json())
        .then(data => {
            document.getElementById('region').value = data.region || '';
            document.getElementById('topic').value = data.topic || '';
        });
}

function checkAvailability() {
    var name = document.getElementById('name').value;

    fetch('/check_availability?name=' + name)
        .then(response => response.json())
        .then(data => {
            displayAvailableMachines(data.available_machines);
        });
}

function displayAvailableMachines(availableMachines) {
    var availableMachinesList = document.getElementById('available-machines');
    availableMachinesList.innerHTML = '';

    if (availableMachines.length > 0) {
        availableMachines.forEach(function (machine) {
            var listItem = document.createElement('li');
            listItem.textContent = machine;
            availableMachinesList.appendChild(listItem);
        });

        // Show the list of available machines
        availableMachinesList.style.display = 'block';
    } else {
        // If no machines are available, hide the list
        availableMachinesList.style.display = 'none';
    }
}

// Close the dropdown if the user clicks outside of it
window.onclick = function (event) {
    if (!event.target.matches('#name')) {
        var dropdown = document.getElementById('name-list');
        if (dropdown.style.display === 'block') {
            dropdown.style.display = 'none';
        }
    }
};
